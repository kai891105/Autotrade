import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf
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

def save_excel(stockbo, stock_his, period_par):
    global local_dir
    global output_file
    output_folder = os.path.join(local_dir, 'history')  # Correct way to concatenate paths
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, stockbo + period_par + '.xlsx')
    #print(output_file)

    # 格式化日期時間列
    stock_his['Date'] = stock_his.index.strftime('%Y-%m-%d %H:%M:%S')

    # 將格式化後的數據寫入 Excel
    stock_his.to_excel(output_file, index=False)

def main_dash():
    global local_dir
    global output_file
    global stockbo
    df = pd.read_excel(output_file)
    #print(df.head())

    # 將索引轉換為DatetimeIndex
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df.drop(columns=['Date'], inplace=True)
    mpf.plot(df, type='candle', style='charles', title=stockbo, volume=True)

    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    
    #print(df['EMA12'])
    '''
    apdict = [mpf.make_addplot(df['EMA12'], color='blue')]
    mpf.plot(df, type='candle', style='charles', title=stockbo, volume=True, addplot=apdict)
    '''
    # 繪製EMA12的折線圖
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['EMA12'], label='EMA12', color='blue')
    plt.title(f'EMA12 for {stockbo}')
    plt.xlabel('Date')
    plt.ylabel('EMA12')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

save_excel(stockbo, stock_his, period_par)
main_dash()