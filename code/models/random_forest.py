import numpy as np
from collections import Counter

import pandas as pd
import random
import seaborn as sns
import sys
sys.path.append("../../data")
import data_class
import test

from sklearn.ensemble import RandomForestClassifier

sns.set_palette('Set2')
sns.set_style("darkgrid")

# load data
data = data_class.Data("../../data/dialog_acts.dat")

# create dataframe
data_frame, label_id_df = data.create_data_frame()

# create bow
y_train = data.train_labels
y_test = data.test_labels
X_train, X_test = data.create_bow()

def main():
    shallow_tree(data,X_train, y_train, X_test)
    deep_tree(data,X_train, y_train, X_test, y_test)

def shallow_tree(data,X_train, y_train, X_test ):
    print("shallow random forest model metrics:")
    random_forest_model = RandomForestClassifier(max_depth=3, random_state=data.SEED).fit(X_train, y_train)
    rf_predicted = random_forest_model.predict(X_test)
    

    # get metrics and matrix
    test.get_metrics(rf_predicted ,y_test)
    
def deep_tree(data,X_train, y_train, X_test, y_test):
    print('deep random forest model metrics:')
    random_forest_model = RandomForestClassifier(max_depth=20, random_state=data.SEED).fit(X_train, y_train)
    rf_predicted = random_forest_model.predict(X_test)

    # get metrics and matrix
    test.get_metrics(rf_predicted ,y_test)
    

if __name__=="__main__":
    shallow_tree(data,X_train, y_train, X_test)
    deep_tree(data,X_train, y_train, X_test, y_test)
    # test.create_confusion_matrix(label_id_df, y_test,rf_predicted, file_name="deep_hm.png")
    # test.create_confusion_matrix(label_id_df, y_test,rf_predicted, file_name="shallow_hm.png")


    

