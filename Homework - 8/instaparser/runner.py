import os
import sys

sys.path.append(os.getcwd() + "\\Homework - 8")

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser import settings
from instaparser.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    print(
        'Введите "followers/following", чтобы собрать данные по подпискам/подписчикам.'
    )
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider, status=input())
    process.start()
