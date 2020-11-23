from flask import Flask, jsonify, request, render_template
import requests
import csv
import io

app = Flask("story_points_predictor", template_folder='templates')
json = ""

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html', json= json)

@app.route('/sendFile', methods=['POST'])
def post():
    f = request.files['file']
    data = []
    if not f:
        return "No file"
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    for row in csv_input:
        print(row)
        data.append({'title': row[0], 'description': row[1]})
    print(data)
    res = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
    json = res.json()
    return get()

app.run(port=8000, debug=True)