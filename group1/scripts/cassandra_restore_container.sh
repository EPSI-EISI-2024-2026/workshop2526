#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME=${CONTAINER_NAME:-$(docker ps --filter "ancestor=cassandra:3.11" --format "{{.Names}}" | head -n1)}
TARBALL=${1:-}

if [ -z "$TARBALL" ]; then
  echo "Usage: $0 /path/to/cassandra-<snapshot>.tar.gz"
  exit 2
fi

if [ -z "$CONTAINER_NAME" ]; then
  echo "No Cassandra container found. Set CONTAINER_NAME env var to override."
  exit 2
fi

echo "Stopping Cassandra container $CONTAINER_NAME"
docker stop "$CONTAINER_NAME"

TMPDIR=$(mktemp -d)
tar -xzf "$TARBALL" -C "$TMPDIR"

echo "Copying data into container"
docker cp "$TMPDIR/cassandra_data/." "$CONTAINER_NAME":/var/lib/cassandra/data/

rm -rf "$TMPDIR"

echo "Starting Cassandra container"
docker start "$CONTAINER_NAME"

echo "Restore requested — run nodetool refresh or follow Cassandra restore best practices to rebuild SSTables as needed."
