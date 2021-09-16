
import tensorflow as tf
from tensorflow.keras import backend as K
import sys
sys.path.append("../data")
import data_class
import inform_baseline
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sns.set_palette('Set2')
sns.set_style("darkgrid")

test_data = ["hey", "how", "are", "you"]
plot_file = "../plots/"

def main():
    model_names = ["inform_baseline"]
    model_name = input("choose one of the following models: inform_baseline key_word_baseline: ")

    while model_name not in model_names:
        model_name = input("wrong model name! choose one of the following models: 'inform_baseline', 'key_word_baseline': ")

    data = data_class.Data("../data/dialog_acts.dat")
    get_metrics(model_name, data.test_sents, data.test_labels)
    
    return True

def get_model_predictions(model_name, x_values, y_values):
    predictions = []

    options = {"inform_baseline" : inform_baseline.classify_request(x_values, y_values),
                "key_word_baseline": "not in use yet",
                "bert" : "not in use yet" }

    y_true, y_pred, positives = options[model_name]
    return y_true, y_pred, positives
    

def get_metrics(model_name, x_values, y_values):
    y_true, y_pred, positives = get_model_predictions(model_name=model_name, x_values=x_values, y_values=y_values)
    print("Y_true and y_pred",y_true, y_pred, positives)
    recall = recall_m(y_true=y_true, y_pred=y_pred, positives=positives)
    precision = precision_m(y_true, y_pred)
    f1 = f1_m(y_true, y_pred, positives)
    tp =TP(y_true, y_pred)
    tn = TN(y_true, y_pred)
    fp = FP(y_true, y_pred)
    
    metrics = {
    "recall": recall,
    "precision": precision,
    "f1": f1,
    "TP": tp,
    "TN":tn,
    "FP": fp }
    print("model metrics are:",metrics)

    return metrics

def create_confusion_matrix(label_id_df, y_labels,predicted, file_name):
    conf_mat = confusion_matrix(y_labels, predicted)

    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=label_id_df.label.values, yticklabels=label_id_df.label.values)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(plot_file + file_name)

def recall_m(y_true, y_pred, positives): # TPR
    # true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    # possible_positives = K.sum(K.round(K.clip(y_true, 0, 1))) # P
    # print("bottom statment", possible_positives + K.epsilon())
    # recall =  tf.cast(true_positives,tf.int32 ) / tf.cast((possible_positives + K.epsilon()), tf.int32 )
    recall = y_true/positives
    return recall
 
def precision_m(y_true, y_pred):
    # true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    # predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1))) # TP + FP
    # precision = true_positives / (predicted_positives + K.epsilon())
    precision = y_true/y_pred
    return precision
 
def f1_m(y_true, y_pred, positives):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred, positives=positives)
    return 2*((precision*recall)/(precision+recall))
 
def TP(y_true, y_pred):
    # tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    # y_pos = K.round(K.clip(y_true, 0, 1))
    # n_pos = K.sum(y_pos)
    # y_neg = 1 - y_pos
    # n_neg = K.sum(y_neg)
    # n = n_pos + n_neg
    return y_true/y_pred
 
def TN(y_true, y_pred):
    y_pos = y_true
    n_pos = y_pos
    y_neg = 1 - y_pos
    n_neg = y_neg
    n = n_pos + n_neg
    y_pred_pos = y_pred
    y_pred_neg = 1 - y_pred_pos
    tn = y_neg * y_pred_neg

    return tn/n
 
def FP(y_true, y_pred):
    y_pos = K.round(K.clip(y_true, 0, 1))
    n_pos = K.sum(y_pos)
    y_neg = 1 - y_pos
    n_neg = K.sum(y_neg)
    n = n_pos + n_neg
    tn = K.sum(K.round(K.clip(y_neg * y_pred, 0, 1))) # FP
    return tn/n
 
def FN(y_true, y_pred):
    y_pos = K.round(K.clip(y_true, 0, 1))
    n_pos = K.sum(y_pos)
    y_neg = 1 - y_pos
    n_neg = K.sum(y_neg)
    n = n_pos + n_neg
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos
    tn = K.sum(K.round(K.clip(y_true * y_pred_neg, 0, 1))) # FN
    return tn/n

    


if __name__=="__main__":
    main()
    
