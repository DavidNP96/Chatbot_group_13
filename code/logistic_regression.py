import numpy as np
import nltk
nltk.download('stopwords')
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


sns.set_palette('Set2')
sns.set_style("darkgrid")

# import data                
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

# logistic model 
logistic_model = LogisticRegression(random_state=data.SEED, multi_class='multinomial').fit(X_train, data.train_labels)
lm_predicted = logistic_model.predict(X_test)
print('accuracy score : ', round(accuracy_score(data.test_labels, lm_predicted),4))
print('f1 score : ', round(f1_score(data.test_labels, lm_predicted, average = 'macro'),4))
print('recall score : ', round(recall_score(data.test_labels, lm_predicted, average = 'macro'),4))
print('precision score : ', round(precision_score(data.test_labels, lm_predicted, average = 'macro'),4))

# save model
# logistic_model.save("../models/logistic_model.model")

# test.create_confusion_matrix(label_id_df, data.test_labels,lm_predicted)

if __name__=="__main__":
    test.create_confusion_matrix(label_id_df,data.test_labels, lm_predicted, file_name="hm_log_reg.png" )