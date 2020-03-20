# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Set keywords and the first site to search
base_url = 'https://www.indiatoday.in'
location = '/world'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'Supreme Court', 'House of Representatives',
            'Congress', 'US President', 'Capitol Hill', 'Washington', 'US Army', 'US Air Force', 'US Navy', 'US Marines')

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup

soup = get_soup(base_url, location)

# Grabs the "latest news" stories from the first page and iterates down to the "li" tags
it_stories = {}
it_stories_list = soup.find(class_='view-content')
it_stories_items = it_stories_list.find_all(class_='detail')

# Grabs the html location and title for each "latest news" story and saves them to a dictionary

for item in it_stories_items:
    for it_stories_anchor in item.find_all('a'):
        for it_stories_paragraph in item.find_all('p'):
            temp = it_stories_paragraph.get_text()
            temp = temp.replace('\n', ' ')
            it_stories.update({it_stories_anchor.get('href'): temp})



# Definition to grab extra pages worth of articles
def it_grab_extra_pages(base_url, location, number_of_pages, class_type, dictionary):
    x = 2
    while x <= number_of_pages:
        temp = location + str(x)
        soup = get_soup(base_url, temp)
        stories_list = soup.find(class_=class_type)
        if stories_list is not None:
            stories_items = stories_list.find_all(class_='detail')
            for item in stories_items:
                for anchor_item in item.find_all('a'):
                    for paragraph_item in item.find_all('p'):
                        clean = paragraph_item.get_text()
                        clean = clean.replace('\n', ' ')
                        dictionary.update({anchor_item.get('href'): clean})
        x += 1

# Grabbing the next 9 pages of articles and adding them to the dictionary
it_grab_extra_pages(base_url, '/world/?page=', 30, 'view-content', it_stories)

#Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in it_stories.items() if v is not None}
it_stories.clear()
it_stories.update(filtered)

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


it_stories_links = []

# Pulling the html location keys out of the dictionaries created above into a pair of lists
dict_search(it_stories, keywords, it_stories_links)
print(f'{len(it_stories_links)} results where found in India Today World News Stories.')

# Definition for pulling the body text from the articles identified above
def it_article_lookup(links, base_url, class_name, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_=class_name)
        article = temp.find_all('p')
        for paragraph in article:
            if paragraph is not None:
                clean = paragraph.get_text()
                clean = clean.replace('\n', ' ')
                save_location = save_location + ' ' + clean
    return save_location


# Pulling the articles and saving their text to a string
it_article_text = ''
it_article_text = it_article_lookup(it_stories_links, base_url, 'description', it_article_text)

print(f'The results are: {it_article_text}')

pickle.dump(it_article_text, open('it_article_text.p', 'wb'))