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
