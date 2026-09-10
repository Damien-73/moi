"""Journal de l'utilisateur et écart comportemental — SPEC-LOT5.

C'est la fonction qui fait payer : elle ne dépend pas de l'existence d'un
avantage de marché. Dire à quelqu'un qu'il entre deux bougies trop tôt garde
toute sa valeur même si aucune figure n'est rentable.

Aucune connexion au compte de courtage : l'utilisateur téléverse un fichier
qu'il a exporté lui-même.
"""
from __future__ import annotations

import csv
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

UTC = timezone.utc
SEUIL_GLOBAL = 30
SEUIL_SEGMENT = 15


# ───────────────────────────── import ─────────────────────────────

class _Tableaux(HTMLParser):
    """Extrait les lignes des tableaux d'un rapport MetaTrader."""

    def __init__(self):
        super().__init__()
        self.lignes, self._ligne, self._cell, self._dans = [], None, None, False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._ligne = []
        elif tag == "td":
            self._cell, self._dans = [], True

    def handle_data(self, data):
        if self._dans:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self._ligne is not None:
            self._ligne.append("".join(self._cell).strip())
            self._dans = False
        elif tag == "tr" and self._ligne:
            self.lignes.append(self._ligne)
            self._ligne = None


def _flottant(x):
    try:
        return float(str(x).replace(" ", "").replace(" ", "").replace(",", "."))
    except (ValueError, AttributeError):
        return None


def _instant(x):
    for f in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M", "%Y-%m-%d %H:%M:%S",
              "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(str(x).strip(), f).replace(tzinfo=UTC)
        except ValueError:
            continue
    return None


def normaliser_symbole(s: str) -> str:
    """EURUSD.pro, EURUSDm, EUR/USD, EURUSD# → EURUSD."""
    n = "".join(c for c in str(s).upper() if c.isalpha())
    return n[:6] if len(n) >= 6 else n


def lire_mt_html(chemin):
    """Rapport MT4/MT5 exporté en HTML."""
    with open(chemin, encoding="utf-8", errors="ignore") as f:
        p = _Tableaux()
        p.feed(f.read())
    trades = []
    for l in p.lignes:
        if len(l) < 10:
            continue
        sens = next((c.lower() for c in l[:5] if c.lower() in ("buy", "sell")), None)
        if sens is None:
            continue
        instants = [x for x in (_instant(c) for c in l) if x]
        nombres = [x for x in (_flottant(c) for c in l) if x is not None]
        if len(instants) < 2 or len(nombres) < 3:
            continue
        symb = next((normaliser_symbole(c) for c in l
                     if len(normaliser_symbole(c)) == 6), None)
        if not symb:
            continue
        trades.append({
            "symbole": symb, "sens": 1 if sens == "buy" else -1,
            "entree_ts": instants[0], "sortie_ts": instants[-1],
            "volume": nombres[0], "entree": nombres[1], "sortie": nombres[-1],
            "stop": None, "objectif": None,
        })
    return trades


