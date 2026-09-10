"""Constantes versionnées — SPEC-LOT2 §1.3.

Aucune valeur numérique de stratégie ne doit apparaître en dur ailleurs dans
le code. Modifier une valeur ici impose de créer une nouvelle version.
"""
from __future__ import annotations

RANGE_V1 = {
    "version": "range.v1",
    "ATR_PERIODE": 14,
    "ZZ_K": 1.5,
    "PIVOTS_MIN": 4,
    "TOLERANCE_BORNE": 0.25,
    "HAUTEUR_MIN": 1.0,
    "HAUTEUR_MAX": 6.0,
    "DUREE_MIN": 15,
    "DUREE_MAX": 200,
    "DEBORDEMENT_MAX": 0.05,
    "PENTE_MAX": 0.50,
    "TOUCHE_ZONE": 0.10,
    "CASSURE_MIN": 0.25,
    "STOP_MARGE": 0.50,
    "RETOUR_MAX": 10,
    "HORIZON": 20,
    "AMORCAGE_MIN": 300,
    "SEUIL_ANNONCE": 0.70,
}

SCORE_V1 = {
    "version": "score.v1",
    "TOL_NIVEAU_ROND": 0.10,
    "PAS_ROND": 0.0050,
    "PAS_ROND_JPY": 0.50,
    "TOL_REFERENCE": 0.15,
    "TOL_ZONE": 0.25,
    "ZONE_TOUCHES_MIN": 3,
    "ZONE_FUSEAU": 0.50,
    "DIVERGENCE_RSI_MIN": 2.0,
    "FAISABILITE_BON": 0.75,
    "FAISABILITE_MAX": 1.50,
    "EXTENSION_MAX": 2.0,
    "ADX_RANGE": 20.0,
    "ADX_TENDANCE": 25.0,
    "PENTE_TENDANCE": 0.10,
    "QUALITE_TOUCHES": 3,
    "QUALITE_ECART": 0.15,
    "MARGE_CALENDRIER_MIN": 30,
}

COUTS_V1 = {
    "version": "couts.v1",
    "MARGE_COURTIER": 0.010,     # 1 % annuel, contre le trader dans les deux sens
    "BASE_JOURS": 360,
    "FACTEUR_MERCREDI": 3,
    "GLISSEMENT_SPREAD": 0.5,    # fraction de spread ajoutée au franchissement du stop
}
