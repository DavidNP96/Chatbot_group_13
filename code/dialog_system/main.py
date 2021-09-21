### the main file to run the dialog system

# import models
import pandas as pd


def main():
    # initial interface for the dialog system
    match = False

    #ds = Dialog_system()

    #while match == False:
    #    customer_input = input("").lower()
    #    response, match = ds.updated_customer_input(customer_input)
    #    print(response)

    rs = RestaurantInfo()
    print(rs.data)
    print("\n\n\n\n ===================== \n\n\n")
    preference = ["centre","european","moderate"]
    filtered_data = rs.filter_info(preference)
    print(filtered_data)

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
                    # fill in rest of options and create fittin functions 
                 }
        
        options[self.dialog_state]


        # return response
        response = ""
        return response
    
    def extract_preferences():
        # extract preferences from levenstein distance
        preferences = ""
        return preferences

    def  calculate_levenstein_distance(self):
        return 

    def inform(self):
        preferences  = self.extract_preferences()
        self.preferances.append(preferences)
        
        #  if preferences are sufficient
            # make request
        # else:
            # ask for missing preferences

class Dialog_state:
    def __init__(self, customer_input):
        self.dialog_state = ""

    def update_state(self, customer_input):
        # use imported model to predict class
        model = "" # import model
        self.dialog_state = model.predict(customer_input)


class RestaurantInfo:

    def __init__(self):   
        self.data = self.load_data()

    #Load function
    ###Load in dataset and change it in a pandas setup
    def load_data(self):
        restaurants_info = pd.read_csv("C:\\Users\\Simon\\Documents\\Master_Code\\Chatbot_group_13\\data\\restaurant_info.csv")
        return restaurants_info

    ##Filter function(pd dataframe, array/list of preferences)
    def filter_info(self, filter_preferences: list):
        
        #unpack array and place array elements into variables
        area = filter_preferences[0]
        food_type = filter_preferences[1]
        price = filter_preferences[2]
       
        ##check if variables exist, and if so, filter the dataframe on it
        if (area != "") & (food_type != "") & (price != ""):
            filtered_restaurant_info = self.data[((self.data["area"]== area) & (self.data["food"]==food_type)) & (self.data["pricerange"]==price)]

        elif (area != "") & (food_type != ""):
            filtered_restaurant_info = self.data[((self.data["area"]== area) & (self.data["food"]==food_type))]

        elif (area != "") &  (price != ""):
            filtered_restaurant_info = self.data[((self.data["area"]== area) & (self.data["pricerange"]==price))]

        elif (food_type != "") & (price != ""):
            filtered_restaurant_info = self.data[(((self.data["food"]==food_type)) & (self.data["pricerange"]==price))]

        elif (area != ""):
            filtered_restaurant_info = self.data["area"]== area
        
        elif (price != ""):
            filtered_restaurant_info = self.data["pricerange"]== price
        
        elif (food_type != ""):
            filtered_restaurant_info = self.data["food"]== food_type

        return filtered_restaurant_info


if __name__=="__main__":
    main()
