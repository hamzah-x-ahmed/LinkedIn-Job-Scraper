# LinkedIn-Job-Scraper
Thanks for using the _Biomedical Engineering Navigation Tool for Opportunities_ (aka BENTO)!

__Overview__

What this code will do is pull 25 jobs from LinkedIn for each company specified in the Companies.csv file. Please have the script and the .csv file in the same directory. This script will take roughly 30 seconds per company. After iterating through all companies, it will output an Excel file of all the jobs it looked at that could theoretically be classified as "entry-level", and this Excel file will be located in the same folder as the script and Companies.csv. The Excel File Name will be JobOpportunities_(month)(day)_(year)_(hour)_(minute)_(second).

__Prerequisites__

This script will __require you to have Python3 and Google Chrome installed__. I recommend running it directly from an IDE or Text Editor, such as Visual Studio Code or Spyder. I'm partial to Spyder, as that was the IDE this script was primarily developed in.

This script will require the following packages to be installed for proper functionality. While I've attempted to handle dependency issues, please install the following packages:
  
  _TQDM_
  
  _Selenium, with a ChromeDriver compatible with your Google Chrome installation_
  
  _Tkinter_
  
  _Pandas_

You can install the packages above by going to your Command Prompt/Terminal and typing in the following (minus the curly brackets}:
  
  _python -m pip install {module name}_

If you are already in a python command line, just run this (again, without curly brackets):
  
  _pip install {module name}_


__Disclaimer:__ I am not a savvy coder, at all. Please let me know if you have any issues at hamzah.x.ahmed@gmail.com 

Potential updates in the future:
  
  _Adding in Selenium selection for "most recent jobs" from LinkedIn published "in the last 2 weeks"_
  
  _Implementing a scroll to try to capture more than 25 jobs per company_
  
  _LinkedIn bot that will automatically post updates once a week_
 
