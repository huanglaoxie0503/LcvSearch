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