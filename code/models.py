from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from collections import Counter
import pickle
import sys
sys.path.append("../../data")

TRAINED_MODEL_FILEPATH = "./trained_models"

def inform_baseline(data):
    #load t test labels
    #we don't need to load train data as this model is not trained
    test_labels = data.test_labels

    #the inform baseline model classifies each label as 'inform'
    y_pred = ['inform' for label in test_labels]
    return y_pred

def keyword_matcher(test_sents, test_labels):
    ### classify sentence based on keywords found in sentence
    labels = ['inform', 'request', 'thankyou', 'reqalts', 'null', 'affirm', 'bye',
              'confirm', 'hello', 'negate', 'deny', 'repeat', 'ack', 'restart', 'reqmore']
    #dictionary with the labels as keys, and their matching keywords as values in a list
    keywords = {"inform": ["know", "food", "restaurant", "town", "part"],
                "request": ["number", "phone", "address", "whats", "code", "post"],
                "thankyou": ["thanks", "appreciate", "thank"], 
                "reqalts": ["else", "anything"],
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
                 for label in labels_counter.items() if label[1] >= max_label[0][1]]

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
    return y_pred

def logistic_regression(data):
    #load train/test text and labels. Transform text to Bag-of-Words representation
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    #train logistic model on train data, make predictions on test data
    logistic_model = LogisticRegression(multi_class='multinomial').fit(X_train, y_train)
    y_pred = logistic_model.predict(X_test)
    # save model
    #f = open(f"{TRAINED_MODEL_FILEPATH}/logistic_regression.pickle", "wb")
    #pickle.dump(logistic_model, f)
    #f.close()
    return y_pred

#train random forest with a given max depth
def random_forest(data, max_depth):
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    #train random forest
    random_forest_model = RandomForestClassifier(
        max_depth=max_depth).fit(X_train, y_train)
    #get predictions for the test set
    y_pred = random_forest_model.predict(X_test)

    # save model
    #if max_depth > 5:
    #    depth = "deep"
    #else: 
    #    depth = "shallow"

    #f = open(f'{TRAINED_MODEL_FILEPATH}/{depth}_tree.pickle', 'wb')
    #pickle.dump(random_forest_model, f)
    #f.close()
    return y_pred

