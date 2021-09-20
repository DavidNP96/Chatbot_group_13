import evaluation
import data_class
import sys
sys.path.append("../../data")

def main(data):
    print(" 'inform' baseline metrics:")
    #load test sentences and test labels
    #we don't need to load train data as this model is not trained
    test_sents = data.test_sents
    test_labels = data.test_labels

    #the inform baseline model classifies each label as 'inform'
    y_pred = ['inform' for label in test_labels]

    #compare classifications with true labels, print evaluation metrics
    print("Evaluation score inform baseline:")
    evaluation.get_metrics(y_pred, test_labels)
    
#this function allows the user to type a sentence, and always classifies it as 'inform'
def process_incoming_string():
    request = input("Enter your value: ")
    return("inform")
