from flask import Flask, Response
import csv
import os

app = Flask(__name__)

data_list = []
file_path = os.path.abspath("./Autotrade/history/5269.TW1mo.csv")
with open(file_path, 'r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data_list.append(row)

count = 0

@app.route('/stream_csv')
def stream_csv():
    global count  # 声明 count 为全局变量
    count += 1
    return data_list[count]

if __name__ == '__main__':
    app.run()