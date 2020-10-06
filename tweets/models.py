from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    person = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.person

class Tweet(models.Model):
    tweet_author = models.ForeignKey(Author,on_delete=models.CASCADE)
    tweet_id = models.CharField(max_length=250,null=True,blank=True)
    tweet_links = models.TextField(blank=True,null=True)
    # published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.tweet_links
