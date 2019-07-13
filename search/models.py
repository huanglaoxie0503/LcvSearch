# -*- coding: utf-8 -*-
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class NewsClsType(DocType):
    # 财联社新闻 构建 es 模型
    suggest = Completion(analyzer=ik_analyzer)
    article_id = Integer()
    title = Text(analyzer="ik_max_word")
    brief = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    create_date = Date()
    stock_code = Keyword()
    stock_name = Keyword()
    url = Keyword()
    source = Keyword()
    website = Keyword()

    class Meta:
        index = "news"
        doc_type = "news_cls"


if __name__ == '__main__':
    NewsClsType.init()
