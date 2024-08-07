import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf
import sys
local_dir = os.path.dirname(__file__)
output_file=""
#s_input = input("輸入股票代碼：")
sema_input=input("請輸入短期EMA條件")
lema_input=input("請輸入長期EMA條件")
if(sema_input>lema_input):
    print("EMA是不是輸入反了")
    sys.exit(1) #强制中断程序并返回异常状态码
    
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
    global stockbo
    global stock_his
    df = stock_his
    #print(df.head())
    df['Date'] = stock_his.index.strftime('%Y-%m-%d %H:%M:%S')
    # 將索引轉換為DatetimeIndex
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df.drop(columns=['Date'], inplace=True)
    mpf.plot(df, type='candle', style='charles', title=stockbo, volume=True)
    #EMA為價格的移動平均線
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()#短期EMA
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()#長期EMA
    #MACD = 短期EMA-長期EMA
    df['MACD'] = df['EMA12'] - df['EMA26']
    #print(df['EMA12'])
    save_csv(stockbo, df, period_par)
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
    

main_dash()