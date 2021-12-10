# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    username = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    target_id = scrapy.Field()
    target_name = scrapy.Field()
    status = scrapy.Field()
