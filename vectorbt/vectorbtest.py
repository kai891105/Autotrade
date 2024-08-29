import vectorbt as vbt

price = vbt.YFData.download('2330.TW').get('Close')
'''
pf = vbt.Portfolio.from_holding(price, init_cash=10000)
pf.total_profit()
'''
fast_ma = vbt.MA.run(price, 5) # 5日線  
slow_ma = vbt.MA.run(price, 20) # 20日線
entries = fast_ma.ma_crossed_above(slow_ma) # 進場訊號
exits = fast_ma.ma_crossed_below(slow_ma) # 出場訊號

pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000) # 建立投資組合
pf.total_profit() # 計算總獲利
print(pf.total_profit()) # 印出總獲利

