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
    
def plt_chinese():
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 修改中文字體
    plt.rcParams['axes.unicode_minus'] = False # 顯示負號

def main_dash(sema,lema):
    global local_dir
    global output_file
    global stockbo
    global stock_his
    sema=int(sema)
    lema=int(lema)
    sema_name="EMA"+str(sema)
    lema_name="EMA"+str(lema)
    df = stock_his
    #print(df.head())
    df['Date'] = stock_his.index.strftime('%Y-%m-%d %H:%M:%S')
    # 將索引轉換為DatetimeIndex
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df.drop(columns=['Date'], inplace=True)
    #mpf.plot(df, type='candle', style='charles', title=stockbo, volume=True)
    #EMA為價格的移動平均線
    df[sema_name] = df['Close'].ewm(span=sema, adjust=False).mean()#短期EMA
    df[lema_name] = df['Close'].ewm(span=lema, adjust=False).mean()#長期EMA
    #MACD = 短期EMA-長期EMA
    df['MACD'] = df[sema_name] - df[lema_name]
    #print(df['EMA12'])
    #資腰整理完後，將數據存入CSV
    save_csv(stockbo, df, period_par)
    
    # 繪製K線圖、EMA12、EMA26和MACD
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # 繪製K線圖和EMA
    plt_chinese()#解決中文顯示
    mpf.plot(df, type='candle', style='charles', ax=ax1, volume=ax2, show_nontrading=True)
    ax1.plot(df.index, df[sema_name], label=sema_name, color='blue')
    ax1.plot(df.index, df[lema_name], label=lema_name, color='red')
    ax1.set_title(f'K線圖和EMA for {stockbo}')
    ax1.legend()
    
    # 繪製MACD
    ax3.plot(df.index, df['MACD'], label='MACD', color='green')
    ax3.set_title('MACD')
    ax3.legend()
    
    plt.tight_layout()
    plt.show()

main_dash(sema_input,lema_input)