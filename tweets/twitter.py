import tweepy,time,re
from django.utils import timezone
from tweepy.auth import OAuthHandler
from .models import Tweet,Author
from django.contrib.auth.models import User
import requests,json
import tldextract
from datetime import datetime
from . import config  
consumer_key = config.CONSUMER_KEY
consumer_secret = config.CONSUMER_SECRET

def Find(string): 
  
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string) 
    return [x[0] for x in url]   
    if not url:
        return False    
    else:
        return True 

def user_tweets(token,token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token,token_secret)
    api = tweepy.API(auth)
    user_tweets = api.home_timeline(count=100)

    return user_tweets

url = 'https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2FInterior%2Fstatus%2F'
embed_tweets = []

def save_to_db(token,token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token,token_secret)
    api = tweepy.API(auth)
    original_tweets = user_tweets(token,token_secret)
    for original_tweet in original_tweets:

        links = original_tweet.entities['urls']        
        if links and (datetime.now() - original_tweet.created_at).days < 8:  
            if links[0]['display_url'][0:7] != 'twitter':   
                domainn = links[0]['display_url']
                info = tldextract.extract(domainn)
                link = info.domain
            elif len(links)>1:    
                domainn = links[1]['display_url']
                info = tldextract.extract(domainn)
                link = info.domain
            try:
                x = url+original_tweet.id_str 
                tmp = requests.get(url=x).json()
                embed_tweets.append(tmp['html'])
                new_tweet = Tweet(tweet_author=Author.objects.get(person=original_tweet.author.screen_name), tweet_id = original_tweet.id, tweet_links=link)
                new_tweet.save()
            except:
                continue       

    return embed_tweets         
              