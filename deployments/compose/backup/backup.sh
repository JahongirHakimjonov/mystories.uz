#!/bin/bash

# Configuration variables
DB_CONTAINER="mystories-backend-db-1"
DB_USER="postgres"
DB_NAME="mystories"
BACKUP_DIR="/home/projects/backups"
BACKUP_FILE="$BACKUP_DIR/$(date +\%Y-\%m-\%d--%H-%M-%S)_$DB_NAME.sql"
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "Telegram configuration is missing" >&2
    exit 1
fi

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Dump the database
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup successfully created at $BACKUP_FILE"
else
    echo "Backup failed" >&2
    exit 1
fi

# Send the backup file to Telegram
curl -F document=@"$BACKUP_FILE" "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendDocument" -F chat_id="$TELEGRAM_CHAT_ID" -F caption="Daily Backup: $(date +\%Y-\%m-\%d--%H-%M-%S)"

# Cleanup old backups - Delete files older than 7 days
find "$BACKUP_DIR" -type f -name "*.sql" -mtime +7 -exec rm {} \;

echo "Old backups older than 7 days have been deleted."