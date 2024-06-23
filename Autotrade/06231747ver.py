import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf

local_dir = os.path.dirname(__file__)
output_file = ""
# s_input = input("輸入股票代碼：")
s_input = "5269"
stockbo = s_input + ".TW"
print(stockbo)

period_par = "1mo"
stock = yf.Ticker(stockbo)
stock_his = stock.history(period=period_par)

# 轉換日期時間為本地時間（不帶時區）
stock_his.index = stock_his.index.tz_localize(None)

def save_excel(stockbo, stock_his, period_par):
    global local_dir
    global output_file
    output_folder = os.path.join(local_dir, 'history')  # 正確的路徑拼接方式
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, stockbo + period_par + '.xlsx')
    # print(output_file)

    # 格式化日期時間列
    stock_his['Date'] = stock_his.index.strftime('%Y-%m-%d %H:%M:%S')

    # 將格式化後的數據寫入 Excel
    stock_his.to_excel(output_file, index=False)

def main_dash():
    global output_file
    global stockbo
    df = pd.read_excel(output_file)
    # print(df.head())

    # 將索引轉換為DatetimeIndex
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df.drop(columns=['Date'], inplace=True)

    # 計算EMA12
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    
    # 使用mplfinance繪製蠟燭圖和EMA12
    apdict = [mpf.make_addplot(df['EMA12'], color='blue')]
    mpf.plot(df, type='candle', style='charles', title=stockbo, volume=True, addplot=apdict)

    # 繪製EMA12的折線圖和成交量的柱狀圖
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 繪製 EMA12
    ax1.plot(df.index, df['EMA12'], label='EMA12', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('EMA12', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45)
    plt.title(f'EMA12 and Volume for {stockbo}')
    plt.grid(True)

    # 創建第二個 y 軸顯示成交量
    ax2 = ax1.twinx()
    ax2.set_ylabel('Volume', color='grey')
    ax2.bar(df.index, df['Volume'], color='grey', alpha=0.3)
    ax2.tick_params(axis='y', labelcolor='grey')

    fig.tight_layout()
    plt.show()

save_excel(stockbo, stock_his, period_par)
main_dash()
