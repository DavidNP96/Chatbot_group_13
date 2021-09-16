import numpy as np
import pandas as pd
import seaborn as sns
import sys
sys.path.append("../../data")
import data_class
import test

from sklearn.linear_model import LogisticRegression



sns.set_palette('Set2')
sns.set_style("darkgrid")

def main():
    print("Logistic regression model metrics:")
    # import data                
    data = data_class.Data("../../data/dialog_acts.dat")

    # create dataframe
    data_frame, label_id_df = data.create_data_frame()

    # create bow
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    # logistic model 
    logistic_model = LogisticRegression(random_state=data.SEED, multi_class='multinomial').fit(X_train, y_train)
    lm_predicted = logistic_model.predict(X_test)

# save model
# logistic_model.save("../models/logistic_model.model")



if __name__=="__main__":
    test.get_metrics(lm_predicted, y_test)
    test.create_confusion_matrix(label_id_df,y_test, lm_predicted, file_name="hm_log_reg.png" )