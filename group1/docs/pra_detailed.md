PRA détaillé

Résumé
-------
Ce document décrit le Plan de Reprise d'Activité (PRA) pour l'infrastructure et l'ensemble des projets présents dans le dépôt (group1 et projets associés). Il fournit :
- les objectifs RTO / RPO,
- l'architecture cible pour HA et DR,
- les procédures automatisées de provisionning (Terraform) et déploiement (Ansible),
- la stratégie de sauvegarde et restauration (Cassandra, Elasticsearch, volumes Docker, etc.),
- les procédures de tests et vérifications (monitoring/health),
- les scripts/automatisations recommandés (CI/CD) et les motivations techniques.

Scope
-----
Couverture : tous les services containerisés (Docker Compose / Docker), bases de données (Cassandra, Elasticsearch), et composants de monitoring (Prometheus/Grafana). Le PRA est conçu pour être réutilisable par au moins un autre défi du dépôt (compatibilité multi-projets requise).

Objectifs (exemples)
--------------------
- RTO cible : 2 heures pour les services critiques (ré-application d'infrastructure + restauration des backups et tests smoke).
- RPO cible : 4 heures pour les données critiques (sauvegardes incrémentales horaires, snapshot quotidien complet).
Ces valeurs sont des exemples — adapter selon criticité réelle.

Hypothèses
----------
- Accès IAM/AWS disponible pour provisionner buckets S3 et VMs.
- Les images Docker des applications sont stockées dans un registry accessible (Docker Hub / ECR).
- Les scripts de snapshot cités existent dans `scripts/` et sont exécutables sur les hôtes.

Architecture et haute disponibilité
----------------------------------
- Multi-AZ / Multi-node pour les composants critiques : Cassandra en cluster (3+ noeuds), Elasticsearch en cluster (3+ master/data), services applicatifs derrière un load balancer (nginx ou ALB), et réplication des volumes critiques.
- Dockerisation : toutes les applications doivent fournir un `Dockerfile` et un `docker-compose.yml` pour faciliter le déploiement local et en production.
- Terraform gère le provisionning réseau (VPC), instances, load balancers, et ressources S3.
- Ansible s'occupe de la configuration des instances, déploiement des containers et des rôles (backup, elastic, monitoring).

Stratégie de sauvegarde
-----------------------
- Backup ciblés par composant :
  - Cassandra : `nodetool snapshot` + archivage des SSTables (scripts : `scripts/cassandra_snapshot.sh`, `scripts/cassandra_container_snapshot.sh`).
  - Elasticsearch : Snapshot API vers repository S3 (script : `scripts/es_snapshot.sh`).
  - Volumes Docker / données applicatives : dump + tar.gz et upload vers S3 (`scripts/upload_backups_to_s3.sh`).
  - Configs Ansible / Terraform : versionning git (pas de backup S3 requis).
- Fréquence : horaires pour les données à haute fréquence (Cassandra), quotidiennes pour snapshots complets.
- Rétention : configurable via variables (ex: 30 jours par défaut).
- Sécurité : chiffrement côté client lors de l'archivage et SSE-KMS côté S3, politiques IAM restrictives pour le rôle de backup.

Provisionning (Terraform)
-------------------------
Exemples de commandes :

```bash
cd terraform
terraform init
terraform apply -var 'ami=ami-xxxxx' -auto-approve
```

Recommandation : fournir des modules Terraform paramétrables (network, compute, s3) et des workspaces pour environnements (dev/staging/prod).

Déploiement (Ansible)
---------------------
Exemples :

```bash
ansible-playbook -i ansible/inventory ansible/playbook.yml -u ubuntu --become
```

Utiliser des tags (backup, elastic, monitoring) pour exécuter des parties spécifiques.

Runbook de restauration (procédure pas-à-pas)
--------------------------------------------
1) Provisionner l'infrastructure (Terraform) dans la région/AZ cible.
   - Vérifier que les ressources réseau et le bucket S3 sont disponibles.

2) Déployer la configuration et services de base (Ansible).
   - `ansible-playbook -i ansible/inventory ansible/playbook.yml -u ubuntu --become`

3) Récupérer les archives depuis S3 et restaurer selon le composant :
   - Volumes Docker / données applicatives :

```bash
aws s3 cp s3://<bucket>/backups/app-data-YYYYMMDD.tar.gz /opt/backups/
tar -xzf /opt/backups/app-data-YYYYMMDD.tar.gz -C /var/lib/docker/volumes/
docker-compose -f docker/docker-compose.yml up -d
```

   - Cassandra (containerisé) :

