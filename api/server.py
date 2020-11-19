# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:54:07 2020
@author: sebastian.luna & dvo
"""
from flask import Flask, flash, jsonify, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import re
import fasttext

UPLOAD_FOLDER = '/path/to/the/uploads'
app = Flask("Story-Points-Predictor", template_folder='templates')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_name = "supervised_classifier_model_75dbe66e-6e11-4d60-ad61-f75a0eaf8519.bin"
model = fasttext.load_model(file_name)

def get_label(label_list):
    p = re.compile(r'\d+')
    labels = []
    for text in label_list[0]:
      m = p.findall(text[0])
      if m:
        label = int(m[0][0])
        labels.append(label)
    return labels

@app.route('/predict', methods=["POST"])
def get_predictions():
    json = request.get_json()
    response=predict(json["stories"])
    story_points = get_label(response)
    return {"predictions": story_points}

def predict(stories_list):
    return model.predict(stories_list)

if __name__ == '__main__':
    app.run()
    
"""
print(predict(["As an user I want to be able to click and have fun",
         "As an user I want to be able to click and play musical instruments",
         "As an user I want to be able to click and do some random stuff"]))
    
"""