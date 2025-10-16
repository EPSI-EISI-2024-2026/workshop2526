#!/usr/bin/env bash
set -euo pipefail
# Elasticsearch snapshot script (assumes snapshot repo configured to a filesystem or S3)
ES_HOST=${ES_HOST:-http://localhost:9200}
REPO=${REPO:-poudlard_repo}
SNAPSHOT_NAME=${SNAPSHOT_NAME:-snapshot-$(date -u +%Y%m%dT%H%M%SZ)}

echo "Creating Elasticsearch snapshot $SNAPSHOT_NAME in repo $REPO"
curl -s -XPUT "$ES_HOST/_snapshot/$REPO/$SNAPSHOT_NAME?wait_for_completion=true" -H 'Content-Type: application/json' -d '{}'
echo "Snapshot created: $SNAPSHOT_NAME"
