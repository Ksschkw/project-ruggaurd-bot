import time
import tweepy
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from trigger_listener import get_new_triggers
from account_analyzer import analyze_account
from trusted_accounts import load_trusted_ids, is_vouched
from reply_system import generate_report, post_reply

# Set up Twitter API v2 Client
print("Setting up Twitter API v2 authentication...")
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
print("API v2 authentication successful.")

# Load trusted account IDs once at startup (cached for efficiency)
print("Loading trusted account IDs...")
trusted_ids = load_trusted_ids(client)
print(f"Loaded {len(trusted_ids)} trusted account IDs.")

# Simulate a trigger tweet for testing (replace with real IDs)
class MockTweet:
    def __init__(self):
        self.id = 1932088985033019583  #  real reply tweet ID
        self.in_reply_to_status_id = 1932088127880847735  #  real original tweet ID
        self.author_id = 1751013659415810048  # user ID

# Main bot loop
while True:
    try:
        # Check for new replies with the trigger phrase
        print("Checking for new trigger replies...")
        new_triggers = get_new_triggers(client)
        if not new_triggers:
            print("No new triggers found, simulating a test trigger...")
            new_triggers = [MockTweet()]  # Simulate a trigger for testing

        print(f"Found {len(new_triggers)} new trigger replies.")
        for trigger in new_triggers:
            # Get the original tweet and its author
            print(f"Processing reply ID {trigger.id} from user ID {trigger.author_id}")
            print(f"Fetching original tweet (ID: {trigger.in_reply_to_status_id})...")
            try:
                original_tweet = client.get_tweet(trigger.in_reply_to_status_id, user_auth=True).data
                author_id = original_tweet.author_id
                print(f"Original tweet by user ID {author_id}")
            except Exception as e:
                print(f"Error fetching original tweet: {e}")
                continue  # Skip if tweet fetch fails

            # Analyze the original author’s account
            print(f"Analyzing account for user ID {author_id}...")
            analysis = analyze_account(client, author_id)
            user = client.get_user(id=author_id, user_auth=True).data
            analysis['screen_name'] = user.username
            print(f"Analysis complete for @{analysis['screen_name']}.")

            # Check if the author is vouched by trusted accounts
            print(f"Checking if @{analysis['screen_name']} is vouched by trusted accounts...")
            vouched = is_vouched(client, author_id, trusted_ids)
            print(f"Vouch status for @{analysis['screen_name']}: {'Vouched' if vouched else 'Not vouched'}")

            # Generate and post the report
            print(f"Generating report for @{analysis['screen_name']}...")
            report = generate_report(analysis, vouched)
            print(f"Posting report for @{analysis['screen_name']}...")
            client.create_tweet(text=report, in_reply_to_tweet_id=trigger.id)
            print(f"Successfully posted reply {trigger.id} for @{analysis['screen_name']}")

        # Wait 5 minutes before checking again (respects API limits)
        print("Waiting 5 minutes before next check...")
        time.sleep(300)
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Waiting 10 minutes before retrying...")
        time.sleep(600)  # Wait longer if there’s an error