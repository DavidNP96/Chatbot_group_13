#In this file, we find sentences that are classified incorrectly for sentences from all models
import models as m
import data_class

#load data
data = data_class.Data("../data/dialog_acts.dat")
train_sents = data.train_sents
train_labels = data.train_labels
test_sents = data.test_sents
test_labels = data.test_labels
models = m.Models()

#load predictions from all models
predictions = [[], [], [], [], []]
predictions[0] = models.inform_baseline()
predictions[1] = models.keyword_matcher()
predictions[2] = models.logistic_regression().tolist()
shallow_tree = models.random_forest(4)
deep_tree = models.random_forest(20)
predictions[3] = shallow_tree.tolist()
predictions[4] = deep_tree.tolist()
listofzeros = [0] * len(test_labels)

#get incorrect predictions for each model
for label_index in range(len(test_labels)):
    for model_index in range(5):
        if test_labels[label_index] != predictions[model_index][label_index]:
            predictions[model_index][label_index] = 0

#check whether sentences are misclassified by each model
incorrect_sents = 0
for label_index in range(len(test_sents)):
    if predictions[0][label_index] == 0 and predictions[1][label_index] == 0 and predictions[2][label_index] == 0 \
            and predictions[3][label_index] == 0 and predictions[4][label_index] == 0:
        #if the model is consistently missclassified: print sentence and add one to the counter
        print(test_labels[label_index], ": ", test_sents[label_index])
        incorrect_sents += 1

print("There are", incorrect_sents, "utterances wrongly classified by all the models.")
