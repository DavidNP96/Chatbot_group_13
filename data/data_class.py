
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from collections import Counter
import random

# FILE_PATH = '../data/dialog_acts.dat'
# STOP_WORDS = set(stopwords.words('english'))
# TRAIN_SPLIT = 0.85
# SEED = 42

class Data:
  def __init__(self, filepath):
    print("get filepath ", filepath)
    self.FILE_PATH = filepath
    # self.STOPWORDS = set(stopwords.words('english'))
    self.TRAIN_SPLIT = 0.85
    self.SEED = 42
    self.dataset = self.get_data()

  def get_data(self):
    dataset = []

    with open(self.FILE_PATH, "r") as f:
        for line in f:
            sent = line.lower().split()
            dataset.append([sent[0], ' '.join(sent[1:])])
    return dataset

  def split_data(self):
    sents = [sent for label, sent in self.dataset]
    labels = [label for label, sent in self.dataset]
    # tokenizer = Tokenizer()

    # # fit the tokenizer on the documents
    # tokenizer.fit_on_texts(doc)

    train_size = int(len(self.dataset) * (self.TRAIN_SPLIT))
    train_sents = sents[:train_size]
    train_labels = labels[:train_size]

    test_sents = sents[train_size:]
    test_labels = labels[train_size:]

    train_data = list(zip(train_sents, train_labels))
    random.Random(self.SEED).shuffle(train_data)
    train_sents, train_labels = zip(*train_data)

    return train_data, train_labels, test_sents, test_labels

if __name__=="__main__":
  data = Data("./dialog_acts.dat")
  splitted_data = data.split_data()
  print(splitted_data[0])