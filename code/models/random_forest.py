from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append("../")
import evaluation
import pickle



TRAINED_MODEL_FILEPATH = "./trained_models"

def main(data):
    global y_train, y_test 
    global X_train, X_test

    #load train and test text and labels
    y_train = data.train_labels
    y_test = data.test_labels
    X_train, X_test = data.create_bow()

    #train both a shallow tree (max depth=3) and a deep tree (max depth=20)
    print("shallow random forest model metrics:")
    shallow_tree_y_pred = random_forest(max_depth=3)
    print("deep random forest model metrics:")
    deep_tree_y_pred = random_forest(max_depth=20)

    return shallow_tree_y_pred, deep_tree_y_pred

#train random forest with a given max depth
def random_forest(max_depth):
    #train random forest
    random_forest_model = RandomForestClassifier(
        max_depth=max_depth).fit(X_train, y_train)
    #get predictions for the test set
    y_predicted = random_forest_model.predict(X_test)
    #get evaluation results
    print("Evaluation score random forest with depth" + str(max_depth) +":")
    evaluation.get_metrics(y_predicted, y_test)

    # save model
    if max_depth > 5:
        depth = "deep"
    else: 
        depth = "shallow"

    f = open(f'{TRAINED_MODEL_FILEPATH}/{depth}_tree.pickle', 'wb')
    pickle.dump(random_forest_model, f)
    f.close()
    return y_predicted

if __name__== "__main__":
    import data_class
    data = data_class.Data("../../data/dialog_acts.dat")
    main(data)