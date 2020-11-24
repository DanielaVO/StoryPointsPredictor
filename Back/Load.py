# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:54:07 2020

@author: sebastian.luna & dvo
"""
from flask import Flask, flash, jsonify, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import re
import fasttext

app = Flask(__name__)
file_name = "classifier.bin"
model = fasttext.load_model(file_name)

def concatenate_test(stories_list):
    full_stories = []
    for story in stories_list:
        full_stories.append(story.title + " " + story.description)
    return full_stories

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
    full_stories = concatenate_test(json)
    prediction = predict(full_stories)
    story_points = get_label(prediction)
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