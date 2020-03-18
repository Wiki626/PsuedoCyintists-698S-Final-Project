# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Set keywords and the first site to search
base_url = 'https://timesofindia.indiatimes.com'
location = '/world/us'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'Supreme Court', 'House of Representatives',
            'Congress', 'US President', 'Capitol Hill', 'Washington', 'US Army', 'US Air Force', 'US Navy', 'US Marines')

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup


soup = get_soup(base_url, location)

# Grabs the "top news" stories from the page and iterates down to the "li" tags
top_news = {}
top_news_list = soup.find('ul', class_='top-newslist clearfix')
top_news_items = top_news_list.find_all('li')

# Grabs the html location and title for each "top news" story and saves them to a dictionary
for item in top_news_items:
    for top_news_items in item.find_all('a'):
        top_news.update({top_news_items.get('href'): top_news_items.get('title')})

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in top_news.items() if v is not None}
top_news.clear()
top_news.update(filtered)

# Grabs the "latest news" stories from the page and iterates down to the "li" tags
latest_stories = {}
latest_stories_list = soup.find('ul', class_='list5 clearfix')
latest_stories_items = latest_stories_list.find_all('li')

# Grabs the html location and title for each "latest news" story and saves them to a dictionary
for item in latest_stories_items:
    for latest_stories_items in item.find_all('a'):
        latest_stories.update({latest_stories_items.get('href'): latest_stories_items.get('title')})

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in latest_stories.items() if v is not None}
latest_stories.clear()
latest_stories.update(filtered)

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


top_news_links = []
latest_stories_links = []

# Pulling the html location keys out of the dictionaries created above into a pair of lists
dict_search(top_news, keywords, top_news_links)
print(f'{len(top_news_links)} results where found in Times of India US Top News Stories.')
dict_search(latest_stories, keywords, latest_stories_links)
print(f'{len(latest_stories_links)} results where found in Times of India US Latest News Stories.')

# Definition for pulling the body text from the Time of India articles identified above
def article_lookup(links, base_url, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_='_3WlLe')
        save_location = save_location + ' ' + temp.get_text()
        return save_location


# Pulling the articles and saving their text to a string
times_article_text = ''
times_article_text = article_lookup(top_news_links, base_url, times_article_text)
times_article_text = article_lookup(latest_stories_links, base_url, times_article_text)

print(f'The results are: {times_article_text}')

pickle.dump(times_article_text, open('times_article_text.p', 'wb'))