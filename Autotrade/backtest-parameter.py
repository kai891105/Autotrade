from flask import Flask, Response, request
import csv
import os

app = Flask(__name__)

@app.route('/stream_csv/<filename>', methods=['GET'])
def stream_csv(filename):
    data_list = []
    file_path = os.path.abspath(f"./Autotrade/history/{filename}")
    
    if not os.path.exists(file_path):
        return Response("File not found", status=404)
    
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_list.append(row)
    
    def generate():
        for row in data_list:
            yield ','.join(row) + '\n'
    
    return Response(generate(), mimetype='text/csv')

if __name__ == '__main__':
    app.run()
