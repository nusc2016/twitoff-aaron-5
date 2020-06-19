# web_app/routes/stats_routes.py

from flask import Blueprint, request, render_template

from sklearn.linear_model import LogisticRegression

from web_app.models import User
from web_app.services.basilica_service import connection as basilica_api_client

stats_routes = Blueprint("stats_routes", __name__)


@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
    # get the tweets from the database:
    user_a = User.query.filter_by(screen_name=screen_name_a).first()
    user_b = User.query.filter_by(screen_name=screen_name_b).first()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    print("fetched tweets", len(user_a_tweets), len(user_b_tweets))

    print("-----------------")
    print("TRAINING THE MODEL...")

    # x values / inputs : embeddings
    # y values / labels : screen_names

    classifier = LogisticRegression()

    embeddings = []
    labels = []

    for tweet in user_a_tweets:
        embeddings.append(tweet.embedding)
        labels.append(screen_name_a)

    for tweet in user_b_tweets:
        embeddings.append(tweet.embedding)
        labels.append(screen_name_b)

    classifier.fit(embeddings, labels)

    print("-----------------")
    print("MAKING A PREDICTION...")

    embedding = basilica_api_client.embed_sentence(tweet_text, model="twitter")

    result = classifier.predict([embedding])

    return render_template("prediction_results.html",
                           screen_name_a=screen_name_a,
                           screen_name_b=screen_name_b,
                           tweet_text=tweet_text,
                           screen_name_most_likely=result[0])
