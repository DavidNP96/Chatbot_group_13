# the main file to run the dialog system

# import models
import sys
sys.path.append("../data")
sys.path.append("../code")

from sklearn.utils.extmath import log_logistic
import pyttsx3
import extract_meaning
import pandas as pd
import pickle
import time

from models import Models

# relevant filepaths
TRAINED_MODELS_FP = "../trained_models/"
DATAPATH = "../data/"

# SETTINGS:
TEXT2SPEECH = False
# friendliness settings: choose between "FRIENDLY" and "TERSE"
FRIENDLINESS = "TERSE"


def main():
    # Interface for the dialog system
    match = False

    ds = Dialog_system()
    engine = pyttsx3.init()

    welcome_message = {"FRIENDLY": "Welcome! I hope you are having a nice day. Are you feeling hungry? If you let me know what and " +
                       "where you would like to eat and how much you are willing to spend, I can recommend you some " +
                       "nice places to  eat. \n If you would like to restart the dialog you can do so at any point by" +
                       " typing \'restart dialog\'.",
                       "TERSE": "Welcome. I am a restaurant recommentation system. Based on cuisine, pricerange and area " +
                       "preferences I recommend restaurants. The dialog can be restarted at " +
                       "any moment by typing \'restart dialog\'."}
    if TEXT2SPEECH:
        engine.say(welcome_message[FRIENDLINESS])
        engine.runAndWait()
    print(welcome_message[FRIENDLINESS])

    while match == False:
        customer_input = input("").lower()
        if customer_input == "restart dialog":
            ds = Dialog_system()
            if TEXT2SPEECH:
                engine.say(welcome_message[FRIENDLINESS])
                engine.runAndWait()
            print(welcome_message[FRIENDLINESS])
        if "retrain" in customer_input:
            ds.dialog_act.retrain_model()
            print("I just retrained my model how can I help you?")
        else:
            response, match = ds.updated_customer_input(customer_input)
            if TEXT2SPEECH:
                engine.say(response)
                engine.runAndWait()
            else:
                time.sleep(0.5)
            print(response)


