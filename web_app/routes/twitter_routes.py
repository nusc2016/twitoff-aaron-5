# web_app/routes/twitter_routes.py

from flask import Blueprint
from web_app.models import db, User, Tweet
from web_app.services.twitter_service import twitter_api
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)


@twitter_routes.route("/user_page")
def user_page():
    return "user page"


@twitter_routes.route("/users/<screen_name>")
def fetch_user(screen_name=None):
    print(screen_name)

    api = twitter_api()

    twitter_user = api.get_user(screen_name)

    # Get user from database if exists, if not initialaize new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)

    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count

    # store user in a database:
    db.session.add(db_user)
    db.session.commit()

    # Get tweets:
    basilica_api = basilica_api_client()
    tweets = api.user_timeline(screen_name, tweet_mode="extended", count=150)
    # exclude_replies=True, include_rts=False)

    all_tweet_texts = [status.full_text for status in tweets]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts,
                                                   model="twitter"))
    print("Number Of Embeddings", len(embeddings))

    for index, status in enumerate(tweets):
        print(index)
        print(status.full_text)
        print("----")

        embedding = embeddings[index]

        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)

        db_tweet.user_id = status.author.id  # or db_user.id
        db_tweet.full_text = status.full_text

        # embedding = embeddings[counter]
        print(len(embeddings))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        db.session.commit()

    return "OK"
