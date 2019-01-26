import tweepy
from Twitter_Credentials import *
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
api = tweepy.API(auth)
text = ''

tweeds = api.user_timeline(screen_name='realDonaldTrump',
                           count=100, include_rts=False, tweet_mode='extended')
for tweed in tweeds:
    text = text + ' ' + tweed.full_text

wordcloud = WordCloud(width=1920, height=1200)
STOPWORDS.update(['https', 'co', 'amp'])
wordcloud.generate(text)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
