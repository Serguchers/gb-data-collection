import scrapy
from leruaparser.items import LeruaparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class LeruaspiderSpider(scrapy.Spider):
    name = "leruaspider"
    allowed_domains = ["leroymerlin.ru"]
    start_urls = ["https://leroymerlin.ru/catalogue/dreli/?page=1"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[contains(@aria-label, 'Следующая страница')]/@href"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.collect_products)

    def collect_products(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)

        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("photos", "//img[@slot='thumbs']/@src")
        loader.add_value("link", response.url)
        loader.add_xpath("price", "//span[@slot='price']/text()")

        yield loader.load_item()
