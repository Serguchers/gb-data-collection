import os
import sys

sys.path.append(f"{os.getcwd()}\\Homework - 6")


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookparser import settings
from bookparser.spiders.labirintru import LabirintruSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    # Передам ранее заданные настройки settings.py
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintruSpider)

    process.start()
