How to run:

Open the code folder and open the main.py file. Run that file and the conversation will start in the console. 

Folder code:

- main.py : The file containing the main code for the dialogue system with the state transition function.

- extract_meaning.py : This file is used to get the meaning out of a user utterance, even if it contains spelling errors. 

- data_class.py : This file preprocesses our data so that it can be used to train the models.

- models.py : The file that contains the 2 baseline models and the 2 machine learning models to train and test the data.

- model_metrics.py : The file that is used to evaluate the 4 models.

- difficult_utterances.py : This file was used to search for difficult cases for our classifiers.

Folder data:
This folder contains all the data to train the models and the restaurants out of which the system could pick based on the user preferences.

Folder plots:
This folder contains different figures of the confusion matrices for the machine learning models.

Folder trained_models:
This folder contains all the trained models saved as a .pickle file.