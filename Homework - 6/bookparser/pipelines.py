# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient, collection


class BookparserPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.mongo_base = client.books_labirint

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        item["price"] = self.convert_value(item["price"])
        item["price_discounted"] = self.convert_value(item["price_discounted"])
        item["rating"] = self.convert_value(item["rating"])

        collection.insert_one(item)
        return item

    def convert_value(self, value):
        try:
            value = float(value)
        except TypeError:
            value = None
        return value