class Dialog_system:

    def __init__(self):
        self.dialog_state = Dialog_state()
        self.dialog_act = Dialog_act()
        self.restaurant_info = RestaurantInfo()
        self.preferences = {"area": [],
                            "food": [],
                            "pricerange": []}
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
        self.dialog_state.update_state(
            self.dialog_act.dialog_act, self.missing_preferences)
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
                   "get_add_preferences": self.get_additional_information,
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
            if value == []:
                self.missing_preferences.append(key)

        # still missing preferences
        if len(self.missing_preferences) > 0:
            # use singular of restaurant when we have 1 restaurant
            if self.restaurant_info.restaurant_count(self.preferences) == 1:
                restaurant = "restaurant"
            else:  # otherwise use plural for restaurants
                restaurant = "restaurants"
            retrieval_update = {"FRIENDLY": f"So far I've found {self.restaurant_info.restaurant_count(self.preferences)} {restaurant} " +
                                "that match your whishes. ",
                                "TERSE": f"{self.restaurant_info.restaurant_count(self.preferences)} {restaurant} matches. "}

            if self.missing_preferences[0] == "area":
                response = {"FRIENDLY": f"{confirmation} {retrieval_update[FRIENDLINESS]} In what area would you like to eat?",
                            "TERSE": f"{retrieval_update[FRIENDLINESS]} What area?"}
                self.item = "area"
            elif self.missing_preferences[0] == "food":
                response = {"FRIENDLY": f"{confirmation} {retrieval_update[FRIENDLINESS]} What type of cuisine do you feel like eating today?",
                            "TERSE": f"{retrieval_update[FRIENDLINESS]} What cuisine ?"}
                self.item = "food"
            else:
                response = {"FRIENDLY": f"{confirmation} {retrieval_update[FRIENDLINESS]} Excuse me for asking, but what is your pricerange today?",
                            "TERSE": f"{retrieval_update[FRIENDLINESS]} What pricerange?"}
                self.item = "pricerange"
            response = response[FRIENDLINESS]
        else:
            self.dialog_state.update_state(
                self.dialog_act.dialog_act, self.missing_preferences)
            response = self.create_response()
        return response

    def extract_preferences(self):
        # extract the preferences from the user input and store these
        preferences = extract_meaning.extract_preferences(
            self.customer_input, self.item, TEXT2SPEECH)
        if preferences == {}:
            confirmation = {"FRIENDLY": f"I\'m sorry I did not quite get that. ",
                            "TERSE": f"I don\'t understand. "}
        else:
            confirmation = {"FRIENDLY": f"Great choice. ",
                            "TERSE": f"OK. "}
        # update preferences
        for preference, value in preferences.items():
            self.preferences[preference] = value
        return confirmation[FRIENDLINESS]

    def refresh_preferences(self):
        # reset the user preference when the dialog restarts or when no restaurant has been found
        self.dialog_state = Dialog_state()
        self.dialog_act = Dialog_act()
        self.restaurant_info = RestaurantInfo()
        self.preferences = {"area": [],
                            "food": [],
                            "pricerange": []}
        self.missing_preferences = ["area", "food", "pricerange"]
        self.restaurant_suggestion = None
        self.provided_info = []
        self.item = ""
        self.count_options = 0
        self.antecedents = []
        self.filtered_restaurant_options = []

    def hello(self):
        # welcome message
        response = {"FRIENDLY": f"Hi! so nice to meet you. What do you feel like eating today?",
                    "TERSE": f"What kind of food?"}
        self.item = "food"
        return response[FRIENDLINESS]

    def suggest_restaurant(self):
        #  filter restaurants
        if self.dialog_state.add_pref == True:
            restaurant_options = self.restaurant_info.filtered_restaurant_options
        else:
            restaurant_options = self.restaurant_info.filter_info(self.preferences)
        # get next restaurant option if user declines the restaurant suggestion
        if self.dialog_state.prev_state == "suggest_restaurant":
            self.count_options += 1
        else:
            self.count_options = 0
        if len(restaurant_options) == 0 or self.count_options >= len(restaurant_options):
            response = {"FRIENDLY": "Unfortunately I cannot find any restaurant that matches your whishes! What else " +
                        "would you like to eat?",
                        "TERSE": "No matches. Restarting dialog. What else do you want to eat?"}
            self.count_options = 0
            self.refresh_preferences()
            self.dialog_state.update_state(
                self.dialog_act.dialog_act, self.missing_preferences)
        else:
            self.restaurant_suggestion = restaurant_options.iloc[self.count_options]
            if self.dialog_state.add_pref == True:
                self.update_antecedents()
            # check for additional preferences
            if "additional_preferences" in self.preferences and self.preferences["additional_preferences"] != ["any"]:

                descript = f"restaurant where you can stay {self.preferences['additional_preferences'][0]}" \
                    if self.preferences["additional_preferences"][0] == "long" or \
                    self.preferences["additional_preferences"][0] == "short" else \
                    f"{self.preferences['additional_preferences'][0]} restaurant"
                response = {"FRIENDLY": f"I think {self.restaurant_suggestion['restaurantname']} would be the perfect restaurant " +
                            f"for you. It is a {self.restaurant_suggestion['pricerange']} {self.restaurant_suggestion['food']} restaurant. "
                            f"It is a {descript} because {self.give_reasons()}. Do you feel like going there?",
                            "TERSE": f"I recommend {self.restaurant_suggestion['restaurantname']}. " +
                            f"It is a {self.restaurant_suggestion['pricerange']} {self.restaurant_suggestion['food']} restaurant in " +
                            f"the {self.restaurant_suggestion['area']} of town.\n" +
                            f"It is a {descript} because {self.give_reasons()}. OK?"}
            else:
                response = {"FRIENDLY": f"I think {self.restaurant_suggestion['restaurantname']} would be the perfect restaurant " +
                            f"for you.It is a {self.restaurant_suggestion['pricerange']} {self.restaurant_suggestion['food']} restaurant" +
                            f"in the {self.restaurant_suggestion['area']} of town,  Do you feel like to going there?",
                            "TERSE": f"I recommend {self.restaurant_suggestion['restaurantname']}. It is a " +
                            f"{self.restaurant_suggestion['pricerange']} {self.restaurant_suggestion['food']} restaurant in the " +
                            f"{self.restaurant_suggestion['area']} of town. OK?"}
        return response[FRIENDLINESS]

    def give_reasons(self):
        # return the reason for the choice of restaurant.
        n = 0
        reasons = []
        for key, value in self.antecedents:
            n += 1
            if key == "length_of_stay":
                if value == "long" and self.preferences["food"][0] == "spanish":
                    reasons.append(
                        "spanish restaurants serve extensive dinners that take a long time to finish")
                else:
                    reasons.append(f"it allows for {value} stays")
            elif key == "crowdedness":
                reasons.append(f"it is usually nice and {value}")
            elif key == "food_quality":
                reasons.append(f"the food is {value}")
            elif key == "pricerange":
                reasons.append(f"the restaurant is {value}")

        reason = " and ".join(reasons)
        return reason

    def get_additional_information(self):
        #  get restaurant info based on preferences
        restaurant_options = self.restaurant_info.filter_info(self.preferences)
        if self.dialog_state.prev_state == "get_add_preferences":
            self.item = "additional_preferences"
            additional_preferences = extract_meaning.extract_preferences(
                self.customer_input, self.item, TEXT2SPEECH, True)
            if "additional_preferences" in additional_preferences:
                self.preferences["additional_preferences"] = additional_preferences["additional_preferences"]
                if self.preferences["additional_preferences"] == ["any"]:
                    self.dialog_state.add_pref = False
                    self.dialog_state.update_state(
                        self.dialog_act.dialog_act, self.missing_preferences)
                    response = self.create_response()
                else:
                    self.dialog_state.add_pref = True
                    # based on additional_preferences get antecedents
                    antecedents = self.get_antecedents()
                    # filter restaurant info based on additional preferences
                    self.antecedents = self.restaurant_info.filter_on_additional_info(
                        antecedents, restaurant_options)
                    self.dialog_state.update_state(
                        self.dialog_act.dialog_act, self.missing_preferences)
                    response = self.create_response()
            else:
                response = {"FRIENDLY": "Sorry I did not understand. Please enter any of the following preferences: " +
                            "romantic, busy, children or long stay.",
                            "TERSE": "I don\'t understand. Choose from : romantic, busy, children or long stay."}[FRIENDLINESS]
                self.dialog_state.add_pref = False

        else:

            response = {"FRIENDLY": "Alright, is there any other preference you have for a restaurant? " +
                        " For instance, do you like some place romantic, busy, suitable for children," +
                        "or do you prefer a place where you can stay a bit longer?",
                        "TERSE": "OK, any other requirements?  Choose from romantic, busy, suitable for children," +
                        " and places where you can stay long."}[FRIENDLINESS]
        return response

    def get_antecedents(self):
        # based on the additional preferences use the dictionary to map the preferences such as 'romantic' to a list of ordered antecedents
        options = {"romantic":  [("crowdedness", "calm"), ("length_of_stay", "long"), ("food_quality", "good")],
                   "busy": [("food_quality", "good"), ("pricerange", "cheap"), ("length_of_stay", "long")],
                   "children": [("length_of_stay", "short")],
                   "long": [("length_of_stay", "long"), ("food_quality", "good"), ("pricerange", "expensive"), ("crowdedness", "calm")]}

        preference = self.preferences["additional_preferences"][0]
        antecedents = options[preference]
        self.all_antecedents = antecedents 
        return antecedents
    def update_antecedents(self):
        # check for next restaurant option which is viable
        new_antecedents = []
        res_sugg = self.restaurant_suggestion
        res_antecedents = [res_sugg["crowdedness"], res_sugg["food_quality"], res_sugg["length_of_stay"]]
        for antecedent in self.all_antecedents:
            if antecedent[1] in res_antecedents: 
                new_antecedents.append(antecedent)
        self.antecedents = new_antecedents
         

    def extract_asked_information(self, costumer_input):
        # get the information that the user wants of the suggested restaurant
        information_dict = {"address": ["address", "adress", "adres", "street", "location"],
                            "phone_number": ["phone", "number", "telephone"],
                            "postcode": ["postcode", "zipcode", "post", "zip", "postalcode", "code", "postal"],
                            "both": ["both", "all"]
                            }
        required_info = []
        sentence = costumer_input.split()
        for information, keywords in information_dict.items():
            for keyword in keywords:
                if keyword in sentence:
                    if information == "both":
                        required_info.append("phone_number")
                        required_info.append("postcode")
                    else:
                        required_info.append(information)
        return required_info

    def request_restaurant_information(self):
        # give the information that the user desires of the suggested restaurant
        information_req = self.extract_asked_information(self.customer_input)
        if self.provided_info == [] and information_req == []:
            information_req.append("address")
            response = {"FRIENDLY": "Great! ", "TERSE": "OK. "}[FRIENDLINESS]
        else:
            response = ""
        if "address" in information_req:
            if str(self.restaurant_suggestion["addr"]) == "nan":
                response += {"FRIENDLY": f"Sorry, we do not have a address registered for {self.restaurant_suggestion['restaurantname']}. ",
                             "TERSE": f"Address of {self.restaurant_suggestion['restaurantname']} unknown. "}[FRIENDLINESS]
            else:
                response += f"The address is {self.restaurant_suggestion['addr']}. "
        if "phone_number" in information_req:
            if str(self.restaurant_suggestion['phone']) == "nan":
                response += {"FRIENDLY": f"Sorry, we do not have a phone number registered for {self.restaurant_suggestion['restaurantname']}. ",
                             "TERSE": f"Phone number of {self.restaurant_suggestion['restaurantname']} unknown. "}[FRIENDLINESS]
            else:
                response += f"The phone number is {self.restaurant_suggestion['phone']}. "
        if "postcode" in information_req:
            if str(self.restaurant_suggestion['postcode']) == "nan":
                response += {"FRIENDLY": f"Sorry, we do not have a postal code registered for {self.restaurant_suggestion['restaurantname']}. ",
                             "TERSE": f"Postal code for {self.restaurant_suggestion['restaurantname']} unknown. "}[FRIENDLINESS]
            else:
                response += f"The postal code is {self.restaurant_suggestion['postcode']}. "
        if information_req == [] or self.provided_info == []:
            response += {"FRIENDLY": "Would you like to know their phone number or the postcode? Or maybe both? ",
                         "TERSE": "Do you want to know their phone number, the postcode, or both? "}[FRIENDLINESS]
        for information in information_req:
            self.provided_info.append(information)
        return response

    def goodbye(self):
        # goodbye message
        response = {"FRIENDLY": "Enjoy your dinner. ", "TERSE": "Bye."}
        return response[FRIENDLINESS]


