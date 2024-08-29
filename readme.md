這是簡易自動交易系統紀錄
===
- [X] 使用yfinance套件讀取指定代碼的台股資訊
- [X] 計算EMA跟MACD
- [X] 把EMA參數化
- [X] 將個股資訊與計算後的EMA跟MACD存入CSV
- [X] 

以下為開發紀錄
----

- 2024/07/13
1. 因為之前的開發沒有做紀錄，今日起嘗試做開發紀錄
2. 變更mainV2.py為起始專案
3. backtest.py 為讀取CSV檔案，並使用flask 製作API，逐筆顯示資料
4. 預先建立backtest-parameter.py的環境，將CSV名稱參數化，未來在查指定個股時，可以直接調用對應的CSV

- 2024/07/27
1. 建立存放交易紀錄的資料夾
2. 建立web方案的資料夾

- 2024/08/29
1.將web方案的資料夾改為web_root
2.index.py 為web方案的入口，使用dash框架(已完成)






