# Import libs
import pickle
from textblob import TextBlob as tb
import numpy as np

# Pull in pickles
times_article_text = pickle.load(open('times_article_text.p', 'rb'))

# Create blobs
times_blob = tb(times_article_text)
times_blob_sentences = times_blob.sentences

filtered_times_blob_sentences = []

# Clear out advertising
for sentence in reversed(times_blob_sentences):
    dirty_words = 'Download The Times of India News App for Latest World News.'
    if dirty_words not in sentence:
        filtered_times_blob_sentences.append(sentence)

times_sentiment = []

# Definition for determining sentiment per sentence
def sentence_sentiment(sentence_blob, storage_location):
    for sentence in sentence_blob:
        sentiment = sentence.sentiment[0]*sentence.sentiment[1]
        storage_location.append(sentiment)
        print(f'The sentiment score is {sentiment} for "{sentence}"')

# Getting the average sentiment for a site
sentence_sentiment(filtered_times_blob_sentences, times_sentiment)
times_ave_sentiment = np.average(times_sentiment)
print(f'The average sentiment for The Times of India is {times_ave_sentiment}')