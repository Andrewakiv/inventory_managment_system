#!/bin/bash

set -e

DB_HOST=${DB_HOST:?Error: DB_HOST is not set}
DB_PORT=${DB_PORT:?Error: DB_PORT is not set}
DB_NAME=${DB_NAME:?Error: DB_NAME is not set}
DB_USER=${DB_USER:?Error: DB_USER is not set}
DB_PASSWORD=${DB_PASSWORD:?Error: DB_PASSWORD is not set}

export PGPASSWORD=$DB_PASSWORD

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for PostgreSQL to be ready at $DB_HOST:$DB_PORT..."
  sleep 2
done

echo "Connecting to $DB_HOST:$DB_PORT, database: $DB_NAME as $DB_USER"
psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" -f /sql/schema.sql

echo "Database initialized successfully."