def lire_csv(chemin):
    """CSV au modèle publié : symbole,sens,entree_ts,entree,sortie_ts,sortie,volume[,stop]."""
    trades = []
    with open(chemin, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            e, s = _instant(r.get("entree_ts")), _instant(r.get("sortie_ts"))
            if not e:
                continue
            sens = r.get("sens", "").strip().lower()
            trades.append({
                "symbole": normaliser_symbole(r.get("symbole", "")),
                "sens": 1 if sens in ("1", "buy", "achat") else -1,
                "entree_ts": e, "sortie_ts": s,
                "entree": _flottant(r.get("entree")),
                "sortie": _flottant(r.get("sortie")),
                "volume": _flottant(r.get("volume")) or 1.0,
                "stop": _flottant(r.get("stop")),
                "objectif": _flottant(r.get("objectif")),
            })
    return trades


# ───────────────────── décalage horaire du courtier ─────────────────────

def detecter_decalage(trades, min_trades=60):
    """Déduit le décalage du serveur du courtier — SPEC-LOT5 §1.4.

    C'est l'erreur qui fausse silencieusement toute l'analyse horaire : les
    rapports MetaTrader sont horodatés en heure du serveur, presque jamais en
    UTC. Sans correction, « vos pertes se concentrent à 9 h » désigne la
    mauvaise séance de deux à trois heures.

    MÉTHODE. Une première version tentait de lire l'heure du dernier trade
    avant le week-end : ce signal n'existe pas, un trader ne trade pas jusqu'à
    la cloche. Le signal réel est le CREUX HEBDOMADAIRE : le marché est fermé
    du vendredi 21:00 au dimanche 21:00 UTC, donc aucun trade ne peut y tomber.
    On cherche le décalage qui aligne le creux observé sur la fermeture réelle.

    Retourne (décalage_heures, fiable). Si ce n'est pas fiable, il faut
    DEMANDER à l'utilisateur — jamais deviner en silence.
    """
    instants = [t["entree_ts"] for t in trades if t.get("entree_ts")]
    if len(instants) < min_trades:
        return 0, False

    # Occupation des 168 créneaux de la semaine, en heure déclarée.
    occupation = [0] * 168
    for x in instants:
        occupation[x.weekday() * 24 + x.hour] += 1

    # Fenêtre réellement fermée, en UTC : vendredi 21:00 → dimanche 21:00.
    fermee = {i % 168 for i in range(4 * 24 + 21, 6 * 24 + 21)}

    scores = {}
    for d in range(-12, 13):
        # un créneau déclaré i correspond au créneau UTC (i - d)
        scores[d] = sum(n for i, n in enumerate(occupation)
                        if (i - d) % 168 in fermee)

    meilleur = min(scores, key=lambda d: scores[d])
    valeurs = sorted(scores.values())
    # Fiable si le meilleur décalage est nettement meilleur que le suivant
    # non adjacent, et s'il ne laisse presque aucun trade en zone fermée.
    concurrents = [v for d, v in scores.items() if abs(d - meilleur) > 1]
    second = min(concurrents) if concurrents else valeurs[-1]
    fiable = (scores[meilleur] <= 0.02 * len(instants)
              and scores[meilleur] < 0.5 * max(second, 1))
    return meilleur, fiable


def appliquer_decalage(trades, heures):
    d = timedelta(hours=heures)
    for t in trades:
        for k in ("entree_ts", "sortie_ts"):
            if t.get(k):
                t[k] = t[k] - d
    return trades


# ───────────────────────── risque et résultats ─────────────────────────

def reconstruire_risque(trades):
    """Trois niveaux, le plus fiable d'abord. La méthode retenue est affichée."""
    avec_stop = [t for t in trades if t.get("stop")]
    if len(avec_stop) >= 0.8 * len(trades) and trades:
        for t in trades:
            t["risque"] = abs(t["entree"] - t["stop"]) if t.get("stop") else None
        return "stop_declare"
    pertes = [abs(t["sortie"] - t["entree"]) for t in trades
              if t.get("sortie") and (t["sortie"] - t["entree"]) * t["sens"] < 0]
    if not pertes:
        for t in trades:
            t["risque"] = None
        return "indeterminable"
    mediane = statistics.median(pertes)
    for t in trades:
        t["risque"] = (abs(t["entree"] - t["stop"]) if t.get("stop") else mediane)
    return "risque_estime"


def resultats_r(trades):
    out = []
    for t in trades:
        if not t.get("sortie") or not t.get("risque"):
            continue
        t["r"] = (t["sortie"] - t["entree"]) * t["sens"] / t["risque"]
        out.append(t)
    return out


# ─────────────────────────── mesures ───────────────────────────

def _correlation(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx and dy else 0.0


def _serie_max(rs):
    m = c = 0
    for r in rs:
        c = c + 1 if r < 0 else 0
        m = max(m, c)
    return m


def mesures(trades):
    """Les huit mesures de SPEC-LOT5 §3.2, chacune chiffrée en coût par trade."""
    ts = sorted(resultats_r(trades), key=lambda t: t["entree_ts"])
    n = len(ts)
    if n < 3:
        return {"n": n, "suffisant": False}
    rs = [t["r"] for t in ts]
    gains = [r for r in rs if r > 0]
    pertes = [r for r in rs if r <= 0]
    esperance = sum(rs) / n
    taux = len(gains) / n

    asymetrie = (abs(sum(pertes) / len(pertes)) / (sum(gains) / len(gains))
                 if gains and pertes else None)

    risques = [t["risque"] for t in ts]
    revanche = _correlation(risques[1:], rs[:-1]) if n > 3 else 0.0

    delais_gain, delais_perte = [], []
    for prec, suiv in zip(ts, ts[1:]):
        d = (suiv["entree_ts"] - prec["entree_ts"]).total_seconds() / 60
        (delais_gain if prec["r"] > 0 else delais_perte).append(d)

    par_heure = defaultdict(list)
    par_jour = defaultdict(list)
    for t in ts:
        par_heure[t["entree_ts"].hour].append(t["r"])
        par_jour[t["entree_ts"].weekday()].append(t["r"])

    ouvertes = 0
    for i, t in enumerate(ts):
        for u in ts[i + 1:]:
            if u["entree_ts"] >= (t["sortie_ts"] or u["entree_ts"]):
                break
            if u["symbole"] != t["symbole"] and u["sens"] == t["sens"]:
                ouvertes += 1

    attendue = (math.log(n) / math.log(1 / max(1 - taux, 1e-9))
                if 0 < taux < 1 else 0)

    return {
        "n": n, "suffisant": n >= SEUIL_GLOBAL,
        "esperance": esperance, "taux_reussite": taux,
        "asymetrie": asymetrie,
        "revanche": revanche,
        "delai_apres_gain": statistics.median(delais_gain) if delais_gain else None,
        "delai_apres_perte": statistics.median(delais_perte) if delais_perte else None,
        "par_heure": {h: (sum(v) / len(v), len(v)) for h, v in par_heure.items()},
        "par_jour": {j: (sum(v) / len(v), len(v)) for j, v in par_jour.items()},
        "positions_correlees": ouvertes,
        "serie_pertes_observee": _serie_max(rs),
        "serie_pertes_attendue": attendue,
    }


def constats(m, base_esperance=None):
    """Au plus TROIS constats, classés par coût en R décroissant.

    Un tableau de bord de quarante indicateurs ne change aucun comportement :
    il donne l'impression d'un diagnostic sans en produire.
    """
    if not m.get("suffisant"):
        return [{"titre": "Pas encore assez de trades pour conclure",
                 "detail": f"{m.get('n', 0)} sur {SEUIL_GLOBAL} nécessaires",
                 "cout": 0.0}]
    out = []

    if m["asymetrie"] and m["asymetrie"] > 1.0:
        cout = (m["asymetrie"] - 1.0) * (1 - m["taux_reussite"])
        out.append({
            "titre": "Vous coupez vos gains et laissez courir vos pertes",
            "detail": f"perte moyenne / gain moyen = {m['asymetrie']:.2f}",
            "cout": cout, "cle": "asymetrie"})

    if m["revanche"] < -0.15:
        out.append({
            "titre": "Vous augmentez votre mise après une perte",
            "detail": f"corrélation risque / résultat précédent = {m['revanche']:+.2f}",
            "cout": abs(m["revanche"]) * 0.5, "cle": "revanche"})

    if m["delai_apres_perte"] and m["delai_apres_gain"]:
        if m["delai_apres_perte"] < 0.6 * m["delai_apres_gain"]:
            out.append({
                "titre": "Vous reprenez trop vite après une perte",
                "detail": f"{m['delai_apres_perte']:.0f} min après une perte "
                          f"contre {m['delai_apres_gain']:.0f} min après un gain",
                "cout": 0.10, "cle": "precipitation"})

    for cle, libelle in (("par_heure", "heure"), ("par_jour", "jour")):
        pires = [(k, v) for k, v in m[cle].items()
                 if v[1] >= SEUIL_SEGMENT and v[0] < m["esperance"] - 0.20]
        if pires:
            k, (esp, nb) = min(pires, key=lambda x: x[1][0])
            out.append({
                "titre": f"Vos trades à cette {libelle} perdent",
                "detail": f"{libelle} {k} : {esp:+.2f} R sur {nb} trades, "
                          f"contre {m['esperance']:+.2f} R en moyenne",
                "cout": (m["esperance"] - esp) * nb / m["n"], "cle": cle})

    if m["positions_correlees"] > m["n"] * 0.15:
        out.append({
            "titre": "Vous cumulez des positions corrélées",
            "detail": f"{m['positions_correlees']} chevauchements : votre risque "
                      f"réel dépasse celui que vous croyez prendre",
            "cout": 0.08, "cle": "correlation"})

    if base_esperance is not None:
        ecart = m["esperance"] - base_esperance
        if ecart < -0.10:
            out.append({
                "titre": "Vous faites moins bien que la base sur les mêmes configurations",
                "detail": f"vous {m['esperance']:+.2f} R contre {base_esperance:+.2f} R",
                "cout": abs(ecart), "cle": "ecart_base"})

    out.sort(key=lambda x: -x["cout"])
    return out[:3]
