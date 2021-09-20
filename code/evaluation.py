from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append("../data")

sns.set_palette('Set2')
sns.set_style("darkgrid")

test_data = ["hey", "how", "are", "you"]
plot_file = "../plots/"

#given predicted labels and true labels, print accuracy, macro- F1, recall and precision
def get_metrics(y_pred, y_true):
    print('accuracy score : ', round(accuracy_score(y_true, y_pred), 4))
    print('macro-f1 score : ', round(f1_score(y_true, y_pred, average='macro'), 4))
    print('macro-recall score : ', round(recall_score(y_true, y_pred, average='macro'), 4))
    print('macro-precision score : ', round(precision_score(y_true, y_pred, average='macro'), 4))

# given predicted and true labels, create a confusion matrix and save a heatmap of the matrix
def create_confusion_matrix(label_id_df, y_true, y_pred, file_name):
    conf_mat = confusion_matrix(y_true, y_pred, labels=label_id_df.label.values)
    print(conf_mat)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=label_id_df.label.values, yticklabels=label_id_df.label.values)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(plot_file + file_name)