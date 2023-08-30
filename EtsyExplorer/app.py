from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from EtsyExplorer.spiders.etsySpider import EtsyspiderSpider
from EtsyExplorer.helperFunc import fileConverter, imgDownloaderConcurrency, mkdir
from EtsyExplorer.sendEmail import sendEmail
import logging

logging.basicConfig(
    filename="logfile.log", format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO
)
# handler = logging.FileHandler("logfile.log", 'w+')

logger = logging.getLogger(__name__)
# logger.addHandler(handler)

def run():
  ###########################################################################################
  # Get shop name
  shopname = input("Please insert SHOP NAME to crawl: ")
  if not shopname:
    return
  while True:
    try:
      # Get num page to crawl
      numpage = input("Please insert number of page to crawl: ")
      if not numpage or numpage == '0':
        numpage = 1_000_000
      else:
        numpage = int(numpage)
    except ValueError:
      print("Not a valid number.")
    else:
      break
  userCustomName = input("Please insert your FILE NAME: ")
  recipient = input("Please insert recipient name: ")
  if not userCustomName:
    userCustomName = shopname
  if not recipient:
    recipient = None
  ###########################################################################################
  # Make image folder
  mkdir()
  ###########################################################################################
  # Starting scrawling session
  process = CrawlerProcess(settings=get_project_settings())
  process.crawl(EtsyspiderSpider, shopname=shopname, numpage = numpage)
  process.start()
  ###########################################################################################
  # Convert csv file into excel
  fileConverter(filename=shopname)
  ###########################################################################################
  sendEmail(recipient)
  ###########################################################################################
  ans = input("Scrawling completed. Do you want to download all images? [y|n]").lower()
  if ans == "y":
    # userCustomName = "shopABC"
    imgDownloaderConcurrency(userCustomName)
  else:
    return

if __name__ == "__main__":
  run()