class Dialog_act:
    def __init__(self):
        self.dialog_act = ""
        self.models = self.load_models()
        self.count_vect = pickle.load(
            open(f"{TRAINED_MODELS_FP}vectorizer.pickle", 'rb'))
        self.tfidf_transformer = pickle.load(
            open(f"{TRAINED_MODELS_FP}tfidf.pickle", 'rb'))

    # classify the dialog act of the user's input
    def update_act(self, customer_input, classifier="logistic_regression"):
        # use imported model to predict dialog_act
        model = self.models[classifier]  # import model
        affirm_words = ["ok", "okay", "oke", "sure", "yeah",
                        "yes", "please", "yes please", "k", "yea"]
        thankyou_words = ["thanks"]
        if customer_input.lower() in affirm_words:
            self.dialog_act = "affirm"
        elif customer_input.lower() in thankyou_words:
            self.dialog_act = "thankyou"
        else:
            self.dialog_act = model.predict(self.create_bow(customer_input))[0]

    # load all models we have available
    def load_models(self, model="logistic_regression"):

        trained_models = {}

        # only load logistic_regression model
        if model == "logistic_regression":
            trained_model = open(
                f"{TRAINED_MODELS_FP}{model}.pickle", 'rb')
            classifier = pickle.load(trained_model)
            trained_models["{}".format(model)] = classifier
            trained_model.close()
        else:
            # all available models
            trained_model_names = [
                "logistic_regression", "deep_tree", "shallow_tree"]

            # load all classifier models
            for trained_model_name in trained_model_names:
                trained_model = open(
                    f"{TRAINED_MODELS_FP}{trained_model_name}.pickle", 'rb')
                classifier = pickle.load(trained_model)
                trained_models["{}".format(trained_model_name)] = classifier
                trained_model.close()

        return trained_models

    # selects classifier model
    def select_model(self, model_name):
        self.model = self.models[model_name]

    # transforms the user's text input (str) to our Bag-of-Word vectors
    def create_bow(self, customer_input):
        bow = self.tfidf_transformer.transform(
            self.count_vect.transform([customer_input]))
        return bow

    def retrain_model(self):
        new_models = Models()
        new_models.logistic_regression()
        self.load_models()




