import my_tweet as mt
from TwitterSearch import *
try:
  tso = TwitterSearchOrder() # create a TwitterSearchOrder object
  tso.set_keywords(['cat']) # let's define all words we would like to have a look for
  tso.set_language('en') # we want to see German tweets only
  tso.set_include_entities(True) # and don't give us all those entity information

  ts = TwitterSearch(
    consumer_key = mt.consumer_key,
    consumer_secret = mt.consumer_secret,
    access_token = mt.access_token,
    access_token_secret = mt.access_token_secret
    )

  tweet = ts.search_tweets(tso)
  # print(tweet)

  cnt = ts.get_amount_of_tweets()
  print(cnt)
     # this is where the fun actually starts :)
  with open('t.out','w') as f:
    for tweet in ts.search_tweets_iterable(tso):
      # f.write(tweet['user']['screen_name'])
      # f.write(" tweeted: ")
      f.write(tweet['text'])
      f.write("\n")
      # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
  print(e)