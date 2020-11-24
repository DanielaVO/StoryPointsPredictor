from flask import Flask, jsonify, request, render_template
import requests
import csv
import io

app = Flask("story_points_predictor", template_folder='templates')
json = ""

@app.route('/', methods=['GET'])
def get(json):
    print(json)
    return render_template('index.html', json=json)

@app.route('/sendFile', methods=['POST'])
def post():
    f = request.files['file']
    data = []
    if not f:
        return "No file"
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    for row in csv_input:
        data.append({'title': row[0], 'description': row[1]})
    res = requests.post('http://localhost:5000/predict', json=data)
    json = res.json()
    return get(json)

app.run(port=8000, debug=True)