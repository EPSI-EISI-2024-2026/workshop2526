#!/usr/bin/env bash
set -euo pipefail

SNAP_NAME=${SNAP_NAME:-snapshot-$(date -u +%Y%m%dT%H%M%SZ)}
BACKUP_DIR=${BACKUP_DIR:-/opt/poudlard/backups}
mkdir -p "$BACKUP_DIR"

echo "Running nodetool snapshot with name $SNAP_NAME"
nodetool snapshot -t "$SNAP_NAME"

echo "Archiving snapshot"
TMPDIR=$(mktemp -d)
cp -r /var/lib/cassandra/data/* "$TMPDIR/"
tar -czf "$BACKUP_DIR/cassandra-$SNAP_NAME.tar.gz" -C "$TMPDIR" .
rm -rf "$TMPDIR"

echo "Snapshot archived to $BACKUP_DIR/cassandra-$SNAP_NAME.tar.gz"
