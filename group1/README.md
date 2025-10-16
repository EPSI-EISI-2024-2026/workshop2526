# POUDLARD - Workshop M2 (Dockerwarts / Pracadabra / CI/CD / Protego Maxima)

Ce dépôt contient une solution de démonstration pour le workshop "POUDLARD À L’EPSI/WIS" (13–17 octobre 2025).
Il regroupe quatre défis : DOCKERWARTS, PRACADABRA, CI/CD EXPRESS – VOIE 9¾ et PROTEGO MAXIMA.

Objectifs :
- Fournir une architecture dockerisée pour un projet Big Data (GLPI, ElasticSearch, Cassandra, Grafana, Prometheus, etc.)
- Automatiser le déploiement et les backups (Ansible + Terraform)
- Mettre en place un pipeline CI/CD (GitHub Actions) avec qualité de code et SonarQube
- Ajouter des mécanismes de sécurité (IDS, WAF, honeypot, pare-feu)

Structure du dépôt (extrait) :
- `docker/` : docker-compose et Dockerfiles
- `ansible/` : playbooks et roles
- `terraform/` : exemples d'infrastructure as code
- `monitoring/` : Prometheus / Grafana provisioning
- `docs/` : architecture, PRA, sécurité
- `.github/workflows/` : CI/CD
- `scripts/` : sauvegardes et utilitaires

Voir `docs/` pour la documentation détaillée (architecture, PRA, sécurité).

Quick start (local dev):

1. Lancer les services en local (démo mono-hôte):

```bash
make up
```

2. Exécuter le playbook Ansible localement (localhost):

```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```

3. Pour provisionner une VM AWS (exemple):

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

Notes:
- Sur macOS, Suricata nécessite une VM Linux pour fonctionner correctement (voir `docs/architecture.md`).
- Compléter les variables Terraform (`terraform/variables.tf`) et remplacer les AMI.

CI/CD - configuration des secrets

Pour permettre l'analyse SonarCloud et le push d'images vers GitHub Container Registry (GHCR), ajoutez les secrets suivants dans votre repo GitHub (Settings -> Secrets -> Actions):

- `SONAR_TOKEN` : token utilisateur/project pour SonarCloud
- `SONAR_PROJECT_KEY` : clé du projet SonarCloud
- `SONAR_ORGANIZATION` : organisation SonarCloud
- `GITHUB_TOKEN` : (déjà fourni automatiquement par GitHub Actions)

Le workflow pousse l'image sur GHCR sous le nom `ghcr.io/<owner>/poudlard-app:latest`.

Trivy (scans d'image):

Le workflow exécute Trivy et publie le rapport JSON comme artifact `trivy-report`.
Pour lancer Trivy localement (installé via `brew` ou curl) :

```bash
# build image
docker build -t poudlard-app:latest -f docker/app/Dockerfile ./docker/app
# run trivy
trivy image --format json -o trivy-report.json poudlard-app:latest
```

Backups and snapshots

Examples to run on the host (or via Ansible):

```bash
# Elasticsearch snapshot (uses ES snapshot repo configured)
S3_BACKUP_BUCKET=my-bucket ansible-playbook -i ansible/inventory ansible/playbook.yml --tags backup

# Or run scripts directly on host
/opt/poudlard/scripts/es_snapshot.sh
/opt/poudlard/scripts/cassandra_snapshot.sh
BUCKET=my-bucket /opt/poudlard/scripts/upload_backups_to_s3.sh
```

Protego Maxima quick run

To start the detection stack locally (filebeat + suricata + cowrie):

```bash
docker-compose -f docker/docker-compose.yml up -d filebeat suricata cowrie
```

Then check Suricata logs in `monitoring/suricata` and Cowrie logs in `monitoring/cowrie`.
