# the main file to run the dialog system

# import models
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import extract_meaning
import pandas as pd
import pickle
import sys
sys.path.append("../models")
sys.path.append("../../data")


# relevant filepaths
TRAINED_MODELS_FP = "../../trained_models/"
DATAPATH = "../../data/"


def main():
    # initial interface for the dialog system
    match = False

    ds = Dialog_system()

    print("Welcome! I hope you are having a nice day. Are you feeling hungry? If you let me know what and where you would like to eat and how much you are willing to spend, I can recommend you some nice restaurants: \n ")

    while match == False:
        customer_input = input("").lower()
        response, match = ds.updated_customer_input(customer_input)
        print(response)

class Dialog_system:

    def __init__(self):
        self.dialog_state = Dialog_state()
        self.dialog_act = Dialog_act()
        self.restaurant_info = RestaurantInfo()
        self.preferences = {"area": "",
                            "food": "",
                            "pricerange": ""}
        self.missing_preferences = ["area", "food", "pricerange"]
        self.restaurant_suggestion = None
        self.provided_info = []
        self.item = ""
        self.count_options = 0

    def updated_customer_input(self, customer_input):
        # triggered if new customer input received

        # update state and customer input
        self.customer_input = customer_input
        self.dialog_act.update_act(customer_input)
        self.dialog_state.update_state(self.dialog_act.dialog_act, self.missing_preferences)
        # create reponse based on updated dialog_state
        response = self.create_response()

        match = False
        if self.dialog_state.state == "goodbye":
            match = True

        return response, match

    def create_response(self):

        # create response based on dialog_state and cutomer_input
        options = {"hello": self.hello,
                   "express_preferences": self.update_preferences,
                   "suggest_restaurant": self.suggest_restaurant,
                   "request_restaurant_information": self.request_restaurant_information,
                   "request_add_info": self.request_restaurant_information,
                   "goodbye": self.goodbye
                   }
        action = options[self.dialog_state.state]

        response = action()

        # return response
        return response

    def update_preferences(self):
        # this function updates the preferences according to the user's input
        confirmation = self.extract_preferences()

        self.missing_preferences = []

        # check for missing preferences
        for key, value in self.preferences.items():
            if value == "":
                self.missing_preferences.append(key)

        # still missing preferences
        if len(self.missing_preferences) > 0:
            if self.missing_preferences[0] == 'area':
                response = confirmation + 'In what area would you like to eat?'
                self.item = "area"
            elif self.missing_preferences[0] == 'food':
                response = confirmation + 'What type of cuisine would you prefer?'
                self.item = "food"
            else:
                response = confirmation + 'Excuse me for asking, but what is your pricerange today?'
                self.item = "pricerange"
        else:
            self.dialog_state.update_state(self.dialog_act.dialog_act, self.missing_preferences)
            response = self.create_response()
        return response

    def extract_preferences(self):
        preferences = extract_meaning.extract_preferences(self.customer_input, self.item)
        if preferences == {}:
            confirmation = 'I am sorry I did not quite get that. '
        else: 
            confirmation  = 'Great choice. '
        # update preferences
        for preference, value in preferences.items():
            print(preference, value)
            self.preferences[preference] = value
        return confirmation

    def refresh_preferences(self):
        self.preferences = {"area": "any",
                            "food": "any",
                            "pricerange": "any"}
        self.missing_preferences = ["area", "food", "pricerange"]

    def hello(self):
        response = "Hi! so nice to meet you. What would you like to eat today?"
        return response

    def suggest_restaurant(self):
        #  filter restaurants
        restaurant_options = self.restaurant_info.filter_info(self.preferences)
        if self.dialog_state.prev_state == "suggest_restaurant":
            self.count_options += 1
        else:
            self.count_options = 0
        if len(restaurant_options) == 0 or self.count_options >= len(restaurant_options):
            response = 'Unfortunately I have not found any restaurant that matches your whishes. Is there anything else you would like to eat?'
            self.count_options = 0
            self.refresh_preferences()
            self.dialog_state.update_state(self.dialog_act.dialog_act, self.missing_preferences)
        else:
            self.restaurant_suggestion = restaurant_options.iloc[self.count_options]
            response = 'I recommend you to go to ' + self.restaurant_suggestion['restaurantname'] + '. Would you like to go there?'
        print(len(restaurant_options))
        return response

    def extract_asked_information(self, costumer_input):
        information_dict = {'address' : ['address', 'adress', 'adres', 'street', 'location'],
                            'phone_number' : ['phone', 'number', 'telephone'],
                            'postcode': ['postcode', 'zipcode', 'post', 'zip', 'postalcode', 'code', 'postal'],
                            'both' : ['both', 'all']
                            }
        required_info = []
        sentence = costumer_input.split()
        for information, keywords in information_dict.items():
            for keyword in keywords:
                if keyword in sentence:
                    if information == 'both':
                        required_info.append('phone_number')
                        required_info.append('postcode')
                    else:
                        required_info.append(information)
        return required_info

    def request_restaurant_information(self):
        information_req = self.extract_asked_information(self.customer_input)
        if self.provided_info == [] and information_req == []:
            information_req.append('address') 
            response = "Great! "
        else:
            response = ""
        if str(self.restaurant_suggestion['addr']) == "nan":
            response += "Sorry, we do not have a address registered for " + self.restaurant_suggestion['restaurantname'] + ". "
        elif "address" in information_req:
            response += "The address is " + str(self.restaurant_suggestion['addr']) +  ". "
        if str(self.restaurant_suggestion['phone']) == "nan":
            response += "Sorry, we do not have a phone number registered for " + self.restaurant_suggestion['restaurantname'] + ". "
        elif "phone_number" in information_req:
            response += "The phone number is " + str(self.restaurant_suggestion['phone']) + ". "
        if str(self.restaurant_suggestion['postcode']) == "nan":
            response += "Sorry, we do not have a postal code registered for " + self.restaurant_suggestion['restaurantname'] + ". "
        elif "postcode" in information_req :
            response += "The postal code is " + str(self.restaurant_suggestion['postcode']) + ". "
        if information_req == [] or self.provided_info == []:
            response += 'Would you like to know the phone number or the postcode? Or maybe both?'
        for information in information_req:
            self.provided_info.append(information)

        return response

    def goodbye(self):
        response = "Enjoy your dinner"
        return response


