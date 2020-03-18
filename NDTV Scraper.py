# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Set keywords and the first site to search
base_url = 'https://www.ndtv.com'
location = '/world-news'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'Supreme Court', 'House of Representatives',
            'Congress', 'US President', 'Capitol Hill', 'Washington', 'US Army', 'US Air Force', 'US Navy', 'US Marines')

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup


soup = get_soup(base_url, location)

# Grabs the "trending" stories from the page and iterates down to the "li" tags.
trending_news = {}
trending_news_list = soup.find(class_='trending_insidelist1')
trending_news_items = trending_news_list.find_all('li')

# Grabs the html location and title for each "trending news" story and saves them to a dictionary
for item in trending_news_items:
    for trending_news_items in item.find_all('a'):
        trending_news.update({trending_news_items.get('href'): trending_news_items.get('title')})

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in trending_news.items() if v is not None}
trending_news.clear()
trending_news.update(filtered)

# Grabs the "new stories" from the page and iterates down to the "li" tags.
# NDTV's HTML appears to have a typo.  "new_storylising" should probably have a
# t for 'listing', but this code is written as it appears in the HTML.
new_stories = {}
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

# Definition for filtering the values of dictionaries by keywords and return keys to a list (only if the key has not
# already been added to that list)
def dict_search(input_dict, keywords_list, save_location):
    temp = []
    for k, v in input_dict.items():
        for keyword in keywords_list:
            if keyword in v:
                if v not in save_location:
                    save_location.append(k)
                    temp.append(keyword)
    print(f'The keywords that triggered were {temp}.')


trending_news_links = []
news_stories_links = []

# Pulling the html location keys out of the dictionaries created above into a pair of lists
dict_search(trending_news, keywords, trending_news_links)
print(f'{len(trending_news_links)} results were found in NDTV World Trending Stories.')
dict_search(new_stories, keywords, new_stories_links)
print(f'{len(new_stories_links)} results were found in NDTV World News Stories.')

article_text = ''

# Definition for pulling the body text from the NDTV articles identified above
def article_lookup(links, base_url, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_='sp-cn ins_storybody')
        save_location = save_location + ' ' + temp.get_text()
    return save_location


# Pulling the articles and saving their text to a string
ndtv_article_text = ''
ndtv_article_text = article_lookup(trending_news_links, base_url, ndtv_article_text)
ndtv_article_text = article_lookup(news_stories_links, base_url, ndtv_article_text)

print(f'The results are: {ndtv_article_text}')

pickle.dump(ndtv_article_text, open('ndtv_article_text.p', 'wb'))
