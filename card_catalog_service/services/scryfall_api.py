import requests
import time
import logging
from functools import lru_cache # For a simple in-memory cache
from config import SCRYFALL_API_BASE_URL, SCRYFALL_USER_AGENT, SCRYFALL_REQUEST_DELAY_SECONDS

# Setup a logger for this module
scryfall_logger = logging.getLogger(__name__)
scryfall_logger.setLevel(logging.INFO)

# A simple in-memory cache for image URLs.
# maxsize=1024 means it will store up to 1024 unique image URLs.
# If more are requested, the least recently used ones will be removed.
@lru_cache(maxsize=1024)
def _get_image_url_from_scryfall_api(scryfall_id: str) -> str | None:
    """
    Internal function to fetch an image URL directly from the Scryfall API.
    This function is rate-limited and cached.
    """
    # Implement rate limiting before making the request
    time.sleep(SCRYFALL_REQUEST_DELAY_SECONDS)
    
    url = f"{SCRYFALL_API_BASE_URL}/cards/{scryfall_id}"
    headers = {
        "User-Agent": SCRYFALL_USER_AGENT,
        "Accept": "application/json"
    }

    try:
        scryfall_logger.info(f"Fetching image URL for Scryfall ID: {scryfall_id} from external API.")
        response = requests.get(url, headers=headers, timeout=5) # Add a timeout for external requests
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Scryfall provides different image URIs. 'normal' is usually a good default.
        # Check Scryfall API docs for other options like 'large', 'art_crop', 'png'.
        image_url = data.get('image_uris', {}).get('normal')
        
        if image_url:
            scryfall_logger.info(f"Successfully retrieved image URL for {scryfall_id}.")
            return image_url
        else:
            scryfall_logger.warning(f"No 'normal' image_uri found for Scryfall ID: {scryfall_id}. Full response: {data}")
            return None

    except requests.exceptions.HTTPError as http_err:
        scryfall_logger.error(f"HTTP error fetching image for {scryfall_id}: {http_err}. Status: {http_err.response.status_code}")
        if http_err.response.status_code == 404:
            scryfall_logger.warning(f"Card with Scryfall ID {scryfall_id} not found on Scryfall API (404).")
        elif http_err.response.status_code == 429:
            scryfall_logger.error(f"Scryfall API rate limit hit for {scryfall_id}. Consider increasing delay or implementing exponential backoff.")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        scryfall_logger.error(f"Connection error fetching image for {scryfall_id}: {conn_err}. Is Scryfall API reachable?")
        return None
    except requests.exceptions.Timeout as timeout_err:
        scryfall_logger.error(f"Timeout error fetching image for {scryfall_id}: {timeout_err}. Scryfall API took too long to respond.")
        return None
    except requests.exceptions.RequestException as req_err:
        scryfall_logger.error(f"An unexpected request error occurred fetching image for {scryfall_id}: {req_err}", exc_info=True)
        return None
    except Exception as e:
        scryfall_logger.error(f"An unexpected error occurred processing Scryfall response for {scryfall_id}: {e}", exc_info=True)
        return None

def get_card_image_url(scryfall_id: str) -> str | None:
    """
    Public function to get a card's image URL.
    Uses an internal cache and fetches from Scryfall API if not cached.
    """
    if not scryfall_id:
        scryfall_logger.warning("Received empty Scryfall ID for image lookup.")
        return None # Or a URL to a generic placeholder image

    # Try to get from cache first (lru_cache handles this automatically for _get_image_url_from_scryfall_api)
    image_url = _get_image_url_from_scryfall_api(scryfall_id)
    
    if image_url:
        scryfall_logger.debug(f"Returning image URL for {scryfall_id}.")
        return image_url
    else:
        scryfall_logger.warning(f"Could not retrieve image URL for Scryfall ID: {scryfall_id}. Returning None.")
        return None # Or a URL to a generic "image not available" placeholder