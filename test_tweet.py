# test_tweet.py
import tweepy
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

try:
    client.create_tweet(text="Test tweet from RUGGUARD bot")
    print("Tweet posted successfully!")
except Exception as e:
    print(f"Error: {e}")