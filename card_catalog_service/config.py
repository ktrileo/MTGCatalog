# MongoDB Connection Details
# These should match your local MongoDB setup
MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
DB_NAME = 'mtg_collection_db'
COLLECTION_NAME = 'cards'

# --- Optional: MongoDB Authentication (uncomment and fill if enabled) ---
# MONGO_USER = 'mtgAdmin'
# MONGO_PASS = 'your_secure_password' # Replace with the password you set for mtgAdmin
# MONGO_AUTH_SOURCE = 'admin' # Database where the user was created

# --- Scryfall API Configuration ---
# Base URL for Scryfall API
SCRYFALL_API_BASE_URL = "https://api.scryfall.com"
# Scryfall recommends a User-Agent. Replace with your app's name/version.
SCRYFALL_USER_AGENT = "MTGCardApp/1.0"
# Scryfall rate limit: 10 requests per second. We'll add a small delay.
SCRYFALL_REQUEST_DELAY_SECONDS = 0.11 # Slightly more than 0.1 to be safe (1/10 RPS = 0.1s per request)

# --- Frontend CORS Origin ---
# IMPORTANT: Replace 'http://localhost:8000' with the actual URL your frontend is served from.
# If you deploy your frontend to a different IP or domain, this MUST be updated.
FRONTEND_ORIGIN = 'http://localhost'