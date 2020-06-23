# Import libs
import pickle
from textblob import TextBlob as tb
import numpy as np

# Definition to clear out any advertising
def kill_advertising(input_list, dirty_words_list, output_list):
    for sentence in input_list:
        for words in dirty_words_list:
            if words not in sentence:
                output_list.append(sentence)

# Definition for determining sentiment per sentence
def sentence_sentiment(sentence_blob, storage_location):
    for sentence in sentence_blob:
        sentiment = sentence.sentiment[0]*sentence.sentiment[1]
        storage_location.append(sentiment)
        #print(f'The sentiment score is {sentiment} for "{sentence}"')

def sentence_search(sentence_blob, keywords_list, save_location):
    for item in sentence_blob:
        for keyword in keywords_list:
            if keyword in item:
                save_location.append(item)

keywords = ('Fed', 'White House', 'Trump', 'US Senate', 'US Government', 'US Supreme Court', 'House of Representatives',
            'US Congress', 'US President', 'Capitol Hill', 'Washington', 'US Foreign Policy','US Army', 'US Air Force',
            'US Navy','US Marines', 'US Coast Guard')

# Pull in pickles
times_article_text = pickle.load(open('times_article_text.p', 'rb'))
ndtv_article_text = pickle.load(open('ndtv_article_text.p', 'rb'))
it_article_text = pickle.load(open('it_article_text.p', 'rb'))
pd_article_text = pickle.load(open('pd_article_text.p', 'rb'))

# Create blobs
times_blob = tb(times_article_text)
ndtv_blob = tb(ndtv_article_text)
it_blob = tb(it_article_text)
pd_blob = tb(pd_article_text)
times_blob_sentences = times_blob.sentences
ndtv_blob_sentences = ndtv_blob.sentences
it_blob_sentences = it_blob.sentences
pd_blob_sentences = pd_blob.sentences

filtered_times_blob_sentences = []
filtered_ndtv_blob_sentences = []
filtered_it_blob_sentences = []
times_dirty_words = ['Download The Times of India News App for Latest World News.']
ndtv_dirty_words = ['Except for the headline, this story has not been edited by NDTV staff and is published from a '
                     'syndicated feed']
it_dirty_words = ['ALSO READ | |']

kill_advertising(times_blob_sentences, times_dirty_words, filtered_times_blob_sentences)
kill_advertising(ndtv_blob_sentences, ndtv_dirty_words, filtered_ndtv_blob_sentences)
kill_advertising(it_blob_sentences, it_dirty_words, filtered_it_blob_sentences)

times_sentiment = []
ndtv_sentiment = []
it_sentiment = []
pd_sentiment = []

truncated_times_blob_sentences = []
truncated_ndtv_blob_sentences = []
truncated_it_blob_sentences = []
truncated_pd_blob_sentences = []

truncated_times_sentiment = []
truncated_ndtv_sentiment = []
truncated_it_sentiment = []
truncated_pd_sentiment = []

# Getting the average sentiment for a site
sentence_sentiment(filtered_times_blob_sentences, times_sentiment)
times_ave_sentiment = np.average(times_sentiment)
sentence_search(times_blob_sentences, keywords, truncated_times_blob_sentences)
sentence_sentiment(truncated_times_blob_sentences, truncated_times_sentiment)
truncated_times_ave_sentiment = np.average(truncated_times_sentiment)
print(f'The average sentiment for The Times of India WITHOUT keyword filtering is {times_ave_sentiment}')
print(f'And the average sentiment for The Times of India WITH keyword filtering sentences is {truncated_times_ave_sentiment}')

sentence_sentiment(filtered_ndtv_blob_sentences, ndtv_sentiment)
ndtv_ave_sentiment = np.average(ndtv_sentiment)
sentence_search(ndtv_blob_sentences, keywords, truncated_ndtv_blob_sentences)
sentence_sentiment(truncated_ndtv_blob_sentences, truncated_ndtv_sentiment)
truncated_ndtv_ave_sentiment = np.average(truncated_ndtv_sentiment)
print(f'The average sentiment for NDTV WITHOUT keyword filtering is {ndtv_ave_sentiment}')
print(f'And average sentiment for NDTV WITH keyword filtering is {truncated_ndtv_ave_sentiment}')

sentence_sentiment(filtered_it_blob_sentences, it_sentiment)
it_ave_sentiment = np.average(it_sentiment)
sentence_search(it_blob_sentences, keywords, truncated_it_blob_sentences)
sentence_sentiment(truncated_it_blob_sentences, truncated_it_sentiment)
truncated_it_ave_sentiment = np.average(truncated_it_sentiment)
print(f'The average sentiment for India Today WITHOUT keyword filtering is {it_ave_sentiment}')
print(f'And average sentiment for India Today WITH keyword filtering is {truncated_it_ave_sentiment}')

all_sentiment = times_sentiment
all_sentiment.extend(ndtv_sentiment)
all_sentiment.extend(it_sentiment)
all_ave_sentiment = np.average(all_sentiment)
truncated_all_sentiment = truncated_times_sentiment
truncated_all_sentiment.extend(truncated_ndtv_sentiment)
truncated_all_sentiment.extend(truncated_it_sentiment)
truncated_all_ave_sentiment = np.average(truncated_all_sentiment)
print(f'The average sentiment across all three Indian sites WITHOUT keyword filtering is {all_ave_sentiment}')
print(f'And average sentiment across all three Indian sites WITH keyword filtering is {truncated_all_ave_sentiment}')

sentence_sentiment(pd_blob_sentences, pd_sentiment)
pd_ave_sentiment = np.average(pd_sentiment)
sentence_search(pd_blob_sentences, keywords, truncated_pd_blob_sentences)
sentence_sentiment(truncated_pd_blob_sentences, truncated_pd_sentiment)
truncated_pd_ave_sentiment = np.average(truncated_pd_sentiment)

print(f'For contrast the average sentiment for the Chinese People Daily WITHOUT keyword filtering is {pd_ave_sentiment}')
print(f'And the average sentiment for the Chinese People Daily WITH keyword filtering is {truncated_pd_ave_sentiment}')
