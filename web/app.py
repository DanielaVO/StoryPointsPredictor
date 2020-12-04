from flask import Flask, jsonify, request, render_template
import requests
import csv
import io

app = Flask("story_points_predictor", template_folder='templates')
json = ""

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')   