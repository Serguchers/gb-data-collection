import scrapy
from scrapy.http import HtmlResponse

from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/приключение/?stype=0&page=1"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//div[@class='product-cover']//a[@class='cover']/@href"
        ).getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//div[@id='product-title']/h1/text()").get()
        author = response.xpath("//a[@data-event-label='author']/text()").get()
        price = response.xpath(
            "//span[@class='buying-priceold-val-number']/text()"
        ).get()
        price_discounted = response.xpath(
            "//span[@class='buying-pricenew-val-number']/text()"
        ).get()
        if not price:
            price = response.xpath(
                "//span[@class='buying-price-val-number']/text()"
            ).get()
            price_discounted = None
        rating = response.xpath("//div[@id='rate']/text()").get()
        book_link = response.url

        yield BookparserItem(
            name=name,
            author=author,
            price=price,
            price_discounted=price_discounted,
            rating=rating,
            book_link=book_link,
        )
