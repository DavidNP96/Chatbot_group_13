from sklearn.linear_model import LogisticRegression
import sys
sys.path.append("../")
import evaluation
import data_class
import numpy as np
import pandas as pd
import seaborn as sns
import pickle




sns.set_palette('Set2')
sns.set_style("darkgrid")

TRAINED_MODEL_FILEPATH = "./trained_models"

def main(data):
    print("Logistic regression model metrics:")

    #load train/test text and labels. Transform text to Bag-of-Words representation
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    #train logistic model on train data, make predictions on test data
    logistic_model = LogisticRegression(multi_class='multinomial').fit(X_train, y_train)
    y_pred = logistic_model.predict(X_test)

    #calculate and print evaluation metrics for this model
    print("Evaluation score logistic regression:")
    evaluation.get_metrics(y_pred, y_test)

    # save model
    f = open(f"{TRAINED_MODEL_FILEPATH}/logistic_regression.pickle", "wb")
    pickle.dump(logistic_model, f)
    f.close()
    return y_pred

if __name__== "__main__":
    import data_class
    data = data_class.Data("../../data/dialog_acts.dat")
    main(data)