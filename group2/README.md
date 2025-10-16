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
