###script to scrape outcome reports from nsf reporter
##takes Awards.csv (download from nsf) as input
##creates grants_0.csv (grants with outcome reports) as output

import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 1. Setup the WebDriver (ensure chromedriver is in your PATH or provide its location)
# service = Service(executable_path='/path/to/chromedriver') # Optional if not in PATH
driver = webdriver.Chrome()

##import the list of IDs
#this csv was downloaded from nsf reporter:
# 26 duplicate grants removed
nsf_df = pd.read_csv ('../input/Awards.csv',encoding='latin-1')

## set up new datafame with columns for all the info we want
df2 = pd.DataFrame(columns=['id','url','outcomes'])
df3 = pd.DataFrame(columns=['id','url','outcomes'])

#convert the awards column to remove "= and "
nsf_df['AwardNumber'] = nsf_df['AwardNumber'].str.replace('\"', '')
nsf_df['AwardNumber'] = nsf_df['AwardNumber'].str.replace('=', '')

#make a list of all the award ids to convert into urls
url_list = nsf_df['AwardNumber'].tolist()

#iterate through all the urls
outcomes = []
for k in range(len(url_list)):
# for k in range(3):

    url_end = str(url_list[k])
    url = 'https://www.nsf.gov/awardsearch/showAward?AWD_ID='+url_end

    try:
        # 2. Navigate to the webpage
        driver.get(url) # Example site

        # 3. Wait for content to load dynamically if necessary
        div_id = "porContent"

        #10 second wait to not trigger the nsf 'too many requests' page
        div_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, div_id))
        )
        # 1. Locate the div element by its ID
        # div_element = driver.find_element(By.ID, div_id)
        # 2. Get the visible text from the element using the .text attribute
        div_text = div_element.text
        # 3. Print the retrieved text
        outcomes.append(div_text)

    except (TimeoutException, NoSuchElementException):
        outcomes.append("")
        
    except Exception as e:
        print(f"An error occurred: {e}")

        # Close the driver

driver.quit()

#add the outcome reports to the dataframe
nsf_df['Outcome Report'] = outcomes

#save the final df to csv
nsf_df.to_csv('../output/grants_0.csv', encoding = 'utf-8', index=False)