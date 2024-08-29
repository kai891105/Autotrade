import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import os

# 你的數據處理代碼
sema_name = 'EMA12'
lema_name = 'EMA26'
stockbo = '5269.TW'
local_dir = 'C:\\Coding\\VScode\\ooschool\\Autotrade\\'
output_folder = os.path.join(local_dir, 'history\\')
output_file = output_folder + '5269.TW1y.csv'
sema = 12
lema = 26

# 讀取 CSV 文件並解析日期列
df = pd.read_csv(output_file, parse_dates=['Date'])
df.set_index('Date', inplace=True)

df[sema_name] = df['Close'].ewm(span=sema, adjust=False).mean()  # 短期EMA
df[lema_name] = df['Close'].ewm(span=lema, adjust=False).mean()  # 長期EMA
df['MACD'] = df[sema_name] - df[lema_name]  # MACD = 短期EMA - 長期EMA

# 創建 Dash 應用程序
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=f'K線圖和EMA for {stockbo}'),

    dcc.Graph(
        id='candle-ema',
        figure={
            'data': [
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                ),
                go.Scatter(
                    x=df.index,
                    y=df[sema_name],
                    mode='lines',
                    name=sema_name,
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=df.index,
                    y=df[lema_name],
                    mode='lines',
                    name=lema_name,
                    line=dict(color='red')
                )
            ],
            'layout': {
                'title': f'K線圖和EMA for {stockbo}',
                'legend': {'x': 0, 'y': 1}
            }
        }
    ),

    dcc.Graph(
        id='macd',
        figure={
            'data': [
                go.Scatter(
                    x=df.index,
                    y=df['MACD'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='green')
                )
            ],
            'layout': {
                'title': 'MACD',
                'legend': {'x': 0, 'y': 1}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(port=9001,debug=True)
