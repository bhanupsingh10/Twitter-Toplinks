from django.shortcuts import render
from .models import Tweet,Author
from django.http import HttpResponseRedirect
from django.urls import reverse
import tweepy
from tweepy.auth import OAuthHandler
from django.db .models import Count
from . import twitter
from . import config
# Create your views here.


def home(request):
    return render(request,'home.html')

def dashboard(request):

    if 'access_token' not in request.session:
        return HttpResponseRedirect(reverse('tweets:login'))    

    auth = OAuthHandler(consumer_key, consumer_secret)
    access_token = request.session['access_token']
    access_token_secret = request.session['access_token_secret']

    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    request.session['user']=api.me().name
    username = Author.objects.filter(person=api.me().screen_name)

    print(username)
    if len(username)==0:
        author = Author(person=api.me().screen_name)
        author.save()
    user_friends = []
    for friend in api.friends(username):
        user_friends.append(friend.screen_name)   

    for x in user_friends:
        userr = Author.objects.filter(person=x)
        if len(userr)==0:
            author = Author(person=x)
            author.save()

    Tweet.objects.all().delete()
    embed_tweets = twitter.save_to_db(access_token,access_token_secret)

    query1 = Tweet.objects.values('tweet_links').annotate(domain_count=Count('tweet_links')).order_by('-domain_count')
    query2 = Tweet.objects.values('tweet_author__person').annotate(domain_count=Count('tweet_author__person')).order_by('-domain_count')

    most_links = []
    cnt1 = 0
    for link in query1:
        if cnt1==3:
            break
        cnt1+=1
        most_links.append(link)

    most_authors = []
    cnt2=0
    for name in query2:
        if cnt2==3:
            break
        cnt2+=1
        most_authors.append(name)

    return render(request, 'tweet_list.html', {'embed_tweets': embed_tweets,'most_links':most_links,'most_authors':most_authors})       

consumer_key = config.CONSUMER_KEY
consumer_secret = config.CONSUMER_SECRET

def auth(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret,'http://127.0.0.1:8000/callback')

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    response = HttpResponseRedirect(redirect_url)
    request.session['request_token']=auth.request_token

    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = request.session['request_token']
    request.session.delete('request_token')
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    request.session['access_token']=auth.access_token
    request.session['access_token_secret']=auth.access_token_secret

    return HttpResponseRedirect(reverse('tweets:dashboard'))
