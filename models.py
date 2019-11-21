from mongoengine import *
import datetime

class Tweet(Document):
    username = StringField(required=True)
    content = StringField(required=True)
    favorites = IntField(required=True)
    polarity = FloatField(required=True)
    subjectivity = FloatField(required=True)

class Sentiment(Document):
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    term = StringField(required=True)
    averagePolarity = FloatField(required=True)
    averageWeighedPolarity = FloatField(required=True)
    positiveTweetsCount = IntField(required=True)
    negativeTweetsCount = IntField(required=True)
    neutralTweetsCount = IntField(required=True)
    positiveTweets = ListField(ReferenceField(Tweet), required=True)
    negativeTweets = ListField(ReferenceField(Tweet), required=True)
    neutralTweets = ListField(ReferenceField(Tweet), required=True)
