def generate_report(analysis, vouched):
    """Generate a trustworthiness report as a string."""
    report = f"Trustworthiness report for @{analysis['screen_name']}:\n"
    report += f"- Account age: {analysis['account_age']} days\n"
    report += f"- Followers: {analysis['followers']}, Following: {analysis['following']} (ratio: {analysis['ratio']:.2f})\n"
    report += f"- Bio length: {analysis['bio_length']} chars\n"
    report += f"- Avg likes: {analysis['avg_likes']:.1f}, Avg retweets: {analysis['avg_retweets']:.1f}\n"
    if vouched:
        report += "- Vouched by trusted network\n"
    report += "- Generated by @_kosisochuk kbv1.0"  # Unique signature
    return report.strip()

def post_reply(client, reply_to_id, report):
    """Post the report as a reply to the triggering comment using API v2.
    Requires 'Read and write and Direct messages' permissions."""
    client.create_tweet(text=report, in_reply_to_tweet_id=reply_to_id)