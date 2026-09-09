# Spécification technique — Catalogue des figures (lots 8 et 14)

Complète `SPEC-LOT2.md`, dont elle reprend le vocabulaire, les constantes et la règle de
confirmation des pivots. Chaque figure est une **version de stratégie** à part entière.

> **Rappel non négociable** (`SPEC-LOT2.md` §2.2) : un pivot au barreau `p` n'existe qu'à partir
> de son barreau de confirmation `c > p`. Toute condition ci-dessous ne porte que sur des pivots
> dont `c ≤ t`.

---

## 1. Vocabulaire commun

| Notation | Sens |
|---|---|
| `P1…Pn` | Pivots confirmés, du plus ancien au plus récent, alternés haut/bas |
| `A` | `ATR(14)` sur l'unité de temps de la détection, au barreau d'évaluation |
| `t_c` | Barreau de confirmation de la figure : celui où la dernière condition devient vraie |
| `L` | Longueur de la figure, en bougies, du premier au dernier pivot |

**Constantes communes** — table `parametre_strategie`, jamais en dur.

| Nom | Valeur | Rôle |
|---|---|---|
| `TOL_NIVEAU` | 0,25 A | Deux extrêmes sont « au même niveau » en deçà |
| `AMPLITUDE_MIN` | 1,0 A | Amplitude minimale d'une figure exploitable |
| `CASSURE_MIN` | 0,25 A | Dépassement de clôture validant une cassure |
| `STOP_MARGE` | 0,50 A | Marge du stop au-delà du niveau structurel |
| `L_MIN` / `L_MAX` | 10 / 200 | Bornes de longueur |
| `RETOUR_MAX` | 10 | Bougies pour qu'un retour post-cassure reste valide |
| `HORIZON` | 20 | Bougies avant classement en « sans issue » |

**Méthodes communes**, mesurées séparément pour chaque figure :

| Code | Entrée |
|---|---|
| `M1` | À la clôture de la bougie de cassure |
| `M2` | Au retour sur le niveau cassé, dans les `RETOUR_MAX` bougies |
| `M3` | À la clôture de la bougie **suivant** la cassure, si elle confirme |

Et pour chaque méthode, **trois objectifs résolus séparément** : projection de la figure,
1,5 R, 2 R (`SPEC-LOT2.md` §4.4).

---

## 2. Figures de retournement

### 2.1 Double creux — `double_creux.v1`

| | |
|---|---|
| **Pivots** | `P1` bas, `P2` haut, `P3` bas |
| **Niveau des creux** | `\|P3 − P1\| ≤ TOL_NIVEAU` |
| **Amplitude** | `P2 − max(P1,P3) ≥ AMPLITUDE_MIN` |
| **Longueur** | `L_MIN ≤ L ≤ L_MAX` |
| **Encolure** | `N = P2` |
| **Confirmation `t_c`** | Clôture `> N + CASSURE_MIN` |
| **Invalidation** | `min(P1,P3) − STOP_MARGE` |
| **Objectif** | `N + (N − min(P1,P3))` |
| **Critères neutralisés** | n° 2 — le creux **est** le support |
| **Score maximal** | 10 |

**Double sommet** — `double_sommet.v1` : strictement symétrique, sens inversé.

### 2.2 Triple creux — `triple_creux.v1`

Identique au double creux avec `P1, P3, P5` bas et `P2, P4` hauts.
Conditions supplémentaires : les trois creux dans un fuseau de `TOL_NIVEAU`, et
`\|P4 − P2\| ≤ 0,5 A` (encolure sensiblement horizontale). Encolure `N = max(P2,P4)`.

**Triple sommet** — symétrique.

### 2.3 Épaule-tête-épaule — `ete.v1`

| | |
|---|---|
| **Pivots** | `P1` haut (épaule gauche), `P2` bas, `P3` haut (tête), `P4` bas, `P5` haut (épaule droite) |
| **Tête dominante** | `P3 − max(P1,P5) ≥ 0,5 A` |
| **Symétrie des épaules** | `\|P5 − P1\| ≤ 0,5 A` |
| **Encolure** | Droite passant par `(P2, P4)`. Sa valeur au barreau `t` est notée `N(t)` |
| **Pente de l'encolure** | `\|N(P4) − N(P2)\| ≤ 0,75 A` — au-delà, la figure n'est pas exploitable |
| **Symétrie temporelle** | `0,5 ≤ (barreau P5 − barreau P3) / (barreau P3 − barreau P1) ≤ 2,0` |
| **Confirmation `t_c`** | Clôture `< N(t) − CASSURE_MIN` |
| **Objectif** | `N(t_c) − (P3 − N(barreau P3))` |
| **Critères neutralisés** | Aucun |
| **Score maximal** | 12 |

