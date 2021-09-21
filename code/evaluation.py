import models.random_forest as random_forest
import models.logistic_regression as logistic_regression
import models.key_word_matching as key_word_matching
import models.inform_baseline as inform_baseline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import data_class
import sys
sys.path.append("../data")

sns.set_palette('Set2')
sns.set_style("darkgrid")

test_data = ["hey", "how", "are", "you"]
plot_file = "../plots/"


def get_metrics(y_pred, y_true):

    print('accuracy score : ', round(accuracy_score(y_true, y_pred), 4))
    print('f1 score : ', round(f1_score(y_true, y_pred, average='macro'), 4))
    print('recall score : ', round(
        recall_score(y_true, y_pred, average='macro'), 4))
    print('precision score : ', round(
        precision_score(y_true, y_pred, average='macro'), 4))


def create_confusion_matrix(label_id_df, y_labels, predicted, file_name):
    conf_mat = confusion_matrix(
        y_labels, predicted, labels=label_id_df.label.values)
    print(conf_mat)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=label_id_df.label.values, yticklabels=label_id_df.label.values)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(plot_file + file_name)


def model_metrics(requested_model_name, model_names):

    data = data_class.Data("./data/dialog_acts.dat")
    get_metrics(data.test_sents, data.test_labels)

    models = {"inform_baseline": inform_baseline.main(data),
              "key_word_matching": key_word_matching.main(data.test_sents, data.test_labels),
              "logistic_regression": logistic_regression.main(data),
              "random_forest": random_forest.main(data)}

    if requested_model_name == "all":
        for name in model_names:
            if name != "all":
                models[name]

    else:
        models[requested_model_name]
        return True