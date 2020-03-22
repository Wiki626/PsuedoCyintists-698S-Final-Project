# Import required libs
from bs4 import BeautifulSoup as bs
import requests
import pickle

# Set keywords and the first site to search
base_url = 'http://en.people.cn'
location = '/90777/index.html'

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'US Supreme Court', 'House of Representatives',
            'US Congress', 'US President', 'Capitol Hill', 'Washington', 'US Army', 'US Air Force', 'US Navy',
            'US Marines', 'US Coast Guard')

# Function for setting up the soup
def get_soup(base_url, location):
    page = requests.get(base_url + location)
    soup = bs(page.content, 'html.parser')
    return soup

soup = get_soup(base_url, location)

# Grabs the "latest news" stories from the first page and iterates down to the "li" tags
pd_stories = {}
pd_stories_list = soup.find(class_='d2p3_left fl')
pd_stories_items = pd_stories_list.find_all('h3')

# Grabs the html location and title for each "latest news" story and saves them to a dictionary
for item in pd_stories_items:
    for pd_stories_anchor in item.find_all('a'):
        pd_stories.update({pd_stories_anchor.get('href'): pd_stories_anchor.get_text()})



# Definition to grab extra pages worth of articles
def pd_grab_extra_pages(base_url, location, number_of_pages, class_type, dictionary):
    x = 2
    while x <= number_of_pages:
        temp = location + str(x) + '.html'
        soup = get_soup(base_url, temp)
        stories_list = soup.find(class_=class_type)
        if stories_list is not None:
            stories_items = stories_list.find_all('h3')
            for item in stories_items:
                for anchor_item in item.find_all('a'):
                    dictionary.update({anchor_item.get('href'): anchor_item.get_text()})
        x += 1

# Grabbing the next 9 pages of articles and adding them to the dictionary
pd_grab_extra_pages(base_url, '/90777/index', 30, 'd2p3_left fl', pd_stories)

#Cleans the dictionary of "None" type entries
filtered = {k: v for k, v in pd_stories.items() if v is not None}
pd_stories.clear()
pd_stories.update(filtered)

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


pd_stories_links = []

# Pulling the html location keys out of the dictionaries created above into a pair of lists
dict_search(pd_stories, keywords, pd_stories_links)
print(f'{len(pd_stories_links)} results where found in People Daily News Stories.')

# Definition for pulling the body text from the articles identified above
def pd_article_lookup(links, base_url, class_name, save_location):
    for link in links:
        soup = get_soup(base_url, link)
        temp = soup.find(class_=class_name)
        if temp is not None:
            article = temp.find_all('p')
            for paragraph in article:
                if paragraph is not None:
                    clean = paragraph.get_text()
                    clean = clean.replace('\n', ' ')
                    save_location = save_location + ' ' + clean
    return save_location


# Pulling the articles and saving their text to a string
pd_article_text = ''
pd_article_text = pd_article_lookup(pd_stories_links, base_url, 'wb_12 wb_12b clear', pd_article_text)

print(f'The results are: {pd_article_text}')

pickle.dump(pd_article_text, open('pd_article_text.p', 'wb'))