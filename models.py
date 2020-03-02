from mongoengine import *
import datetime


class Tweet(Document):
    meta = {'strict': False}
    username = StringField(required=True)
    content = StringField(required=True)
    favorites = IntField(required=True)
    retweets = IntField(required=True)
    polarity = FloatField(required=True)
    neg = FloatField(required=True)
    neu = FloatField(required=True)
    pos = FloatField(required=True)
    normalizedSentiment = StringField(required=True)
    createdAt = DateTimeField(required=True)
    profileImage = StringField()
    name = StringField(required=True)
    tweetId = StringField(required=True)


class Sentiment(Document):
    meta = {'strict': False}
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    term = StringField(required=True)
    averagePolarity = FloatField(required=True)
    averageWeighedPolarity = FloatField(required=True)
    positiveTweetsCount = IntField(required=True)
    negativeTweetsCount = IntField(required=True)
    neutralTweetsCount = IntField(required=True)
    tweets = ListField(ReferenceField(Tweet))
