# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup

# Definition to grab extra pages worth of articles
def grab_extra_pages(base_url, location, number_of_pages, class_type, dictionary):
    x = 2
    while x <= number_of_pages:
        temp = location + str(x)
        soup = get_soup(base_url, temp)
        stories_list = soup.find(class_=class_type)
        if stories_list is not None:
            stories_items = stories_list.find_all('li')
            for item in stories_items:
                for stories_items in item.find_all('a'):
                    dictionary.update({stories_items.get('href'): stories_items.get('title')})
        x += 1

'''
Definition for filtering the values of dictionaries by keywords and return keys to a list (only if the key has not
already been added to that list)
'''
def dict_search(input_dict, keywords_list, save_location):
    temp = []
    for k, v in input_dict.items():
        for keyword in keywords_list:
            if keyword in v:
                if v not in save_location:
                    save_location.append(k)
                    temp.append(keyword)
    print(f'The keywords that triggered were {temp}.')

# Definition for pulling the body text from the NDTV articles identified above
def article_lookup(links, base_url, class_name, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_=class_name)
        if temp is not None:
            save_location = save_location + ' ' + temp.get_text()
    return save_location

# Set keywords and the first site to search
base_url = 'https://www.ndtv.com'
location = '/world-news'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'US Supreme Court', 'House of Representatives',
            'US Congress', 'US President', 'Capitol Hill', 'Washington', 'US Foreign Policy','US Army', 'US Air Force',
            'US Navy','US Marines', 'US Coast Guard')

soup = get_soup(base_url, location)

# Grabs the "trending" stories from the page and iterates down to the "li" tags.
trending_news = {}
trending_news_list = soup.find(class_='trending_insidelist1')
trending_news_items = trending_news_list.find_all('li')

# Grabs the html location and title for each "trending news" story and saves them to a dictionary
for item in trending_news_items:
    for trending_news_items in item.find_all('a'):
        trending_news.update({trending_news_items.get('href'): trending_news_items.get('title')})

new_stories = {}

# Grabbing the next 9 pages of articles and adding them to the dictionary
grab_extra_pages(base_url, '/world-news/page-', 30, 'new_storylising', new_stories)

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in trending_news.items() if v is not None}
trending_news.clear()
trending_news.update(filtered)

# Grabs the "new stories" from the page and iterates down to the "li" tags.
# NDTV's HTML appears to have a typo.  "new_storylising" should probably have a
# t for 'listing', but this code is written as it appears in the HTML.

new_stories_list = soup.find(class_='new_storylising')
new_stories_items = new_stories_list.find_all('li')

# Grabs the html location and title for each "new stories" article and saves them to a dictionary
for item in new_stories_items:
    for new_stories_items in item.find_all('a'):
        new_stories.update({new_stories_items.get('href'): new_stories_items.get('title')})

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in new_stories.items() if v is not None}
new_stories.clear()
new_stories.update(filtered)

trending_news_links = []
new_stories_links = []

# Pulling the html location keys out of the dictionaries created above into a pair of lists
dict_search(trending_news, keywords, trending_news_links)
print(f'{len(trending_news_links)} results were found in NDTV World Trending Stories.')
dict_search(new_stories, keywords, new_stories_links)
print(f'{len(new_stories_links)} results were found in NDTV World News Stories.')

base_url = ''

# Pulling the articles and saving their text to a string
ndtv_article_text = ''
ndtv_article_text = article_lookup(trending_news_links, base_url, 'sp-cn ins_storybody', ndtv_article_text)
ndtv_article_text = article_lookup(new_stories_links, base_url, 'sp-cn ins_storybody', ndtv_article_text)

print(f'The results are: {ndtv_article_text}')

pickle.dump(ndtv_article_text, open('ndtv_article_text.p', 'wb'))
