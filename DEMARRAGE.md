# Démarrage — les étapes, dans l'ordre

Aucune connaissance technique supposée. Compte **30 minutes** pour les étapes 1
à 4, puis un téléchargement qui tourne tout seul.

---

## Étape 1 — Installer Python

Ouvre un terminal :
- **Mac** : Spotlight (loupe en haut à droite) → tape `Terminal`
- **Windows** : menu Démarrer → tape `PowerShell`
- **Linux** : Ctrl + Alt + T

Tape :

```
python3 --version
```

**Si tu vois `Python 3.11` ou plus** → passe à l'étape 2.
**Sinon** → va sur [python.org/downloads](https://www.python.org/downloads/),
télécharge, installe. Sur Windows, **coche « Add Python to PATH »** pendant
l'installation. Ferme le terminal, rouvre-le, retape la commande.

---

## Étape 2 — Récupérer le projet

```
git clone https://github.com/Damien-73/moi.git
cd moi
git checkout claude/trading-app-discussion-jzalrz
```

**Si `git` n'existe pas** : va sur la page du dépôt, bouton vert **Code** →
**Download ZIP**, décompresse, et ouvre le dossier dans le terminal avec
`cd chemin/vers/le/dossier`.

---

## Étape 3 — Vérifier que tout fonctionne

```
cd app
python3 tests/test_forexlab.py
python3 tests/test_lot2.py
```

Tu dois voir `OK` deux fois. **Si un test échoue, arrête-toi et envoie-moi le
message** — c'est le test qui a raison, pas le code.

---

## Étape 4 — Voir le produit tourner

```
python3 tout.py
```

Données synthétiques, mais toute la chaîne s'exécute. À la fin, ouvre
`app/data/site/index.html` dans ton navigateur : ce sont les écrans.

```
python3 reel.py
```

Cette fois sur de **vraies** bougies EUR/USD (2017-2018).

```
python3 replication.py
```

Le même moteur sur **trois périodes indépendantes**. C'est le résultat le plus
solide dont on dispose aujourd'hui.

---

## Étape 5 — Le vrai travail : télécharger les données

**Commence petit, pour vérifier que la connexion fonctionne :**

```
python3 telecharger.py EURUSD 2025-01-01 2025-04-01
```

Environ **5 minutes**. Tu dois voir des lignes défiler du type
`2160/2160 heures · 92000 bougies`.

- **Si ça marche** → passe à la commande longue ci-dessous.
- **Si ça échoue** → copie-colle-moi le message d'erreur, je corrige.

**Puis la vraie série, 2 ans :**

```
python3 telecharger.py EURUSD 2024-01-01 2026-01-01
```

Environ **45 minutes** (8 téléchargements en parallèle).
**Tu peux l'interrompre à tout moment** avec Ctrl + C : relancer exactement la
même commande reprend là où ça s'était arrêté.

---

## Étape 6 — L'analyse réelle

```
python3 analyser.py EURUSD H1
python3 tout.py EURUSD H1
```

Le second te rend un **verdict** : positif, nul ou négatif, avec la conduite à
tenir dans chaque cas — écrite avant qu'on connaisse le chiffre.

---

## Étape 7 — Élargir, si le premier passage tient

Plus de paires, c'est plus d'occurrences, donc des conclusions plus solides.
Il en faut **2 400** pour affirmer un avantage de 2 points ; un an sur une seule
paire n'en donne que quelques centaines.

```
python3 telecharger.py GBPUSD 2024-01-01 2026-01-01
python3 telecharger.py USDJPY 2024-01-01 2026-01-01
python3 telecharger.py AUDUSD 2024-01-01 2026-01-01
```

---

## Ce que tu m'envoies

Copie-colle **toute la sortie de `python3 tout.py EURUSD H1`**. Elle contient
le nombre de détections, l'espérance nette, le Sharpe déflaté, la validation
séquentielle et le verdict. C'est tout ce qu'il me faut pour la suite.

---

## Si quelque chose bloque

| Message | Cause | Solution |
|---|---|---|
| `python3: command not found` | Python absent ou hors du PATH | Refaire l'étape 1. Sur Windows, essayer `python` au lieu de `python3` |
| `No such file or directory` | Mauvais dossier | `cd app` depuis le dossier `moi` |
| `Tunnel connection failed` / `403` | Réseau ou pare-feu bloquant Dukascopy | Essayer depuis une autre connexion, ou me le dire |
| Le téléchargement s'arrête seul | Coupure réseau | Relancer **la même commande** : il reprend tout seul |
| `ModuleNotFoundError: backtesting` | Paquet optionnel absent | `pip3 install backtesting` — utile seulement pour `reel.py` |

Le noyau (`app/forexlab/`) n'a **aucune dépendance** : Python seul suffit.

---

## En une phrase

> Étapes 1 à 4 : trente minutes, tu vois le produit tourner.
> Étape 5 : quarante-cinq minutes qui tournent sans toi.
> Étape 6 : le verdict.
