import main
import time
import random
import pandas as pd


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
    start = time.time()

    #  lof = level off friendliness
    for lof in friendliness:
        
        for round in range(rounds):
            data = {"participant number": paricipant_number}
            start = time.time()
            # find random taks and remove it from possible tasks
            task = random.choice(possible_tasks)
            possible_tasks.remove(task)

            # perform dialog
            print("\n your tasks:\n", f"{task}\n")
            dialog, number_of_turns = main.main(lof)
            end = time.time()
            total_time = end-start

            # inform user of progress
            time.sleep(0)
            print(f"{rounds-(round+1)} more tasks to complete")
        

            # add data to dataframe
            data["dialog number"] = [round + 1]
            data["friendliness"] = [lof]
            data["task"] =[task]
            data["time in seconds"] = [total_time]
            data["number of turns"] = [number_of_turns]
            
            # save dialogs
            dialogs.append(f"\n dialog: {round} in setting: {lof}")
            dialogs.append(dialog)
            df2 = pd.DataFrame.from_dict(data)
            df = df.append(df2, ignore_index=True)

        # check which setting is used and direct to right survey
        if lof == "TERSE":
            print(f"\nThank you for completing this round! please fill in this short survery by holding 'CTRL' and click on the following link https://docs.google.com/forms/d/e/1FAIpQLSfQ_OxCTdcEIBdD7GHXGTx8El1rulup5H9eWtolbJpuF0jUbg/viewform \n your participant number is: {paricipant_number}")
            print("please come back here after filling in the survery")
            time.sleep(0)
        else:
            print(f"\nThank you for completing this round! please fill in this short survery https://docs.google.com/forms/d/e/1FAIpQLSctlXF1v_ZF1g6yJigmx4aJM0Q1vfc3mOP1BSERisyS2Wu6aQ/viewform \n your participant number is: {paricipant_number}")
            print("after filling in the survey you are done! Thank you very much for helping us!")
    # save data and dialogs
    df.to_csv("../data/participants.csv")
    file = open("../data/dialogs.txt", "a")
    for dia in dialogs:
        file.writelines(dia)
            
if __name__ == "__main__":
    research()