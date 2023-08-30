import pandas as pd
import requests
import logging
import os
import concurrent.futures
import time
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def loggerDecor(func):
  @wraps(func)
  def wrapper(*agrs, **kwargs):
    logger.debug(f" {func.__name__} Start func.")
    result = func(*agrs, **kwargs)
    logger.debug(f" {func.__name__} End func.")
    return result
  return wrapper

def mkdir():
	try:
		os.mkdir("Images_Folder")
	except FileExistsError:
		pass

# @loggerDecor
def downLoadImage(*argv):
	try:
		imgconcatname, userCustomName, dateName = argv
		logger.debug(f"{imgconcatname} : {userCustomName} : {dateName}")

		img_id, img_name, imgUrl = imgconcatname.split("*")
		headers = {
			'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"}
		time.sleep(3)
		response = requests.get(imgUrl, headers=headers)
		while response.status_code != 200:
			logger.debug(f"GET response not successful . CODE: {response.status_code}")
			time.sleep(60)
			response = requests.get(imgUrl, headers=headers)
		img_bytes = response.content
		
		# <TÊN TỰ ĐẶT>_YYYYMMDD_<ID>_<TÊN CỦA SẢN PHẨM>
		img_name = f"{userCustomName}_{dateName}_{img_id}_{img_name}.jpg"
		with open(f"Images_Folder/{img_name}", "wb") as w_img:
			w_img.write(img_bytes)
	except Exception as e:
		logger.debug(f"{'!' * 50}")
		logger.error(f"{e}")
		logger.debug(f"Down load picture error. Picture name : {img_name} .")
		logger.debug(f"{'!' * 50}")

def fileConverter(filename):
	logger.info("Starting convert to file excel.")
	df = pd.read_csv("file.csv")
	if df.empty:
		logger.debug("File is Empty . Can not convert to exel.")
		return
	df.to_csv(f"{filename}.csv")
	df.to_excel(f"{filename}.xlsx")

@loggerDecor
def imgDownloaderConcurrency(userCustomName):
	# Get currdir
	currDir = os.getcwd()
	filePath = os.path.join(currDir, "file.csv")
	
	# Read in chunks to minimize memory
	df = pd.read_csv(
		filepath_or_buffer=filePath,
		chunksize=200, index_col=None, usecols=["concatidnameurl"])
	
	dateName = datetime.now().strftime("%Y%m%d")
	for chunk in df:
		arr = chunk.to_numpy()
		arr = arr.ravel()
		# argv = (arr, userCustomName, dateName)
		# with concurrent.futures.ProcessPoolExecutor() as executor:
		# 	executor.map(downLoadImage, argv)
		for item in arr:
			downLoadImage(item, userCustomName, dateName)
		time.sleep(60)