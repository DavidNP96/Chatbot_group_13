### the main file to run the dialog system

# import models



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

if __name__=="__main__":
    main()