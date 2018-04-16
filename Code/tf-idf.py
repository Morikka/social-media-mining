from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
from sklearn.feature_extraction import stop_words
import nltk
import operator
from wordcloud import (get_single_color_func)
import matplotlib.pyplot as plt
import math

def clean_str(string, TREC=False):
  """
    Tokenization/string cleaning for all datasets except for SST.
    Every dataset is lower cased except for TREC
  """
  string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
  string = re.sub(r"\'s", " \'s", string)
  string = re.sub(r"\'ve", " \'ve", string)
  string = re.sub(r"n\'t", " n\'t", string)
  string = re.sub(r"\'re", " \'re", string)
  string = re.sub(r"\'d", " \'d", string)
  string = re.sub(r"\'ll", " \'ll", string)
  string = re.sub(r",", " , ", string)
  string = re.sub(r"!", " ! ", string)
  string = re.sub(r"\(", " \( ", string)
  string = re.sub(r"\)", " \) ", string)
  string = re.sub(r"\?", " \? ", string)
  string = re.sub(r"\s{2,}", " ", string)
  return string.strip() if TREC else string.strip().lower()

def process(words):
  word_dict = {}
  result = ""
  real_words = set(nltk.corpus.words.words())
  for w in words:
    if w not in stop_words.ENGLISH_STOP_WORDS and w in real_words and len(w)>1:
      # print(w)
      result = result + w + " "
      if w in word_dict:
        word_dict[w] += 1
      else:
        word_dict[w] = 1
  sorted_word_dict = sorted(word_dict.items(), key=lambda kv: kv[1], reverse=True)
  res = {}
  # with open("t.out","w") as f:
  tmp = 0
  for items in sorted_word_dict:
    if int(items[1]) < 50:
#     # if tmp>200:
      break
    # f.write(str(items[0]))
    # f.write(" , ")
    # f.write(str(items[1]))
    # f.write('\n')
    res[str(items[0])] = int(items[1])
    tmp += 1
  return res

def drawname(kind):
  d = path.dirname(__file__)
  # Read text
  text = open(path.join(d, '../Data/Testdata/'+kind+'.in')).read()

  text = clean_str(text)
  # print(text)
  words = text.split()
  # text.close()

# with open('../Data/Dict/positive-words.txt') as f:
  text = open(path.join(d, '../Data/Dict/positive-words.txt')).read()
  pos_word = text.split()
  text = open(path.join(d, '../Data/Dict/negative_words.in')).read()
  neg_word = text.split()

# doc-term matrix with raw word count

  final_text = process(words)

  return final_text

cat = drawname("cat")
dog = drawname("dog")

d = path.dirname(__file__)

text = open(path.join(d, '../Data/Dict/positive-words.txt')).read()
pos_word = text.split()
text = open(path.join(d, '../Data/Dict/negative_words.in')).read()
neg_word = text.split()

lis = []
for items in dog:
  lis.append(items)

for items in cat:
  if items not in lis:
    lis.append(items)
cat_pos = 0.0;
cat_neg = 0.0;
dog_pos = 0.0;
dog_neg = 0.0;

for items in lis:
  if items in pos_word:
    if items in cat and items in dog:
      tmp = 1.0*(cat[items]+dog[items])
      cat_pos += cat[items] * math.log(1+cat[items]/tmp,10)
      dog_pos += dog[items] * math.log(1+dog[items]/tmp,10)
    elif items in cat and items not in dog:
      cat_pos += cat[items]
    elif items in dog and items not in cat:
      dog_pos += dog[items]
  elif items in neg_word:
    if items in cat and items in dog:
      tmp = 1.0*(cat[items]+dog[items])
      cat_neg += cat[items] * math.log(1+cat[items]/tmp,10)
      dog_neg += dog[items] * math.log(1+dog[items]/tmp,10)
      # print(cat[items])
      # print(cat[items] * math.log(1+cat[items]/tmp))
    elif items in cat and items not in dog:
      cat_neg += cat[items]
    elif items in dog and items not in cat:
      dog_neg += dog[items]

