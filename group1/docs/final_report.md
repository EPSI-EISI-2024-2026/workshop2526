# POUDLARD - Rapport technique final

Date: 2025-10-14

Résumé
------
Ce document rassemble l'architecture, les choix techniques, le PRA et les mécanismes de sécurité mis en place pour le workshop "POUDLARD À L’EPSI/WIS".

Architecture (vue d'ensemble)
-------------------------------
Diagramme ASCII (simplifié)

Internet
  |
  v
[Load Balancer / NGINX + WAF]
  |
  +--> GLPI (PHP) -> MariaDB (persistent)
  |
  +--> App demo
  |
  +--> ElasticSearch cluster
  |
  +--> Cassandra cluster (datalake)
  |
  +--> Prometheus / Grafana (monitoring)
  |
  +--> Filebeat -> ElasticSearch (logs)
  |
  +--> Suricata (IDS) [host networking]
  |
  +--> Cowrie (honeypot)

Réseau & segmentation
- Trois réseaux Docker: `front`, `internal`, `monitoring`.
- Services exposés seulement via le reverse proxy frontal (NGINX + ModSecurity).
- Services stateful (ElasticSearch, Cassandra) sur `internal` non exposés directement.

Choix techniques et justification
---------------------------------
- GLPI: outil de ticketing open-source, déployé en container pour la démo.
- ElasticSearch: historisation et corrélation des logs (Filebeat -> ES).
- Cassandra: stockage distribué (datalake) pour ingestion massive.
- Prometheus/Grafana: métriques & dashboards.
- WAF (ModSecurity + OWASP CRS): protection applicative en frontal.
- Suricata: IDS pour détection réseau et signatures.
- Cowrie: honeypot pour recueillir attaques automatiques.
- Ansible/Terraform: automatisation de l'infrastructure, déploiement et PRA.
- CI: GitHub Actions (lint, tests, build, Trivy, SonarCloud placeholder, push vers GHCR).

Déploiement
-----------
- Local (démonstration): `docker-compose -f docker/docker-compose.yml up -d`
- Infra cloud (exemple): Terraform (`terraform/`) crée instances, VPC et bucket S3 (placeholders).
- Configuration fine et orchestration via `ansible/playbook.yml` (rôles: docker, monitoring, security, backup, elastic).

PRA & sauvegardes
------------------
- Objectifs RTO/RPO: définis dans `docs/pra.md` (RTO cible 1h, RPO 15min pour services critiques).
- Sauvegardes:
  - Docker volumes (GLPI, MariaDB, ES data, Cassandra data) archivés via scripts dans `scripts/`.
  - ES snapshots via API (`scripts/es_snapshot.sh`) — repository peut être S3 (role Ansible `elastic` pour création).
  - Cassandra snapshots via `nodetool` (scripts pour hôte et pour container `cassandra_container_snapshot.sh`).
  - Uploads vers S3 avec `scripts/upload_backups_to_s3.sh`.
- Restauration guidée: `docs/pra_detailed.md` contient runbook pas-à-pas.

CI/CD
------
- GitHub Actions workflows:
  - Lint (flake8), Tests (pytest), Build Docker image.
  - Trivy scan (artifact JSON uploaded), SonarCloud scanning (placeholder, requires secrets).
  - Push image to GHCR on `main`.

Sécurité (Protego Maxima)
-------------------------
- WAF: ModSecurity configuration placeholder (`docker/nginx/modsecurity` + OWASP CRS placeholder). DoD: activer CRS, affiner règles, monter en mode detection puis IPS après tests.
- IDS: Suricata container (host networking recommended on Linux). Rules fournies dans `monitoring/suricata/rules.rules`.
- Honeypot: Cowrie container placeholder; logs collectés par Filebeat.
- Fail2Ban: role Ansible copy `ansible/roles/security/files/fail2ban/jail.local`.
- Log collection: Filebeat shipper vers ElasticSearch.

Tests et validation
-------------------
- Un test unitaire pytest pour l'app existant (path `docker/app/tests/test_app.py`).
- Scans: Trivy pour images; SonarCloud pour code quality (configure token).
- PRA validation: prévoir GitHub Action qui provisionne VM ephemeral, restaure backup et exécute tests d'acceptance.

Limitations & work-in-progress
------------------------------
- Les configurations ES cluster & Cassandra replication sont des exemples mono-noeud pour la démo; il faut adapter pour production (réplication, discovery, heap sizing, etc.).
- ModSecurity & OWASP CRS fournis en placeholder — nécessitent tuning et tests sur staging.
- Suricata nécessite host networking (Linux) — sur macOS utiliser une VM.
- Terraform modules et IAM policies compris à titre d'exemple — revoir pour sécurité et conventions cloud.

Fichiers importants
-------------------
- `docker/docker-compose.yml` — stack local (services listés ci-dessus).
- `ansible/*` — playbooks & roles d'automatisation.
- `terraform/*` — exemples de provisioning (VPC, S3, IAM user for ES snapshots).
- `monitoring/*` — Prometheus/Grafana/Filebeat/Suricata/Cowrie placeholders.
- `scripts/*` — backup & restore helpers.
- `docs/*` — architecture, PRA détaillé, security.

Prochaines recommandations
--------------------------
1. Hardening production: migrer vers Kubernetes (Helm), config secrets manager, policy IAM stricte.
2. Tests PRA automatisés (GitHub Actions orchestration + ephemeral infra) pour valider RTO/RPO.
3. Mise en place d’un pipeline de détection SOC (ELK + alerting + playbooks de réponse automatisée).

Annexes
-------
- README.md contient quick-start et instructions pour secrets CI.
- `docs/pra_detailed.md` contient runbook de restauration et commandes utiles.

Fin du rapport.
