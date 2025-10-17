# Wigor Schedule Windows

## Présentation
Wigor Schedule Windows est une application de bureau Windows (client Python) qui récupère et affiche un emploi du temps en consommant le projet WSPS (https://github.com/kaelianbaudelet/WSPS.git).

Important : le dépôt WSPS est un projet TypeScript/Node (pas une librairie Python). On ne peut donc pas l'installer via pip. Deux intégrations cohérentes et recommandées :

1) Mode recommandé — WSPS en service HTTP séparé (local ou distant)
- Cloner et lancer WSPS (Node) séparément ; l'application Python communique via HTTP (requests) vers ce service.
- Avantages : séparation claire des responsabilités, facilité de packaging du client Windows (PyInstaller), tests unitaires isolés (mock HTTP).

Exemple (WSPS — côté serveur Node) :
```bash
git clone https://github.com/kaelianbaudelet/WSPS.git externals/WSPS
cd externals/WSPS
npm install
npm run start   # ou npm run dev selon le repo
```
Puis lancer l'application client :
```powershell
pip install -r requirements.txt
python src/main.py
```

2) Mode alternatif — adapter WSPS en tant que microservice embarqué
- Construire WSPS (npm run build) et exécuter le binaire/node dans le bundle d'installation, ou packager un conteneur Docker avec WSPS + l'application.
- Avantage : distribution autonome (mais packaging plus complexe).

## Modifications apportées au projet
- L'API du projet n'est plus une dépendance pip. Le client Python appelle les endpoints HTTP exposés par WSPS.
- src/wigor_client.py : doit appeler les endpoints REST de WSPS (auth, fetch schedule). Utiliser requests et mocker ces appels en tests.
- Tests : mocker les réponses HTTP (pytest + pytest-mock) afin d'obtenir une couverture >80 %.

## Dépendances (requirements.txt)
- Python : Requests, PySide6 (GUI), python-dotenv, pytest, pytest-cov, pytest-mock, pyinstaller.
- Node (WSPS) : Node.js + npm (installées séparément) ; dépendances gérées par le repo WSPS.

## Installation (développement)
1. Cloner ce dépôt :
```
git clone <repo> && cd wigor-schedule-windows
```
2. Installer Python deps :
```
pip install -r requirements.txt
```
3. Installer et lancer WSPS (séparé) :
```
git clone https://github.com/kaelianbaudelet/WSPS.git externals/WSPS
cd externals/WSPS
npm install
npm run start
```
4. Lancer le client :
```
python src/main.py
```

## Packaging — créer un exécutable Windows
- Lancer WSPS comme service distant (ou inclure dans l'installateur).
- Packager le client Python :
```
pyinstaller --onefile --noconfirm --name WigorSchedule src/main.py
```
- Si WSPS doit être inclus, documenter le service Node dans l'installeur (ou fournir un bundle avec Node + WSPS).

## Tests et couverture
- Mocker les endpoints WSPS (pytest-mock) pour tests unitaires.
- Commandes :
```
pytest --cov=src --cov-report=term-missing tests
```
Objectif : coverage >= 80%.

## Justification rapide
- WSPS est un projet TypeScript/Node ; l'intégrer comme service HTTP est la solution la plus simple et cohérente pour un client Python.
- Séparation client/service facilite tests, sécurité et packaging Windows.
- Alternatives (revenir à Node/Electron pour UI) sont possibles mais nécessitent de réécrire la GUI. Le choix Python+PySide6 est conservé pour préserver le travail déjà réalisé.

## Sécurité
- Ne jamais stocker les credentials en clair. Préférer cookies temporaires, token ephemeral, ou stockage sécurisé (Windows Credential Manager).
- Voir docs/security.md pour recommandations.

## Documentation
- Mettre à jour docs/README_API.md pour documenter les endpoints WSPS consommés.