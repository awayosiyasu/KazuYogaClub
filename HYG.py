# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

fieldname = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
hygdata = pd.read_csv('enthought/hyg.csv', header=None, names=fieldname, index_col='Date',
    dtype = {'Date':'object', 'Open':'float', 'Hight':'float', 'Low':'float', 'Close':'float', 'Adj Close':'float', 'Volume':'float'})
hygdata_close = hygdata['Adj Close']
#hx = hygdata_close.plot(x='Date', y='Adj Close', title='HYG Chart -- Adj Close')

# ボリンジャーバンドの計算
rm = hygdata_close.rolling(window=20).mean()
rstd = hygdata_close.rolling(window=20).std()
upper_band = rm + rstd * 2
lower_band = rm - rstd * 2

# プロット
ax = hygdata_close.plot(title='HYG Chart -- Adj Close', color='blue')
rm.columns = ['Rolling mean']
rm.plot(ax=ax, color='green')
upper_band.columns = ['Upper band']
upper_band.plot(ax=ax, color="red")
lower_band.columns = ["Lower band"]
lower_band.plot(ax=ax, color="red")

#rm.Columns = ['Rolling mean']
#rm.plot(ax=hx)
plt.show()
