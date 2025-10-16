#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME=${CONTAINER_NAME:-$(docker ps --filter "ancestor=cassandra:3.11" --format "{{.Names}}" | head -n1)}
SNAP_NAME=${SNAP_NAME:-snapshot-$(date -u +%Y%m%dT%H%M%SZ)}
BACKUP_DIR=${BACKUP_DIR:-/opt/poudlard/backups}

if [ -z "$CONTAINER_NAME" ]; then
  echo "No Cassandra container found (searched for image cassandra:3.11). Set CONTAINER_NAME env var to override."
  exit 2
fi

echo "Creating nodetool snapshot ($SNAP_NAME) inside container $CONTAINER_NAME"
docker exec "$CONTAINER_NAME" nodetool snapshot -t "$SNAP_NAME"

TMPDIR=$(mktemp -d)
echo "Copying snapshot data from container to temporary directory"
docker cp "$CONTAINER_NAME":/var/lib/cassandra/data "$TMPDIR/cassandra_data"

mkdir -p "$BACKUP_DIR"
ARCHIVE="$BACKUP_DIR/cassandra-container-$SNAP_NAME.tar.gz"
tar -czf "$ARCHIVE" -C "$TMPDIR" .
rm -rf "$TMPDIR"

echo "Container snapshot archived to $ARCHIVE"
