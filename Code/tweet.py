import tweepy
import my_tweet as mt

auth = tweepy.OAuthHandler(mt.consumer_key,mt.consumer_secret)
auth.set_access_token(mt.access_token,mt.access_token_secret)

api = tweepy.API(auth)
# for tweet in tweepy.Cursor(api.search,
#                            q='cat',
#                            count=100).items():
#   print(tweet.created_at, tweet.text)

with open('t.out','w') as f:
  for tweet in tweepy.Cursor(api.search,
                           q='#dog', #when getting data about cats, q should be changed into #cat
                           lang="en",
                           count=100).items():
    # print(tweet.created_at, tweet.text)
    f.write(tweet.text)
    f.write("\n")