class Dialog_state:

    def __init__(self):
        self.state = "hello"
        self.prev_state = "hello"
        self.add_pref = False

    def update_info(self, request):
        self.info[request[0]] = request[1]

    def update_state(self, act, missing_preferences=[]):
        # update the current state with the previous state and the dialog act of the user input
        if act == "bye":
            self.state = "goodbye"
        elif self.state == "hello":
            if act == "inform":
                self.state = "express_preferences"
                self.prev_state = "hello"
            elif act == "hello":
                self.state == "hello"
                self.prev_state = "hello"

        elif self.state == "express_preferences":
            if len(missing_preferences) == 0:
                self.state = "get_add_preferences"
                self.prev_state = "express_preferences"
            else:
                self.state = "express_preferences"
                self.prev_state = "express_preferences"

        elif self.state == "get_add_preferences":
            if act == "deny" or act == "negate" or (self.prev_state == "get_add_preferences" and self.add_pref == False) or self.add_pref == True :
                self.state = "suggest_restaurant"
            else:
                self.state = "get_add_preferences"
                self.add_pref = True
            self.prev_state = "get_add_preferences"

        elif self.state == "suggest_restaurant":

            if len(missing_preferences) > 0:
                self.state = "express_preferences"
                self.prev_state = "suggest_restaurant"
            elif act == "affirm":
                self.state = "request_restaurant_information"
                self.prev_state = "suggest_restaurant"
            elif act == "deny" or act == "negate" or act == "reqalts" or act == "reqmore":
                self.state = "suggest_restaurant"
                self.prev_state = "suggest_restaurant"
            else:
                self.prev_state = "express_preferences"
                f'Sorry I didn\'t understand that, please answer with yes or no.'

        elif self.state == "request_restaurant_information":
            if act == "thankyou" or act == "bye" or act == "deny" or act == "negate":
                self.state = "goodbye"


