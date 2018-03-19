# 2016年1年分のDataFrameを用意
start_date = "2016-01-01"
end_date = "2016-12-31"
df = pd.DataFrame(index=pd.date_range(start_date, end_date))

# 日経平均のデータを読み込んでjoinする
df = df.join(pd.read_csv("n225.csv", index_col="Date", parse_dates=True, usecols=["Date", "Adj Close"]))

# 終値がない日（市場が休みの日）を取り除く
df = df.dropna()
print(df.head())

#                Adj Close
# 2016-01-04  18450.980469
# 2016-01-05  18374.000000
# 2016-01-06  18191.320312
# 2016-01-07  17767.339844
# 2016-01-08  17697.960938
