import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EtsySpider(CrawlSpider):
	name = "etsy"
	allowed_domains = ["etsy.com"]
	# start_urls = ["https://www.etsy.com/shop/OzzieDigitalArt"]
	user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"

	def start_requests(self):
		yield scrapy.Request(url="https://www.etsy.com/shop/OzzieDigitalArt", headers={"User-Agent": self.user_agent})
	
	rules = (
		Rule(LinkExtractor(
			restrict_xpaths="//div[@class='responsive-listing-grid wt-grid wt-grid--block wt-justify-content-flex-start wt-mb-xs-3 appears-ready']/div[1]/a"), 
			callback="parse_item", follow=True, process_request="set_user_agent"), 
		)

	def set_user_agent(self, request, spider):
		request.headers["User-Agent": self.user_agent]
		return request
		
	def parse_item(self, response):
		print("heelllnoo")
		print(response.url)