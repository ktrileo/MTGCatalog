Magic: The Gathering Card Collection App
This repository contains the full stack for a personal Magic: The Gathering (MTG) card collection application. It allows users to search for cards from a local database (populated from a ManaBox CSV) and retrieve associated images from the Scryfall API. The application is designed for a homelab environment and is fully containerized using Docker Compose.

Project Structure
mtg-app-project/
├── frontend/                     # Static HTML/CSS/JS frontend served by Nginx
├── card_catalog_service/         # Python Flask backend service
├── Dockerfile.backend            # Dockerfile for the Flask backend
├── Dockerfile.frontend           # Dockerfile for the Nginx frontend
├── requirements.txt              # Python dependencies for the backend
└── docker-compose.yml            # Docker Compose orchestration file


Services
MongoDB Database: Stores your MTG card collection data.

Card Catalog Service (Python/Flask): Backend API for searching cards in MongoDB and fetching image URLs from Scryfall.

Scryfall Image Service (Integrated in Backend): Handles external API calls to Scryfall, including rate limiting and in-memory caching for card images.

Frontend (HTML/CSS/JS/Nginx): User interface for searching and displaying card information and images.