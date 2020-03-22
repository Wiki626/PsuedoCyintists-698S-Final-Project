# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Set keywords and the first site to search
base_url = 'https://timesofindia.indiatimes.com'
location = '/world/us'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'US Supreme Court', 'House of Representatives',
            'US Congress', 'US President', 'Capitol Hill', 'Washington', 'US Army', 'US Air Force', 'US Navy',
            'US Marines', 'US Coast Guard')

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup


soup = get_soup(base_url, location)

# Grabs the "top news" stories from the page and iterates down to the "li" tags
top_news = {}
top_news_list = soup.find(class_='top-newslist clearfix')
top_news_items = top_news_list.find_all('li')

# Grabs the html location and title for each "top news" story and saves them to a dictionary
for item in top_news_items:
    for top_news_items in item.find_all('a'):
        top_news.update({top_news_items.get('href'): top_news_items.get('title')})

# Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in top_news.items() if v is not None}
top_news.clear()
top_news.update(filtered)

# Grabs the "latest news" stories from the first page and iterates down to the "li" tags
latest_stories = {}
latest_stories_list = soup.find(class_='list5 clearfix')
latest_stories_items = latest_stories_list.find_all('li')

# Grabs the html location and title for each "latest news" story and saves them to a dictionary
for item in latest_stories_items:
    for latest_stories_items in item.find_all('a'):
        latest_stories.update({latest_stories_items.get('href'): latest_stories_items.get('title')})

# Definition to grab extra pages worth of articles
def grab_extra_pages(base_url, location, number_of_pages, class_type, dictionary):
    x = 2
    while x <= number_of_pages:
        temp = location + str(x)
        soup = get_soup(base_url, temp)
        stories_list = soup.find(class_=class_type)
        stories_items = stories_list.find_all('li')
        for item in stories_items:
            for stories_items in item.find_all('a'):
                dictionary.update({stories_items.get('href'): stories_items.get('title')})
        x += 1


# Grabbing the next 9 pages of articles and adding them to the dictionary
grab_extra_pages(base_url, '/world/us/', 30, 'list5 clearfix', latest_stories)

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
def article_lookup(links, base_url, class_name, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_=class_name)
        if temp is not None:
            save_location = save_location + ' ' + temp.get_text()
    return save_location


# Pulling the articles and saving their text to a string
times_article_text = ''
times_article_text = article_lookup(top_news_links, base_url, '_3WlLe', times_article_text)
times_article_text = article_lookup(latest_stories_links, base_url, '_3WlLe', times_article_text)

print(f'The results are: {times_article_text}')

pickle.dump(times_article_text, open('times_article_text.p', 'wb'))