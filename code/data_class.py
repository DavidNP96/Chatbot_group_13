# This Class is meant to be used to split the data into tokenized or vectrized data that we can use as input for our models
import random
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class Data:
    def __init__(self, filepath):
        self.FILE_PATH = filepath
        self.TRAIN_SPLIT = 0.85
        self.dataset = self.get_data()
        self.split_data()

    ##open data; save sentences in a list in the following format:
    ## [label (str), sentence (str)]
    def get_data(self):
        dataset = []
        with open(self.FILE_PATH, "r") as f:
            for line in f:
                #remove all capitals in the text; create a list out of sentence where each word is an element
                sent = line.lower().split()
                #save sentences into a list with labels and sentences seperated
                dataset.append([sent[0], ' '.join(sent[1:])])
        return dataset

    #split the data into test- and train sentences and -labels
    def split_data(self):
        #extract sentences and labels seperately from the data
        self.sents = [sent for _, sent in self.dataset]
        labels = [label for label,_ in self.dataset]

        #split data into a train and test set
        train_size = int(len(self.dataset) * (self.TRAIN_SPLIT))
        train_sents = self.sents[:train_size]
        train_labels = labels[:train_size]

        #save test sentences and labels
        self.test_sents = self.sents[train_size:]
        self.test_labels = labels[train_size:]

        #randomly shuffle the train data; then save train sentences and labels
        train_data = list(zip(train_sents, train_labels))
        random.shuffle(train_data)
        self.train_sents, self.train_labels = zip(*train_data)

    #create Bag-of-Words vectors for the train and test sentences
    def create_bow(self):
        count_vect = CountVectorizer()
        #create vectors for the train text
        X_train_counts = count_vect.fit_transform(self.train_sents)
        #transform vectors using TF-IDF
        tfidf_transformer = TfidfTransformer()
        X_train = tfidf_transformer.fit_transform(X_train_counts)

        #fit test sentences to the bag of words vectors
        X_test = tfidf_transformer.transform(
            count_vect.transform(self.test_sents))
        return X_train, X_test, count_vect, tfidf_transformer

    #this function creates a dataframe from the input data
    #another dataframe is created in which the unique labels are listed with their corresponding ids
    def create_data_frame(self):
        #open data
        text_data = []
        with open(self.FILE_PATH, "r") as f:
            for line in f:
                sent = line.lower().split()
                text_data.append([sent[0], ' '.join(sent[1:])])
        #create dataframe
        data_frame = pd.DataFrame(text_data, columns=['label', 'text'])
        #assign ids per label in the data
        data_frame['label_id'] = data_frame['label'].factorize()[0]
        #create dataframe with just the unique labels and their ids
        label_id_df = data_frame[['label', 'label_id']].drop_duplicates().sort_values('label_id')
        #save sentences, labels, label ids and unique-label-dataframe
        self.sents = data_frame['text']
        self.labels = data_frame['label']
        self.label_ids = data_frame['label_id']
        self.label_id_df = label_id_df
        return data_frame, label_id_df

if __name__ == "__main__":
    data = Data("./data/dialog_acts.dat")
    splitted_data = data.split_data()
    print(splitted_data[0])
