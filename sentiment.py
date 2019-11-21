from textblob import TextBlob
import re
from twitter import *

t = Twitter(
    auth=OAuth("748419493425197056-JvgR5mGNWfJQgmPblTQvW9MDC1WpH02", "BrYphqpOETnUye01JBznHOiWaLM6e762RIDETcm36kpoM",
               "kXjaifOSjWbmzafTmcEh3qmxc", "gzXFVm8w8MJ7lxLlQDLaJKtch1Qw7aZuBYKfkUszUmZGl7FXOz"))


def get_sentiment_results(term):
    if re.search("^[\w\s!#$]+$", term):
        statuses = t.search.tweets(q=term, count=100, tweet_mode="extended", result_type="mixed")["statuses"]
        totalPolarity = 0
        totalWeighedPolarity = 0
        totalFavorites = 0
        positiveTweets = []
        negativeTweets = []
        neutralTweets = []
        positiveTweetsCount = 0
        negativeTweetsCount = 0
        neutralTweetsCount = 0

        # Increment tweets
        for status in statuses:
            blob = TextBlob(status["full_text"])

            favorites = status["favorite_count"]
            totalFavorites += favorites
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            weighedPolarity = 0
            if favorites != 0:
                weighedPolarity = polarity * favorites

            tweet = {"username": status["user"]["screen_name"],
                     "text": status["full_text"],
                     "favorites": favorites, "polarity": polarity,
                     "subjectivity": subjectivity}
            if polarity < 0:
                negativeTweetsCount += 1
                negativeTweets.append(tweet)
            elif polarity == 0:
                neutralTweetsCount += 1
                neutralTweets.append(tweet)
            elif polarity > 0:
                positiveTweetsCount += 1
                positiveTweets.append(tweet)

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
                           "positiveTweets": positiveTweets,
                           "negativeTweets": negativeTweets,
                           "neutralTweets": neutralTweets}
    else:
        raise Exception("Invalid term")
