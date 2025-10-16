Protego Maxima — Hardening guide

This document contains minimal, example steps used to harden the workshop WAF/IDS placeholders and to run test vectors.

Files added:
- `docker/nginx/modsecurity/rules.conf` — example ModSecurity rules (SQLi, XSS, RCE patterns).
- `docker/nginx/modsecurity/crs-tuning.conf` — example CRS tuning (disable noisy rule, reduce paranoia).
- `monitoring/suricata/expanded.rules` — extra Suricata rules to detect SQLi/XSS/scanners.
- `scripts/test_security/*` — simple scripts that exercise HTTP and SSH attack vectors against localhost services.

How to run tests (quick):

1. Ensure services are running (nginx with ModSecurity on port 8080 for the demo app; Suricata running on the host and reading `local.rules`).
2. Make test scripts executable:

```bash
chmod +x scripts/test_security/*.sh
```

3. Run the test runner:

```bash
bash scripts/test_security/run_tests.sh
```

Notes:
- These are demo rules only. For production, use the full OWASP CRS, tune rules incrementally in staging, and enable logging to an ELK/EFK stack for analysis.
