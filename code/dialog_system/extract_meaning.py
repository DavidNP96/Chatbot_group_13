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
                    {'cheap': ['cheap', 'cheaply']}]}
additional_pref_keywords = {
    'additional_preferences': ['romantic', "busy", "children", "long", {"short":["fast"]}]}

#this dictionary stores common textual patterns for different attributes in the following way:
#('TEXT PATTERN', 'KEYWORD_POSITION') where TEXT PATTERN is the textual pattern (str) to be recognized and
# KEYWORD_POSITION indicated the relative position of the keyword where 
# 'l' indicates the keyword is positioned left of the pattern and 'r' indicated the keyword can be found at the right of the pattern
# 'c' indicates that the keyword is the whole utterance (1 word)
pref_patterns = { 
    'food' : [(r'[^\s]*[\s]food', 'food'), (r'[^\s]*[\s]restaurant','restaurant'), (r'[^\s]*[\s]food restautant', 'food restaurant')],
    'area' : [(r'[^\s]*[\s]part of town', 'part of town'), (r'[^\s]*[\s]area', 'area'), (r'in the[^\s]*[\s]', 'in the')],
    'pricerange': [(r'[^\s]*[\s]priced', 'priced'), (r'[^\s]*[\s]restaurant', 'restaurant'), (r'[^\s]*[\s]price', 'restaurant')]}
additional_pref_patterns = {
    'additional_preferences' : [(r'[^\s]*[\s]restaurant', 'restaurant'), (r'without[^\s]*[\s]', 'without'), (r'with[^\s]*[\s]', 'with') ]  
}

#list of words that map to 'dontcare'
dontcare_keywords = ["any", "anything", "don't", "care", 'dont', "doesn't", 'matter', 'doesnt', 'dont care', "don't care", "doesn't matter",
                     'doesnt matter']

engine = pyttsx3.init()

#to extract preferences from an utterance, we first try to recognize keywords, and next we recognize patterns
def extract_preferences(utterance, item, text2speech, additional_prefs = False):
    global TEXT2SPEECH
    TEXT2SPEECH = text2speech
    preferences_dict = {}
    preferences_dict = match_keywords(utterance, preferences_dict, item, additional_prefs)
    preferences_dict = match_patterns(utterance, preferences_dict, additional_prefs)
    return preferences_dict

#go through the words in the given utterance, and compare if these words are relevant preference keywords
# if so, add the the preference to the preferences dictionary
def match_keywords(utterance, preferences_dict, item, additional_prefs=False):
    # map utterance to dontcare 
    print(item)
    if item != "" :
        for word in dontcare_keywords:
            if word in utterance:
                print(word, "in ", utterance)
                preferences_dict[item] = ["any"]
                return(preferences_dict)
    sent = utterance.split()

    #compare against appropriate set of keywords
    if additional_prefs:
        keywords = additional_pref_keywords
    else:
        keywords = pref_keywords
    for attribute, preference in keywords.items():
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
def match_patterns(utterance, preferences_dict, additional_prefs=False):
    #take appropriate set of patterns
    if additional_prefs:
        patterns = additional_pref_patterns
    else:
        patterns = pref_patterns
    for attribute, patterns in patterns.items():
        #check the patterns for all attributes that are not yet known
        if attribute in preferences_dict:
            continue
        for pattern, keyword in patterns:
            matches = re.findall(pattern, utterance)
            for match in matches:
                potential_keyword = match.replace(keyword, '').replace(' ', '')
                match_keyword(potential_keyword, preferences_dict, attribute)
        if attribute not in preferences_dict and len(utterance.split()) == 1 and utterance != "any":
            match_keyword(utterance, preferences_dict, attribute, additional_prefs)
    return preferences_dict

def match_keyword(potential_keyword, preferences_dict, attribute, additional_prefs=False):
    #check if potential keyword expresses there is no preference
    if potential_keyword in dontcare_keywords and attribute not in preferences_dict:
        preferences_dict[attribute] = ['any']
    #compare whether potential keyword is similar to any known keywords belonging to given attribute
    else:
        closest_word = find_similar_word(potential_keyword, attribute, additional_prefs)
        if closest_word != None:
            correction_message = f'I did not recognize {potential_keyword}. Did you mean {closest_word}?' + \
                                        ' Please reply yes (y) or no (n).'
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
def find_similar_word(potential_keyword, attribute, additional_prefs =False):
    distance_dict = {}
    if len(potential_keyword) > 8:
        threshold = 4
    elif len(potential_keyword) > 5:
        threshold = 3
    else:
        threshold = 2
    #take appropriate set of keywords
    if additional_prefs:
        keywords = additional_pref_keywords
    else:
        keywords = pref_keywords
    #go through keywords belonging to relevant attribute
    for word in keywords[attribute]:
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
# if __name__ == "__main__":
#     #test performance for test sentences
#     for sent in test_sents:
#         print(sent)
#         print(extract_preferences(sent))
