from enum import unique
from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as DKE

headers = {"User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"}
url = "https://news.mail.ru/?_ga=2.191912418.917681127.1637505591-971961022.1616528196"
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)


client = MongoClient("127.0.0.1", 27017)
db = client["lenta_news"]
news = db.news

news_list = []

links_to_check = []


def link_collector(el: str, cls: str):
    els = dom.xpath(f'//{el}[contains(@class, "{cls}")]')

    for el in els:
        link = "".join(el.xpath(".//a/@href"))
        links_to_check.append(link)


link_collector("div", "daynews__item")
link_collector("li", "list__item")


def link_handler(link: str):
    headers = {
        "User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"
    }
    url = link
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    link_info = {}

    source_name = dom.xpath(
        '//div[contains(@class, "article")]//span[@class="link__text"]/text()'
    )[0]
    time = "".join(
        dom.xpath('//span[contains(@class, "note__text")]/@datetime')
    ).replace("T", " ")
    news_link = link
    news_name = "".join(dom.xpath("//h1/text()"))

    link_info["name"] = news_name
    link_info["link"] = news_link
    link_info["datetime"] = time
    link_info["source"] = source_name

    return link_info


for link in links_to_check:
    news_list.append(link_handler(link))


for elem in news_list:
    try:
        news.insert_one(elem)
    except DKE:
        continue