class Dialog_act:
    def __init__(self):
        self.dialog_act = ""
        self.models = self.load_models()
        self.count_vect = pickle.load(
            open("../../trained_models/vectorizer.pickle", 'rb'))
        self.tfidf_transformer = pickle.load(
            open("../../trained_models/tfidf.pickle", 'rb'))

    #classify the dialog act of the user's input
    def update_act(self, customer_input, classifier="logistic_regression"):
        # use imported model to predict dialog_act
        model = self.models[classifier]  # import model
        self.dialog_act = model.predict(self.create_bow(customer_input))[0]

    #load all models we have available
    def load_models(self):
        trained_models = {}
        # all available models
        trained_model_names = ["logistic_regression", "deep_tree", "shallow_tree"]

        # load all classifier models
        for trained_model_name in trained_model_names:
            trained_model = open(
                f"{TRAINED_MODELS_FP}{trained_model_name}.pickle", 'rb')
            classifier = pickle.load(trained_model)
            trained_models['{}'.format(trained_model_name)] = classifier
            trained_model.close()
        return trained_models

    #selects classifier model
    def select_model(self, model_name):
        self.model = self.models[model_name]

    #transforms the user's text input (str) to our Bag-of-Word vectors
    def create_bow(self, customer_input):
        bow = self.tfidf_transformer.transform(self.count_vect.transform([customer_input]))
        return bow

class Dialog_state:

    def __init__(self):
        self.state = "hello"
        self.prev_state = "hello"

    def update_info(self, request):
        self.info[request[0]] = request[1]

    def update_state(self, act, missing_preferences=[]):
        if self.state == "hello":
            if act == "inform":
                self.state = "express_preferences"
                self.prev_state = "hello"
            elif act == "hello":
                self.state == "hello"
                self.prev_state = "hello"

        elif self.state == "express_preferences":
            if len(missing_preferences) == 0:
                self.state = "suggest_restaurant"
                self.prev_state = "express_preferences"
            else:
                self.state = "express_preferences"
                self.prev_state = "express_preferences"

        elif self.state == "suggest_restaurant":
            if len(missing_preferences) > 0:
                self.state = "express_preferences"
                self.prev_state = "suggest_restaurant"
            if act == "affirm":
                self.state = "request_restaurant_information"
                self.prev_state = "suggest_restaurant"
            elif act == "deny" or act == "negate" or act == "reqalts" or act == "reqmore":
                self.state ="suggest_restaurant"
                self.prev_state = "suggest_restaurant"

        elif self.state == "request_restaurant_information":
            #if act == "reqmore":
            #    self.state = "request_add_info"
            if act == "thankyou":
                self.state = "goodbye"

    def extract_preferences(self, customer_input):
        return


class RestaurantInfo:

    def __init__(self):
        self.data = self.load_data()
        self.recommendations = []

    # Load restaurant to a dataframe
    def load_data(self):
        restaurants_info = pd.read_csv(
            f"{DATAPATH}restaurant_info.csv")
        return restaurants_info

    # Filter restaurants given the user's preferences
    def filter_info(self, filter_preferences):

        # unpack array and place array elements into variables
        area = filter_preferences["area"]
        food = filter_preferences["food"]
        pricerange = filter_preferences["pricerange"]

        filtered_restaurant_info = self.data
        
        # check if variables exist, and if so, filter the dataframe on it
        if (area != "any") & (food != "any") & (pricerange != "any"):
            filtered_restaurant_info = self.data[((self.data["area"] == area) & (
                self.data["food"] == food)) & (self.data["pricerange"] == pricerange)]

        elif (area != "any") & (food != "any"):
            filtered_restaurant_info = self.data[(
                (self.data["area"] == area) & (self.data["food"] == food))]

        elif (area != "any") & (pricerange != "any"):
            filtered_restaurant_info = self.data[(
                (self.data["area"] == area) & (self.data["pricerange"] == pricerange))]

        elif (food != "any") & (pricerange != "any"):
            filtered_restaurant_info = self.data[(
                ((self.data["food"] == food)) & (self.data["pricerange"] == pricerange))]

        elif (area != "any"):
            filtered_restaurant_info = self.data["area"] == area

        elif (pricerange != "any"):
            filtered_restaurant_info = self.data["pricerange"] == pricerange

        elif (food != "any"):
            filtered_restaurant_info = self.data["food"] == food
            
        return self.data[filtered_restaurant_info]


if __name__ == "__main__":
    main()
