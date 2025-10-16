Plan de Reprise d'Activité (PRA) - Résumé

Objectifs:
- RTO cible: 1 heure pour services critiques (GLPI, Monitoring)
- RPO cible: 15 minutes pour données critiques

Sauvegardes:
- Volumes Docker (GLPI, MariaDB, ElasticSearch, Cassandra) sont sauvegardés par script `scripts/backup.sh` vers un stockage externe (S3 compatible ou NFS monté).
- Snapshots pour Elasticsearch et Cassandra (nodetool snapshot) planifiés.

Procédure de restauration (haute-niveau):
1. Provisionner nouvel hôte via Terraform (ou récupérer instances existantes)
2. Restauration des volumes depuis les backups
3. Démarrer les services via `docker-compose up -d`
4. Vérifier l'intégrité: Prometheus health-checks, tests applicatifs.

Tests et automatisation:
- Playbook Ansible `ansible/playbook.yml` automatise le déploiement et la vérification des health-checks.
- Tests de restauration seront planifiés (chaque semaine) pour valider les backups.

Note: Voir `docs/pra_detailed.md` (à ajouter) pour scripts détaillés et runbook pas-à-pas.
