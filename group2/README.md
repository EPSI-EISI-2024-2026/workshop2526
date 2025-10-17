
Contexte :
Workshop EPSI/WIS – Thème “Poudlard”. Chaque défi correspond à un projet IA / Data magique.

Défis à combiner :

1️⃣ **PROFESSEUR DUMBLEDORE (#19)**  
Créer une IA de reconnaissance vocale capable de reconnaître au moins 8 formules magiques des livres ou films Harry Potter.  
S’informer sur NLU/NLP/NLG et constituer un dataset adapté.

2️⃣ **IS IT YOU HARRY? (#20)**  
Créer un réseau de neurones convolutif (CNN) dans un notebook Jupyter pour reconnaître au moins 10 personnages d’Harry Potter à partir d’images.  
Utiliser images réelles ou de synthèse.

3️⃣ **LE NIMBUS 3000 (#21)**  
Effectuer un benchmark d’optimizers (Adagrad, RMSProp, Adam, AdamW, SGD, etc.) sur le réseau précédent et rédiger un document de recherche complet.

4️⃣ **LE PROCÈS DE J.K. ROWLING (#22)**  
Réaliser une data-visualisation complète sur la saga (analyse textuelle) :  
- Nombre de fois que certains personnages parlent ou agissent.  
- Fréquences par livre, par 100 pages.  
- Tendances globales et graphiques interprétables.  

Tâche demandée :
Crée un projet de Data Science complet "HarryPotter.AI" :
- Architecture Python : notebooks, datasets, modèles et visualisations.  
- Fournis les notebooks d’entraînement (voix + vision + texte).  
- Implémente le benchmark des optimizers et commente les résultats.  
- Crée la data-viz finale (matplotlib/pandas).  
- Rédige un rapport scientifique en Markdown.

Sortie attendue :
- Code source complet (Jupyter notebooks)
- Datasets ou scripts de génération
- Rapport technique format recherche

Utilise mise pour la gestion d'env et outils par example mise use python@3.13 pour utilisé python dans le projet



# HarryPotter.AI

A comprehensive Data Science project combining AI challenges inspired by Harry Potter:

1. **Voice Recognition**: Recognize at least 8 magical spells using speech recognition.
2. **Image Recognition**: CNN to identify 10+ Harry Potter characters from images.
3. **Optimizer Benchmark**: Compare various optimizers on the CNN model.
4. **Text Analysis**: Visualize character appearances and frequencies in the Harry Potter saga.

## Project Structure

- `notebooks/`: Jupyter notebooks for training and analysis
- `datasets/`: Data generation scripts and sample data
- `models/`: Saved trained models
- `visualizations/`: Generated plots and charts
- `reports/`: Scientific report and documentation
- `scripts/`: Utility scripts

## Setup

1. Install mise: https://mise.jdx.dev/
2. Use Python 3.13: `mise use python@3.13`
3. Install dependencies: `pip install -r requirements.txt`

## Data Preparation

### Voice Data
Run the voice_recognition.ipynb notebook to generate synthetic audio for spells.

### Image Data
Run `python scripts/generate_images.py` to download character images from Harry Potter API.

### Text Data
Run `python scripts/prepare_texts.py` and place Harry Potter book texts in `datasets/texts/` (respect copyrights).

## Notebooks

- `voice_recognition.ipynb`: Spell recognition training
- `character_recognition.ipynb`: Character identification CNN
- `optimizer_benchmark.ipynb`: Optimizer comparison
- `text_analysis.ipynb`: Saga text visualization

## Running the Project

1. Prepare data using the scripts above
2. Run notebooks in order: voice, character, benchmark, text
3. View results in `visualizations/` and `reports/`

## Note on Copyrights

This project uses synthetic data where possible. For text analysis, ensure you have legal access to Harry Potter book texts. Images are sourced from public APIs.
