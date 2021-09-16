import numpy as np
import nltk
from nltk.corpus import stopwords
from collections import Counter

import pandas as pd
import random
import seaborn as sns
import sys
sys.path.append("../data")
import data_class
import test

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

sns.set_palette('Set2')
sns.set_style("darkgrid")

data = data_class.Data("../data/dialog_acts.dat")
train_sents = data.train_sents
train_labels = data.train_labels
test_sents = data.train_sents
test_labels = data.test_labels

# transform text to bag of words
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_sents)
tfidf_transformer = TfidfTransformer()
X_train = tfidf_transformer.fit_transform(X_train_counts)
X_test = tfidf_transformer.transform(count_vect.transform(test_sents))

# create dataframe
data_frame, label_id_df = data.create_data_frame()
sents = data_frame['text']
labels = data_frame['label']
label_ids = data_frame['label_id']

# create bof
X_train, X_test = data.create_bof()

def shallow_tree(data,X_train, train_labels, X_test ):
    random_forest_model = RandomForestClassifier(max_depth=3, random_state=data.SEED).fit(X_train, train_labels)
    rf_predicted = random_forest_model.predict(X_test)
    print('accuracy score : ', round(accuracy_score(test_labels, rf_predicted),4))
    test.create_confusion_matrix(label_id_df, data.test_labels,rf_predicted)

def deep_tree(data,X_train, train_labels, X_test, test_labels):
    print('random forest model')
    random_forest_model = RandomForestClassifier(max_depth=20, random_state=data.SEED).fit(X_train, train_labels)
    rf_predicted = random_forest_model.predict(X_test)
    print('accuracy score : ', round(accuracy_score(test_labels, rf_predicted),4))
    print('f1 score : ', round(f1_score(test_labels, rf_predicted, average = 'macro'),4))
    print('recall score : ', round(recall_score(test_labels, rf_predicted, average = 'macro'),4))
    print('precision score : ', round(precision_score(test_labels, rf_predicted, average = 'macro'),4))
    test.create_confusion_matrix(label_id_df, data.test_labels,rf_predicted)

if __name__=="__main__":
    shallow_tree(data,X_train, train_labels, X_test)
    deep_tree(data,X_train, train_labels, X_test, test_labels)
    

