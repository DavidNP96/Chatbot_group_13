
import evaluation
import data_class
import sys
sys.path.append("../../data")

data = data_class.Data("../../data/dialog_acts.dat")
test_sents = data.test_sents
test_labels = data.test_labels


def main():
    print(" 'inform' baseline metrics:")
    data = data_class.Data("../../data/dialog_acts.dat")
    test_sents = data.test_sents
    test_labels = data.test_labels

    predictions = []
    y_true = 0
    y_pred = 0
    predictions = []
    positives = 0
    for line, label in zip(test_sents, test_labels):
        if label == "inform":
            y_true += 1
            positives += 1
        predictions.append("inform")

        y_pred += 1

    print("Evaluation score inform baseline:")
    evaluation.get_metrics(predictions, test_labels)
    return predictions, y_true, y_pred, positives


def process_incoming_string():
    request = input("Enter your value: ")
    return("inform")
