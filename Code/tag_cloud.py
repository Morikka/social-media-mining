from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def drawname(kind):
  d = path.dirname(__file__)

  # Read text
  text = open(path.join(d, '../Data/Testdata/'+kind+'.in')).read()

  # read image
  mask = np.array(Image.open(path.join(d, "../Data/img/"+kind+".png")))

  stopwords = set(STOPWORDS)
  # stopwords.add("said")

  wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
                 random_state=1).generate(text)

  # generate word cloud
  # wc.generate(text)

  # store to file
  wc.to_file(kind+".png")

  # show
  plt.imshow(wc, interpolation='bilinear')
  plt.axis("off")
  plt.figure()
  default_colors = wc.to_array()
  plt.imshow(default_colors, interpolation="bilinear")
  # plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
  plt.axis("off")
  plt.show()