import vectorbt as vbt

# 获取台积电的收盘价数据
price_data = vbt.YFData.download('5269.TW').get('Close')

# 计算 MACD 指标
macd = vbt.MACD.run(price_data, fast_window=12, slow_window=26, signal_window=9)

# 生成买入和卖出信号
entries = macd.macd_crossed_above(macd.signal)  # 买入信号：DIF 上穿 MACD9
exits = macd.macd_crossed_below(macd.signal)    # 卖出信号：DIF 下穿 MACD9

# 基于信号生成投资组合并执行回测
portfolio = vbt.Portfolio.from_signals(price_data, entries, exits)

# 查看回测结果
print(portfolio.stats())
portfolio.plot().show()