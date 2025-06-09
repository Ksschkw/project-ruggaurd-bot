# Project Ruggaurd Bot

A Twitter (X) bot that monitors replies for "@projectruggaurd riddle me this," analyzes the original tweet's author, and posts a trustworthiness report. Built for deployment on Replit.

## Setup and Installation

### Prerequisites
- A Twitter Developer account with API access (free tier is fine).
- A Replit account (free tier works).

### Steps
1. **Create a Replit Project**
   - Go to [Replit](https://replit.com/), sign in, and click "Create Replit."
   - Choose "Python" as the language and name it (e.g., `project-ruggaurd-bot`).

2. **Upload Files**
   - Copy all files from this repository into your Replit project:
     - `main.py`
     - `config.py`
     - `trigger_listener.py`
     - `account_analyzer.py`
     - `trusted_accounts.py`
     - `reply_system.py`
     - `requirements.txt`
     - `processed.txt` (can be empty initially)
   - You can drag-and-drop them into the Replit file explorer.

3. **Configure Twitter API Keys**
   - Get your API keys from [Twitter Developer Portal](https://developer.twitter.com/):
     - API Key
     - API Secret Key
     - Access Token
     - Access Token Secret
   - In Replit, go to the "Secrets" tab (lock icon on the left).
   - Add these as environment variables:
     - Key: `API_KEY`, Value: (your API Key)
     - Key: `API_SECRET_KEY`, Value: (your API Secret Key)
     - Key: `ACCESS_TOKEN`, Value: (your Access Token)
     - Key: `ACCESS_TOKEN_SECRET`, Value: (your Access Token Secret)

4. **Install Dependencies**
   - Replit will automatically install the libraries listed in `requirements.txt` (`tweepy` and `requests`) when you run the project.

## How to Run the Bot

1. Open `main.py` in the Replit editor.
2. Click the green "Run" button at the top.
3. The bot will start monitoring Twitter for replies containing "@projectruggaurd riddle me this."
   - It checks every 5 minutes and posts reports as replies.
   - If there’s an error (e.g., rate limit), it’ll wait longer and retry.

To stop the bot, click the red "Stop" button in Replit.

## Bot Architecture

The bot is designed with modularity and simplicity in mind:

- **`main.py`**: Runs the bot in a loop, coordinates all modules, and handles errors.
- **`config.py`**: Stores Twitter API credentials securely using environment variables.
- **`trigger_listener.py`**: Monitors replies for the trigger phrase and tracks processed replies.
- **`account_analyzer.py`**: Analyzes the original author’s account (age, followers, bio, engagement).
- **`trusted_accounts.py`**: Checks if the author is followed by 3+ trusted accounts from the [trust list](https://github.com/devsyrem/turst-list/blob/main/list).
- **`reply_system.py`**: Generates and posts the trustworthiness report.

## Dependencies
- `tweepy`: For interacting with the Twitter API.
- `requests`: For fetching the trusted accounts list from GitHub.

## Notes
- The bot uses the free Twitter API tier, so it respects rate limits (e.g., 15 follower ID requests per 15 minutes).
- Store this code in a public GitHub repository for submission.
- Test it with a friend’s Twitter account to trigger it (e.g., reply to their tweet with "@projectruggaurd riddle me this").
