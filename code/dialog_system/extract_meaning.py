from Levenshtein import distance
import re
import pyttsx3

#this list stores keywords related to each category. Some keywords are stored as different variations (value) of the same keyword (key)
pref_keywords = {
    'food' : ['bistro', 'mediterranean', 'seafood', 'fusion', '"asian', 'scottish', 'chinese', 'mexican', 'european', 'crossover', 
            'vietnamese', 'greek', 'english', 'british', 'thai', 'corsica', 'gastropub', 'christmas', 'indian', 'turkish', 'polynesian', 
            'gastropub', 'japanese', 'kosher', 'venetian', 'dontcare', 'tuscan', 'korean', 'spanish', 'portuguese', 'danish', 'world', 
            'vegetarian', 'creative', 'international', 'cantonese', 'italian', '"modern', 'french', 'basque', 'traditional', 'brazilian', 
            'canapes', 'moroccan', 'romanian', 'hungarian', 'austrian', 'indonesian', 'halal', 'african', 'australian', 'german', 
            'cuban', 'steakhouse', 'catalan', 'caribbean', 'scandinavian', 'russian', 'singaporean', 'belgian', 'welsh', 'afghan', 
            'malaysian', 'persian', 'barbeque', 'irish', 'swiss', 'lebanese', 'jamaican', 'eritrean', 'unusual', 'swedish', 'polish', 
            'australasian', 'singaporean'],
    'area' : ['west', 'north', 'south', {'centre': ['centre', 'center']}, 'east'],
    'pricerange' : [{'moderate': ['moderate', 'moderately']}, {'expensive': ['expensive', 'expensively']}, 
                    {'cheap': ['cheap', 'cheaply']}]
    # 'additional_preferences': [TODO]
}

#this dictionary stores common textual patterns for different attributes in the following way:
#('TEXT PATTERN', 'KEYWORD_POSITION') where TEXT PATTERN is the textual pattern (str) to be recognized and
# KEYWORD_POSITION indicated the relative position of the keyword where 
# 'l' indicates the keyword is positioned left of the pattern and 'r' indicated the keyword can be found at the right of the pattern
# 'c' indicates that the keyword is the whole utterance (1 word)
pref_patterns = { 
    'food' : [(r'[^\s]*[\s]food', 'food'), (r'[^\s]*[\s]restaurant','restaurant'), (r'[^\s]*[\s]food restautant', 'food restaurant')], #('restaurant', 'l'), ('food', 'l'), ('food restaurant', 'l'), ('', 'c')],
    'area' : [(r'[^\s]*[\s]part of town', 'part of town'), (r'[^\s]*[\s]area', 'area'), (r'in the[^\s]*[\s]', 'in the')],# ('', 'c')],
    'pricerange': [(r'[^\s]*[\s]priced', 'priced'), (r'[^\s]*[\s]restaurant', 'restaurant'), (r'[^\s]*[\s]price', 'restaurant')]#, ('', 'c')]
    # 'additional_preferences' : [ TODO]  
}

#list of words that map to 'dontcare'
dontcare_keywords = ['any', "don't", "care", 'dont', "doesn't", 'matter', 'doesnt', 'anything', 'dont care', "don't care", "doesn't matter",
                     'doesnt matter']

#a list of sentences to test our algorithm on
test_sents = ['I\'m looking for world food', 'I want a restaurant that serves world food', 'I want a restaurant serving Swedish food',
            'I\'m looking for a restaurant in the center', 'I would like a cheap restaurant in the west part of town', 
            'I\'m looking for a moderately priced restaurant in the west part of town', 
            'I\'m looking for a restaurant in any area that serves Tuscan food',
            'Can I have an expensive restaurant', 'I\'m looking for an expensive restaurant and it should serve international food',
            'I need a Cuban restaurant that is moderately priced', 'I\'m looking for a moderately priced restaurant with Catalan food',
            'What is a cheap restaurant in the south part of town', 'What about Chinese food', 'I wanna find a cheap restaurant', 
            'I\'m looking for Persian food please', 'Find a Cuban restaurant in the center', 'I want to go to a restaurant in the weest']
test_sents = [sent.lower() for sent in test_sents]

engine = pyttsx3.init()

#to extract preferences from an utterance, we first try to recognize keywords, and next we recognize patterns
def extract_preferences(utterance, item, text2speech):
    global TEXT2SPEECH
    TEXT2SPEECH = text2speech
    preferences_dict = {}
    preferences_dict = match_keywords(utterance, preferences_dict, item)
    preferences_dict = match_patterns(utterance, preferences_dict)
    print(preferences_dict)
    return preferences_dict

