import pandas as pd
df = pd.read_csv("file.csv")
df.to_excel("file.xlsx")
print(df)