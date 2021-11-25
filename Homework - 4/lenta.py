from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as DKE

headers = {"User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"}
url = "https://lenta.ru"
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)


client = MongoClient("127.0.0.1", 27017)
db = client["lenta_news"]
news = db.news

news_list = []


top_news = dom.xpath('//div[contains(@class, "span4")]')[:2]

for elem in top_news:
    elem = elem.xpath('./div[contains(@class, "item")]')
    for item in elem:
        item_info = {}
        item_name = item.xpath(".//a/text()")[0].replace("\xa0", " ")
        item_link = url + item.xpath(".//a/@href")[0]
        item_time = "".join(item.xpath(".//a/time/@datetime"))

        item_info["name"] = item_name
        item_info["link"] = item_link
        item_info["datetime"] = item_time
        item_info["source"] = "https://lenta.ru"

        news_list.append(item_info)


news.create_index("link", unique=True)

for elem in news_list:
    try:
        news.insert_one(elem)
    except DKE:
        continue
