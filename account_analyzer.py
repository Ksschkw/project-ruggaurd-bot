from datetime import datetime

def analyze_account(client, user_id):
    """Analyze the Twitter account of the given user ID using API v2."""
    user = client.get_user(id=user_id, user_fields=['created_at', 'public_metrics', 'description'], user_auth=True).data

    # Account age in days
    account_age = (datetime.now() - user.created_at).days

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