##script to take the "consensus categories" coded for both the llm and manual fields, 
#and produce a final list of disciplines and categories
#takes as input discipline_terms_manual.csv and discipline_terms_llm.csv 
#AFTER they have been checked by two independent category assigners and a consensus category list has been reached
#produces the final list: discipline_terms.csv 

import pandas as pd
import re

#manual categories
manual_df = pd.read_csv("../output/discipline_terms_manual.csv")

#llm categories
llm_df = pd.read_csv("../output/discipline_terms_llm.csv")

## create master terms list using llm1 and manual

##make mega dataframe
new_manual = manual_df[['terms', 'consensus']]
new_llm = llm_df[['terms', 'consensus']]

#rename columns
new_manual = new_manual.rename(columns={'consensus': 'categories'})
new_llm = new_llm.rename(columns={'consensus': 'categories'})

#concatenate
mega_df = pd.concat([new_manual, new_llm], ignore_index=True)
mega_df = mega_df.drop_duplicates(subset=['terms'], keep='first')

#make combined list
term_list = mega_df['terms'].tolist()
term_list = list(set(term_list))
term_list.sort()

##add correction columns
terms_df = pd.DataFrame(term_list, columns=['terms'])
terms_df = pd.merge(terms_df, mega_df, on='terms', how='left')

##remove rows with NaN
terms_df = terms_df.dropna()

#save grants csv
terms_df.to_csv("../output/discipline_terms1.csv", index=False)

