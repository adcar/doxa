import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Tweet as TweetModel, Sentiment as SentimentModel
from database import add_sentiment
from datetime import datetime, timedelta


def get_recent_sentiment_in_db(term):
    for sentiment in SentimentModel.objects:
        createdAt = sentiment.createdAt + timedelta(minutes=15)
        present = datetime.utcnow()
        if sentiment.term == term and present < createdAt:
            return sentiment


class Sentiment(MongoengineObjectType):
    class Meta:
        model = SentimentModel
        interfaces = (Node,)


class Tweet(MongoengineObjectType):
    class Meta:
        model = TweetModel
        interfaces = (Node,)


# This should not be used very often.
class AddTerm(graphene.Mutation):
    class Arguments:
        term = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, term):
        ok = True
        add_sentiment(term)

        return AddTerm(ok=ok)


class MyMutations(graphene.ObjectType):
    add_term = AddTerm.Field()


class Query(graphene.ObjectType):
    node = Node.Field()
    all_sentiment = MongoengineConnectionField(Sentiment)
    sentiment = graphene.Field(Sentiment, term=graphene.String(required=True))

    def resolve_sentiment(parent, info, term):
        sentiment = get_recent_sentiment_in_db(term)
        if sentiment is None:  # No sentiment for this term found (or it was older than 15 minutes)
            add_sentiment(term)
            sentiment = get_recent_sentiment_in_db(term)
            return sentiment
        else:
            return sentiment


schema = graphene.Schema(query=Query, types=[Tweet, Sentiment], mutation=MyMutations)
