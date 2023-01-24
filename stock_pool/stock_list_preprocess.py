import pandas as pd
import csv
import numpy as np

# http://moneydj.emega.com.tw/js/StockTable.htm

csv_ = pd.read_excel("./stock_list.xlsx", header=None)
csv_ = csv_.to_numpy().T

first = []
second = []

cnt = 0
for row in csv_:
    if cnt % 2 == 0:
        first.extend(row)
    else:
        second.extend(row)
    cnt += 1

result = [first, second]
result = np.asarray(result)

csv_resized = result.T

special_characters=['@','#','$','*','&', '＃', '＊']

df = pd.DataFrame(columns=["symbol", "name", "status", "category"])
cnt = 0
for i, j in csv_resized:
    i, j = str(i), str(j)
    j = "".join(filter(lambda char: char not in special_characters , j))

    if i[:2] == "上市":
        k = "上市"
        l = j
    elif i[:2] == "上櫃":
        k = "上櫃"
        l = j
    else:
        if k == "上市":
            i = i[:-1] + ".TW"
        else:
            i = i[:-1] + ".TWO"

        entry = pd.DataFrame.from_dict({
            "symbol":   [i],
            "name":     [j[:-1]],
            "status":   [k],
            "category": [l[:-1]]
        })
        df = pd.concat([df, entry], ignore_index=True)
        
df = df[df['name']!="na"]
df.to_csv('stock_list_csv.csv', index=False, encoding="utf_8_sig")

print (df)