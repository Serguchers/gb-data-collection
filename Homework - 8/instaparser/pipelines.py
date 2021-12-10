# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient, collection

class InstaparserPipeline:
    def __init__(self) -> None:
        client = MongoClient('127.0.0.1', 27017)
        db = client['instagram_1012']
        self.collection = db.users
        
    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item
