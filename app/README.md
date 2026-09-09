# Lot 1 — le noyau

Première brique de l'application. Elle ne détecte encore aucune figure : elle
met en place **les fondations et les garde-fous** sans lesquels tous les
chiffres publiés plus tard seraient faux.

> **Décision d'ingénierie.** Ce lot n'utilise **aucune bibliothèque externe** et
> stocke les données dans **SQLite**, inclus avec Python. Ni Docker, ni base de
> données à installer, ni dépendance à mettre à jour. Le passage à
> PostgreSQL + TimescaleDB interviendra au lot 3, quand le service deviendra
> public et multi-utilisateur. Le SQL est volontairement standard pour que
> cette migration soit mécanique.

---

## Démarrer — 5 minutes, aucun prérequis

### 1. Vérifier que Python est installé

Ouvre un terminal et tape :

```
python3 --version
```

Il doit afficher `Python 3.11` ou plus. Sinon : télécharge-le sur
[python.org](https://www.python.org/downloads/) et relance.

### 2. Lancer les tests

Depuis le dossier `app` :

```
python3 tests/test_forexlab.py
```

Attendu : `Ran 25 tests` puis `OK`. Si un seul test échoue, ne va pas plus loin
— c'est le test qui a raison.

### 3. Lancer la démonstration

```
python3 demo.py
```

Elle fabrique une série de 20 000 bougies, les stocke, les agrège en H1, H4 et
journalier, calcule les indicateurs, détecte les pivots et exécute le test
point-in-time. Tu dois voir `✓ aucun effet` deux fois.

---

## Ce que fait chaque fichier

| Fichier | Rôle |
|---|---|
| `forexlab/calendrier.py` | Conventions de temps : journée qui clôture à 17:00 New York, alignement des bougies, ouverture du marché |
| `forexlab/indicateurs.py` | ATR de Wilder, EMA, RSI, ADX — définitions exactes de `SPEC-LOT2.md` §1.2 |
| `forexlab/pivots.py` | ZigZag à seuil ATR, avec la règle de confirmation (voir ci-dessous) |
| `forexlab/agregation.py` | Reconstruction de H1, H4 et journalier depuis les bougies M1 |
| `forexlab/stockage.py` | Base SQLite : schéma, écriture, lecture |
| `forexlab/ingestion.py` | Lecture des fichiers M1 (HistData, CSV générique) |
| `forexlab/determinisme.py` | Empreintes canoniques et **harnais point-in-time** |
| `tests/test_forexlab.py` | 25 tests |
| `demo.py` | Démonstration de bout en bout |

---

## Les trois choses à comprendre avant de continuer

### 1. Un pivot n'est pas connu quand le graphique l'affiche

C'est le piège qui invalide la majorité des systèmes chartistes automatisés.

Un creux se situe à la bougie 100. Mais on ne sait qu'il s'agissait d'un creux
qu'à la bougie 104, quand le prix est remonté suffisamment pour le confirmer.
Le graphique, lui, dessine le pivot à la bougie 100 — ce qui donne l'illusion
qu'il était connu à ce moment.

Chaque pivot porte donc **deux numéros de bougie** : où il se trouve, et où il
devient connaissable. Tout calcul filtre sur le second. La démonstration
affiche ce délai : il va de 1 à 8 bougies.

Un système qui ignore cette distinction produit des résultats **spectaculaires
et faux**, sans que rien ne le signale.

### 2. Le test point-in-time est le test le plus important du projet

Principe : on calcule les résultats sur la première moitié des données, puis on
recommence après avoir collé **des données absurdes** après la coupure (prix
multipliés par dix). Si un seul résultat de la première moitié change, c'est
qu'une information future a fui dans le calcul.

Le fichier de tests contient aussi la **contre-épreuve** : un calcul
volontairement fautif, qui doit faire échouer le harnais. Un test qui ne peut
pas échouer ne prouve rien.

### 3. Le changement d'heure

La journée de négociation clôture à 17:00 **heure de New York**, pas à une
heure UTC fixe. Deux fois par an, la journée dure 23 ou 25 heures. Le code
raisonne sur le fuseau horaire, jamais sur un décalage figé — c'est vérifié sur
deux années complètes.

Attention aussi au format HistData : ses fichiers sont horodatés en heure de
l'Est **sans** changement d'heure, ce qui n'est pas le fuseau
`America/New_York`. Le fuseau du fichier source est donc un paramètre
obligatoire de l'import, jamais deviné.

---

## Charger de vraies données

1. Télécharge un fichier M1 sur [histdata.com](https://www.histdata.com)
   (gratuit, format « ASCII M1 »), place-le dans `app/data/`.
2. Puis :

```python
from forexlab import ingestion, agregation, stockage

bougies, lues = ingestion.lire_histdata("data/DAT_ASCII_EURUSD_M1_2025.csv",
                                        fuseau="EST_FIXE")
print(f"{len(bougies)} bougies retenues sur {lues} lignes")

manquantes = ingestion.trous(bougies)
print(f"{len(manquantes)} minutes manquantes pendant les heures d'ouverture")

cx = stockage.ouvrir("data/forexlab.db")
stockage.enregistrer_bougies(cx, "EURUSD", "M1", bougies, "histdata")
for unite in ("H1", "H4", "D1"):
    stockage.enregistrer_bougies(cx, "EURUSD", unite,
                                 agregation.agreger(bougies, unite), "agregat")
```

---

## Critères d'acceptation du lot 1

| # | Critère | État |
|---|---|---|
| 1 | Les bougies M1 se chargent et se relisent à l'identique | ✅ |
| 2 | H1, H4 et journalier sont reconstruits depuis M1, jamais repris d'un fournisseur | ✅ |
| 3 | Les indicateurs sont conformes aux définitions de `SPEC-LOT2.md` §1.2 | ✅ |
| 4 | Les pivots portent leur bougie de confirmation, toujours postérieure | ✅ |
| 5 | Le test point-in-time passe, y compris avec des données futures aberrantes | ✅ |
| 6 | La contre-épreuve échoue bien sur un calcul fautif | ✅ |
| 7 | Les empreintes sont stables et sensibles au dernier chiffre | ✅ |
| 8 | Le changement d'heure est traité, vérifié sur deux ans | ✅ |
| 9 | Aucune constante numérique en dur — table de paramètres | ⬜ lot 2 |
| 10 | Recalcul nocturne complet en intégration continue | ⬜ lot 3 |

---

## Ensuite

**Lot 2** — détection du range, résolution en M1, modèle de coûts.
Tout est spécifié dans `../SPEC-LOT2.md`, formule par formule.
