###script to extract topic terms from titles
##Adapted from Milojevic (2015) and code written by Hongyu Zhou 
# takes as input grants.csv and genword_master.txt stopwords
# creates as output an updated grants.csv

import pandas as pd

#import data
nsf_df = pd.read_csv("../output/grants.csv")

def normalize_cog(title):     
    title = title.lower() # lowercase
    title = title.replace('&', ' and ')  # replace & with 'and'
    title = ''.join(e if e.isalnum() else ' ' for e in title) # remove punctuation
    title = ''.join(e if not e.isdigit() else '' for e in title)   # remove numbers
    title = ' '.join([word for word in title.split() if len(word) > 1]).strip() 
    return title

def plural3(word):
    # handle plural forms
    if len(word) > 3:
        if word.endswith("sses"):
            return word[:-2]
        elif word.endswith("ies") and word != "species":
            return word[:-3] + "y"
        elif word[-1] == "s" and not word.endswith(("ss", "sses", "sis", "ous")):
            return word[:-1]
    return word

exc = {}  # stop words that delimit the phrases
with open('../input/genword_master.txt', 'r') as file: 
    for line in file:
        word = line.strip().lower()
        exc[word] = 1    

def extract_cog(title):
    
    title = normalize_cog(title)
    words = title.split()
    phrase_words = []  #candidate words, not in genwords
    pwcount = 0
    output_phrase = set()
    
    for word in words:  #go thru words in title sequantially
        orig = word
        word = plural3(word)  #remove plurarity
        if word not in exc and orig not in exc: #check word in genwords
            pwcount += 1
            phrase_words.append(word)
        else:  #meet a general words
            if 0 < pwcount < 4: #ideal length for phrase
                phrase = '_'.join(phrase_words)
                output_phrase.add(phrase)
            if pwcount > 3:   # now handle phrases longer than 3
                phrase = '_'.join(phrase_words[-3:])  # keep only the last three words
                output_phrase.add(phrase)
            pwcount = 0  # clear the candidate pool and move on
            phrase_words = []  # same as above

    #handle the last phrase separately, since it's behind the genwords, so wont triger processing
    if 0 < pwcount < 4:
        phrase = '_'.join(phrase_words)
        output_phrase.add(phrase)
    if pwcount > 3:
        phrase = '_'.join(phrase_words[-3:])
        output_phrase.add(phrase)
    
    return output_phrase

docs= nsf_df['Title']

#make list to fill
topics_list = []

for i in docs:
    #print (extract_cog(i))
    topic = str(extract_cog(i))
    topic = topic.replace("{", "")
    topic = topic.replace("}", "")
    topic = topic.replace("'", "")
    topics_list.append(topic)

nsf_df['Title Topics'] = topics_list

#save these terms to master csv
nsf_df.to_csv('../output/grants.csv', index=False)