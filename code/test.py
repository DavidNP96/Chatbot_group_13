
import tensorflow as tf
from tensorflow.keras import backend as K
import inform_baseline

test_data = ["hey", "how", "are", "you"]

def main():
    model_names = ["inform_baseline"]
    model_name = input("choose one of the following models: inform_baseline key_word_baseline: ")

    while model_name not in model_names:
        model_name = input("wrong model name! choose one of the following models: 'inform_baseline', 'key_word_baseline': ")

    get_metrics(model_name, test_data)
    
    return True

def get_model_predictions(model_name, x_values):
    predictions = []

    options = {"inform_baseline" : inform_baseline.classify_request(x_values),
                "key_word_baseline": "not in use yet",
                "bert" : "not in use yet" }

    return predictions
    

def get_metrics(model_name, x_values, y_values):
    y_pred = get_model_predictions(model_name=model_name, x_values=x_values)
    recall_m(y_values, y_pred)
    precision_m(y_values, y_pred)
    f1_m(y_values, y_pred)
    TP(y_values, y_pred)
    TN(y_values, y_pred)
    FP(y_values, y_pred)

def recall_m(y_true, y_pred): # TPR
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1))) # P
    recall = true_positives / (possible_positives + K.epsilon())
    return recall
 
def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1))) # TP + FP
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision
 
def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))
 
def TP(y_true, y_pred):
    tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # TP
    y_pos = K.round(K.clip(y_true, 0, 1))
    n_pos = K.sum(y_pos)
    y_neg = 1 - y_pos
    n_neg = K.sum(y_neg)
    n = n_pos + n_neg
    return tp/n
 
def TN(y_true, y_pred):
    y_pos = K.round(K.clip(y_true, 0, 1))
    n_pos = K.sum(y_pos)
    y_neg = 1 - y_pos
    n_neg = K.sum(y_neg)
    n = n_pos + n_neg
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos
    tn = K.sum(K.round(K.clip(y_neg * y_pred_neg, 0, 1))) # TN
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
    
