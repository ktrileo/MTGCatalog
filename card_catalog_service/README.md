MTG Card Catalog Service (Python Flask Backend)
This directory contains the Python Flask application that serves as the backend for the Magic: The Gathering Card Collection App. It handles API requests for card searches, interacts with the MongoDB database, and integrates with the Scryfall API to fetch card images.

Files
app.py: The main Flask application instance, responsible for setting up logging, initializing the database connection, registering blueprints, and running the Flask server.

config.py: Stores all configuration variables, including MongoDB connection details, Scryfall API settings, and CORS origins.

database.py: Manages the MongoDB client connection and provides functions to access the card collection.

routes.py: Defines the API endpoints for card search (/api/cards).

services/: A package containing specialized service modules.

services/scryfall_api.py: Handles all interactions with the external Scryfall API, including rate limiting and in-memory caching for image URLs.

requirements.txt: Lists all Python dependencies required for this service.

Functionality
Card Search API: Provides an endpoint (/api/cards) to search for MTG cards by name.

MongoDB Integration: Connects to and queries the MongoDB database to retrieve card data.

Scryfall Image Fetching: Calls the Scryfall API to get image URLs for found cards, applying rate limits and caching.

CORS Enabled: Configured to allow requests from the frontend application.

Logging: Comprehensive logging for monitoring and troubleshooting.