**Deux invalidations, mesurées comme deux méthodes distinctes** — c'est un débat classique que
personne n'a chiffré :

| Variante | Invalidation | Effet attendu |
|---|---|---|
| `ete.large` | `P3 + STOP_MARGE` (sommet de la tête) | Peu d'invalidations, mais risque élevé donc R faible |
| `ete.serree` | `P5 + STOP_MARGE` (sommet de l'épaule droite) | Plus d'invalidations, mais R nettement meilleur |

**Épaule-tête-épaule inversée** — `ete_inversee.v1` : symétrique.
Critère n° 2 neutralisé (la tête **est** le support).

---

## 3. Figures de continuation et de compression

### 3.1 Triangle symétrique — `triangle_sym.v1`

| | |
|---|---|
| **Pivots** | Au moins 4 alternés, dont 2 hauts et 2 bas |
| **Convergence** | Sommets strictement décroissants **et** creux strictement croissants |
| **Compression** | `largeur(dernier) ≤ 0,5 × largeur(premier)`, largeur mesurée entre les deux droites |
| **Amplitude initiale** | `largeur(premier) ≥ AMPLITUDE_MIN` |
| **Apex** | Intersection des deux droites, au barreau `t_apex` |
| **Fenêtre valide** | `t_c ≤ barreau(P1) + 0,75 × (t_apex − barreau(P1))`. **Au-delà de 75 % de la distance à l'apex, la figure est écartée** : la compression y devient du bruit |
| **Confirmation** | Clôture au-delà d'une des deux droites de `CASSURE_MIN` |
| **Invalidation** | Droite opposée, à la valeur qu'elle prend au barreau d'entrée |
| **Objectif** | `entrée ± largeur(premier)` |
| **Critères neutralisés** | Aucun |
| **Score maximal** | 12 |

### 3.2 Triangle ascendant — `triangle_asc.v1`

Sommets **alignés** (tous dans `TOL_NIVEAU` de leur moyenne), creux **strictement croissants**.
Résistance `R` = moyenne des sommets. Confirmation : clôture `> R + CASSURE_MIN`.
Invalidation : dernier creux `− STOP_MARGE`. Objectif : `R + largeur(premier)`.
**Critère n° 2 neutralisé** — les sommets alignés *sont* la résistance. Score maximal 10.

**Triangle descendant** — `triangle_desc.v1` : symétrique.

### 3.3 Biseau montant — `biseau_montant.v1`

*Figure de retournement baissière, malgré son orientation haussière.*

Sommets croissants **et** creux croissants, mais **convergents** :
`pente(creux) > pente(sommets)`, et `largeur(dernier) ≤ 0,6 × largeur(premier)`.
Confirmation : clôture sous la droite des creux, de `CASSURE_MIN`.
Invalidation : dernier sommet `+ STOP_MARGE`. Objectif : `entrée − largeur(premier)`.
Score maximal 12.

**Biseau descendant** — `biseau_descendant.v1` : symétrique, haussier.

### 3.4 Drapeau — `drapeau.v1`

| | |
|---|---|
| **Impulsion** | Mouvement net `≥ 3 A` en `≤ 10` bougies, sans retracement supérieur à `0,5 A` |
| **Consolidation** | 5 à 20 bougies, contenue dans un canal de largeur `≤ 1,5 A`, incliné **contre** l'impulsion |
| **Retracement** | `≤ 50 %` de l'impulsion |
| **Confirmation** | Clôture au-delà du canal, dans le sens de l'impulsion, de `CASSURE_MIN` |
| **Invalidation** | Borne opposée du canal `− STOP_MARGE` |
| **Objectif** | `entrée ± amplitude de l'impulsion` |
| **Critères neutralisés** | **n° 1 — la figure n'existe que dans une tendance** |
| **Score maximal** | 10 |

### 3.5 Fanion — `fanion.v1`

Identique au drapeau, sauf la consolidation : **convergente** au lieu d'être parallèle
(sommets décroissants et creux croissants), et plus courte, 5 à 15 bougies.
Critère n° 1 également neutralisé. Score maximal 10.

### 3.6 Rectangle — `range.v1`

Défini intégralement dans `SPEC-LOT2.md` §3. Critère n° 2 neutralisé, score maximal 10.

---

## 4. Structures hors catalogue chartiste

*Elles ne sont pas des « figures » au sens classique, mais elles sont fréquentes, objectivables,
et fournissent une puissance statistique élevée. Elles servent aussi de référence contre laquelle
comparer les figures : **si une figure ne bat pas une simple cassure de niveau, elle n'apporte
rien.***

### 4.1 Cassure de niveau — `cassure_niveau.v1`

Niveau construit par regroupement de pivots (`SPEC-LOT2.md` §5.2, critère 2) : au moins
3 pivots dans un fuseau de `0,5 A`. Confirmation : clôture au-delà de `CASSURE_MIN`.
Invalidation : niveau `∓ STOP_MARGE`. Objectif : `entrée ± 2 × (amplitude moyenne des rejets
antérieurs sur ce niveau)`. Critère n° 2 neutralisé. Score maximal 10.

### 4.2 Retour sur moyenne en tendance — `pullback_tendance.v1`

Tendance établie (critère 1 satisfait à `+2`), puis retour du prix à moins de `0,3 A` de
l'`EMA20`, sans clôture au-delà de l'`EMA50`. Entrée à la clôture de la bougie de reprise.
Invalidation : extrême de la bougie de retour `∓ STOP_MARGE`. Objectif : dernier extrême de la
tendance. **Critère n° 1 neutralisé.** Score maximal 10.

---

## 5. Lot 8 — les figures à livrer en premier

| Priorité | Figures | Motif |
|---|---|---|
| 1 | `range`, `cassure_niveau`, `pullback_tendance` | Les plus fréquentes : puissance statistique atteinte en quelques mois |
| 2 | `double_creux`, `double_sommet`, `triangle_asc`, `triangle_desc` | Objectivables, fréquence moyenne |
| 3 | `ete.large`, `ete.serree`, `ete_inversee`, `triangle_sym` | Les plus connues du public, donc les plus recherchées |
| 4 | `drapeau`, `fanion`, `biseau_montant`, `biseau_descendant` | Complètent la couverture |

Soit **16 versions de stratégie**, chacune × 3 méthodes × 3 objectifs = **144 séries
statistiques distinctes**. C'est précisément pourquoi la correction de tests multiples
(`CAHIER-DES-CHARGES.md` §9.1) n'est pas optionnelle.

---

## 6. Lot 14 — étendre le catalogue

**Procédure d'ajout, sans exception :**

1. Écrire la définition géométrique dans ce document, avec ses constantes nommées.
2. Déclarer les critères de score que la figure satisfait d'office, et le score maximal ajusté.
3. Ajouter 10 fenêtres annotées à la main au jeu de référence : 5 valides, 5 à rejeter.
4. **Pré-enregistrer publiquement la stratégie avant d'observer le moindre résultat**
   (`CAHIER-DES-CHARGES.md` §8.6).
5. Publier après 100 occurrences, sous la mention « provisoire ».

**Interdit :** ajouter une figure parce qu'une autre ne donne pas de bons résultats.
C'est la définition du test multiple, et c'est ainsi qu'on fabrique un avantage qui n'existe pas.

---

## 7. Figures écartées, et pourquoi

| Figure | Motif du rejet |
|---|---|
| Tasse avec anse | Aucune définition géométrique consensuelle. Deux implémentations donneraient deux résultats |
| Sommet et creux arrondis | Idem : la « rondeur » n'est pas objectivable sans lissage arbitraire |
| Élargissements (mégaphones) | Trop rares pour atteindre un seuil de publication, même sur 28 paires |
| Figures en chandeliers (marteau, avalement, doji) | Une seule bougie : indissociables du bruit sur données de change, et fortement dépendantes de l'heure de clôture retenue |
| Vagues d'Elliott, Gann | Non déterministes : le comptage dépend de l'analyste. Incompatibles avec le principe fondateur |

**Ces rejets sont publiés sur le site.** Expliquer ce qu'on refuse de mesurer, et pourquoi, est
une information que personne ne fournit — et c'est un contenu de référencement à part entière.
