
### script to extract field/discipline terms to generate term list for broader extraction
#run through all the "from" statements from the abstracts and pull the ones that are relevant
#takes grants_0.csv (awards with outcome reports) as input
#creates grants_1.csv as output (grants with column for from statement and extracted discipline sentence fragments)

import pandas as pd
import re

#import grant data
nsf_df = pd.read_csv("../output/grants_0.csv")

###extract sentence phrases that describe the fields/disciplines involved in the grant
#(often in the form, e.g. 'trainees from biology and statistical science')
##create one new row with manually vetted "from" statements

#loop all the abstracts
for row in range(0, len(nsf_df)):
    #set abstract
    abstract = nsf_df.loc[row, 'Abstract']
    #empty the list
    field_list=[]
    #loop all the 'from' statements
    
    #check for 'from' in the text
    if not pd.isna(abstract):
        matches = re.findall('from .*?\.',abstract)
    if matches:
        #loop all 'from' matches'
        for statement in matches:
            #print that statement
            print(statement)
            #ask to keep-- input 'k' for keep 'l' for lose
            if input() == 'k':
                #add it to the list
                field_list.append(statement)
    #add the list to the df
    nsf_df.loc[row, 'from_sentences'] = str(field_list)

##create a second row with extracted sentence phrases based on keywords/typical constructions

#pull out sentences that contain one of the following:
# discipline, interdisciplinary’ ‘trainees in’ ‘’trainees across’ ‘from’
# students, combine/combines, department, program/programs, domain experts in, field, 
# students from, trainees from

#make regex expression
regex_rule = 'domain experts in .*?\.|department.*?\.|combine.*?\.|students.*?\.|field.*?\.|trainee.*?\.|disciplin.*?\.'
#regex_rule = 'from .*?\.'

#pull out relevant sentences from abstract into new column
for row in range(0,len(nsf_df)):
    #set abstract
    abstract = nsf_df.loc[row, 'Abstract']
    #empty the list
    discipline_list=[]
    #loop all the 'from' statements
    if isinstance(abstract, str): 
        for statement in re.findall(regex_rule,abstract):
            discipline_list.append(statement)
    #add the list to the df
    nsf_df.loc[row, 'trimmed_sentences'] = str(discipline_list)

##save simplified dataframe
nsf_df.to_csv ('../output/grants_1.csv', index=False)
