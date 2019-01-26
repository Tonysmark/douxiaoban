# -*- coding: utf-8 -*-
import pymongo
from douxiaoban.settings import * 



class DouxiaobanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        collection = mongo_db_collection
        client = pymongo.MongoClient(host=host,port=port)
        db = client[dbname]
        self.post = db[collection]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
