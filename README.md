# LinkedIn-Job-Scraper
What this code will do is pull 25 jobs from LinkedIn for each company specified in the Companies.csv file. Please have the script and the .csv file in the same directory. This script will take roughly 30 seconds per company. After iterating through all companies, it will output an Excel file of all the jobs it looked at that could theoretically be classified as "entry-level", and this Excel file will be located in the same folder as the script and Companies.csv. The Excel File Name will be JobOpportunities_(month)_(day)_(year)_(hour)_(minute)_(second).

This script will require you to have Python3 and Google Chrome installed. I recommend running it directly from an IDE or Text Editor, such as Visual Studio Code or Spyder. I'm partial to Spyder, as that was the IDE this script was primarily developed in.

This script will require the following packages to be installed for proper functionality. While I've attempted to handle dependency issues, please install the following packages:
  TQDM
  Selenium, with a ChromeDriver compatible with your Google Chrome installation
  Tkinter
  Pandas
You can install the packages above by going to your Command Prompt/Terminal and typing in the following (minus the curly brackets}:
  python -m pip install {module name}
If you are already in a python command line, just run this (again, without curly brackets):
  pip install {module name}


Disclaimer: I am not a savvy coder, at all. Please let me know if you have any issues at hamzah.x.ahmed@gmail.com 

Potential updates in the future:
  Adding in Selenium selection for "most recent jobs" from LinkedIn published "in the last 2 weeks"
  Implementing a scroll to try to capture more than 25 jobs per company
  LinkedIn bot that will automatically post updates once a week
 
