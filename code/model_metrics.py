from models import Models
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

#all models
model_names = ["inform_baseline", "key_word_matching", "logistic_regression", "shallow_random_forest", "deep_random_forest", "all"]

models = Models()

#given predicted labels and true labels, print accuracy, macro- F1, recall and precision
def get_metrics(y_pred, y_true, model_name):
    print('accuracy score : ', round(accuracy_score(y_true, y_pred), 4))
    print('macro-f1 score : ', round(f1_score(y_true, y_pred, average='macro'), 4))
    print('macro-recall score : ', round(recall_score(y_true, y_pred, average='macro', zero_division=0), 4))
    print('macro-precision score : ', round(precision_score(y_true, y_pred, average='macro', zero_division=0), 4))
    create_confusion_matrix(models.label_id_df, y_true, y_pred, model_name)


# given predicted and true labels, create a confusion matrix and save a heatmap of the matrix
def create_confusion_matrix(label_id_df, y_true, y_pred, file_name):
    conf_mat = confusion_matrix(y_true, y_pred, labels=label_id_df.label.values)
    print(conf_mat)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=label_id_df.label.values, yticklabels=label_id_df.label.values)
    plt.ylabel('Actual', fontsize=16)
    plt.xlabel('Predicted', fontsize=16)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=14)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig(plot_file + file_name)

#get input of user: which models to load
requested_model_name = input("choose one of the following models: 'inform_baseline', 'key_word_matching', 'logistic_regression', "\
        "'shallow_random_forest', 'deep_random_forest' or 'all': ")

#check if input is an existing model
while requested_model_name not in model_names:
    requested_model_name = input(
        "wrong model name! choose one of the following models: 'inform_baseline', 'key_word_matching', \
            'logistic_regression', 'shallow_random_forest', 'deep_random_forest' or 'all': ")

#create dictionary with model names as keys and their predictions as values
all_models = {"inform_baseline": models.inform_baseline(),
            "key_word_matching": models.keyword_matcher(),
            "logistic_regression": models.logistic_regression(),
            "shallow_random_forest": models.random_forest(max_depth=3),
            "deep_random_forest": models.random_forest(max_depth=20)}

#get y_test labels
y_test = models.data.test_labels

# if all models are requested: print performance scores for all models;
# otherwise print performance scores for selected model
if requested_model_name == "all":
    for model_name in model_names:
        if model_name != "all":
            print('Performance metrics for ', model_name, ':')
            y_pred = all_models[model_name]
            get_metrics(y_pred, y_test, model_name)
else:
    all_models[requested_model_name]
    print('Performance metrics for ', requested_model_name, ':')
    y_pred = all_models[requested_model_name]
    get_metrics(y_pred, y_test, requested_model_name)
