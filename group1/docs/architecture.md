Architecture réseau et applicative

Diagramme ASCII (simplifié)

Internet
   |
   |  (1) Bastion / Reverse proxy (NGINX + WAF/ModSecurity)
   v
[ Load Balancer / Reverse Proxy ] ---> [ GLPI (PHP) ]
                  |                     [ MariaDB (GLPI DB) ]
                  |
                  +--> [ ELASTICSEARCH cluster (historisation) ]
                  +--> [ CASSANDRA cluster (datalake) ]
                  +--> [ PROMETHEUS + GRAFANA (monitoring) ]
                  +--> [ SURICATA (IDS) / HONEYPOT (cowrie placeholder) ]

Notes:
- Chaque composant est déployé via Docker Compose pour la démo; en production on utilisera Kubernetes/Swarm.
- Haute disponibilité: services stateful (ElasticSearch, Cassandra) sont configurés en cluster (replicas/répliques) et exposés via un reverse-proxy + load-balancer.
- Pare-feu: choix d'un pare-feu applicatif (WAF) en frontal + IDS réseau (Suricata) pour détection d'intrusion.

Notes pratiques:
- Suricata est configuré dans `docker-compose.yml` avec `network_mode: host` pour pouvoir sniffer le trafic réseau. Cette configuration nécessite un hôte Linux (Docker sur Linux). Sur macOS (Docker Desktop) le mode host ne fournit pas le trafic réseau de la machine hôte, donc pour tests sur macOS on peut:
   - Exécuter Suricata dans une VM Linux, ou
   - Lancer une instance Suricata directement sur une machine Linux distante.
- Cowrie (honeypot) est ajouté comme service placeholder; pour une vraie collecte, personnaliser les volumes `monitoring/cowrie` et surveiller ses logs via ElasticSearch/Grafana.

Justification des choix:
- GLPI est un outil mature de ticketing et facile à containeriser.
- ElasticSearch est adapté pour l'historisation et recherche rapide de logs/événements.
- Cassandra est choisi pour la scalabilité en écriture et le datalake distribué.
- Prometheus/Grafana pour métriques et dashboards.
- Un WAF en frontal protège contre les attaques applicatives (OWASP top 10); Suricata détecte attaques réseau/Anomalies.
