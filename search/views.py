import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from elasticsearch import Elasticsearch

from search.models import NewsClsType

# Create your views here.
client = Elasticsearch(hosts=["127.0.0.1"])


class SuggestView(View):
    """
    自动补全
    """
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_data = []
        if key_words:
            s = NewsClsType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_data.append(source["title"])
        return HttpResponse(json.dumps(re_data), content_type="application/json")


class SearchView(View):
    """
    关键词搜索
    """
    def get(self, request):
        keywords = request.GET.get('q', "")
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        start_time = datetime.now()
        response = client.search(
            index="news",
            body={
                "query": {
                    "multi_match": {
                        "query": keywords,
                        "fields": ["title", "brief", "content"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "brief": {},
                        "content": {},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if page % 10 > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]

            if "brief" in hit["highlight"]:
                hit_dict["brief"] = "".join(hit["highlight"]["brief"])
            else:
                hit_dict["brief"] = hit["_source"]["brief"]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["share_url"]
            hit_dict["score"] = hit["_score"]
            hit_dict['source'] = hit['_source']['source']
            hit_dict['website'] = hit['_source']['website']

            hit_list.append(hit_dict)

        return render(request, "result.html", {
            "all_hits": hit_list,
            "key_words": keywords,
            "page": page,
            "total_nums": total_nums,
            "page_nums": page_nums,
            "last_seconds": last_seconds,
        })

