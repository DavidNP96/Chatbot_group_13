# the main file to run the dialog system

# import models
import pyttsx3
import extract_meaning
import pandas as pd
import pickle
import time
import sys
sys.path.append("../models")
sys.path.append("../../data")


# relevant filepaths
TRAINED_MODELS_FP = "../../trained_models/"
DATAPATH = "../../data/"

# SETTINGS:
TEXT2SPEECH = False

FRIENDLY    = False


def main():
    # initial interface for the dialog system
    match = False

    ds = Dialog_system()
    engine = pyttsx3.init()

    if FRIENDLY:
        welcome_message = f"Welcome! I hope you are having a nice day. Are you feeling hungry? If you let me know what and where you"+ \
        " would like to eat and how much you are willing to spend, I can recommend you some nice places to  eat. \n" + \
        "If you would like to restart the dialog you can do so at any point by typing \'restart dialog\'."
    else:
        welcome_message = "Welcome. I am a restaurant recommentation system. Based on your preferences for the type of cuisine, " + \
            "pricerange and area I can recommend you a restaurant. The dialog can be restarted at any moment by typing \'restart dialog\'."
    if TEXT2SPEECH:
        engine.say(welcome_message)
        engine.runAndWait()
    print(welcome_message)

    while match == False:
        customer_input = input("").lower()
        if customer_input == 'restart dialog':
            ds = Dialog_system()
            if TEXT2SPEECH:
                engine.say(welcome_message)
                engine.runAndWait()
            print(welcome_message)
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
                restaurant = 'restaurant'
            else:  # otherwise use plural for restaurants
                restaurant = 'restaurants'
            if FRIENDLY:
                retrieval_update = f"So far I've found {self.restaurant_info.restaurant_count(self.preferences)} {restaurant} that match your whishes. "
            else:
                retrieval_update = f"There are {self.restaurant_info.restaurant_count(self.preferences)} matching restaurants so far. "
            if self.missing_preferences[0] == 'area':
                if FRIENDLY:
                    response = f'{confirmation} {retrieval_update} In what area would you like to eat?'
                else:
                    response = f'{confirmation} {retrieval_update} In what area do you want to eat?'
                self.item = "area"
            elif self.missing_preferences[0] == 'food':
                if FRIENDLY:
                    response = f'{confirmation} {retrieval_update} What type of cuisine do you feel like eating today?'
                else:
                    response = f'{confirmation} {retrieval_update} What cuisine do you prefer?'
                self.item = "food"
            else:
                if FRIENDLY:
                    response = f'{confirmation} {retrieval_update} Excuse me for asking, but what is your pricerange today?'
                else:
                    response = f'{confirmation} {retrieval_update} What is your pricerange?'
                self.item = "pricerange"
        else:
            self.dialog_state.update_state(
                self.dialog_act.dialog_act, self.missing_preferences)
            response = self.create_response()
        return response

    def extract_preferences(self):
        preferences = extract_meaning.extract_preferences(
            self.customer_input, self.item, TEXT2SPEECH)
        if preferences == {}:
            if FRIENDLY:
                confirmation = f'I\'m sorry I did not quite get that. '
            else:
                conformation = f'I\'m sorry I do not understand. '
        else: 
            if FRIENDLY:
                confirmation  = f'Great choice. '

            else:
                confirmation = f'OK. '
        # update preferences
        for preference, value in preferences.items():
            self.preferences[preference] = value
        return confirmation

    def refresh_preferences(self):
        self.preferences = {"area": [],
                            "food": [],
                            "pricerange": []}
        self.missing_preferences = ["area", "food", "pricerange"]

    def hello(self):
        if FRIENDLY:
            response = f'Hi! so nice to meet you. What do you feel like eating today?'
        else:
            response = f'Hello. What would you like to eat today?'
        return response

    def suggest_restaurant(self):
        #  filter restaurants
        if self.dialog_state.add_pref == True:
            restaurant_options = self.restaurant_info.filtered_restaurant_options
        else:
            restaurant_options = self.restaurant_info.filter_info(
                self.preferences)

        if self.dialog_state.prev_state == "suggest_restaurant":
            self.count_options += 1
        else:
            self.count_options = 0
        if len(restaurant_options) == 0 or self.count_options >= len(restaurant_options):
            if FRIENDLY:
                response = f'Unfortunately I cannot find any restaurant that matches your whishes! Is there something else you would like to eat?'
            else:
                response = f'I cannot find any restaurant that matches your whishes. Is there anything else you would like to eat?'
            self.count_options = 0
            self.refresh_preferences()
            self.dialog_state.update_state(
                self.dialog_act.dialog_act, self.missing_preferences)
        else:
            self.restaurant_suggestion = restaurant_options.iloc[self.count_options]

            if FRIENDLY:

                # check for additional preferences
                if "additional_preferences" in self.preferences:
                    response = f'I think {self.restaurant_suggestion["restaurantname"]} would be the perfect restaurant for you.' +\
                        f'It is a {self.preferences["pricerange"][0]} {self.preferences["food"][0]} restaurant' +\
                        f'It is a %s  because {self.give_reasons()}. Do you feel like going there?' % f"restaurant where you can stay +\
                        {self.preferences.additional_preferences[0]}"  if self.preferences["additional_preferences"][0] == "long" or self.preferences["additional_preferences"][0]  == "short" else f"{self.preferences['additional_preferences'][0]} restaurant"
                else:
                    response = f'I think {self.restaurant_suggestion["restaurantname"]} would be the perfect restaurant for you.' +\
                    f'It is a {self.preferences["pricerange"][0]} {self.preferences["food"][0]} restaurant' +\
                    f'in the {self.restaurant_suggestion["area"]} of town,  Do you feel like to going there?'
            else:

                # check for additional preferences
                if "additional_preferences" in self.preferences:

                    descript = f"restaurant where you can stay {self.preferences['additional_preferences'][0]}"  if self.preferences["additional_preferences"][0] == "long" or self.preferences["additional_preferences"][0]  == "short" else f"{self.preferences['additional_preferences'][0]} restaurant"

                    print ("descript", descript)
                    response = f'I recommend {self.restaurant_suggestion["restaurantname"]}. ' +\
                        f'It is a {self.preferences["pricerange"][0] if self.preferences["food"][0] != "any" else ""} {self.preferences["food"][0] if self.preferences["food"][0] != "any" else ""} restaurant in the {self.restaurant_suggestion["area"]} of town.\n' +\
                        f'It is a {descript}  because {self.give_reasons()}. Do you want to go there?'        
                else:
                    response = f'I recommend {self.restaurant_suggestion["restaurantname"]}. It is a {self.preferences["pricerange"][0] if self.preferences["food"][0] != "any" else ""} +\
                    {self.preferences["food"][0] if self.preferences["food"][0] != "any" else ""} restaurant in the {self.restaurant_suggestion["area"]} of town. Do you want to go there?'
        return response

    def give_reasons(self):
        n = 0
        reasons = []
        for key, value in self.antecedents:
            n += 1
            if key == "length_of_stay":
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
            print("extracted meaning",extract_meaning.extract_preferences(
                self.customer_input, self.item, TEXT2SPEECH))
            self.preferences["additional_preferences"] = extract_meaning.extract_preferences(
                self.customer_input, self.item, TEXT2SPEECH)["additional_preferences"]

            # based on additional_preferences get antecedents
            antecedents = self.get_antecedents()

            # filter restaurant info based on additional preferences
            self.antecedents = self.restaurant_info.filter_on_additional_info(
                antecedents, restaurant_options)

            self.dialog_state.update_state(
                self.dialog_act.dialog_act, self.missing_preferences)
            response = self.create_response()

        else:
            if FRIENDLY:
                response = f'Alright, is there any other preference you have for a restaurant? '+ \
                 ' For instance, do you like some place romantic, busy, suitable for children,' + \
                     'or do you prefer a place where you can stay a bit longer?'
            else:
                response = f'OK, do you have any other requirements for your restaurant?' + \
                    ' You can choose from romantic, busy, suitable for children, and places where you can stay long'

        return response

    def get_antecedents(self):
        # TODO based on the additional preferences use the dictionary to map the preferences such as 'romantic' to a list of ordered antecedents
        options = {"romantic":  [("crowdedness", "calm"), ("length_of_stay", "long"), ("food_quality", "good")],
                   "busy": [("food_quality", "good"), ("pricerange", "cheap"), ("length_of_stay", "long")],
                   "children": [("length_of_stay", "short")],
                   "long": [("food_quality", "good"), ("pricerange", "expensive"), ("crowdedness", "calm")],}

        preference = self.preferences["additional_preferences"][0]
        antecedents = options[preference]

        return antecedents

    def extract_asked_information(self, costumer_input):
        information_dict = {'address': ['address', 'adress', 'adres', 'street', 'location'],
                            'phone_number': ['phone', 'number', 'telephone'],
                            'postcode': ['postcode', 'zipcode', 'post', 'zip', 'postalcode', 'code', 'postal'],
                            'both': ['both', 'all']
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
            if FRIENDLY:
                response = f'Great! '
            else:
                response = f'OK. '
        else:
            response = ""
        if "address" in information_req:
            if str(self.restaurant_suggestion['addr']) == "nan":
                if FRIENDLY:
                    response += f'Sorry, we do not have a address registered for %s. ' % self.restaurant_suggestion['restaurantname']
                else:
                    response += f'The address of %s is unknown. ' % self.restaurant_suggestion['restaurantname']
            else:
                response += f'The address is %s. ' % self.restaurant_suggestion['addr']
        if "phone_number" in information_req:
            if str(self.restaurant_suggestion['phone']) == "nan":
                if FRIENDLY:
                    response += f'Sorry, we do not have a phone number registered for %s. ' % self.restaurant_suggestion['restaurantname']
                else:
                    response += f'The phone number for %s is unknown. ' % self.restaurant_suggestion['restaurantname']
            else:
                response += f'The phone number is %s. ' % self.restaurant_suggestion['phone']
        if "postcode" in information_req:
            if str(self.restaurant_suggestion['postcode']) == "nan":
                if FRIENDLY:
                    response += f'Sorry, we do not have a postal code registered for %s. ' % self.restaurant_suggestion['restaurantname']
                else:
                    response += f'The postal code for %s is unknown. ' % self.restaurant_suggestion['restaurantname']
            else:
                response += f'The postal code is %s. ' % self.restaurant_suggestion['postcode']
        if information_req == [] or self.provided_info == []:
            if FRIENDLY:
                response += f'Would you like to know their phone number or the postcode? Or maybe both? '
            else:
                response += f'Do you want to know their phone number, the postcode, or both? '
        for information in information_req:
            self.provided_info.append(information)
        return response

    def goodbye(self):
        if FRIENDLY:
            response = f'Enjoy your dinner '
        else:
            response = f'Bye'
        return response


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
        self.dialog_act = model.predict(self.create_bow(customer_input))[0]

    # load all models we have available
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

    # selects classifier model
    def select_model(self, model_name):
        self.model = self.models[model_name]

    # transforms the user's text input (str) to our Bag-of-Word vectors
    def create_bow(self, customer_input):
        bow = self.tfidf_transformer.transform(
            self.count_vect.transform([customer_input]))
        return bow


class Dialog_state:

    def __init__(self):
        self.state = "hello"
        self.prev_state = "hello"
        self.add_pref = False

    def update_info(self, request):
        self.info[request[0]] = request[1]

    def update_state(self, act, missing_preferences=[]):
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
            if act == "deny" or act == "negate" or self.prev_state == "get_add_preferences":
                self.state = "suggest_restaurant"
            else:
                self.state = "get_add_preferences"
                self.add_pref = True
            self.prev_state = "get_add_preferences"

        elif self.state == "suggest_restaurant":
            if len(missing_preferences) > 0:
                self.state = "express_preferences"
                self.prev_state = "suggest_restaurant"
            if act == "affirm":
                self.state = "request_restaurant_information"
                self.prev_state = "suggest_restaurant"
            elif act == "deny" or act == "negate" or act == "reqalts" or act == "reqmore":
                self.state = "suggest_restaurant"
                self.prev_state = "suggest_restaurant"
            else:
                self.prev_state = "express_preferences"
                f'Sorry I didn\'t understand that, please answer with yes or no.'

        elif self.state == "request_restaurant_information":
            # if act == "reqmore":
            #    self.state = "request_add_info"
            if act == "thankyou" or act == "bye" or act == "deny" or act == "negate":
                self.state = "goodbye"

    # def extract_preferences(self, customer_input):
    #    return


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
        print(self.restaurant_options)
        return filtered_restaurant_info

    def filter_on_additional_info(self, antecedents, restaurant_options):
        # within the restaurant options perform a second filter based on the filter preferences
        all_restaurant_options = restaurant_options
        found = False
        length_of_stay = ["any"]
        crowdedness = ["any"]
        food_quality = ["any"]
        # make shure that list object does not convert to tuple
        if not type(antecedents) == list:
            antecedents = [antecedents]
        if len(antecedents) < 1:

            filtered_restaurant_info = []
        else:
            # filter the antecedents from
            for key, antecedent in antecedents:
                antecedent = [antecedent]
                if key == "length_of_stay":
                    length_of_stay = antecedent
                elif key == "crowdedness":
                    crowdedness = antecedent
                else:
                    food_quality = antecedent

            if (length_of_stay != ["any"]) & (crowdedness != ["any"]) & (food_quality != ["any"]):
                filtered_restaurant_info = restaurant_options[(restaurant_options.length_of_stay.isin(length_of_stay)) & (
                    restaurant_options.crowdedness.isin(crowdedness)) & (restaurant_options.food_quality.isin(food_quality))]
            elif (length_of_stay != ["any"]) & (crowdedness != ["any"]) & (food_quality == ["any"]):
                filtered_restaurant_info = restaurant_options[(restaurant_options.length_of_stay.isin(
                    length_of_stay)) & (restaurant_options.crowdedness.isin(crowdedness))]

            elif (length_of_stay != ["any"]) & (food_quality != ["any"]) & (crowdedness == ["any"]):
                filtered_restaurant_info = restaurant_options[(restaurant_options.length_of_stay.isin(
                    length_of_stay)) & (restaurant_options.food_quality.isin(food_quality))]

            elif (crowdedness != ["any"]) & (food_quality != ["any"]) & (length_of_stay == ["any"]):
                filtered_restaurant_info = restaurant_options[(restaurant_options.crowdedness.isin(
                    crowdedness)) & (restaurant_options.food_quality.isin(food_quality))]

            elif (length_of_stay != ["any"]) & (crowdedness == ["any"]) & (food_quality == ["any"]):
                filtered_restaurant_info = restaurant_options[restaurant_options.length_of_stay.isin(
                    length_of_stay)]

            elif (food_quality != ["any"]) & (crowdedness == ["any"]) & (length_of_stay == ["any"]):
                filtered_restaurant_info = restaurant_options[restaurant_options.food_quality.isin(
                    food_quality)]

            elif (crowdedness != ["any"]) & (length_of_stay == ["any"]) & (food_quality == ["any"]):
                filtered_restaurant_info = restaurant_options[restaurant_options.crowdedness.isin(
                    crowdedness)]

            if len(filtered_restaurant_info) < 1:

                antecedents.pop()
                print("antecedents", antecedents)
                self.filter_on_additional_info(
                    antecedents, all_restaurant_options)
            else:
                self.filtered_restaurant_options = filtered_restaurant_info

        return antecedents

    def restaurant_count(self, filter_preferences):
        return len(self.filter_info(filter_preferences))


if __name__ == "__main__":
    main()
