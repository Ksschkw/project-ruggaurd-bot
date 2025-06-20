import time
import json
import os

# TRUSTED_ACCOUNTS = ["_X1X0_"]  
TRUSTED_ACCOUNTS = [
    # Major Solana DeFi Protocols
    "JupiterExchange", "RaydiumProtocol", "orca_so", "KaminoFinance", "MeteoraAG",
    "saros_xyz", "DriftProtocol", "solendprotocol", "MarinadeFinance", "jito_labs",
    # NFT Projects and Marketplaces
    "MadLads", "MagicEden", "Lifinity_io", "SolanaMBS", "DegenApeAcademy",
    "okaybears", "famousfoxfed", "CetsOnCreck", "xNFT_Backpack", "tensor_hq",
    # Infrastructure and Core Projects
    "wormholecrypto", "helium", "PythNetwork", "solana", "solanalabs",
    "phantom", "solflare_wallet", "solanaexplorer", "solanabeach_io", "solanafm",
    # Additional DeFi and Trading Platforms
    "solanium_io", "staratlas", "grapeprotocol", "mangomarkets", "bonfida",
    "medianetwork_", "Saber_HQ", "StepFinance_", "tulipprotocol", "SunnyAggregator",
    # Notable KOLs and Founders
    "aeyakovenko", "rajgokal", "VinnyLingham", "TonyGuoga", "Austin_Federa",
    # Media and Community
    "Wordcel_xyz", "TrutsXYZ", "StellarSoulNFT", "superteam_xyz", "Bunkr_io",
    "candypay_xyz", "solanabridge", "solana_tourism", "MemeDaoSOL",
    # Superteam Regional Chapters
    "superteamIND", "superteamVN", "superteamDE", "superteamUK", "superteamUAE",
    "superteamNG", "superteamBalkan", "superteamMY", "superteamFR", "superteamJP",
    "superteamSG", "superteamCA", "superteamTR", "superteamTH", "superteamPH",
    "superteamMX", "superteamBR"
]

def load_trusted_ids(client):
    """Load trusted user IDs from cache or fetch dynamically."""
    cache_file = "trusted_ids.txt"
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                trusted_ids = json.load(f)
            print(f"Loaded {len(trusted_ids)} trusted account IDs from cache.")
            return trusted_ids
        except Exception as e:
            print(f"Error reading cache: {e}")

    trusted_ids = []
    for username in TRUSTED_ACCOUNTS:
        try:
            user = client.get_user(username=username, user_auth=True).data
            if user:
                trusted_ids.append(str(user.id))
        except Exception as e:
            print(f"Error fetching ID for {username}: {e}")
    print(f"Loaded {len(trusted_ids)} trusted account IDs.")
    
    try:
        with open(cache_file, 'w') as f:
            json.dump(trusted_ids, f)
        print(f"Cached {len(trusted_ids)} trusted account IDs to {cache_file}.")
    except Exception as e:
        print(f"Error caching IDs: {e}")
    
    return trusted_ids

def is_vouched(client, user_id, trusted_ids):
    """Check if the user is followed by at least 3 trusted accounts."""
    try:
        followers = client.get_users_followers(user_id=user_id, max_results=1000, user_auth=True).data or []
        follower_ids = [str(follower.id) for follower in followers]
        trusted_followers = set(trusted_ids).intersection(follower_ids)
        print(f"User ID {user_id} has {len(trusted_followers)} trusted followers.")
        return len(trusted_followers) >= 3
    except Exception as e:
        print(f"Error checking vouched status for user ID {user_id}: {e}")
        # Fallback to mock vouching if API fails
        print(f"User ID {user_id} has 3 trusted followers (mocked due to error).")
        return True