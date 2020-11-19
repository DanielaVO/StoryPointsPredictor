# -*- coding: utf-8 -*-
"""PreTrain-Vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fx9OgbFwkIcScuGkDjxTv25c3J2adPmE
"""
"""
!pip uninstall -y scikit-learn
!pip uninstall -y pandas
!pip uninstall -y pandas_ml

!pip install scikit-learn==0.21
!pip install pandas==0.24.2
!pip install pandas_ml
!pip install fasttext
!pip install cython
!pip install pyfasttext
"""
import pandas as pd
import numpy as np
import nltk
from sklearn.metrics import confusion_matrix
from pandas_ml import ConfusionMatrix
#import fasttext
import pandas as pd
import numpy as np
import csv
import uuid
import subprocess
import glob
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import fasttext

#from pyfasttext import FastText

csv_files = glob.glob('*.csv')
list_data = []
  
for filename in csv_files:
    data = pd.read_csv(filename)
    list_data.append(data)
    
df = pd.concat(list_data, ignore_index=True)
df.isnull().sum()
df.head(100)

df = df.dropna(how='any')
df.groupby('storypoint').size()

df.loc[df.storypoint <= 2, 'storypoint'] = 0 #small
df.loc[(df.storypoint > 2) & (df.storypoint <= 5), 'storypoint'] = 1 #medium
df.loc[df.storypoint > 5, 'storypoint'] = 2 #big

plt.hist(df.storypoint, bins=20, alpha=0.6, color='y')
plt.title("#Items per Point")
plt.xlabel("Points")
plt.ylabel("Count")
 
plt.show()

rows1 = df.loc[df.storypoint == 0, :][0:3000]
rows2 = df.loc[df.storypoint == 1, :][0:3000]
rows3 = df.loc[df.storypoint == 2, :][0:3000]
df1 = pd.DataFrame()
df1 = df1.append(rows1, ignore_index=True)
df1 = df1.append(rows2, ignore_index=True)
df1 = df1.append(rows3, ignore_index=True)
df = df1 
df.head()

col = df.groupby('storypoint')
classes = set()
for i, row in col:
  classes.update(row["storypoint"])
print(classes)

plt.hist(df.storypoint, bins=20, alpha=0.6, color='y')
plt.title("#Items per Point")
plt.xlabel("Points")
plt.ylabel("Count")
 
plt.show()

htmltokens = ['{html}','<div>','<pre>','<p>', '</div>','</pre>','</p>']

#Clean operation
#Remove english stop words and html tokens
def cleanData(text):
    
    result = ''
    
    for w in htmltokens:
        text = text.replace(w, '')
    
    text_words = text.split()    
    
    resultwords  = [word for word in text_words if word not in stopwords.words('english')]
    
    if len(resultwords) > 0:
        result = ' '.join(resultwords)
    else:
        print('Empty transformation for: ' + text)
    return result

def formatFastTextClassifier(label):
    return "__label__" + str(label) + " "

df['title_desc'] = df['title'].str.lower() + ' - ' + df['description'].str.lower()
df['label_title_desc'] = df['storypoint'].apply(lambda x: formatFastTextClassifier(x)) + df['title_desc'].apply(lambda x: cleanData(str(x)))

df = df.reset_index(drop=True)

#df.to_csv("pre_train_data.csv")

from collections import Counter

def SimpleOverSample(_xtrain, _ytrain):
    xtrain = list(_xtrain)
    ytrain = list(_ytrain)

    samples_counter = Counter(ytrain)
    max_samples = sorted(samples_counter.values(), reverse=True)[0]
    for sc in samples_counter:
        init_samples = samples_counter[sc]
        samples_to_add = max_samples - init_samples
        if samples_to_add > 0:
            #collect indices to oversample for the current class
            index = list()
            for i in range(len(ytrain)):
                if(ytrain[i] == sc):
                    index.append(i)
            #select samples to copy for the current class    
            copy_from = [xtrain[i] for i in index]
            index_copy = 0
            for i in range(samples_to_add):
                xtrain.append(copy_from[index_copy % len(copy_from)])
                ytrain.append(sc)
                index_copy += 1
    return xtrain, ytrain

