import os
print(os.path.abspath(__file__))

import itertools
import pandas as pd
import numpy as np

# def iterate_dataframe_lazy(df):
#   """Iterates through a DataFrame using lazy evaluation.

#   Args:
#     df: The DataFrame to iterate through.

#   Yields:
#     Each row of the DataFrame.
#   """
#   # Create a shallow copy of the DataFrame.
#   df_copy = df.copy()

#   # Create two iterators over the DataFrame.
#   it1, it2 = itertools.tee(df_copy.iterrows())

#   # Iterate over the first iterator.
#   for _, row in it1:
#     yield row


# df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
# rows = iterate_dataframe_lazy(df)
# # for row in iterate_dataframe_lazy(df):
# #   print(row)
# print(next(rows))
# print(next(rows))
# print(next(rows))
# df = 

# def mapping(int):
# 	mapDict = {
# 		1: "A", 2: "B", 3: "C", 4: "D",
# 		5: "E",	6: "F", 7: "G",	8: "H",
# 		9: "I", 10: "J", 11: "K", 12: "L"
# 	}
# 	try:
# 		res = mapDict[int]
# 	except KeyError:
# 		res = "Z"
# 	return res
# df = pd.read_csv("/home/mickeyvu0811/Documents/MyProjects/scr4py_3tsy/EtsyExplorer/file.csv", 
#                  chunksize=200, index_col=None, usecols=["concatidnameurl"])

df = pd.read_csv("/home/mickeyvu0811/Documents/MyProjects/scr4py_3tsy/EtsyExplorer/file.csv", index_col=None)

# for chunk in df:
#   arr = chunk.to_numpy()
#   arr = arr.ravel()
#   for i in range(10):
#     print(arr[i].split("*"))
#   _ = input()
# df['concatidnameurl'] = df.groupby('id').cumcount() + 1
# df["concatidnameurl"] = df["id"].astype("str") + df["concatidnameurl"].map(mapping) + "*" + df['name'] + "*" + df['img_url']
# print(df.head(10))
df.head(20).to_csv("/home/mickeyvu0811/Documents/MyProjects/scr4py_3tsy/EtsyExplorer/filetest.csv")

# df["concatidnameurl"] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)
# print(mapping(7))

# from datetime import datetime
# now = datetime.now()
# print(datetime.now().strftime("%Y%m%d"))


############################################################################################################3
# from scrapy.mail import MailSender
# from scrapy.utils.project import get_project_settings
# mailer = MailSender()
# mailer = MailSender.from_settings(settings=get_project_settings())

# mailer.send(
#     to=["vutienhung2212@gmail.com"],
#     subject="Job scraping",
#     body="This is a test"
# )