#!/bin/bash


E_NO_POSTGRES_USERNAME=60
E_NO_DATABASE_NAME=61
E_NO_CONTAINER_NAME=62

# Prompt the user for the Docker container name
read -p "Enter your PostgreSQL Docker container name: " CONTAINER_NAME

# Check if the user provided a container name
if [[ -z "$CONTAINER_NAME" ]]; then
  echo "You must provide a Docker container name."
  exit "$E_NO_CONTAINER_NAME"
fi

# Prompt the user for the PostgreSQL username
read -p "Enter your PostgreSQL username: " POSTGRES_USERNAME

# Check if the user provided a username
if [[ -z "$POSTGRES_USERNAME" ]]; then
  echo "You must provide a PostgreSQL username."
  exit "$E_NO_POSTGRES_USERNAME"
fi

# Prompt the user for the database name
read -p "Enter the name of the database to manage: " DATABASE_NAME

# Check if the user provided a database name
if [[ -z "$DATABASE_NAME" ]]; then
  echo "You must provide a database name."
  exit "$E_NO_DATABASE_NAME"
fi

# Drop the database if it exists
docker exec -it "$CONTAINER_NAME" dropdb --if-exists -U "$POSTGRES_USERNAME" "$DATABASE_NAME"

# Create the database with the provided username as the owner
docker exec -it "$CONTAINER_NAME" createdb -O "$POSTGRES_USERNAME" -U "$POSTGRES_USERNAME" "$DATABASE_NAME"