```bash
aws s3 cp s3://<bucket>/backups/cassandra-YYYYMMDD.tar.gz /opt/backups/
docker stop cassandra || true
tar -xzf /opt/backups/cassandra-YYYYMMDD.tar.gz -C /var/lib/cassandra/data/
docker start cassandra
# puis sur chaque noeud : nodetool refresh / rebuild s'il est nécessaire
```

   - Elasticsearch :
     - S'assurer que le repository snapshot (S3) est configuré puis restaurer via API :

```bash
curl -X POST "http://localhost:9200/_snapshot/my_s3_repo/snapshot-YYYYMMDD/_restore"
```

4) Démarrer les stacks et vérifier santé des services.

Vérifications post-restauration (checks)
---------------------------------------
- Docker :

```bash
docker ps --format '{{.Names}}: {{.Status}}'
docker inspect --format '{{.Name}} {{if .State.Health}}{{.State.Health.Status}}{{else}}no-health{{end}}' $(docker ps -q)
```

- Applications : exécuter un jeu de tests smoke (script `docker/tests/run_smoke_tests.sh` ou équivalent).
- Datastores :
  - Cassandra : `nodetool status`, vérifier l'anneau et l'absence de tombstones en excès.
  - Elasticsearch : `_cluster/health`, vérifier `status` green/greenish et nombre de shards.
- Monitoring : s'assurer que Prometheus scrape et Grafana affiche les dashboards attendus.

Automatisation des tests de restauration (CI)
-------------------------------------------
- Proposition : GitHub Actions workflow qui :
  1. Provisionne une VM ephemeral (via terraform). 
  2. Déploie via Ansible.
  3. Télécharge un backup de test depuis un bucket S3 public ou mock.
  4. Lance le script de restauration et exécute les tests smoke.
- Stocker les artefacts de test et logs pour audit.

Exemples de scripts existants
----------------------------
- `scripts/es_snapshot.sh` — snapshot ES -> S3
- `scripts/cassandra_snapshot.sh` — snapshot Cassandra (host)
- `scripts/cassandra_container_snapshot.sh` — snapshot Cassandra (container)
- `scripts/cassandra_restore_container.sh` — restauration container
- `scripts/upload_backups_to_s3.sh` — upload des archives vers S3

Sécurité et IAM
---------------
- Créer un rôle IAM dédié au backup/restoration avec permissions minimales (GetObject/PutObject sur le bucket S3, accès KMS si nécessaire).
- Activer SSE-KMS sur les buckets S3 et chiffrer les archives côté client pour double sécurité.
- Restreindre l'accès SSH via bastion et utiliser des clés temporaires (SSM Session Manager si AWS).

Monitoring & health status
--------------------------
- Stack recommandée : Prometheus (metrics), node_exporter (host metrics), cAdvisor (container metrics), Blackbox exporter (endpoint checks), Alertmanager, Grafana.
- Définir alertes pour : service down, utilisation disque élevée, erreurs 5xx, latence API, cluster health (ES/Cassandra).

Compatibilité multi-projets
---------------------------
- Standardiser l'approche : chaque projet doit fournir : `Dockerfile`, `docker-compose.yml` (ou Helm chart), playbook Ansible minimal et variables Terraform si nécessaire.
- Le PRA doit permettre de déployer au moins un autre défi du dépôt sans modification structurelle (paramétrisation via variables).

Justification des choix technologiques
-------------------------------------
- Terraform pour l'infrastructure as code : large adoption, modules réutilisables, état (remote backend) pour la traçabilité.
- Ansible pour la configuration : idempotence, playbooks lisibles, intégration facile avec Terraform outputs.
- Docker / Docker Compose : portabilité des applications et facilité de test.
- S3 pour stockage des backups : durable, économique, et intégré aux snapshot repositories ES.
- Prometheus/Grafana : standard pour métriques et dashboards.

Checklist de validation (Test de PRA)
------------------------------------
Avant test : configurer variables (bucket S3, clés AWS, region, paramètres Terraform/Ansible).

1) Test provisionning : exécuter Terraform et vérifier ressources créées.
2) Test déploiement : exécuter Ansible et vérifier que containers démarrent.
3) Test backup : lancer les scripts de snapshot pour Cassandra/ES et vérifier la présence des archives dans S3.
4) Test restauration : effectuer une restauration sur une VM ephemeral et exécuter les tests smoke.
5) Vérifier monitoring & alerting : simuler incident et vérifier réception d'alerte.

