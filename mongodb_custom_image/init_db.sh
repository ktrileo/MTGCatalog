#!/bin/bash
# init_db.sh

echo "--- Running MongoDB initialization script ---"

# Wait for MongoDB to be ready
# The official MongoDB entrypoint already handles waiting for the server,
# but a small sleep here can't hurt for robustness if mongorestore starts too early.
sleep 5

# Restore the database from the dump
# The dump will be located at /docker-entrypoint-initdb.d/dump/mtg_collection_db/ inside the container
mongorestore --drop --db mtg_collection_db /docker-entrypoint-initdb.d/dump/mtg_collection_db/

echo "--- MongoDB initialization script finished ---"