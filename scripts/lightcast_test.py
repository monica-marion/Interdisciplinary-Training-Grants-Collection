
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

nsf_df = pd.read_csv("../output/grants_0.csv")
bg_df = pd.read_csv("../input/lightcast.csv")

terms_list = bg_df['data.name'].tolist()
print (len(terms_list))

#convert terms to string
for i in range(len(terms_list)):
    terms_list[i] = str(terms_list[i]).lower()

print ('making matcher')

#make spacy matcher out of terms list
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(name) for name in terms_list]
print (patterns)

matcher.add("Names", patterns)

for row in range(1):
    #empty the list
    programs_list=[]
    abstract = 'This integrative Graduate Education and Research Training (IGERT) award supports a multidisciplinary graduate training program of education and research in urban ecology at Arizona State University. The primary study site is Phoenix and central Arizona but both historic (through archeology) and comparative approaches are employed. Intellectual merit.  The purpose of the program is to provide doctoral students with enhanced cross disciplinary collaborative training in the natural and social sciences relevant to urban ecology, broadly construed. Training will involve team research through student-originated workshops, interdisciplinary "issues" seminars, dissertation research in urban ecology with an explicitly collaborative component, and an international experience.  Broader impacts of the project include close attention to the conduct of research and the engagement of science with law, policy, and the public sphere. Unlike most doctoral programs in the United States that are based on independence, this program will use and investigate the efficacy of interdependence (collaboration, cooperation) as a research mode. The premise is that scientific investigation in important arenas such as cities is increasingly multidisciplinary, yet students commonly receive little direct training or experience in collaborative research strategies and group dynamics necessary for effective communication among disciplines. IGERT is an NSF-wide program intended to meet the challenges of educating U.S. Ph.D. scientists and engineers with the interdisciplinary background, deep knowledge in a chosen discipline, and the technical, professional, and personal skills needed for the career demands of the future. The program is intended to catalyze a cultural change in graduate education by establishing innovative new models for graduate education and training in a fertile environment for collaborative research that transcends traditional disciplinary boundaries.'
    abstract = abstract.lower()
    print (abstract)
    #if abstract:
    if not pd.isna(abstract):
        print('ok')
        doc = nlp(abstract)
        for match_id, start, end in matcher(doc):
            #append to list
            print ('match_id')
            programs_list.append(str(doc[start:end]))
            
        #remove repeats
        print (programs_list)
        programs_list=list(set(programs_list))
    else:
        programs_list=[]
    #add list to df
    nsf_df.loc[row, 'Lightcast Skills'] = str(programs_list)
