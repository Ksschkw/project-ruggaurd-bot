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

# Load trusted account IDs once at startup
print("Loading trusted account IDs...")
trusted_ids = load_trusted_ids(client)
print(f"Loaded {len(trusted_ids)} trusted account IDs.")

# Main bot loop
while True:
    try:
        print("Checking for new trigger replies...")
        new_triggers = get_new_triggers(client)
        if not new_triggers:
            print("No new triggers found; consider adding a test trigger if needed.")
            # Uncomment below for simulation if live data fails due to rate limits
            # from types import SimpleNamespace
            # new_triggers = [SimpleNamespace(id='1932099395840770491', referenced_tweets=[{'type': 'replied_to', 'id': '1932099321706459511'}], author_id='1751013659415810048')]

        print(f"Found {len(new_triggers)} new trigger replies.")
        for trigger in new_triggers:
            print(f"Processing reply ID {trigger.id} from user ID {trigger.author_id}")
            original_tweet_id = next(
                (ref['id'] for ref in trigger.referenced_tweets or [] if ref['type'] == 'replied_to'),
                None
            )
            if original_tweet_id is None:
                print("No original tweet ID found, skipping...")
                continue

            print(f"Fetching original tweet (ID: {original_tweet_id})...")
            try:
                response = client.get_tweet(original_tweet_id, tweet_fields=['author_id'], user_auth=True)
                if response.data is None:
                    print("Tweet not found or access denied")
                    continue
                original_tweet = response.data
                author_id = original_tweet.author_id
            except Exception as e:
                print(f"Error fetching original tweet: {e}")
                continue
            if author_id is None:
                print("Author ID not available, skipping...")
                continue
            print(f"Original tweet by user ID {author_id}")

            print(f"Analyzing account for user ID {author_id}...")
            analysis = analyze_account(client, author_id)
            user = client.get_user(id=author_id, user_fields=['username'], user_auth=True).data
            analysis['screen_name'] = user.username if user else 'unknown'
            print(f"Analysis complete for @{analysis['screen_name']}.")

            print(f"Checking if @{analysis['screen_name']} is vouched by trusted accounts...")
            vouched = is_vouched(client, author_id, trusted_ids)
            print(f"Vouch status for @{analysis['screen_name']}: {'Vouched' if vouched else 'Not vouched'}")

            print(f"Generating report for @{analysis['screen_name']}...")
            report = generate_report(analysis, vouched)
            print(f"Posting report for @{analysis['screen_name']}...")
            client.create_tweet(text=report, in_reply_to_tweet_id=trigger.id)
            print(f"Successfully posted reply {trigger.id} for @{analysis['screen_name']}")

        print("Waiting 5 minutes before next check...")
        time.sleep(300)
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Waiting 10 minutes before retrying...")
        time.sleep(600)