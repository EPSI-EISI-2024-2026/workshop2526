#!/usr/bin/env bash
set -euo pipefail
# Simple restore helper - expects backup tarballs in /opt/poudlard/backups or passed path
BACKUP_TARBALL=${1:-}
if [ -z "$BACKUP_TARBALL" ]; then
  echo "Usage: $0 /path/to/backup.tar.gz"
  exit 2
fi

echo "Restoring $BACKUP_TARBALL"
# Extract to docker volumes directory (example) - adjust paths accordingly
sudo tar -xzf "$BACKUP_TARBALL" -C /var/lib/docker/volumes/

echo "Restarting compose"
sudo docker-compose -f /opt/poudlard/docker/docker-compose.yml up -d

echo "Restore complete"
