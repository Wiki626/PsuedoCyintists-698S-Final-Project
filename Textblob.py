# Import libs
import pickle
from textblob import TextBlob as tb
import numpy as np

# Pull in pickles
times_article_text = pickle.load(open('times_article_text.p', 'rb'))
ndtv_article_text = pickle.load(open('ndtv_article_text.p', 'rb'))
it_article_text = pickle.load(open('it_article_text.p', 'rb'))

# Create blobs
times_blob = tb(times_article_text)
ndtv_blob = tb(ndtv_article_text)
it_blob = tb(it_article_text)
times_blob_sentences = times_blob.sentences
ndtv_blob_sentences = ndtv_blob.sentences
it_blob_sentences = it_blob.sentences

filtered_times_blob_sentences = []
filtered_ndtv_blob_sentences = []
filtered_it_blob_sentences = []
times_dirty_words = ['Download The Times of India News App for Latest World News.']
ndtv_dirty_words = ['Except for the headline, this story has not been edited by NDTV staff and is published from a '
                     'syndicated feed']
it_dirty_words = ['ALSO READ | |']

# Definition to clear out any advertising
def kill_advertising(input_list, dirty_words_list, output_list):
    for sentence in input_list:
        for words in dirty_words_list:
            if words not in sentence:
                output_list.append(sentence)


kill_advertising(times_blob_sentences, times_dirty_words, filtered_times_blob_sentences)
kill_advertising(ndtv_blob_sentences, ndtv_dirty_words, filtered_ndtv_blob_sentences)
kill_advertising(it_blob_sentences, it_dirty_words, filtered_it_blob_sentences)

times_sentiment = []
ndtv_sentiment = []
it_sentiment = []

# Definition for determining sentiment per sentence
def sentence_sentiment(sentence_blob, storage_location):
    for sentence in sentence_blob:
        sentiment = sentence.sentiment[0]*sentence.sentiment[1]
        storage_location.append(sentiment)
        #print(f'The sentiment score is {sentiment} for "{sentence}"')

# Getting the average sentiment for a site
sentence_sentiment(filtered_times_blob_sentences, times_sentiment)
times_ave_sentiment = np.average(times_sentiment)
print(f'The average sentiment for The Times of India is {times_ave_sentiment}')

sentence_sentiment(filtered_ndtv_blob_sentences, ndtv_sentiment)
ndtv_ave_sentiment = np.average(ndtv_sentiment)
print(f'The average sentiment for NDTV is {ndtv_ave_sentiment}')

sentence_sentiment(filtered_it_blob_sentences, it_sentiment)
it_ave_sentiment = np.average(it_sentiment)
print(f'The average sentiment for India Today is {it_ave_sentiment}')

all_sentiment = times_sentiment
all_sentiment.extend(ndtv_sentiment)
all_sentiment.extend(it_sentiment)
all_ave_sentiment = np.average(all_sentiment)
print(f'The average sentiment across all three sites is {all_ave_sentiment}')