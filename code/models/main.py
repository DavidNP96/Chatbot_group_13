import evaluation

model_names = ["inform_baseline", "key_word_matching", "logistic_regression", "random_forest", "all"]
requested_model_name = input("choose one of the following models: 'inform_baseline', 'key_word_matching', 'logistic_regression', 'random_forest' or 'all': ")

while requested_model_name not in model_names:
    requested_model_name = input("wrong model name! choose one of the following models: 'inform_baseline', 'key_word_matching', 'logistic_regression', 'random_forest' or 'all': ")

evaluation.model_metrics(requested_model_name, model_names)