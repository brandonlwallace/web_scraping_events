# -*- coding: utf-8 -*-
"""

@author: Brandon Wallace

"""

# Scraping the web for food events and free food

# This module uses BeautifulSoup to parse HTML and extract information. 

import requests
from bs4 import BeautifulSoup
import re

httpString = 'https://discoverevvnt.com/framed/eyJwX2lkIjoicGl0dHNidXJnaG1hZ2F6aW5lLmNvbSIsIndpZGdldCI6ZmFsc2UsImxhbmRzY2FwZSI6ZmFsc2UsInZpcnR1YWwiOmZhbHNlLCJjX2lkIjpudWxsLCJkX2JhY2tmaWxsX2ltYWdlcyI6ZmFsc2V9/food-drink'

# This webpage displays the events listed on a public calendar that has been filtered for food only 

page = requests.get(httpString)

soup = BeautifulSoup(page.content, 'html.parser')

# It is fed into the Beautiful soup package to make extracting information simplier. 
# Cards corresponds to how the information is displayed on the web. Each event is styled like a trading card with information therein.
cards = soup.find(id='main-container')

# Part 1 - Event Information
# This code finds where the event name is in the text based on the class from the HTML. 

event_names = cards.find_all(class_='font-bold line-clamp-2 leading-5')

# A for loop iterates over the strings and uses get text to return the name of the event. It is stored in a list. 
event_list = []
for event in event_names:
    event_list.append(event.get_text())
    
# The process is repeated for locations. Again, the text is returned in a list. 
locations = cards.find_all(class_='line-clamp-1')

location_list = []
for location in locations:
    location_list.append(location.get_text())

# Time is an exceptional case. Because of the layout of the webpage, this script transform a larger block into a collection of 
# strings and stores them in a list called raw_block. 

text_block = cards.find_all(class_='w-full h-28')
raw_block = []
for x in text_block:
    raw_block.append(str(x))
    
# This script then uses regex to find times. It looks for digits on either side of a colon followed by an AM or PM (or am or pm)

time_format = r'[0-9]*:[0-9]*[AaPp][Mm]'

time_list = []
for items in raw_block:
    x = re.search(time_format, items)
    time_list.append(x.group())

# The final loop pulls the date. It stores the inforamtion in a list as well.

dates = cards.find_all(class_='-mt-1 shadow-md')

date_list = []
for date in dates:
   date_list.append(date.get_text())
   

# Part 2 - Transforming Events to a Dataframe
# This script utilizes pandas to zip the lists together into a dataframe since there will always be the same number of
# event names, locations, times, and dates. 

import pandas as pd

rows = list(zip(time_list, date_list, location_list, event_list))

event_df = pd.DataFrame(rows, columns = ['Time', 'Date', 'Location', 'Event'])

# To confirm the code works, we look at the first five rows of the dataframe.         
event_df.head(5)

  








