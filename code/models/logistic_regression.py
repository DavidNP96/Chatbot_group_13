from sklearn.linear_model import LogisticRegression
import evaluation
import data_class
import numpy as np
import pandas as pd
import seaborn as sns
import sys
sys.path.append("../../data")


sns.set_palette('Set2')
sns.set_style("darkgrid")


def main(data):
    print("Logistic regression model metrics:")

    #load train/test text and labels. Transform text to Bag-of-Words representation
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    #train logistic model on train data, make predictions on test data
    logistic_model = LogisticRegression(multi_class='multinomial').fit(X_train, y_train)
    lm_predicted = logistic_model.predict(X_test)

    #calculate and print evaluation metrics for this model
    print("Evaluation score logistic regression:")
    evaluation.get_metrics(lm_predicted, y_test)
    return lm_predicted