import re
class FastTextClassifier:
    model = ""
    rand = ""
    inputFileName = ""
    outputFileName = ""
    testFileName = ""
    
    def __init__(self):
        self.rand = str(uuid.uuid4())
        self.inputFileName = "issues_train_" + self.rand + ".txt"
        self.outputFileName = "supervised_classifier_model_" + self.rand
        self.testFileName = "issues_test_" + self.rand + ".txt"
    
    def fit(self, xtrain, ytrain):
        outfile=open(self.inputFileName, mode="w", encoding="utf-8")
        for i in range(len(xtrain)):
            line = xtrain[i]
            outfile.write(line + '\n')
        outfile.close()
        
        #self.model.supervised(input=self.inputFileName, output=self.outputFileName, epoch=500, wordNgrams=4, dim=300, minn=4, maxn=6, pretrainedVectors="./drive/My Drive/wiki-news-300d-1M.vec")#, pretrainedVectors="issues_pretrain.txt")
        self.model = fasttext.train_supervised(input=self.inputFileName, epoch=500, wordNgrams=4, dim=300, minn=4, maxn=6, pretrainedVectors="./wiki-news-300d-1M.vec")#, pretrainedVectors="issues_pretrain.txt")
        self.model.save_model(self.outputFileName + ".bin")
        #p1 = subprocess.Popen(["cmd", "/C", "fasttext supervised -input " + self.inputFileName + " -output " + self.outputFileName + " -epoch 500 -wordNgrams 4 -dim 300 -minn 4 -maxn 6 -pretrainedVectors pretrain_model.vec"],stdout=subprocess.PIPE)
        #p1.communicate()[0].decode("utf-8").split("\r\n")
        
        
    def predict(self, xtest):
        #save test file
        outfile=open(self.testFileName, mode="w", encoding="utf-8")
        for i in range(len(xtest)):
            outfile.write(xtest[i] + '\n')
        outfile.close()
        lines = []
        with open(self.testFileName, encoding="utf8") as f:
            lines = f.read().splitlines()

        test_pred = self.model.predict(lines)
        #get predictions
        #p1 = subprocess.Popen(["cmd", "/C", "fasttext predict " + self.outputFileName + ".bin " + self.testFileName], stdout=subprocess.PIPE)
        #output_lines = p1.communicate()[0].decode("utf-8").split("\r\n")
        p = re.compile(r'\d+')
        labels = []
        #print("test pred", test_pred[0])
        for text in test_pred[0]:
          #print("text", text)
          m = p.findall(text[0])
          if m:
            label = int(m[0][0])
            labels.append(label)
        #test_pred = [int(p[0]) for p in test_pred if p != '']
        #print("labels", labels)
        return labels

def rebuild_kfold_sets(folds, k, i):
    training_set = None
    testing_set = None

    for j in range(k):
        if(i==j):
            testing_set = folds[i]
        elif(training_set is not None):
            training_set = pd.concat([training_set, folds[j]])
        else:
            training_set = folds[j]
    
    return training_set, testing_set

import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
def plot_confusion_matrix_with_accuracy(classes, y_true, y_pred, title, sum_overall_accuracy, total_predictions):
    cm = ConfusionMatrix(y_true, y_pred) 
    print('Current Overall accuracy: ' + str(cm.stats()['overall']['Accuracy']))
    if total_predictions != 0:
        print('Total Overall Accuracy: ' + str(sum_overall_accuracy/total_predictions))
    else:
        print('Total Overall Accuracy: ' + str(cm.stats()['overall']['Accuracy']))

    conf_matrix = confusion_matrix(y_true, y_pred)
    plt.figure()
    plot_confusion_matrix(conf_matrix, classes=classes, title=title)
    plt.show()

# K-folds cross validation 
# K=5 or K=10 are generally used. 
# Note that the overall execution time increases linearly with k
k = 5

# Define the classes for the classifier
#classes = ['0','1','2']

# Make Dataset random before start
df_rand = df.sample(df.storypoint.count(), random_state=99)

# Number of examples in each fold
fsamples =  int(df_rand.storypoint.count() / k)

# Fill folds (obs: last folder could contain less than fsamples datapoints)
folds = list()
for i in range(k):
    folds.append(df_rand.iloc[i * fsamples : (i + 1) * fsamples])
        
# Init
sum_overall_accuracy = 0
total_predictions = 0

# Repeat k times and average results
for i in range(k):
    
    #1 - Build new training and testing set for iteration i
    training_set, testing_set  = rebuild_kfold_sets(folds, k, i)
    y_true = testing_set.storypoint.tolist()
    
    #2 - Oversample (ONLY TRAINING DATA)
    X_resampled, y_resampled = SimpleOverSample(training_set.label_title_desc.values.tolist(), training_set.storypoint.values.tolist())
    
    #3 - train
    clf = FastTextClassifier()
    clf.fit(X_resampled, y_resampled)
    
    #4 - Predict
    y_pred = clf.predict(testing_set.label_title_desc.values.tolist())

    #3 - Update Overall Accuracy
    for num_pred in range(len(y_pred)):
        if(y_pred[num_pred] == y_true[num_pred]):
            sum_overall_accuracy += 1
        total_predictions += 1

    #4 - Plot Confusion Matrix and accuracy 
    plot_confusion_matrix_with_accuracy(classes, y_true, y_pred, 'Confusion matrix (testing-set folder = ' + str(i) + ')', sum_overall_accuracy, total_predictions)

ts = testing_set[["issuekey", "title", "description", "storypoint"]] #select only the columns to be serialized

ts["prediction"] = y_pred # add predictions to the dataframe

from IPython.html import widgets
jsonDf = ts.to_json(orient='records')
widgets.HTML(value = ''' backlog_items = ''' + jsonDf)

y_pred = [int(integer) for integer in y_pred]
plot_confusion_matrix_with_accuracy(classes, y_true, y_pred, 'Confusion matrix (testing-set folder = ' + str(i) + ')', sum_overall_accuracy, total_predictions)



