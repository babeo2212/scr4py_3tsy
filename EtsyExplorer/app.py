from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from EtsyExplorer.spiders.etsySpider import EtsyspiderSpider
from EtsyExplorer.helperFunc import fileConverter, picDownloaderConcurrency, mkdir
import logging

logging.basicConfig(
    filename="logfile.log", format="%(levelname)s: %(message)s", level=logging.DEBUG
)
# handler = logging.FileHandler("logfile.log", 'w+')

logger = logging.getLogger(__name__)
# logger.addHandler(handler)

def run():
  process = CrawlerProcess(settings=get_project_settings())
  shopname = input("Please insert shop name to crawl: ")
  if not shopname:
    return
  while True:
    try:
      numpage = input("Please insert number of page to crawl: ")
      if not numpage or numpage == '0':
        numpage = 1_000_000
      else:
        numpage = int(numpage)
    except ValueError:
      print("Not a valid number.")
    else:
      break

  mkdir()
  
  process.crawl(EtsyspiderSpider, shopname=shopname, numpage = numpage)
  process.start()

  fileConverter()

  # picDownloader()

if __name__ == "__main__":
  # BaileyDesignedCo
  # MayaPrintDesign
  # OzzieDigitalArt
  run()
