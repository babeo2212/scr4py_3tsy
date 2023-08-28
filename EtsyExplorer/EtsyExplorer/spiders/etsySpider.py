import scrapy
import logging

class EtsyspiderSpider(scrapy.Spider):
	name = "etsySpider"
	allowed_domains = ["www.etsy.com"]
	user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
	countPage = 0
	def start_requests(self):
		yield scrapy.Request(url=f"https://www.etsy.com/shop/{self.shopname}", headers={"User-Agent": self.user_agent})
			
	def set_user_agent(self, request, spider):
		request.headers["User-Agent"] = self.user_agent
		return request
	
	def parse(self, response):
		logging.info(response.url)
		self.countPage += 1
		if self.countPage > self.numpage:
			return
		items = response.xpath("//div[@class=' wt-animated']/div[3]/div/div/div")
		for item in items:
			url = item.xpath(".//a/@href").get()
			yield scrapy.Request(url=url, headers={"User-Agent": self.user_agent}, meta={"url": url}, callback=self.parse_item)
		
		nextPage = response.xpath("//a[@class='wt-action-group__item wt-btn wt-btn--icon '])[1]/@href").get()
		if nextPage:
			yield scrapy.Request(url=nextPage, headers={"User-Agent": self.user_agent}, callback=self.parse)

	def parse_item(self, response):
		logging.info(response.url)
		name = response.xpath("normalize-space(//h1[@class='wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1']/text())").get()
		tags = response.xpath("//div[@class='tags-section-container tag-cards-section-container-with-images']/ul/li")
		tagnames = ""

		picUrls = response.xpath("//li[contains(@class, 'wt-position-absolute wt-width-full wt-height-full wt-position-top wt-position-left carousel-pane')]")
		picUrlList = list()
		isFirst = True
		for pic in picUrls:
			if isFirst:
				picUrlList.append(pic.xpath(".//img/@src").extract_first())
				isFirst = False
			picUrlList.append(pic.xpath(".//img/@data-src").extract_first())
		# Clean out null value
		picUrlList = [pic for pic in picUrlList if pic]	

		for tag in tags:
			tagname = tag.xpath("normalize-space(.//a/h3/text())").get()
			tagnames += (tagname + ",")
		tagnames = tagnames[:-1]

		for pic in picUrlList:
			yield {
				"name": name,
				"tags": tagnames,
				"pic_urls": pic
			}




	# def parse(self, response):
	# 		countries = response.xpath("//td/a")
	# 		for country in countries:
	# 				name = country.xpath(".//text()").get()
	# 				link = country.xpath(".//@href").get()

	# 				absolute_link = response.urljoin(link)
	# 				yield scrapy.Request(absolute_link, callback=self.parse_country, meta={"country_name": name})

	# def parse_country(self, response):
	# 		logging.info(response.url)
	# 		name = response.request.meta["country_name"]
	# 		rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
	# 		for row in rows:
	# 				year = row.xpath(".//td[1]/text()").get()
	# 				pop = row.xpath(".//td[2]/strong/text()").get()
	# 				yield {
	# 						"country_name": name,
	# 						"year": year,
	# 						"population": pop,
	# 				} 