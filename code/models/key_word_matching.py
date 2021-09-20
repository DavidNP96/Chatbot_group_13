import test
import data_class
import numpy as np
import random
import sklearn.metrics as skm
from operator import itemgetter
from collections import Counter
import sys
sys.path.append("../../data")
import data_class
import evaluation

def main(test_sents, test_labels):
    ### classify sentence based on keywords found in sentence
    print("keyword matching metrics:")
    labels = ['inform', 'request', 'thankyou', 'reqalts', 'null', 'affirm', 'bye',
              'confirm', 'hello', 'negate', 'deny', 'repeat', 'ack', 'restart', 'reqmore']
    #dictionary with the labels as keys, and their matching keywords as values in a list
    keywords = {"inform": ["know", "food", "restaurant", "town", "part"],
                "request": ["number", "phone", "address", "whats", "code", "post"],
                "thankyou": ["thanks", "appreciate", "thank"], "reqalts": ["else", "anything"],
                "null": ["ah", "uh", "ugh", "oh", "noise", "sil", "unintelligible"],
                "affirm": ["yes", "true", "correct", "affirmative", "uh-huh", "agree", "acknowledge", "concede", "right", "yea", "yeah"],
                "bye": ["goodbye", "bye", "cya", "farewell", "laters"],
                "confirm": ["serve", "priced", "center"],
                "hello": ["hi", "hey", "hello", "greetings"],
                "negate": ["not", "none"],
                "deny": ["dont", "wont", "no", "negative", "false", "disagree", "reject", "wrong", "want", "incorrect"],
                "repeat": ["repeat", "recur", "echo", "back"],
                "ack": ["okay", "alright", "ok", "kay", "um"],
                "restart": ["start", "reset", "restart"],
                "reqmore": ["more", "other"]}

    y_pred = []
    for sentence in test_sents:
        labels_counter = Counter()

        for word in sentence.split(' '):

            for label, keyword in keywords.items():
                if word in keyword:
                    labels_counter[label] += 1

        # select the most probable one
        max_label = labels_counter.most_common(1)

        # check if there is a tie between most likely labels
        maxes = [label[0]
                 for label in labels_counter.items() if label[1] >= mx[0][1]]

        if len(maxes) == 1:
            y_pred.append(maxes[0])
        elif len(maxes) == 0: # if no keywords are found select the most probable class based on distribution
            y_pred.append("inform")
        else:
            # check which of the multiple classes is most likely based on prior
            filled = False
            for label in labels:
                for max in maxes:
                    if max == label and filled == False:
                        y_pred.append(label)
                        filled = True
    
    print("Evaluation score keyword matching:")
    evaluation.get_metrics(y_pred, test_labels)
    return y_pred
