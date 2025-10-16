#!/usr/bin/env bash
set -euo pipefail

BUCKET=${BUCKET:-}
BACKUP_DIR=${BACKUP_DIR:-/opt/poudlard/backups}

if [ -z "$BUCKET" ]; then
  echo "BUCKET environment variable required"
  exit 2
fi

for f in "$BACKUP_DIR"/*.tar.gz; do
  if [ -f "$f" ]; then
    echo "Uploading $f to s3://$BUCKET/"
    aws s3 cp "$f" "s3://$BUCKET/"
  fi
done

echo "Upload complete"
