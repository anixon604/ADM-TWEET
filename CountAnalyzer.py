import operator
import os
import json
import tweepy
import re
import nltk
import string
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (6,6)
import matplotlib.pyplot as plt
import sys

from nltk.corpus import stopwords
nltk.download("stopwords") # download the stopword corpus on our computer
from nltk.tokenize import word_tokenize
from collections import Counter

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', '’']

emoticons_str = r"""
    (?:
        [<>]?
        [:;=8]                          # eyes
        [\-o\*\'-]?                     # optional nose
        [\)\]\(\[dDpP/\:\>\<\}\{@\|\\]  # mouth
        |
        [\)\]\(\[dDpP/\:\>\<\}\{@\|\\]  # mouth
        [\-o\*\'-]?                     # optional nose
        [:;=8]                          # eyes
        [<>]?
        |
        <3                              # heart
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:[a-zA-Z0-9_%\.+-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z0-9-.]+)', # <<<<<<< V.2 -process email addresses.
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fname = sys.argv[1] # first argument is JSON to analyse
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and term not in stop]
        count_all.update(terms_hash)
# Print the first 10 most frequent words
print(count_all.most_common(15))

sorted_x, sorted_y = zip(*count_all.most_common(15))
print(sorted_x, sorted_y)

plt.bar(range(len(sorted_x)), sorted_y, width=0.75, align='center')
plt.xticks(range(len(sorted_x)), sorted_x, rotation=60)
plt.axis('tight')
plt.tight_layout()

fig1 = plt.gcf()
plt.show()                