#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR=${BACKUP_DIR:-./backups}
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)

echo "Backing up Docker volumes to $BACKUP_DIR"
# Example: tar important volumes (paths are examples and may require root)
VOLUMES=( "./data/glpi_db" "./data/es" "./data/cassandra" )
for v in "${VOLUMES[@]}"; do
  if [ -d "$v" ]; then
    tar -czf "$BACKUP_DIR/$(basename $v)-$TIMESTAMP.tar.gz" -C "$(dirname $v)" "$(basename $v)"
  else
    echo "Volume path $v not found, skipping"
  fi
done

echo "Backup complete: $BACKUP_DIR"
