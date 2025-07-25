# MTG Card App: Project Overview

This repository hosts a personal Magic: The Gathering (MTG) card collection application. It allows users to search for cards from a local MongoDB database (populated from a ManaBox CSV) and retrieve associated images from the Scryfall API. The entire application stack is containerized using Docker Compose, making it ideal for self-hosting in a homelab environment.
Build as a proof concept, for future works in my homelab. Not intended for major functionalities.

## Project Structure


mtg-app-project/
├── frontend/                     # Static HTML/CSS/JS frontend (served by Nginx)
├── card_catalog_service/         # Python Flask backend API
├── Dockerfile.backend            # Dockerfile for the Flask backend
├── Dockerfile.frontend           # Dockerfile for the Nginx frontend
├── requirements.txt              # Python dependencies for the backend
├── mongodb_custom_image/         # Custom MongoDB image assets (includes pre-loaded data)
└── docker-compose.yml            # Docker Compose orchestration file


## Core Components

* **MongoDB Database:** Stores your MTG card collection. Initial data is pre-loaded into its custom Docker image.
* **Card Catalog Service (Python/Flask):** Provides a REST API for searching cards in MongoDB and fetching image URLs from Scryfall.
* **Frontend (HTML/CSS/JS/Nginx):** The user interface for searching and displaying card information.
* **Scryfall Integration:** Handles external API calls for card images with built-in rate limiting and caching.

## Getting Started (Docker Compose)

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS/Windows) or Docker Engine & Docker Compose (Linux) installed.

### Setup

1.  **Prepare Backend Requirements:**
    Navigate to `card_catalog_service/` and generate `requirements.txt`:

    ```bash
    cd card_catalog_service
    pip install gunicorn # Ensure gunicorn is included
    pip freeze > requirements.txt
    cd .. # Return to project root
    ```
    *(Note: If using a virtual environment, activate it before `pip install` and `pip freeze`.)*

2.  **Build and Run the Stack:**
    From the `mtg-app-project/` root directory, execute:

    ```bash
    docker compose up --build -d
    ```

    This command builds all necessary Docker images (including your custom MongoDB image with pre-loaded data) and starts all services in the background.

3.  **Access the Application:**
    Open your web browser and navigate to `http://localhost`.