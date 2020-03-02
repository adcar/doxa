import re
from twitter import *
from enum import Enum
import nltk
import time
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer

t = Twitter(
    auth=OAuth(os.environ.get('TWITTER_TOKEN'), os.environ.get('TWITTER_TOKEN_SECRET'),
               os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_SECRET')))


def get_sentiment_results(term):
    sid = SentimentIntensityAnalyzer()
    if re.search("^[\w\s!#$']+$", term):
        statuses = \
            t.search.tweets(q='"' + term + '"', lang="en", count=100, tweet_mode="extended", result_type="mixed")[
                "statuses"]
        totalPolarity = 0
        totalWeighedPolarity = 0
        totalFavorites = 0
        tweets = []
        positiveTweetsCount = 0
        negativeTweetsCount = 0
        neutralTweetsCount = 0

        # Increment tweets
        for status in statuses:

            if "retweeted_status" in status:
                full_text = status["retweeted_status"]["full_text"]
            else:
                full_text = status["full_text"]

            scores = sid.polarity_scores(full_text)

            favorites = status["favorite_count"]
            retweets = status["retweet_count"]
            totalFavorites += favorites
            polarity = scores['compound']

            createdAt = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))

            weighedPolarity = 0
            if favorites != 0:
                weighedPolarity = polarity * favorites

            tweet = {"username": status["user"]["screen_name"],
                     "text": full_text,
                     "favorites": favorites, "retweets": retweets, "polarity": polarity, "normalizedSentiment": "",
                     "createdAt": createdAt,
                     "profileImage": status["user"]["profile_image_url_https"],
                     "name": status["user"]["name"],
                     "tweetId": status["id_str"],
                     "neg": scores["neg"],
                     "neu": scores["neu"],
                     "pos": scores["pos"],
                     }

            if -0.05 < polarity < 0.05:
                neutralTweetsCount += 1
                tweet["normalizedSentiment"] = "neutral"
            elif polarity >= 0.05:
                positiveTweetsCount += 1
                tweet["normalizedSentiment"] = "positive"
            elif polarity <= 0.05:
                negativeTweetsCount += 1
                tweet["normalizedSentiment"] = "negative"
            tweets.append(tweet)
            totalPolarity += polarity
            totalWeighedPolarity += weighedPolarity

        averagePolarity = totalPolarity / 100
        if totalFavorites != 0:
            averageWeighedPolarity = totalWeighedPolarity / totalFavorites
        else:
            averageWeighedPolarity = 0

        return {"averagePolarity": averagePolarity,
                "averageWeighedPolarity": averageWeighedPolarity,
                "positiveTweetsCount": positiveTweetsCount,
                "negativeTweetsCount": negativeTweetsCount,
                "neutralTweetsCount": neutralTweetsCount,
                "tweets": tweets}
    else:
        raise Exception("Invalid term")
