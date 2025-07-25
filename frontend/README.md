MTG Card Search Frontend
This directory contains the static web files for the Magic: The Gathering Card Collection Application's user interface. It's built with plain HTML, CSS (via Tailwind CSS CDN), and JavaScript to interact with the backend Card Catalog Service.

Files
index.html: The main HTML file containing the structure, content, and JavaScript logic for the search interface.

nginx.conf: Nginx configuration file used by the Docker container to serve these static files.

Functionality
Provides a search bar for users to enter card names.

Displays search results, including card names, basic details, and images fetched from the backend.

Handles basic loading indicators and error messages.