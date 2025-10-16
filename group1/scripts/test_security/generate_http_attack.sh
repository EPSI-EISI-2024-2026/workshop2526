#!/usr/bin/env bash
# Simple test vectors to exercise WAF/IDS placeholders
set -eu

TARGET_HOST=${1:-http://localhost:8080}

echo "[test] Sending benign request"
curl -s -o /dev/null -w "%{http_code}\n" "$TARGET_HOST/"

echo "[test] Sending SQLi payload"
curl -s -o /dev/null -w "%{http_code}\n" "$TARGET_HOST/?id=1 UNION SELECT username,password FROM users"

echo "[test] Sending XSS payload"
curl -s -o /dev/null -w "%{http_code}\n" -G --data-urlencode "q=<script>alert(1)</script>" "$TARGET_HOST/search"

echo "done"
