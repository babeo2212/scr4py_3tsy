import scrapy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def mapping(int):
	mapDict = {
		1: "A", 2: "B", 3: "C", 4: "D",
		5: "E",	6: "F", 7: "G",	8: "H",
		9: "I", 10: "J", 11: "K", 12: "L",
		13: "M", 14: "N", 15: "O", 16: "P",
		17: "Q", 18: "R", 19: "S", 20: "T" 
	}
	try:
		res = mapDict[int]
	except KeyError:
		res = "Z"
	return res

class EtsyspiderSpider(scrapy.Spider):
	name = "etsySpider"
	allowed_domains = ["www.etsy.com"]
	user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
	countPage = 0
	countItem = 0
	def start_requests(self):
		yield scrapy.Request(url=f"https://www.etsy.com/shop/{self.shopname}", headers={"User-Agent": self.user_agent})
			
	def set_user_agent(self, request, spider):
		request.headers["User-Agent"] = self.user_agent
		return request
	
	def parse(self, response):
		logger.info(response.url)
		self.countPage += 1
		logger.info(f"{'>' *27} Scrape page number: {self.countPage} {'<' * 27}.")
		if self.countPage > self.numpage:
			return
		# //div[@class='responsive-listing-grid wt-grid wt-grid--block wt-justify-content-flex-start wt-mb-xs-3 appears-ready']
		# This is for BaileyDesignedCo and OzzieDigitalArt
		# #//div[@class="" and @data-listings-container=""]/div/div/div
		#################################################################################################################
		# Change log
		# Replace xpath from "//div[@class=' wt-animated']/div[3]/div/div/div"
		items = response.xpath("//div[contains(@class, 'responsive-listing-grid')]/div")
		for item in items:
			url = item.xpath(".//a/@href").get()
			yield scrapy.Request(url=url, headers={"User-Agent": self.user_agent}, meta={"url": url}, callback=self.parse_item)
		#################################################################################################################
		# Change log
		# Replace xpath from "(//a[@class='wt-action-group__item wt-btn wt-btn--icon '])[1]/@href"
		# -> pick last li a[contains(@class, 'wt-is-disabled')]
		pages = response.xpath("//div[@class='wt-show-xl']/nav[@aria-label='Pagination of listings']/ul/li")
		# Get the last elem
		lastElem = pages[-1]
		# If current page is the last page, the spider will stop
		isLastPage = lastElem.xpath(".//a[contains(@class, 'wt-is-disabled')]")
		if not isLastPage:
			nextPage = lastElem.xpath(".//a/@href").get()
			yield scrapy.Request(url=nextPage, headers={"User-Agent": self.user_agent}, callback=self.parse)
		else:
			return

	def parse_item(self, response):
		self.countItem += 1
		logger.info(f"Item {self.countItem} : {response.url}")
		name = response.xpath("normalize-space(//h1[@class='wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1']/text())").get()
		tags = response.xpath("//div[@class='tags-section-container tag-cards-section-container-with-images']/ul/li")
		tagnames = ""

		imgUrls = response.xpath("//li[contains(@class, 'wt-position-absolute wt-width-full wt-height-full wt-position-top wt-position-left carousel-pane')]")
		imgUrlList = list()
		isFirst = True
		for img in imgUrls:
			if isFirst:
				imgUrlList.append(img.xpath(".//img/@src").extract_first())
				isFirst = False
			imgUrlList.append(img.xpath(".//img/@data-src").extract_first())
		# Clean out null value from list
		imgUrlList = [img for img in imgUrlList if img]	

		for tag in tags:
			tagname = tag.xpath("normalize-space(.//a/h3/text())").get()
			tagnames += (tagname + ",")
		tagnames = tagnames[:-1]
		countImg = 0
		for img in imgUrlList:
			countImg += 1
			yield {
				"id": f"{self.countItem}{mapping(countImg)}",
				"name": name,
				"tags": tagnames,
				"img_url": img,
				"concatidnameurl": f"{self.countItem}{mapping(countImg)}*{name}*{img}"
			}
