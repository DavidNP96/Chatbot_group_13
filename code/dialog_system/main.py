# the main file to run the dialog system

# import models
import pandas as pd
import pickle
import sys
sys.path.append("../models")
import extract_meaning

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

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

    # rs = RestaurantInfo()
    # print(rs.data)
    # print("\n\n\n\n ===================== \n\n\n")
    # preference = ["centre", "european", "moderate"]
    # filtered_data = rs.filter_info(preference)
    # print(filtered_data)


class Dialog_system:

    def __init__(self):
        self.dialog_state = Dialog_state()
        self.dialog_act = Dialog_act()
        self.preferences = {"area": "",
                            "food": "",
                            "pricerange": ""}
        self.missing_preferences = ["area", "food", "pricerange"]

    def updated_customer_input(self, customer_input):
        # triggered if new customer input received

        # update state and customer input
        self.customer_input = customer_input
        self.dialog_act.update_act(customer_input)
        self.dialog_state.update_state(self.dialog_act.dialog_act, self.missing_preferences)

        # create reponse based on updated dialog_state
        response, match = self.create_response(customer_input)

        return response, match

    def create_response(self, customer_input):

        # create response based on dialog_state and cutomer_input
        options = {"hello": self.hello(),
                   "express_preferences": self.update_preferences(customer_input),
                   "suggest_restaurant": self.suggest_restaurant(),
                   "request_restaurant_information": self.request_restaurant_information(),
                   "request_add_info": self.request_restaurant_information(),
                   "goodbye": self.goodbye()
                   }

        response, match = options[self.dialog_act]

        # return response
        response = ""
        return response, match

    def update_preferences(self, customer_input):

        # TODO assumes that this function updates the preferences
        self.extract_preferences(customer_input)

        self.missing_preferences = []

        # check for missing preferences
        for key, value in self.preferences.items():
            if value == "":
                self.missing_preferences.append(key)

        # still missing preferences
        if len(self.missing_preferences) > 0:
            # TODO create response in form of question
            pass
        else:
            Dialog_state.update_state(self.missing_preferences)
            # TODO create response for first missing preference
            pass
        return

    def extract_preferences(self, customer_input):
        preferences = extract_meaning.extract_preferences(customer_input)
        for preference, value in preferences.items:
            self.preferences[preference] = value
        return

    def refresh_preferences(self):
        self.info = {"area": "",
                     "food": "",
                     "pricerange": ""}

    def calculate_levenstein_distance(self):
        return

    def hello(self):
        # TODO return hello response
        pass

    def suggest_restaurant():
        # TODO suggest restaurant response
        pass

    def request_restaurant_information(self, information_req="phone_number"):
        # TODO retreive extra information
        if information_req == "phone_number":
            # return phone number resposne
            pass
        else:
            # return postal code response
            pass
        return

    def goodbye():
        return


class Dialog_act:
    def __init__(self):
        self.dialog_act = ""
        self.models = self.load_models()
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

    def update_act(self, customer_input, classifier="logistic_regression"):
        # use imported model to predict dialog_act
        model = self.models[classifier]  # import model
        self.dialog_act = model.predict(self.create_bow(customer_input))

    def load_models(self):
        trained_models = {}
        # all available models
        trained_model_names = [
            "logistic_regression", "deep_tree", "shallow_tree"]

        # load all classifier models
        for trained_model_name in trained_model_names:
            trained_model = open(
                f"{TRAINED_MODELS_FP}{trained_model_name}.pickle", 'rb')
            classifier = pickle.load(trained_model)
            trained_models['{}'.format(trained_model_name)] = classifier
            trained_model.close()
        return trained_models

    def select_model(self, model_name):
        # reselects classifier
        self.model = self.models[model_name]
        
    def create_bow(self, customer_input):
        
        #create vectors of custome input
        input_counts = self.count_vect.fit_transform(customer_input)

        #transform vectors using TF-IDF
        tdfidf_vector = self.tfidf_transformer.fit_transform(input_counts)
        return tdfidf_vector

class Dialog_state:

    def __init__(self):
        self.state = "hello"

    def update_info(self, request):
        self.info[request[0]] = request[1]

    def update_state(self, act, missing_preferences=[]):

        if self.state == "hello":
            if act == "inform":

                self.state = "express_preferences"
            elif act == "hello":
                self.state == "hello"
        elif self.state == "express_preferences":
            if len(missing_preferences) == 0:
                self.sate = "suggest_restaurant"
            else:
                self.state = "express_preferences"

        elif self.state == "suggest_restaurant":
            if act == "accept":
                self.state = "request_restaurant_information"
            elif act == "deny" or act == "negate" or act == "reqalts" or act == "reqmore":
                self.state == "suggest_restaurant"

        elif self.state == "request_restaurant_information":
            if act == "reqmore":
                self.state = "request_add_info"
            elif act == "thankyou":
                self.state == "goodbye"

    def extract_preferences(self, customer_input):
        return


class RestaurantInfo:

    def __init__(self):
        self.data = self.load_data()

    # Load function
    # Load in dataset and change it in a pandas setup
    def load_data(self):
        restaurants_info = pd.read_csv(
            "C:\\Users\\Simon\\Documents\\Master_Code\\Chatbot_group_13\\data\\restaurant_info.csv")
        return restaurants_info

    # Filter function(pd dataframe, array/list of preferences)
    def filter_info(self, filter_preferences: list):

        # unpack array and place array elements into variables
        area = filter_preferences[0]
        food_type = filter_preferences[1]
        price = filter_preferences[2]

        # check if variables exist, and if so, filter the dataframe on it
        if (area != "") & (food_type != "") & (price != ""):
            filtered_restaurant_info = self.data[((self.data["area"] == area) & (
                self.data["food"] == food_type)) & (self.data["pricerange"] == price)]

        elif (area != "") & (food_type != ""):
            filtered_restaurant_info = self.data[(
                (self.data["area"] == area) & (self.data["food"] == food_type))]

        elif (area != "") & (price != ""):
            filtered_restaurant_info = self.data[(
                (self.data["area"] == area) & (self.data["pricerange"] == price))]

        elif (food_type != "") & (price != ""):
            filtered_restaurant_info = self.data[(
                ((self.data["food"] == food_type)) & (self.data["pricerange"] == price))]

        elif (area != ""):
            filtered_restaurant_info = self.data["area"] == area

        elif (price != ""):
            filtered_restaurant_info = self.data["pricerange"] == price

        elif (food_type != ""):
            filtered_restaurant_info = self.data["food"] == food_type

        return filtered_restaurant_info


if __name__ == "__main__":
    main()
