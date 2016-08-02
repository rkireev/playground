import scrapy

from tutorial.items import TjItem
from scrapy.utils.response import open_in_browser

class TjSpider(scrapy.Spider):
    name = "tj"
    allowed_domains = ["tjournal.ru"]
    start_urls = [
        "https://tjournal.ru/club/entries?count=30&offset=0&additional=%7B%22type%22%3A0%2C%22mode%22%3A%22mainpage%22%7D&additionalHash=c8ee441d0c5f82dd4442e07362feedca",
    ]

    def parse(self, response):
        for offset in range(0, 301, 30):
            url = "https://tjournal.ru/club/entries?count=50&offset="+str(offset)+"&additional=%7B%22type%22%3A0%2C%22mode%22%3A%22mainpage%22%7D&additionalHash=c8ee441d0c5f82dd4442e07362feedca"
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//div[@class="b-articles__b__header"]'):

            item = TjItem()
            item['date'] = sel.xpath('.//div//a[@class="b-articles__b__date"]//text()').extract()
            item['title'] = sel.xpath('.//div//a[@class="b-articles__b__t"]//text()').extract()
            yield item
