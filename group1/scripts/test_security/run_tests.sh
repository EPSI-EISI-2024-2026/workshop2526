#!/usr/bin/env bash
set -eu
here=$(cd "$(dirname "$0")" && pwd)
echo "Running Protego Maxima test vectors"
"$here/generate_http_attack.sh" || echo "HTTP tests finished (some failures expected if service not running)"
"$here/ssh_simulate_failures.sh" || echo "SSH simulation finished"
echo "All tests invoked"
