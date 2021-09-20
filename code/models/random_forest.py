from sklearn.ensemble import RandomForestClassifier
import evaluation

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
    rf_predicted = random_forest_model.predict(X_test)
    #get evaluation results
    print("Evaluation score random forest with depth" + str(max_depth) +":")
    evaluation.get_metrics(y_predicted, y_test)
    return y_predicted