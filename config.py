import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Load Twitter API credentials from Replit secrets (environment variables)
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')