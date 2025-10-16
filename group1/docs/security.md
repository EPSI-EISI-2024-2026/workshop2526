Protego Maxima - Stratégie de sécurité

Composants de défense:
- WAF (ModSecurity + OWASP CRS) en frontal pour protéger les applications web.
- IDS/IPS (Suricata) pour la détection d'attaques réseau; journaux envoyés à ElasticSearch.
- Honeypot (ex: Cowrie) pour attirer et analyser les attaques automatisées.
- Fail2Ban sur services exposés pour bloquer bruteforce.
- Segmentation réseau: services internes (Cassandra, ElasticSearch) non exposés sur Internet, uniquement accessibles depuis le réseau interne/proxy.

Monitoring et alerting:
- Prometheus scrappe métriques; Alertmanager route les alertes (mail/Slack).
- Grafana dashboards pour visibilité.

Hardening:
- Mise à jour régulière des images, scan de vulnérabilités via Trivy/SonarQube.
- Least-privilege pour comptes de service.

Documentation:
- Chaque mesure est documentée dans ce dossier; règles WAF et playbooks Ansible fournis pour déploiement.

Protego Maxima - composantes détaillées

- Collecte des logs: Filebeat lit les logs Docker et Suricata et les envoie vers Elasticsearch (indexation + recherche).
- Détection réseau: Suricata rules (stockées dans `monitoring/suricata`) détectent signatures connues et anomalies; les alertes sont envoyées vers Elasticsearch pour corrélation.
- Honeypot: Cowrie capture tentatives SSH et interagit avec les attaquants; ses logs sont collectés via Filebeat et analysés dans Kibana/Grafana.
- WAF: ModSecurity (placeholder fourni) doit être complété par OWASP CRS et adapté aux endpoints exposés.

Notes opérationnelles:
- Les règles Suricata doivent être testées en environnement staging avant d'être activées en IPS/Drop mode.
- Stocker les logs critiques (Suricata alerts, Cowrie sessions) dans un bucket centralisé et appliquer une rétention conforme à la PRA.
