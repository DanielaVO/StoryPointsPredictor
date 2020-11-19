from flask import Flask, jsonify, request, render_template
import requests

app = Flask("story_points_predictor", template_folder='templates')

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')

app.run(port=8000, debug=True)