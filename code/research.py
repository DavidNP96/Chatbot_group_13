import main
import time
import random
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def research():
    # load tasks
    tasks = open("tasks.txt")
    possible_tasks = []
    # column_names = ["participant number", "dialog number","friendliness","task", "time in seconds", "number of turns"]
    df = pd.read_csv("../data/participants.csv")
    for line in tasks:
        possible_tasks.append(line)

    dialogs = []

    rounds = 5
    friendliness = ["TERSE", "FRIENDLY"]
    paricipant_number = input('Enter your participant number:')

    print("Welcome! Thanks a lot for participating in our experiment, carried out for the course 'Methods in AI Research' at Utrecht University.\n"\
            "In this experiment you will engage in 10 dialogs with a restaurant recommendation system. \nFor each dialog you will be assigned a "\
            "specific task which specifies the type of restaurant that you are supposed to find. \n" \
            "The experiment consists of two rounds of 5 dialogs, and after each round we ask you to fill out a survey. \n" \
            "We will save the text of all the dialogs, but this will only be used for analysis purposes. \n" \
            "No data will be shared outside or our research team, which consists of Nick Beukenkamp, Goya van Boven, David Pantophlet and Simon van de Fliert. \n"\
            "You are free to stop your participation at any moment during the experiment, in this case we will delete all the data from your interactions with the system. \n" \
            "Thank you again for participanting and good luck with the conversations." )
    input("Please press enter to start.")
    start = time.time()
    # reverse order of freindliness if participant number is even
    if int(paricipant_number) % 2 == 0:
        friendliness.reverse()

    #  lof = level off friendliness
    for setting_n, lof in enumerate(friendliness):
        for round in range(rounds):
            data = {"participant number": paricipant_number}
            start = time.time()
            # find random taks and remove it from possible tasks
            task = random.choice(possible_tasks)
            possible_tasks.remove(task)

            print(f"\nRound {setting_n + 1} out of 2; task {round+1} out of 5.")#: {rounds-(round+1)} more tasks to complete in this round.")
            # perform dialog
            print("\nYour tasks:\n", f"{task}\n")
            dialog, number_of_turns = main.main(lof)
            end = time.time()
            total_time = end-start

            # inform user of progress
            time.sleep(0)

            # add data to dataframe
            data["dialog number"] = [round + 1]
            data["friendliness"] = [lof]
            data["task"] =[task]
            data["time in seconds"] = [total_time]
            data["number of turns"] = [number_of_turns]
            
            # save dialogs
            dialogs.append("---")
            dialogs.append(f"\n participant : {paricipant_number} dialog: {round} in setting: {lof}")
            dialogs.append(dialog)
            df2 = pd.DataFrame.from_dict(data)
            df = df.append(df2, ignore_index=True)

        # check which setting is used and direct to right survey
        if setting_n == 0:
            print(f"\nThank you for completing this round! please fill in this short survery by holding 'CTRL' and click on the following link https://docs.google.com/forms/d/e/1FAIpQLSfQ_OxCTdcEIBdD7GHXGTx8El1rulup5H9eWtolbJpuF0jUbg/viewform \n your participant number is: {paricipant_number}")
            print("Please come back here after filling in the survery")
            input("Press enter to continue.")
        elif setting_n == 1:
            print(f"\nThank you for completing this round! please fill in this short survery by holding 'CTRL' and click on the following link https://docs.google.com/forms/d/e/1FAIpQLSctlXF1v_ZF1g6yJigmx4aJM0Q1vfc3mOP1BSERisyS2Wu6aQ/viewform \n your participant number is: {paricipant_number}")
            print("After filling in the survey you are done! Thank you very much for helping us!")
    # save data and dialogs
    df.to_csv("../data/participants.csv", mode="a", header=False)
    file = open("../data/dialogs.txt", "a")
    for dia in dialogs:
        file.writelines(dia)
            
if __name__ == "__main__":
    research()