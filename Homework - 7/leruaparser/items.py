# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders import processors
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    try:
        value = value.replace(" ", "")
        value = int(value)
    except Exception as f:
        print(f)

    return value


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field(output_processors=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processors=TakeFirst())
    price = scrapy.Field(
        output_processors=TakeFirst(), input_processor=MapCompose(process_price)
    )
