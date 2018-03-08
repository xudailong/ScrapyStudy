# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


"""
这个类主要是进行结构化输出，我们需要获取哪些内容，就在这里定义就好了
"""
class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 关键字
    keywords = scrapy.Field()
    # 发表时间
    release_time = scrapy.Field()
    # 内容部分
    body = scrapy.Field()
    # 原始url
    orginal_url = scrapy.Field()