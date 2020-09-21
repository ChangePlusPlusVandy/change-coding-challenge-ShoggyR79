import config
import tweepy
import re
import random
import time
# Can Change, default value to 100 for purpose of
num_fetched_tweets = 100

first_tweets = []
second_tweets = []

# standard tweepy-twitter api setup procedure
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)

api = tweepy.API(auth)
# Start of Game
print("Welcome to Guess the Tweet 2.0 ")

# prompts user to send in ids
print("This program requires Twitter ID of two person.\nYou can use tweeterid.com to find the ID based on username")
first_id = input("Please enter the ID for the first person:    ")
second_id = input("Please enter the ID for the second person:    ")

# gets the name of the two users
first_name = (api.get_user(first_id)).name
second_name = (api.get_user(second_id)).name

print("Please wait will we gather tweets of " + first_name + " and " + second_name)

# gets x amount of tweets from "user_id"

# First Person
for status in tweepy.Cursor(api.user_timeline,
                            user_id=first_id,
                            tweet_mode="extended",
                            include_rts=False,
                            exclude_replies=True
                            ).items(num_fetched_tweets):

    # deletes urls from tweet
    filtered_tweet = re.sub(r"http\S+", "", status.full_text)

    # if tweet still contains stuff after URL is deleted, it is added to stash
    if filtered_tweet:
        first_tweets.append(status)

# Second Person
for status in tweepy.Cursor(api.user_timeline,
                            user_id=second_id,
                            tweet_mode="extended",
                            include_rts=False,
                            exclude_replies=True
                            ).items(num_fetched_tweets):
    # deletes urls from tweet
    filtered_tweet = re.sub(r"http\S+", "", status.full_text)

    # if tweet still contains stuff after URL is deleted, it is added to stash
    if filtered_tweet:
        second_tweets.append(status)

# adds the list of tweets into a list of tweets
tweet_inventory = [first_tweets, second_tweets]


# Using delay to simulate a better game experience
num_of_questions = int(input("How Many Tweets will you be guessing?"))
time.sleep(1)

print("Lets Start!")
time.sleep(2)
print("\n" * 3)

question_asked = 0
correct = 0
score = 0

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

    # Prints that tweet.
    print(filtered_tweet + "\ntweeted at " + str(chosen_tweet.created_at))

    print(" Who wrote this tweet? \n1. "+ first_name + "\n2. "+ second_name)
    player_answer = int(input("     Input your answer:"))

    # Compare player answer with correct answer
    if (player_answer - 1) == correct_answer:
        correct += 1
        print("Correct!")
    else:
        print("Wrong, try harder next time~")
    print("\n" * 5)
    time.sleep(1)
    question_asked += 1

print("Calculating score, please wait a few milliseconds!")
print("\n" * 3)
time.sleep(.5)
score = str(correct) + "/" + str(num_of_questions)

print("Your final score is: " + score)
print("\n" * 3)

time.sleep(2)
print("Have a great day!")