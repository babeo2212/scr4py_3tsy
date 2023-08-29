import pandas as pd
import requests
import logging
import os
import concurrent.futures
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def mkdir():
	try:
		os.mkdir("Images_Folder")
	except FileExistsError:
		pass

def downLoadImage(imgUrl):
	time.sleep(1)
	img_name = "abc.jpg"
	img_bytes = requests.get(imgUrl)
	with open(img_name, "wb") as wi:
		wi.write(img_bytes)

def fileConverter():
	logger.debug("Starting convert to file excel.")
	df = pd.read_csv("file.csv")
	if df.empty:
		logger.debug("File is Empty . Can not convert to exel.")
		return
	df.to_excel("file.xlsx")

def picDownloaderConcurrency(data):
  with concurrent.futures.ThreadPoolExecutor() as executor:
	  executor.map(downLoadImage, data)