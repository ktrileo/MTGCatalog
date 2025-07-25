from flask import Flask, jsonify
import logging
from database import initialize_mongodb_connection, close_mongodb_connection # Import database functions
from routes import api_bp # Import the API blueprint
from config import FRONTEND_ORIGIN # Import the frontend origin for CORS
from flask_cors import CORS # Import CORS

# --- Flask Application Setup ---
app = Flask(__name__)

# --- Configure CORS ---
# This allows your frontend (FRONTEND_ORIGIN) to make requests to this Flask app.
# Adjust origins in config.py if your frontend is hosted elsewhere.
CORS(app, resources={r"/api/*": {"origins": FRONTEND_ORIGIN}})

# --- Configure Root Logging ---
# This sets up the basic logging for the entire application.
# Messages will be output to the console (stderr).
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
# Set Flask's default logger level
app.logger.setLevel(logging.INFO)

# --- Initialize MongoDB Connection at App Startup ---
# This ensures the database connection is ready before handling requests.
with app.app_context():
    initialize_mongodb_connection()

# --- Register Blueprints ---
# This connects the routes defined in routes.py to your Flask app.
app.register_blueprint(api_bp)

# --- Basic Health Check Endpoint ---
# This endpoint allows you to check if your service and its database connection are healthy.
@app.route('/health', methods=['GET'])
def health_check():
    """Provides a simple health check for the service."""
    try:
        from database import _mongo_client # Access the global client directly for health check
        if _mongo_client:
            _mongo_client.admin.command('ping') # Attempt a simple database operation
            app.logger.info("Health check: Database connection is healthy.")
            return jsonify({"status": "ok", "database_connection": "healthy"}), 200
        else:
            app.logger.warning("Health check: Database connection not established at service startup.")
            return jsonify({"status": "degraded", "database_connection": "not established"}), 500
    except Exception as e:
        app.logger.error(f"Health check: Database connection unhealthy. Details: {e}", exc_info=True)
        return jsonify({"status": "degraded", "database_connection": f"unhealthy: {e}"}), 500

# --- Run the Flask Application ---
if __name__ == '__main__':
    # When running locally for development, use Flask's built-in server.
    # For homelab deployment, you'd use a production-ready WSGI server like Gunicorn.
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Ensure MongoDB connection is closed when the app shuts down,
        # preventing resource leaks.
        close_mongodb_connection()