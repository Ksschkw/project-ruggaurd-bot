import tweepy
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# Set up Twitter API v2 Client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Get user ID for a specific username (use this during setup to get dynamic IDs)
username = "_X1X0_"  # Example; replace with target username for deployment
try:
    user = client.get_user(username=username, user_auth=True).data
    print(f"User ID for @{username}: {user.id}")
except Exception as e:
    print(f"Error getting user ID: {e}")