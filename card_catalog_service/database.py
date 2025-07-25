from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import logging # Use standard logging here as this module doesn't depend on Flask's app.logger

# Import configuration from config.py
from config import MONGO_HOST, MONGO_PORT, DB_NAME, COLLECTION_NAME
# from config import MONGO_USER, MONGO_PASS, MONGO_AUTH_SOURCE # Uncomment if using authentication

# Setup a logger for this module
db_logger = logging.getLogger(__name__)
db_logger.setLevel(logging.INFO)

# Global variables to hold the MongoDB client and collection instance
_mongo_client = None
_cards_collection = None

def initialize_mongodb_connection():
    """
    Initializes the MongoDB client and collection.
    This function should be called once at application startup.
    """
    global _mongo_client, _cards_collection

    if _mongo_client is not None:
        db_logger.info("MongoDB client already initialized. Skipping re-initialization.")
        return

    try:
        # Connect to MongoDB
        # For local setup without authentication:
        _mongo_client = MongoClient(MONGO_HOST, MONGO_PORT, serverSelectionTimeoutMS=5000)

        # If you enabled authentication, use this instead:
        # _mongo_client = MongoClient(
        #     MONGO_HOST, MONGO_PORT,
        #     username=MONGO_USER,
        #     password=MONGO_PASS,
        #     authSource=MONGO_AUTH_SOURCE,
        #     serverSelectionTimeoutMS=5000
        # )

        # The ping command verifies that the connection is actually established
        _mongo_client.admin.command('ping')
        db = _mongo_client[DB_NAME]
        _cards_collection = db[COLLECTION_NAME]
        db_logger.info(f"Database: Successfully connected to MongoDB database '{DB_NAME}' and collection '{COLLECTION_NAME}'.")
    except ConnectionFailure as cf:
        db_logger.error(f"Database ERROR: MongoDB Connection Failure. "
                        f"Is the server running? Check host/port '{MONGO_HOST}:{MONGO_PORT}'. Details: {cf}")
        _mongo_client = None
        _cards_collection = None
    except OperationFailure as of:
        db_logger.error(f"Database ERROR: MongoDB Operation Failure (e.g., Authentication/Permissions). "
                        f"Check username/password if authentication is enabled. Details: {of}")
        _mongo_client = None
        _cards_collection = None
    except Exception as e:
        db_logger.error(f"Database ERROR: An unexpected error occurred during MongoDB initialization. Details: {e}", exc_info=True)
        _mongo_client = None
        _cards_collection = None

def get_cards_collection():
    """
    Returns the MongoDB cards collection instance.
    Raises an error if the connection has not been successfully initialized.
    """
    if _cards_collection is None:
        db_logger.error("Attempted to get cards_collection before MongoDB connection was established.")
        raise ConnectionError("MongoDB cards collection is not initialized. Database connection failed.")
    return _cards_collection

def close_mongodb_connection():
    """Closes the MongoDB client connection if it's open."""
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        db_logger.info("MongoDB connection closed.")