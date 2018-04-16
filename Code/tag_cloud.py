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

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


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
  with open("t.out","w") as f:
    tmp = 0
    for items in sorted_word_dict:
      if int(items[1]) < 50:
      # if tmp>200:
        break
      f.write(str(items[0]))
      f.write(" , ")
      f.write(str(items[1]))
      f.write('\n')
      res[str(items[0])] = int(items[1])
      tmp += 1
  # print(sorted_word_dict)
  # return result
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

  # read image
  mask = np.array(Image.open(path.join(d, "../Data/img/"+kind+".png")))

  wc = WordCloud(max_words=200, mask=mask, margin=10,random_state=1).fit_words(final_text)
  # # generate word cloud

  color_to_words = {
      # words below will be colored with a green single color function
      '#00ff00': pos_word,
      # will be colored with a red single color function
      'red': neg_word
  }

  default_color = 'grey'

  grouped_color_func = GroupedColorFunc(color_to_words, default_color)

  # Apply our color function
  wc.recolor(color_func=grouped_color_func)

  # Plot
  plt.figure()
  plt.imshow(wc, interpolation="bilinear")
  plt.axis("off")
  plt.show()