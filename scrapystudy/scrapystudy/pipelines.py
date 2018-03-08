# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo


class NewsPipeline(object):
    def open_spider(self, spider):
        # 存储的json文件
        self.filename = open('data.json', 'w')

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + "\n"
        self.filename.write(content.encode('utf-8').decode('unicode-escape'))
        return item

    def close_spider(self, spider):
        self.filename.close()


class DevMongoPipeline(object):

    collection_name = 'article'

    def __init__(self, mongo_uri, mongo_db,mongo_user,mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'news'),
            mongo_user = crawler.settings.get('MONGO_USER'),
            mongo_pwd = crawler.settings.get('MONGO_PWD')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,port=27017,maxPoolSize=15)
        self.client.admin.authenticate(self.mongo_user,self.mongo_pwd)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 插入到mongodb里面
        self.db[self.collection_name].insert_one(dict(item))
        return item
