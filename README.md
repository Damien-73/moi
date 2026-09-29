# Moteur de setups forex — phase 1 (validation statistique)

Consignes complètes : voir les instructions du projet. Ce fichier dit seulement comment lancer.

## Installation
```
pip install -r requirements.txt
```

## 1. Données (Dukascopy M1 bid + ask, 2014 → aujourd'hui)
```
python -m src.data.download                 # ~7 paires x 2 côtés x 13 ans, plusieurs heures
python -m src.data.quality                  # -> results/data_quality.md
```
Besoin d'un accès réseau à `datafeed.dukascopy.com` et de Node.js (`npx`).

## 2. Tests (doivent être verts avant chaque commit)
```
python -m pytest
```

## 3. Setup en in-sample (2014–2022)
```
python -m src.backtest.runner --setup zone_a_zone --pairs EURUSD   # étape 4
python -m src.backtest.runner --setup zone_a_zone                  # étape 5 (7 paires)
```
Chaque lancement ajoute 2 essais (sortie simple + TP partiels) dans `results/trials.csv`.

## 4. Out-of-sample (2023 → aujourd'hui) — une seule fois, après accord
Verrouillé dans le code : il faut la ligne « Statut : FIGÉ » dans `docs/setups/<setup>.md`,
`OOS_ACCORD=<setup>`, et le setup ne doit jamais avoir été testé en OOS (`results/oos_log.csv`).
```
OOS_ACCORD=zone_a_zone python -m src.backtest.runner --setup zone_a_zone --oos
```