#go through the words in the given utterance, and compare if these words are relevant preference keywords
# if so, add the the preference to the preferences dictionary
def match_keywords(utterance, preferences_dict, item):
    # map utterance to dontcare 
    for word in dontcare_keywords:
        if word == utterance:
            preferences_dict[item] = ["any"]
            return(preferences_dict)
    sent = utterance.split()

    for attribute, preference in pref_keywords.items():
        attribute_matches = []
        #if a keyword has multiple spelling variations, check if any of the variations is present in the text
        #if so add the keyword to the preferences dictionary
        for pref in preference:
            if type(pref) == dict:
                for preference_variation in list(pref.values())[0]:
                    if preference_variation in sent:
                        attribute_matches.append(list(pref.keys())[0])
                        #preferences_dict[attribute] = list(pref.keys())[0]
            #check if keyword is expressed in the sentence, if so add preference to preferences dictionary
            else:
                if pref in sent:
                    attribute_matches.append(pref)
                    #preferences_dict[attribute] = pref
        if len(attribute_matches) > 0:
            preferences_dict[attribute] = attribute_matches
    return(preferences_dict)

#recognizes patterns in the text that belong to certain attributes, and compares whether the found potential keywords 
#are similar to any known keywords
def match_patterns(utterance, preferences_dict):
    for attribute, patterns in pref_patterns.items():
        #check the patterns for all attributes that are not yet known
        if attribute in preferences_dict:
            continue
        for pattern, keyword in patterns:
            matches = re.findall(pattern, utterance)
            for match in matches:
                potential_keyword = match.replace(keyword, '').replace(' ', '')
                match_keyword(potential_keyword, preferences_dict, attribute)
        if attribute not in preferences_dict and len(utterance.split()) == 1 and utterance != "any":
            match_keyword(utterance, preferences_dict, attribute)
    return preferences_dict

def match_keyword(potential_keyword, preferences_dict, attribute):
    #check if potential keyword expresses there is no preference
    if potential_keyword in dontcare_keywords and attribute not in preferences_dict:
        preferences_dict[attribute] = ['any']
    #compare whether potential keyword is similar to any known keywords belonging to given attribute
    else:
        closest_word = find_similar_word(potential_keyword, attribute)
        if closest_word != None:
            correction_message = f'I did not recognize {potential_keyword}. Did you mean {closest_word}?' + \
                                        'Please reply yes (y) or no (n).'
            if TEXT2SPEECH:
                engine.say(correction_message)
                engine.runAndWait()
            check_correction = input(correction_message)
            
            while check_correction not in ['yes', 'y', 'no', 'n']:
                correction_message_2 = f'Sorry I did not understand. Please reply with yes or no. '
                if TEXT2SPEECH:
                    engine.say(correction_message_2)
                    engine.runAndWait()
                check_correction = input()
            if check_correction == 'yes' or check_correction == 'y':
                preferences_dict[attribute] = [closest_word]

#this function returns the most similar keyword for the relevant attribute for a given potential keyword if there is one
def find_similar_word(potential_keyword, attribute):
    distance_dict = {}
    if len(potential_keyword) > 8:
        threshold = 4
    elif len(potential_keyword) > 5:
        threshold = 3
    else:
        threshold = 2
    #go through keywords belonging to relevant attribute
    for word in pref_keywords[attribute]:
        #if keyword has multiple spelling variations, go through all of them
        if type(word) == dict:
            keyword = list(word.keys())[0]
            for word_variantion in list(word.values())[0]:
                #calculate distance for each variation
                levenshtein_dist = distance(potential_keyword, word_variantion)
                if levenshtein_dist < threshold:
                    #if another spelling variation of the same keyword was already saved, check if this variation has a lower score
                    if keyword in distance_dict:
                        if levenshtein_dist < distance_dict[keyword]:
                            distance_dict[keyword] = levenshtein_dist
                    #otherwise, save the score of this variation
                    else:
                        distance_dict[keyword] = levenshtein_dist
        else:
            #compare distance between keyword and potential keyword
            levenshtein_dist = distance(potential_keyword, word)
            #if distance is smaller than 3, save the score
            if levenshtein_dist < threshold:
                distance_dict[word] = levenshtein_dist
    #if multiple similar words are found, return the one with the lowest distance score
    if len(distance_dict.keys()) > 0:
        return min(distance_dict, key=distance_dict.get)
    #if no similar words are found, return None
    else:
        return None
if __name__ == "__main__":
    #test performance for test sentences
    for sent in test_sents:
        print(sent)
        print(extract_preferences(sent))
