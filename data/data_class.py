import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
from keras.preprocessing.text import Tokenizer
import random

# FILE_PATH = '../data/dialog_acts.dat'
# STOP_WORDS = set(stopwords.words('english'))
# TRAIN_SPLIT = 0.85
# SEED = 42

class Data:
  def __init__(self, filepath):
    self.FILE_PATH = filepath
    self.STOPWORDS = set(stopwords.words('english'))
    self.TRAIN_SPLIT = 0.85
    self.SEED = 42
    self.data = self.get_data

  def get_data(self):
    data = []

    with open(self.FILE_PATH, "r") as f:
        for line in f:
            sent = line.lower().split()
            data.append([sent[0], ' '.join(sent[1:])])
    return data

  def split_data(self, data):
    sents = [sent for label, sent in data]
    labels = [label for label, sent in data]
    # tokenizer = Tokenizer()

    # # fit the tokenizer on the documents
    # tokenizer.fit_on_texts(doc)

    train_size = int(len(data) * (self.TRAIN_SPLIT))
    train_sents = sents[:train_size]
    train_labels = labels[:train_size]

    test_sents = sents[train_size:]
    test_labels = labels[train_size:]

    train_data = list(zip(train_sents, train_labels))
    random.Random(self.SEED).shuffle(train_data)
    train_sents, train_labels = zip(*train_data)

    return train_data, train_labels, test_sents, test_labels