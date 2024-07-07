import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf
import sys
local_dir = os.path.dirname(__file__)
output_file=""
#s_input = input("輸入股票代碼：")
s_input = "5269"
stockbo = s_input + ".TW"
print(stockbo)

period_par = "1mo"
stock = yf.Ticker(stockbo)
stock_his = stock.history(period=period_par)

# 轉換日期時間為本地時間（不帶時區）
stock_his.index = stock_his.index.tz_localize(None)

def save_csv(stockbo, stock_his, period_par):
    global local_dir
    global output_file
    output_folder = os.path.join(local_dir, 'history')  # 正確的路徑拼接方式
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, stockbo + period_par + '.csv')
    #print(output_file)

    # 格式化日期時間列
    stock_his['Date'] = stock_his.index.strftime('%Y-%m-%d %H:%M:%S')

    # 將格式化後的數據寫入 CSV
    stock_his.to_csv(output_file, index=False)

def main_dash():
    global local_dir
    global output_file
    df = pd.read_excel(output_file)
    print(df.head())

save_csv(stockbo, stock_his, period_par)
main_dash()