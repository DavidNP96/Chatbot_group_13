# This Class is meant to be used to split the data into tokenized or vectrized data that we can use as input for our models

import random
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
from keras.preprocessing.text import Tokenizer
import random


class Data:
  def __init__(self, filepath):
    print("get filepath ", filepath)
    self.FILE_PATH = filepath
    # self.STOPWORDS = set(stopwords.words('english'))
    self.TRAIN_SPLIT = 0.85
    self.SEED = 42
    self.dataset = self.get_data()
    self.split_data()

  def get_data(self):
    dataset = []

    with open(self.FILE_PATH, "r") as f:
        for line in f:
            sent = line.lower().split()
            dataset.append([sent[0], ' '.join(sent[1:])])
    return dataset

  def split_data(self):
    self.sents = [sent for label, sent in self.dataset]
    labels = [label for label, sent in self.dataset]
    # tokenizer = Tokenizer()

    # # fit the tokenizer on the documents
    # tokenizer.fit_on_texts(doc)

    train_size = int(len(self.dataset) * (self.TRAIN_SPLIT))
    train_sents = self.sents[:train_size]
    train_labels = labels[:train_size]

    self.test_sents = self.sents[train_size:]
    self.test_labels = labels[train_size:]

    train_data = list(zip(train_sents, train_labels))
    random.Random(self.SEED).shuffle(train_data)
    self.train_sents, self.train_labels = zip(*train_data)


  def create_vectors(self, mode="tfidf"):
    tokenizer = tokenizer = Tokenizer()
    encoded_docs = tokenizer.texts_to_matrix(self.sents, mode=mode)
    
if __name__=="__main__":
  data = Data("./dialog_acts.dat")
  splitted_data = data.split_data()
  print(splitted_data[0])