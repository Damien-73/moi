"""Paramètres globaux du projet (paires, dates, coûts).

Toutes les valeurs de coûts sont ici pour être modifiables en un seul endroit.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
M1_DIR = DATA_DIR / "m1"
RESULTS_DIR = ROOT / "results"

PAIRS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"]

# Période in-sample : 2014-01-01 inclus -> 2023-01-01 exclu.
IS_START = "2014-01-01"
OOS_START = "2023-01-01"  # tout ce qui est >= cette date est verrouillé

# Taille d'un pip dans l'unité de prix.
PIP = {p: (0.01 if p.endswith("JPY") else 0.0001) for p in PAIRS}

# Glissement appliqué à CHAQUE ordre (entrée, sortie, sortie partielle), en pips.
SLIPPAGE_PIPS = 0.3

# Swap estimé par nuit (roll-over 17h00 New York), en pips, signe négatif = coût.
# Valeurs volontairement pessimistes (estimations, pas des données de courtier).
# Le mercredi compte triple (week-end).
SWAP_PIPS = {
    "EURUSD": {"long": -0.8, "short": -0.2},
    "GBPUSD": {"long": -0.6, "short": -0.4},
    "USDJPY": {"long": -0.2, "short": -1.2},
    "USDCHF": {"long": -0.2, "short": -0.9},
    "AUDUSD": {"long": -0.6, "short": -0.3},
    "USDCAD": {"long": -0.4, "short": -0.6},
    "NZDUSD": {"long": -0.6, "short": -0.3},
}

# R/R cible de la sortie simple.
RR_TARGET = 2.0

# Fuseau de référence du marché forex (clôture quotidienne 17h00 New York).
NY_TZ = "America/New_York"
ROLLOVER_HOUR_NY = 17
