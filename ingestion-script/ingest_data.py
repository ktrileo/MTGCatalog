import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
import logging

# Setup a logger for this ingestion script
ingest_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
ingest_logger.setLevel(logging.INFO)

# --- 1. MongoDB Connection Details for HOST-BASED INGESTION ---
# IMPORTANT: When running this script directly on your host machine (not in Docker Compose),
# you must connect to MongoDB via 'localhost' and the exposed port.
# The 'mongodb' hostname is only resolvable within the Docker network.
MONGO_HOST_INGESTION = 'localhost'
MONGO_PORT_INGESTION = 27017
DB_NAME = 'mtg_collection_db'
COLLECTION_NAME = 'cards'

# --- 2. Path to Your Magic: The Gathering CSV File ---
# IMPORTANT: REPLACE THIS with the actual full path to your CSV file!
# Example: CSV_FILE_PATH = '/Users/yourusername/Documents/my_mtg_collection.csv'
CSV_FILE_PATH = 'ManaBox_Collection.csv'

def connect_to_mongodb_for_ingestion():
    """Connects to your local MongoDB server for data ingestion."""
    client = None
    cards_collection = None
    try:
        client = MongoClient(MONGO_HOST_INGESTION, MONGO_PORT_INGESTION, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DB_NAME]
        cards_collection = db[COLLECTION_NAME]
        ingest_logger.info(f"Connection successful to MongoDB database '{DB_NAME}' for ingestion!")
        return client, cards_collection
    except ConnectionFailure as cf:
        ingest_logger.error(f"ERROR: MongoDB Connection Failure during ingestion. "
                            f"Is the Dockerized MongoDB server running and port {MONGO_PORT_INGESTION} exposed on host? "
                            f"Check host/port '{MONGO_HOST_INGESTION}:{MONGO_PORT_INGESTION}'. Details: {cf}")
    except OperationFailure as of:
        ingest_logger.error(f"ERROR: MongoDB Operation Failure during ingestion (e.g., Authentication). "
                            f"Check username/password if authentication is enabled. Details: {of}")
    except Exception as e:
        ingest_logger.error(f"ERROR: An unexpected error occurred during MongoDB connection for ingestion. Details: {e}", exc_info=True)
    return None, None

def ingest_csv_data(cards_collection):
    """Reads CSV and loads card data into MongoDB."""
    if not os.path.exists(CSV_FILE_PATH):
        ingest_logger.error(f"ERROR: CSV file not found at '{CSV_FILE_PATH}'. Please update the path.")
        return

    ingest_logger.info(f"\n--- Starting CSV Data Ingestion from '{CSV_FILE_PATH}' ---")
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        ingest_logger.info(f"Successfully loaded {len(df)} rows from CSV.")

        if df.empty:
            ingest_logger.warning("CSV file loaded successfully, but it appears to be empty or contains no data rows.")
            return # Exit if DataFrame is empty

        documents_to_insert = []
        for index, row in df.iterrows():
            card_doc = {
                # Mapped all provided CSV keys to MongoDB document fields
                "binder_name": row.get('Binder Name', None),
                "binder_type": row.get('Binder Type', None),
                "name": row.get('Name', 'Unknown Card Name'), # This is the primary card name
                "set_code": row.get('Set code', None),
                "set_name": row.get('Set name', None),
                "collector_number": row.get('Collector number', None),
                "foil": row.get('Foil', None),
                "rarity": row.get('Rarity', None),
                "quantity": row.get('Quantity', None),
                "manabox_id": row.get('ManaBox ID', None),
                "scryfall_id": row.get('Scryfall ID', None),
                "purchase_price": row.get('Purchase price', None),
                "misprint": row.get('Misprint', None),
                "altered": row.get('Altered', None),
                "condition": row.get('Condition', None),
                "language": row.get('Language', None),
                "purchase_price_currency": row.get('Purchase price currency', None)
            }
            
            # Ensure at least 'name' is present, or add more robust validation
            if not card_doc["name"] or card_doc["name"] == 'Unknown Card Name':
                ingest_logger.warning(f"Skipping row {index} due to missing or unknown 'Name'. Row data: {row.to_dict()}")
                continue # Skip this row if card name is missing

            # Remove any fields that might be None to keep documents cleaner
            card_doc = {k: v for k, v in card_doc.items() if v is not None}
            documents_to_insert.append(card_doc)
        
        ingest_logger.info(f"Prepared {len(documents_to_insert)} documents for insertion after processing CSV rows.")

        if documents_to_insert:
            try:
                result = cards_collection.insert_many(documents_to_insert)
                ingest_logger.info(f"Successfully inserted {len(result.inserted_ids)} card documents into MongoDB. First 3 IDs: {result.inserted_ids[:3]}...")
            except OperationFailure as of:
                ingest_logger.error(f"ERROR: MongoDB Operation Failure during insert_many. Check database permissions or data integrity. Details: {of}", exc_info=True)
            except Exception as e:
                ingest_logger.error(f"ERROR: An unexpected error occurred during insert_many: {e}", exc_info=True)
        else:
            ingest_logger.info("No documents were prepared for insertion. Check your CSV and mapping logic.")

    except pd.errors.EmptyDataError:
        ingest_logger.error("ERROR: The CSV file is empty.")
    except pd.errors.ParserError as pe:
        ingest_logger.error(f"ERROR: Problem parsing CSV file: {pe}. Check CSV format (e.g., delimiters, quotes).")
    except Exception as e:
        ingest_logger.error(f"An unexpected error occurred during CSV ingestion: {e}", exc_info=True)

def verify_ingestion(cards_collection):
    """Checks if data was loaded correctly into MongoDB."""
    ingest_logger.info("\n--- Verifying Data in MongoDB ---")
    total_cards = cards_collection.count_documents({})
    ingest_logger.info(f"Total documents found in the '{COLLECTION_NAME}' collection: {total_cards}")

    if total_cards > 0:
        ingest_logger.info("\nDisplaying 3 sample cards from your collection:")
        for i, card in enumerate(cards_collection.find().limit(3)):
            ingest_logger.info(f"Sample {i+1}: {card}")
    else:
        ingest_logger.warning("No cards found in the collection. Ingestion might have failed.")

if __name__ == "__main__":
    ingest_logger.info("Starting ingestion script...")
    client, cards_collection = connect_to_mongodb_for_ingestion()
    if client is not None and cards_collection is not None:
        # Optional: Clear existing data before re-ingesting (useful for development)
        #ingest_logger.info("\nClearing existing data from 'cards' collection (Optional for testing)...")
        #cards_collection.delete_many({})
        #ingest_logger.info("Collection cleared.")

        ingest_csv_data(cards_collection)
        verify_ingestion(cards_collection)
        client.close()
        ingest_logger.info("MongoDB connection closed.")
    else:
        ingest_logger.error("Failed to establish MongoDB connection. Cannot proceed with ingestion.")