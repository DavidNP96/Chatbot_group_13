import models.random_forest as random_forest
import models.logistic_regression as logistic_regression
import models.key_word_matching as key_word_matching
import models.inform_baseline as inform_baseline
import data_class

#load data
data = data_class.Data("./data/dialog_acts.dat")
model_names = ["inform_baseline", "key_word_matching", "logistic_regression", "random_forest", "all"]

#get input of user: which models to load
requested_model_name = input(
    "choose one of the following models: 'inform_baseline', 'key_word_matching', 'logistic_regression', 'random_forest' or 'all': ")

#check if input is an existing model
while requested_model_name not in model_names:
    requested_model_name = input(
        "wrong model name! choose one of the following models: 'inform_baseline', 'key_word_matching', \
            'logistic_regression', 'random_forest' or 'all': ")

#create dictionary with model names as keys and their predictions as values
models = {"inform_baseline": inform_baseline.main(data),
            "key_word_matching": key_word_matching.main(data.test_sents, data.test_labels),
            "logistic_regression": logistic_regression.main(data),
            "random_forest": random_forest.main(data)}

# if all models are requested: print performance scores for all models;
# otherwise print performance scores for selected model
if requested_model_name == "all":
    for name in model_names:
        if name != "all":
            models[name]
else:
    models[requested_model_name]
