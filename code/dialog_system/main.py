# the main file to run the dialog system

# import models
import pickle
import sys
sys.path.append("../models")

# relevant filepaths
TRAINED_MODELS_FP = "../models/trained_models/"


def main():
    # initial interface for the dialog system
    match = False

    ds = Dialog_system()

    while match == False:
        customer_input = input("").lower()
        response, match = ds.updated_customer_input(customer_input)
        print(response)


class Dialog_system:

    def __init__(self):
        self.dialog_state = Dialog_state()
        self.preferences = {}

    def updated_customer_input(self, customer_input):
        # triggered if new customer input received

        # update state and customer input
        self.customer_input = customer_input
        self.dialog_state.update_state(customer_input)

        # create reponse based on updated dialog_state
        response, match = self.create_response()

        return response, match

    def create_response(self):

        # create response based on dialog_state and cutomer_input
        options = {"inform": self.inform(),
                   # fill in rest of options and create fitting functions
                   }

        options[self.dialog_state]

        # return response
        response = ""
        return response

    def extract_preferences():
        # extract preferences from levenstein distance
        preferences = ""
        return preferences

    def calculate_levenstein_distance(self):
        return

    def inform(self):
        preferences = self.extract_preferences()
        self.preferances.append(preferences)

        #  if preferences are sufficient
        # make request
        # else:
        # ask for missing preferences


class Dialog_state:
    def __init__(self, customer_input):
        self.dialog_state = ""
        self.models = self.load_models()

    def update_state(self, customer_input, classifier="logistic_regression"):
        # use imported model to predict class
        model = self.models[classifier]  # import model
        self.dialog_state = model.predict(customer_input)
        print("new state: ", self.dialog_state)

    def load_models():
        trained_models = {}
        # all available models
        trained_model_names = [
            "logistic_regression", "deep_tree", "shallow_tree"]

        # load all classifier models
        for trained_model_name in trained_model_names:
            trained_model = open(
                f"{TRAINED_MODELS_FP}{trained_model_name}", 'rb')
            classifier = pickle.load(trained_model)
            trained_models['{}'.format(trained_model_name)] = classifier
            trained_model.close()
        return trained_models

    def select_model(self, model_name):
        # reselects classifier
        self.model = self.models[model_name]



if __name__ == "__main__":
    main()
