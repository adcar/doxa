from mongoengine import *
from models import Tweet, Sentiment
from sentiment import get_sentiment_results
connect(host="mongodb+srv://adcar:3yHbmDyKrKDiWVIK@cluster0-jxi9y.azure.mongodb.net/sentiment?retryWrites=true&w=majority")


def init_db():
    print("initializing database...")
    # # Create the fixtures
    # tweet1 = Tweet(username="adcar", content="Test....", favorites=5, polarity=0.03125, subjectivity=0.6875).save()
    # tweet2 = Tweet(username="adcar", content="Test....", favorites=5, polarity=0.03125, subjectivity=0.6875).save()
    # tweet3 = Tweet(username="adcar", content="Test....", favorites=5, polarity=0.03125, subjectivity=0.6875).save()
    # tweet4 = Tweet(username="adcar", content="Test....", favorites=5, polarity=0.03125, subjectivity=0.6875).save()
    # sentiment = Sentiment(
    #     term="Bruh",
    #     averagePolarity=0,
    #     averageWeighedPolarity=0,
    #     positiveTweetsCount=0,
    #     negativeTweetsCount=0,
    #     neutralTweetsCount=0,
    #
    #     positiveTweets=[tweet1, tweet2],
    #     negativeTweets=[tweet3],
    #     neutralTweets=[tweet4]
    # )
    # sentiment.save()

def add_sentiment(term):
    results = get_sentiment_results(term)
    positiveTweets = []
    negativeTweets = []
    neutralTweets = []
    for tweet in results['positiveTweets']:
        tweetInstance = Tweet(username=tweet['username'], content=tweet['text'], favorites=tweet['favorites'],
                              polarity=tweet['polarity'], subjectivity=tweet['subjectivity']).save()
        positiveTweets.append(tweetInstance)
    for tweet in results['negativeTweets']:
        tweetInstance = Tweet(username=tweet['username'], content=tweet['text'], favorites=tweet['favorites'],
                              polarity=tweet['polarity'], subjectivity=tweet['subjectivity']).save()
        negativeTweets.append(tweetInstance)
    for tweet in results['neutralTweets']:
        tweetInstance = Tweet(username=tweet['username'], content=tweet['text'], favorites=tweet['favorites'],
                              polarity=tweet['polarity'], subjectivity=tweet['subjectivity']).save()
        neutralTweets.append(tweetInstance)


    sentiment = Sentiment(
        term=term,
        averagePolarity=results['averagePolarity'],
        averageWeighedPolarity=results['averageWeighedPolarity'],
        positiveTweetsCount=results['positiveTweetsCount'],
        negativeTweetsCount=results['negativeTweetsCount'],
        neutralTweetsCount=results['neutralTweetsCount'],

        positiveTweets=positiveTweets,
        negativeTweets=negativeTweets,
        neutralTweets=neutralTweets
    )
    sentiment.save()

