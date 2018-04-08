from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
from sklearn.feature_extraction import stop_words
import nltk
import operator

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
      print(w)
      result = result + w + " "
      if w in word_dict:
        word_dict[w] += 1
      else:
        word_dict[w] = 1
  sorted_word_dict = sorted(word_dict.items(), key=lambda kv: kv[1], reverse=True)
  with open("t.out","w") as f:
    for items in sorted_word_dict:
      f.write(str(items))
      f.write("\n")
  print(sorted_word_dict)
  return result




def drawname(kind):
  d = path.dirname(__file__)

  # Read text
  text = open(path.join(d, '../Data/Testdata/'+kind+'.in')).read()
  text = clean_str(text)
  # print(text)
  words = text.split()

# doc-term matrix with raw word count
  final_text = process(words)
  print(final_text)

  # read image
  mask = np.array(Image.open(path.join(d, "../Data/img/"+kind+".png")))

  # stopwords = set(STOPWORDS)
  # stopwords.add("rt")
  # # text = "aa bb cc dd aa cc aa dd aa cc aa cc"

  # wc = WordCloud(max_words=1000, mask=mask, margin=10,random_state=1).generate(final_text)
  # # # generate word cloud
  # # wc.generate(text)
  # # store to file
  # wc.to_file(kind+".png")

  # # show
  # plt.imshow(wc, interpolation='bilinear')
  # plt.axis("off")
  # plt.figure()
  # default_colors = wc.to_array()
  # plt.imshow(default_colors, interpolation="bilinear")
  # # plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
  # plt.axis("off")
  # plt.show()