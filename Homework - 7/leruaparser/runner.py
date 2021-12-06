import sys
import os
sys.path.append(os.getcwd() + '\\Homework - 7')

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leruaparser import settings
from leruaparser.spiders.leruaspider import LeruaspiderSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    # Передам ранее заданные настройки settings.py
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaspiderSpider)

    process.start()