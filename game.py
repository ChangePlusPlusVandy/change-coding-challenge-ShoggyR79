import config
import tweepy
import re
import random

# Can Change, default value to 100 for purpose of
num_fetched_tweets = 100

kanye_id = 169686021
elon_id = 44196397


kanye_tweets = []
elon_tweets = []

# standard tweepy-twitter api setup procedure
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)

api = tweepy.API(auth)

# gets x amount of tweets from "user_id"

# Kanye West
for status in tweepy.Cursor(api.user_timeline,
                            user_id=kanye_id,
                            tweet_mode="extended",
                            include_rts=False,
                            exclude_replies=True
                            ).items(num_fetched_tweets):

    # deletes urls from tweet
    filtered_tweet = re.sub(r"http\S+", "", status.full_text)

    # if tweet still contains stuff after URL is deleted, it is added to stash
    if filtered_tweet:
        kanye_tweets.append(status)

# Elon Musk
for status in tweepy.Cursor(api.user_timeline,
                            user_id=elon_id,
                            tweet_mode="extended",
                            include_rts=False,
                            exclude_replies=True
                            ).items(num_fetched_tweets):
    # deletes urls from tweet
    filtered_tweet = re.sub(r"http\S+", "", status.full_text)

    # if tweet still contains stuff after URL is deleted, it is added to stash
    if filtered_tweet:
        elon_tweets.append(status)

# adds the list of tweets into a list of tweets
tweet_inventory = [kanye_tweets, elon_tweets]



# Start of Game
print("Welcome to Guess the Tweet (ft. @kanyewest and @elonmusk) ")
num_of_questions = int(input("How Many Tweets will you be guessing?"))

question_asked = 0
correct = 0

# Asking of questions
while question_asked < num_of_questions:
    # generate a correct answer
    correct_answer = random.randint(0, 1)
    # picks a random tweets from that person
    chosen_tweet = random.choice(tweet_inventory[correct_answer])
    # deletes that tweet from the tweet inventory (so no tweet can be picked twice)
    tweet_inventory[correct_answer].remove(chosen_tweet)

    # filters out the url again (the filtering done above only serve as a checking mechanism)

    filtered_tweet = re.sub(r"http\S+", "", chosen_tweet.full_text)
