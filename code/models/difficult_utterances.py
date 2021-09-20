import numpy as np
import inform_baseline as ib
import key_word_matching as km
import logistic_regression as lr
import random_forest as rf
import data_class

data = data_class.Data("../../data/dialog_acts.dat")
train_sents = data.train_sents
train_labels = data.train_labels
test_sents = data.test_sents
test_labels = data.test_labels

pred = [[], [], [], [], []]
pred[0] = ["inform"] * len(test_labels)
pred[1] = km.main(test_sents, test_labels)
pred[2] = lr.main().tolist()
st, dt = rf.main()
pred[3] = st.tolist()
pred[4] = dt.tolist()
listofzeros = [0] * len(test_labels)

print(len(pred[0]), len(pred[1]), len(pred[2]), len(pred[3]), len(pred[4]))

for i in range(0, len(test_labels)):
    for j in range(0, 5):
        if test_labels[i] != pred[j][i]:
            pred[j][i] = 0

j = 0
for i in range(0, len(test_sents)):
    if pred[0][i] == 0 and pred[1][i] == 0 and pred[2][i] == 0 and pred[3][i] == 0 and pred[4][i] == 0:
        print(test_labels[i], ": ", test_sents[i])
        j += 1

print("There are", j, "utterances wrongly classified by all the models.")
