# Dockerfile for custom MongoDB image with pre-loaded data

# Use the official MongoDB image as base
FROM mongo:8.0

# Set the working directory to the MongoDB entrypoint init directory
# This is where MongoDB's entrypoint script looks for initialization scripts
WORKDIR /docker-entrypoint-initdb.d/

# Copy the data dump into the image
# The 'dump' directory on the host will be copied to '/docker-entrypoint-initdb.d/dump' inside the image
COPY dump/ ./dump/

# Copy the initialization script into the image
# This script will be executed by the MongoDB entrypoint when the container first starts
COPY init_db.sh .

# No CMD or ENTRYPOINT needed here, as the base 'mongo' image already has a robust entrypoint
# that will automatically execute .sh files in /docker-entrypoint-initdb.d/