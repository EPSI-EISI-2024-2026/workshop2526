#!/usr/bin/env bash
# Simulate SSH connection failures to the honeypot (connect then close)
set -eu

TARGET_HOST=${1:-localhost}
TARGET_PORT=${2:-2222}

echo "[test] Simulating SSH attempts to ${TARGET_HOST}:${TARGET_PORT}"
for i in 1 2 3 4 5; do
  # use bash TCP redirection to open a connection then close; harmless simulation
  (echo >/dev/tcp/${TARGET_HOST}/${TARGET_PORT}) >/dev/null 2>&1 || true
  sleep 0.2
done

echo "done"
