from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from EtsyExplorer.spiders.etsySpider import EtsyspiderSpider

def run():
  process = CrawlerProcess(settings=get_project_settings())
  shopname = input("Please insert shop name to crawl: ")
  if not shopname:
    return
  while True:
    try:
      numpage = input("Please insert number of page to crawl: ")
      if not numpage or numpage == '0':
        numpage = 1000000
      else:
        numpage = int(numpage)
    except ValueError:
      print("Not a valid number.")
    else:
      break
  process.crawl(EtsyspiderSpider, shopname=shopname, numpage = numpage)
  process.start()

if __name__ == "__main__":
  run()