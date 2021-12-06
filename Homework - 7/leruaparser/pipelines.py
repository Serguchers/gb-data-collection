# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class LeruaparserPipeline:
    def process_item(self, item, spider):
        return item


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for photo in item["photos"]:
                try:
                    yield scrapy.Request(photo.replace("82", "800"))
                except Exception as f:
                    print(f)

    def item_completed(self, results, item, info):
        item["photos"] = [itm[1] for itm in results if itm[0]]
        return item