class RestaurantInfo:

    def __init__(self):
        self.data = self.load_data()
        self.recommendations = []
        self.restaurant_options = self.data
        self.filtered_restaurant_options = []

    # Load restaurant to a dataframe
    def load_data(self):
        restaurants_info = pd.read_csv(
            f"{DATAPATH}updated_restaurant_info.csv")
        return restaurants_info

    # Filter restaurants given the user's preferences
    def filter_info(self, filter_preferences):

        # unpack array and place array elements into variables
        area = filter_preferences["area"]
        food = filter_preferences["food"]
        pricerange = filter_preferences["pricerange"]

        filtered_restaurant_info = self.data

        # change empty string to any to filter
        if area == []:
            area = ["any"]
        if food == []:
            food = ["any"]
        if pricerange == []:
            pricerange = ["any"]

        # check if variables exist, and if so, filter the dataframe on it
        if (area != ["any"]) & (food != ["any"]) & (pricerange != ["any"]):
            filtered_restaurant_info = self.data[(self.data.area.isin(area)) & (
                self.data.food.isin(food)) & (self.data.pricerange.isin(pricerange))]

        elif (area != ["any"]) & (food != ["any"]):
            filtered_restaurant_info = self.data[(
                self.data.area.isin(area)) & (self.data.food.isin(food))]

        elif (area != ["any"]) & (pricerange != ["any"]):
            filtered_restaurant_info = self.data[(self.data.area.isin(
                area)) & (self.data.pricerange.isin(pricerange))]

        elif (food != ["any"]) & (pricerange != ["any"]):
            filtered_restaurant_info = self.data[(self.data.food.isin(
                food)) & (self.data.pricerange.isin(pricerange))]

        elif (area != ["any"]):
            filtered_restaurant_info = self.data[self.data.area.isin(area)]

        elif (pricerange != ["any"]):
            filtered_restaurant_info = self.data[self.data.pricerange.isin(
                pricerange)]

        elif (food != ["any"]):
            filtered_restaurant_info = self.data[self.data.food.isin(food)]

        self.restaurant_options = filtered_restaurant_info
        return filtered_restaurant_info

    def filter_on_additional_info(self, antecedents, restaurant_options):
        # general reasoning function

        # temp df used to update dataframe
        temp_df = restaurant_options
        final_df = pd.DataFrame(columns = list(restaurant_options.columns))
        new_antecedents = []
        dfs = []
        for key, antecedent in antecedents:
            # look for every key if it occurs in dataframe
            filtererd_result = temp_df
            temp_df = filtererd_result[filtererd_result[key] == antecedent]
            dfs.append(temp_df)
            new_antecedents.append((key,antecedent))
            # checks if restaurant no longer fulfills requirements
            if temp_df.empty:
                # stack all erstaurant options form most relevant to less relevant
                dfs.reverse()

                # Give all df's common column names
                for dataframe in dfs:
                    dataframe.columns = list(restaurant_options.columns)

                self.filtered_restaurant_options = pd.concat(dfs).reset_index(drop=True).drop_duplicates()
                # self.filtered_restaurant_options = filtererd_result
                new_antecedents.pop()
                # found a restauratn that fullfills minimal requirements
                return new_antecedents
        # found a restaurant that fulfills all requirements
        dfs.reverse()

        # Give all df's common column names
        for dataframe in dfs:
            dataframe.columns = list(restaurant_options.columns)

        self.filtered_restaurant_options = pd.concat(dfs).reset_index(drop=True).drop_duplicates()
        self.filtered_restaurant_options = temp_df
        return new_antecedents

    def restaurant_count(self, filter_preferences):
        # return the number of restaurants found
        return len(self.filter_info(filter_preferences))


if __name__ == "__main__":
    main()