Commandes utiles (extraits)
--------------------------
```bash
# Terraform
cd terraform
terraform plan -var-file=env.tfvars
terraform apply -var-file=env.tfvars

# Ansible
ansible-playbook -i ansible/inventory ansible/playbook.yml --tags "deploy,monitoring,backup"

# Vérification ES
curl -sS http://localhost:9200/_cluster/health | jq

# Vérification Cassandra
nodetool status

# Lister backups S3
aws s3 ls s3://<bucket>/backups/ --profile prod
```

Limitations et points à améliorer
---------------------------------
- Les scripts de snapshot/restauration doivent être testés en continu (CI) et rendus idempotents.
- La configuration multi-AZ dépend du provider cloud; prévoir tests de basculement (failover) réguliers.
- Prévoir playbooks Ansible pour tests automatisés post-restauration et nettoyages.

Annexes et fichiers liés
-----------------------
- `terraform/` : modules et exemples pour provisionning
- `ansible/` : playbooks et rôles (backup, elastic, monitoring, docker)
- `scripts/` : snapshots et restore helpers

Conclusion
----------
Le PRA fournit une couverture fonctionnelle des besoins exprimés : provisionning automatisé (Terraform), déploiement (Ansible), sauvegarde/restore pour les composants critiques, monitoring et verification de santé, automatisation de tests via CI. Pour rendre le PRA «professionnel» il reste à :
- Paramétrer RTO/RPO réels selon SLAs clients,
- Rendre tous les scripts idempotents, testés et signés,
- Mettre en place workflows CI qui exécutent régulièrement les tests de restauration.
PRA détaillé - (Placeholder)

Ce fichier doit contenir le runbook complet: commandes de restauration, vérification des snapshots, procédure de basculement sur DR site, jeux de tests post-restauration.

(À compléter automatiquement par des scripts de test de restauration.)

Runbook de restauration (exemple)

1) Provisionner un hôte (Terraform)

```bash
cd terraform
terraform init
terraform apply -var 'ami=ami-xxxxx' -auto-approve
```

2) Déployer l'application via Ansible

```bash
ansible-playbook -i inventory playbook.yml -u ubuntu --become
```

3) Restaurer les volumes depuis S3 (exemple):

```bash
aws s3 cp s3://my-poudlard-backups/glpi_db-20251014.tar.gz /opt/poudlard/backups/
cd /opt/poudlard
tar -xzf backups/glpi_db-20251014.tar.gz -C /var/lib/docker/volumes/
docker-compose -f docker/docker-compose.yml up -d
```

4) Vérifications post-restauration:
- Vérifier santé des containers `docker ps` et `docker inspect --format '{{.State.Health.Status}}' <container>`
- Vérifier Prometheus / Grafana dashboards
- Lancer tests applicatifs (script de test automatique à ajouter)

Automatisation des tests de restauration:
- Ajouter un GitHub Action qui provisionne une VM ephemeral, restaure un backup et exécute des tests d'acceptance.

Snapshots et backups:

- Elasticsearch: utiliser l'API Snapshot/Restore. Exemple de script `scripts/es_snapshot.sh`.
- Cassandra: utiliser `nodetool snapshot` puis archiver les données; exemple `scripts/cassandra_snapshot.sh`.
- Upload: les archives tar.gz peuvent être uploadées vers un bucket S3 via `scripts/upload_backups_to_s3.sh` (nécessite `awscli` et variables d'environnement AWS configurées ou un rôle IAM attaché à la VM).

Containerized Cassandra:

- Si Cassandra est déployé en container (Docker Compose), utilisez `scripts/cassandra_container_snapshot.sh` qui exécute `nodetool snapshot` à l'intérieur du container, copie les données et archive.
- Pour restaurer dans un container, utilisez `scripts/cassandra_restore_container.sh /path/to/archive.tar.gz`. Le script stoppe le container, injecte les fichiers et redémarre. Après restauration, exécuter `nodetool refresh` ou suivre la procédure de rebuild SSTables selon la version.

Ansible backup role:
- Le rôle `ansible/roles/backup` copie les scripts de snapshot sur l'hôte, exécute les snapshots et (si variable `S3_BACKUP_BUCKET` existante) upload vers S3.

Configuration du repository Elasticsearch (S3):

1) Provisionner le bucket S3 et l'utilisateur IAM (ex: via `terraform/s3.tf`).
2) Exécuter le rôle Ansible `ansible/roles/elastic` en fournissant `s3_bucket` et `s3_region` pour créer le snapshot repository ES.

Exemple Ansible:

```bash
ansible-playbook -i ansible/inventory playbook.yml -e "s3_bucket=my-bucket s3_region=eu-west-3" --tags elastic
```

Vérifier que le repository existe:

```bash
curl http://localhost:9200/_snapshot/_all
```
