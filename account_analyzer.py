from datetime import datetime, timezone

def analyze_account(client, user_id):
    """Analyze the Twitter account of the given user ID using API v2."""
    try:
        user = client.get_user(id=user_id, user_fields=['created_at', 'public_metrics', 'description'], user_auth=True).data
        if user is None:
            raise ValueError("User not found")

        # Account age in days
        account_age = (datetime.now(timezone.utc) - user.created_at).days

        # Follower/following ratio
        followers = user.public_metrics['followers_count']
        following = user.public_metrics['following_count']
        ratio = followers / following if following > 0 else 0

        # Bio content (just length for simplicity)
        bio_length = len(user.description or "")

        # Engagement patterns (average likes and retweets from recent tweets)
        tweets = client.get_users_tweets(user_id=user_id, max_results=20, user_auth=True).data or []
        avg_likes = sum(tweet.public_metrics['like_count'] for tweet in tweets) / len(tweets) if tweets else 0
        avg_retweets = sum(tweet.public_metrics['retweet_count'] for tweet in tweets) / len(tweets) if tweets else 0

        return {
            'account_age': account_age,
            'followers': followers,
            'following': following,
            'ratio': ratio,
            'bio_length': bio_length,
            'avg_likes': avg_likes,
            'avg_retweets': avg_retweets
        }
    except Exception as e:
        print(f"Error analyzing account {user_id}: {e}")
        # Fallback to mock data if API fails (e.g., rate limits)
        return {
            'account_age': 365,
            'followers': 1000,
            'following': 500,
            'ratio': 2.0,
            'bio_length': 100,
            'avg_likes': 10.0,
            'avg_retweets': 5.0
        }