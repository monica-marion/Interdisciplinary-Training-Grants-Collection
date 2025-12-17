
## script to create a list of discipline terms extracted manually from grants
# run this after manually filling the 'disciplines_clean_manual' column with discipline terms taken directly from the 'from_sentences' and 'trimmed_sentences' column
# takes grants_1.csv as input (grant awards with extracted discipline sentences)
# creates discipline_terms_manual.csv as output
import pandas as pd


##import the data
nsf_df = pd.read_csv("../output/grants_1.csv")

## make list of discipline terms (combined with llm terms list to create final discipline list)

#make empty list to fill
terms_list=[]

#iterate through all the awards
for row in range(len(nsf_df)):
    #get disciplines
    disc = str(nsf_df.loc[row, 'disciplines_manual']).lower()
    for j in disc.split(','):
        terms_list.append(str(j)) 

#remove duplicates
terms_list = list(set(terms_list))

#set all as strings
for i in terms_list:
    str(i)

#create sorted list of discipline terms
terms_list = sorted(terms_list, key=len, reverse=True)

##save terms_list
terms_df = pd.DataFrame(terms_list)
terms_df.to_csv('../output/discipline_terms_manual_test.csv', index=False)

