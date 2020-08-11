# -*- coding: utf-8 -*-
# Biomedical Employment Navigation Tool for Opportunities (BENTO)
"""
Created on Sat Jun  6 01:05:52 2020

@author: Hamzah Ahmed
"""

# Required packages that may need to be installed:
# Pandas
# TQDM
# Selenium (and corresponding ChromeDriver)
# Tkinter
#%% Setting Up Dependencies
# gets current directory info
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
current_dir = os.getcwd()

# imports subprocess to force Python package installation using pip
import sys
import subprocess

# Initializes a list containing all packages installed, that can then be used
# to check if user has necessary packages and install if necessary
reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'list'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

# Pandas package used for managing information organization
if ("pandas" in installed_packages) == False:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pandas'], check = True)
import pandas as pd

# Xlsx because VSCode doesn't seem to install it with pandas, for some reason
if ("xlsxwriter" in installed_packages) == False:
   subprocess.run([sys.executable, '-m', 'pip', 'install', 'xlsxwriter'], check = True) 
# TQDM used to generate progress bars as scraping is occurring
if ("tqdm" in installed_packages) == False:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'tqdm'], check = True)
import tqdm

# Selenium used to automate browsing and scrape from LinkedIn
if ("selenium" in installed_packages) == False:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'Selenium'], check = True)

# Chromedriver is necessary for Selenium
if ("chromedriver_autoinstaller" in installed_packages) == False:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'chromedriver-autoinstaller'],
                           check = True)
    import chromedriver_autoinstaller
    driver_path = chromedriver_autoinstaller.install()
else:
    import chromedriver_autoinstaller


del installed_packages, reqs, driver_path, abspath, dname
#%% Taking Inputs
company_index_path = current_dir + "/Companies.csv"
company_df = pd.read_csv(company_index_path)
#%% Imports for Selenium  
# import web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
#%% Choosing Whether to run Headless
import tkinter as tk

# Sets root window for user selection of how to run the scraping
root = tk.Tk()
root.attributes("-topmost", True)
root.geometry("400x300")
v = tk.IntVar(root)

tk.Label(root, 
        text="""How do you want to run the web scrape?""",
        justify = tk.LEFT,
        padx = 20).pack()
tk.Radiobutton(root, 
              text="Run headless",\
              width = 0,
              padx = 20, 
              variable=v, 
              value=1).pack(anchor=tk.W)
tk.Radiobutton(root, 
              text="Show me the browser",
              width = 0,
              padx = 20, 
              variable=v, 
              value=2).pack(anchor=tk.W)
tk.Button(root, text = "Close Window", command = root.destroy,
          padx = 20, width = 20).pack(anchor = tk.W)

root.mainloop()

if v.get() == 1:
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.headless = True
    driver = webdriver.Chrome(options = chrome_options)
elif v.get() == 2:
    driver = webdriver.Chrome()     
#%% Scraping LinkedIn
# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/jobs/')

# Initializes dataframe that will eventually be used to report jobs
jobs_df = pd.DataFrame(columns = ['Company','Job Title','Location',
                                  'Posting Date', 'Link to Posting'])
from tqdm import tqdm
for company in tqdm(company_df.Companies,position = 0, leave = True, 
                  desc = "Companies Scraped"):
    try: 
        # Clears "Location" box
        driver.find_element_by_name('location').clear()
        
        # Locates "Search job titles or companies" search box, searches for company
        company_input = driver.find_element_by_name("keywords")
        company_input.send_keys(company)
        company_input.send_keys(Keys.RETURN)
        
        # Locates "Search Jobs" button and clicks (Invalidated by RETURN Keystroke)
        # search_button = driver.find_element_by_xpath('//button[@form="JOBS"]')
        # search_button.click()
        
        # Job List Element
        jobs_list = driver.find_elements_by_class_name("result-card__full-card-link")
        links_list = []
        # After checking how many jobs are present (will probably be 25), grabs
        # corresponding link for each job
        for job_num in range(0,len(jobs_list)):
            links_list.append(jobs_list[job_num].get_attribute("href"))    
        job_title_list = []
        job_location_list=[]
        job_posted_date_list = []
        for link in links_list:
            # Navigates to job's LinkedIn page
            driver.get(link)
            # Grabs job title
            try:
                job_title_list.append(
                    driver.find_element_by_class_name("topcard__title").text)
            except:
                break
            # Grabs job location
            job_location_list.append(
                driver.find_element_by_xpath(
                    '//span [@class = "topcard__flavor topcard__flavor--bullet"]').text)
            # Because LinkedIn encodes posting dates less than 24 hours differently 
            # compared to posting dates in days or weeks, try-catch implemented
            try:
                job_posted_date_list.append(
                    driver.find_element_by_xpath(
                        '//span [@class = "topcard__flavor--metadata posted-time-ago__text"]').text)
            except NoSuchElementException:
                job_posted_date_list.append(
                    driver.find_element_by_xpath(
                        '//span [@class = "topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new"]').text)
            else:
                continue
        # Formats all of the lists into a dictionary 
        output_dict = {
            'Company': [company]*len(links_list),
            'Job Title': job_title_list,
            'Location': job_location_list,
            'Posting Date' : job_posted_date_list,
            'Link to Posting' : links_list 
            }
        # Dictionary converted to dataframe, which is then appended to reporting
        # dataframe
        output_df = pd.DataFrame(output_dict)
        jobs_df = jobs_df.append(output_df,ignore_index = True)
        # Navigates back to original page to restart the process
        driver.get('https://www.linkedin.com/jobs/')
    except KeyboardInterrupt:
        break
driver.close()
driver.quit()
#%% Filtering Dataframe for Appropriate Jobs
# Jobs that aren't relevant to university students are filtered out, or at least
# attempted to be
senior_positions =  ["Senior","Director","Manager","Chief","Principal",
                     "President","Sr"]
pattern = '|'.join(senior_positions)
jobs_df = jobs_df[~jobs_df['Job Title'].str.contains(pattern, case= False)]
#%% Outputting Dataframe as Excel File
# Current time is used to help distinguish output excel filename
from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
# dd_mm_YYYY_H_M_S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
file_name = "JobOpportunities_"+dt_string+".xlsx"
file_path = current_dir +"/"+ file_name

# Excel file is made from dataframe, saved in the directory of the script
writer = pd.ExcelWriter(file_path, engine='xlsxwriter') 
jobs_df.to_excel(writer, sheet_name='Jobs')
writer.save()    
    
            
        
    
        
