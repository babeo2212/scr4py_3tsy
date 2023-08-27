import scrapy


class EtsyspiderSpider(scrapy.Spider):
    name = "etsySpider"
    allowed_domains = ["www.etsy.com"]
    start_urls = ["https://www.etsy.com"]

    def parse(self, response):
        pass
