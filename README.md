基于 ElasticSearch 的新闻、研报、互动易搜索引擎

1、使用 ElasticSearch 5.1.1 中文发行版，针对中文集成了相关插件，方便学习测试.

2、ElasticSearch-head

3、kibana-5.1.1

-----
添加热搜关键词、热词统计并取出前5个

```python
 import redis
 redis_cli = redis.StrictRedis()
 keywords = "关键词"
 # 搜索关键词+1操作
 redis_cli.zincrby("search_keywords_set", 1, keywords)
  # 统计热词Top5
 top_n_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
```
----
es的文档、索引的CRUD操作
```markdown
新建分片、副本数量
PUT article
{
    "settings": {
        "index": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        }
    }
}

查看设置
GET article/_settings
GET .all/-settings
GET _settings

修改设置
PUT article/_settings
{
    "number_of_replicas": 2
}

查看索引信息
GET all
GET article

新增文档
POST article/cls
{
    "title": "新闻标题"，
    "salary_min": 15000,
    "company": {
        "stock_name": "万科A",
        "stock_code": "000002"
    },
    "publish_time": "发布日期",
    "content": "新闻内容"
}

POST article/cls/1
{
    "title": "新闻标题"，
    "salary_min": 18000,
    "company": {
        "stock_name": "平安银行",
        "stock_code": "000001"
    },
    "publish_time": "发布日期",
    "content": "新闻内容"
}

查看文档
GET article/cls/1
GET article/cls/1?_source
GET article/cls/1?_source=title
GET article/cls/1?_source=title, content

修改文档（覆盖式）
PUT article/cls/1
{
    "title": "新闻标题"，
    "salary_min": 18000,
    "company": {
        "stock_name": "平安银行",
        "stock_code": "000001"
    },
    "publish_time": "发布日期",
    "content": "新闻内容"
}

指定修改
POST article/cls/1/_update
{
    "doc": {
        content: "内容......"
    }
}

删除文档，类（无法删除），索引
DELETE article/cls/1
DELETE article/cls
DELETE article
```
----
es的mget和bulk批量操作
```markdown
mget操作实例
GET _mget
{
    "docs": [
        {
            "_index": "test_db"
            "_type": "job1",
            "_id": 1
        },
        {
             "_index": "test_db"
            "_type": "job1",
            "_id": 2
        }
    ]
}
GET test_db/_mget
{
    "docs": [
        {
            "_type": "article1",
            "_id": 1
        },
        {
        "_type": "article1",
        "_id": 2
        }
    ]
}
GET test_db/article1/_mget
{
    "docs": [
        {
            "_id": 1
        },
        {
        "_id": 2
        }
    ]
}
GET test_db/job1/_mget
{
    "ids": [1, 2]
}

```
