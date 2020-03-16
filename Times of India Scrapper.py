# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:04:08 2020

@author: student
"""

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import re

kw = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'Supreme Court', 'House of Representatives', 'Congress', 'US President')

test = requests.get('https://timesofindia.indiatimes.com/world/us')

soup = bs(test.content, 'html.parser')
#print(soup.find_all('a'))

top_news = soup.find('ul', class_ ='top-newslist clearfix')
latest_stories = soup.find('ul', class_ = 'list5 clearfix')

print(top_news.prettify())
print(latest_stories.prettify())
