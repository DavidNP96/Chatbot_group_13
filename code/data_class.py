# This Class is meant to be used to split the data into tokenized or vectrized data that we can use as input for our models

import random
import numpy as np
import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from collections import Counter
from keras.preprocessing.text import Tokenizer
import random
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


class Data:
    def __init__(self, filepath):
        import os
        path = os.getcwd()
        print(path)
        print('xxxxxxxxxxxxxxxx')
        print("get filepath ", filepath)
        self.FILE_PATH = filepath
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

    def create_bow(self):
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(self.train_sents)
        tfidf_transformer = TfidfTransformer()
        X_train = tfidf_transformer.fit_transform(X_train_counts)

        X_test = tfidf_transformer.transform(
            count_vect.transform(self.test_sents))
        return X_train, X_test

    def create_data_frame(self):
        text_data = []
        with open(self.FILE_PATH, "r") as f:
            for line in f:
                sent = line.lower().split()
                text_data.append([sent[0], ' '.join(sent[1:])])

        data_frame = pd.DataFrame(text_data, columns=['label', 'text'])
        data_frame['label_id'] = data_frame['label'].factorize()[0]
        label_id_df = data_frame[['label', 'label_id']
                                 ].drop_duplicates().sort_values('label_id')
        self.sents = data_frame['text']
        self.labels = data_frame['label']
        self.label_ids = data_frame['label_id']
        self.label_id_df = label_id_df
        return data_frame, label_id_df


if __name__ == "__main__":
    data = Data("../data/dialog_acts.dat")
    splitted_data = data.split_data()
    print(splitted_data[0])
