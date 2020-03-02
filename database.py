from mongoengine import *
from models import Tweet, Sentiment
from sentiment import get_sentiment_results
import os

connect(
    host=os.environ.get('MONGODB_URL'))


def add_sentiment(term):
    results = get_sentiment_results(term)
    tweets = []
    for tweet in results['tweets']:
        tweetInstance = Tweet(username=tweet['username'], content=tweet['text'], favorites=tweet['favorites'],
                              retweets=tweet['retweets'],
                              polarity=tweet['polarity'], normalizedSentiment=tweet['normalizedSentiment'],
                              createdAt=tweet["createdAt"],
                              profileImage=tweet["profileImage"],
                              tweetId=tweet["tweetId"],
                              name=tweet["name"],
                              neg=tweet['neg'], neu=
                              tweet['neu'], pos=tweet['pos']).save()
        tweets.append(tweetInstance)

    sentiment = Sentiment(
        term=term,
        averagePolarity=results['averagePolarity'],
        averageWeighedPolarity=results['averageWeighedPolarity'],
        positiveTweetsCount=results['positiveTweetsCount'],
        negativeTweetsCount=results['negativeTweetsCount'],
        neutralTweetsCount=results['neutralTweetsCount'],
        tweets=tweets
    )
    sentiment.save()
