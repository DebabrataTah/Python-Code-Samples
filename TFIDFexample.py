
# coding: utf-8

# In[1]:

import string
import json
import pickle as pkl
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pyspark as ps
from collections import Counter
import numpy as np


# In[2]:

sc = ps.SparkContext()


# In[27]:

test_strings = ['the quick brown fox jumps over the brown fence','the boy paints a tall fence brown!',
               'basketball players are tall.','quick basketball players jump high']


# In[28]:

import nltk, string
#nltk.download()

def tokenize(text):
    tokens = []
    
    for word in nltk.word_tokenize(text):
        if word             not in nltk.corpus.stopwords.words('english')             and word not in string.punctuation             and word != '``':
                tokens.append(word)
                
    return tokens
                


# In[29]:

test_tokens = sc.parallelize(test_strings).map(tokenize)
test_tokens.collect()


# In[30]:

vocab = test_tokens.flatMap(lambda words: words).distinct()


# In[31]:

#flatten out tokens
vocab.collect()


# In[32]:

#total number of words 
vocab.count()


# In[33]:

from collections import Counter


# In[34]:

#bag of words vectorization
import numpy as np

broadcastVocab = sc.broadcast(vocab.collect())

def bow_vectorize(tokens):
    word_counts = Counter(tokens)
    vector = [word_counts[v] if v in word_counts else 0 for v in broadcastVocab.value]
    return np.array(vector)


# In[35]:

test_tokens.map(bow_vectorize).collect()


# In[37]:

test_tokens.collect()


# In[36]:

broadcastVocab.value


# In[45]:

#Term frequency (fraction of document the word represents) and Inverse Document frequency(TF-IDF)
#from collections import Counter
term_freq = test_tokens.map(lambda terms: Counter(terms))


# In[46]:

doc_freq = term_freq.flatMap(lambda counts: counts.keys()).map(lambda keys: (keys, 1)).reduceByKey(lambda a,b: a+b)


# In[47]:

total_docs = term_freq.count()


# In[51]:

import math

idf = map(lambda tup: (tup[0],math.log(float(total_docs)/(1+tup[1]))),doc_freq.collect())

broadcast_idf = sc.broadcast(idf)

def tfidf_vectorize(tokens):
    word_counts = Counter(tokens)
    doc_length = sum(word_counts.values())
    
    vector =[word_counts.get(word[0],0)*word[1]/float(doc_length) for word in broadcast_idf.value]
    return np.array(vector)


# In[52]:

test_tokens.map(tfidf_vectorize).collect()


# In[ ]:



