import numpy as np
import random
import sklearn.metrics as skm
from operator import itemgetter
from collections import Counter
import sys
sys.path.append("../../data")
import data_class
import test

def main(sents, labels):
    ### classify sentence based on keywords found in sentence
    print("keyword matching metrics:")
    labels = ['inform', 'request', 'thankyou', 'reqalts', 'null', 'affirm', 'bye', 
    'confirm', 'hello', 'negate', 'deny', 'repeat', 'ack', 'restart', 'reqmore']

    keywords = {"inform":["know", "food", "restaurant", "town", "part"], 
                    "request": ["number", "phone", "address", "whats", "code", "post"], 
                    "thankyou": ["thanks", "appreciate", "thank"], "reqalts":["else", "anything"], 
                    "null": ["ah", "uh", "ugh", "oh", "noise", "sil", "unintelligible"], 
                    "affirm": ["yes", "true", "correct","affirmative", "uh-huh", "agree", "acknowledge","concede", "right", "yea", "yeah"], 
                    "bye": ["goodbye", "bye", "cya", "farewell", "laters"],
                    "confirm": ["serve","priced","center"], 
                    "hello": ["hi", "hey", "hello", "greetings"], 
                    "negate": ["not","none"], 
                    "deny": ["dont", "wont","no", "negative", "false","disagree", "reject", "wrong", "want", "incorrect"],
                    "repeat":["repeat", "recur", "echo", "back"], 
                    "ack":["okay", "alright", "ok", "kay", "um"], 
                    "restart":["start", "reset", "restart"], 
                    "reqmore":["more","other"]}

    # import data                
    data = data_class.Data("../../data/dialog_acts.dat")
    train_sents = sents
    train_labels = labels

    train_pred = []
    for sentence in train_sents:
        labels_counter = Counter()

        for word in sentence.split(' '):
            
            for label, keyword in keywords.items():
                if word in keyword:
                    labels_counter[label] += 1

        # select the most probable one            
        mx = labels_counter.most_common(1)

        # check if there is a tie between most likely labels
        maxes = [ele[0] for ele in labels_counter.items() if ele[1] >= mx[0][1]]

        if len(maxes) == 1:
            train_pred.append(maxes[0])
        elif len(maxes) == 0: # if no keywords are found select the most probable class based on distribution
            train_pred.append("inform")
        else:
            # check which of the multiple classes is most likely based on prior
            filled = False
            for label in labels:
                for max in maxes:
                    if max == label and filled == False:
                        train_pred.append(label)
                        filled = True
    

    #test.get_metrics(train_pred, train_labels)
    return train_pred