def get_new_triggers(client):
    """Search for new replies containing the trigger phrase using API v2.
    Note: Set to '@_Kosisochuk' for testing; update to '@projectruggaurd' for deployment."""
    query = "@_Kosisochuk riddle me this is:reply"  # Update to "@projectruggaurd riddle me this is:reply" for final use
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=100,
            tweet_fields=['referenced_tweets', 'author_id'],
            user_auth=True
        ).data or []
        print(f"API v2 search returned {len(tweets)} tweets.")
    except Exception as e:
        print(f"Error in search_recent_tweets: {e}")
        return []

    try:
        with open('processed.txt', 'r') as f:
            processed_ids = set(f.read().splitlines())
    except FileNotFoundError:
        processed_ids = set()

    new_triggers = []
    for tweet in tweets:
        if str(tweet.id) not in processed_ids:
            new_triggers.append(tweet)
            with open('processed.txt', 'a') as f:
                f.write(str(tweet.id) + '\n')

    return new_triggers