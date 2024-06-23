import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
'''
# 獲取台灣積體電路製造公司（TSMC, 股票代號：2330.TW）的歷史數據
ticker = '2330.TW'
data = yf.download(ticker, start='2023-01-01', end='2023-01-05') #download方法是一種非常有用的功能，它允許用戶批量下載多個股票的歷史市場數據

# 查看數據
print(data.head())

# 繪製收盤價的時間序列圖
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='TSMC Close Price')
plt.title('TSMC Close Price (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Close Price (TWD)')
plt.legend()
plt.grid(True)
plt.show()
'''

#history 方法是用來獲取股票或其他金融工具的歷史市場數據的主要方式。這個方法返回一個包含了選定時間範圍內的市場數據的 Pandas DataFrame。這些數據通常包括開盤價、最高價、最低價、收盤價和交易量。
# 創建一個股票對象
stock = yf.Ticker("5269.TW")

# 使用 history 方法獲取歷史數據
#historical_data = stock.history(period="1mo", interval="1d", start=None, end=None, actions=True, auto_adjust=True, back_adjust=False)
#以上資料蘭園為 https://ithelp.ithome.com.tw/articles/10341344

data2=stock.history(period="1mo")
print(data2)

# 绘制收盘价图表
data2['Close'].plot()
plt.title('Closing Prices for 5269.TW Over the Last Month')
plt.xlabel('Date')
plt.ylabel('Closing Price (TWD)')
plt.show()