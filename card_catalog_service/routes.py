from flask import Blueprint, request, jsonify
from database import get_cards_collection # Import the function to get the collection
import logging # Use standard logging here
from services.scryfall_api import get_card_image_url # Import the new function for images

# Create a Blueprint for your API routes
# Blueprints help organize routes into modular components
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Get a logger specific to this blueprint/module
routes_logger = logging.getLogger(__name__)
routes_logger.setLevel(logging.INFO)

@api_bp.route('/cards', methods=['GET'])
def search_cards():
    """
    Handles GET requests to search for Magic: The Gathering cards.
    Expects a 'query' parameter in the URL (e.g., /api/cards?query=lightning)
    """
    try:
        cards_collection = get_cards_collection() # Get the initialized collection
    except ConnectionError as ce:
        routes_logger.error(f"Search request failed: {ce}")
        return jsonify({"error": "Database connection not established."}), 500

    search_query = request.args.get('query', '').strip()

    if not search_query:
        routes_logger.warning("Search request received with no 'query' parameter.")
        return jsonify({"message": "Please provide a 'query' parameter."}), 400

    routes_logger.info(f"Received search query: '{search_query}'")

    try:
        # Use a case-insensitive regex search for card names
        # For more complex searches, you'd build a more sophisticated query
        query_filter = {"name": {"$regex": search_query, "$options": "i"}}
        
        # Find documents matching the query, limit to a reasonable number for display
        # In a real app, you'd implement pagination if dealing with many results
        found_cards = list(cards_collection.find(query_filter).limit(20))

        # MongoDB's ObjectId is not directly JSON serializable, so convert it to string
        # before sending the response.
        processed_cards = []
        for card in found_cards:
            card['_id'] = str(card['_id'])
            
            # Fetch image URL using the Scryfall Image Service 
            scryfall_id = card.get('scryfall_id')
            if scryfall_id:
                card['image_url'] = get_card_image_url(scryfall_id)
            else:
                routes_logger.warning(f"Card '{card.get('name')}' (ID: {card['_id']}) is missing 'scryfall_id'. Cannot fetch image.")
                card['image_url'] = None # Or a URL to a generic "image not available" placeholder

            processed_cards.append(card)

        if processed_cards:
            routes_logger.info(f"Found and processed {len(processed_cards)} cards for query '{search_query}'")
            return jsonify(processed_cards), 200
        else:
            routes_logger.info(f"No cards found for query '{search_query}'")
            return jsonify({"message": "No cards found matching your query."}), 404

    except Exception as e:
        routes_logger.error(f"Error during card search for query '{search_query}': {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred during search."}), 500