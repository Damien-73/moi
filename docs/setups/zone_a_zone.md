# Setup 1 — « zone à zone » H1

Statut : brouillon — in-sample uniquement (2014–2022). Le verrou out-of-sample exige la ligne
de statut « FIGÉ », qui ne sera écrite qu'après ton accord (étape 5).

Écrit AVANT le code (règle 5). Toute modification de ce document après un test = un nouvel
essai, journalisé dans `results/trials.csv`.

## Idée en une phrase

Le prix revient pour la première fois sur une zone où il a fait demi-tour, la rejette (la bougie
clôture en dehors), et il y a assez de place jusqu'à la zone opposée suivante pour viser 2 R.

## Données

- Bougies H1 en prix milieu `(bid + ask) / 2`, notées pour la bougie `t` : `O_t, H_t, L_t, C_t`.
- Une bougie n'est connue qu'à sa clôture. Toute grandeur indicée `t` n'utilise que les bougies `≤ t`.

## Paramètres (4, valeurs fixées a priori, non optimisées)

| symbole | rôle | valeur |
|---|---|---|
| `k` | force d'un pivot (bougies de chaque côté) | 3 |
| `w` | épaisseur d'une zone, en ATR | 0,5 |
| `b` | marge du stop au-delà de la zone, en ATR | 0,2 |
| `n` | période de l'ATR | 14 |

Imposé par le projet, donc pas un paramètre : R/R = 2 (TP = entrée + 2 × risque).

## Définitions

**ATR.** `TR_t = max(H_t, C_{t−1}) − min(L_t, C_{t−1})` ; `ATR_t = moyenne(TR_{t−n+1} … TR_t)`.

**Pivot bas en `i`** : `L_i < min(L_{i−k} … L_{i−1})` et `L_i ≤ min(L_{i+1} … L_{i+k})`.
Il n'est **confirmé qu'à la clôture de la bougie `c = i + k`** (sinon on utiliserait le futur).

**Pivot haut en `i`** : `H_i > max(H_{i−k} … H_{i−1})` et `H_i ≥ max(H_{i+1} … H_{i+k})`, confirmé en `c = i + k`.

**Zone de demande** (créée en `c` par un pivot bas) : `[bas, haut] = [L_i, L_i + w · ATR_c]`.
**Zone d'offre** (créée en `c` par un pivot haut) : `[bas, haut] = [H_i − w · ATR_c, H_i]`.

**Cycle de vie d'une zone** (examiné à partir de la bougie `c + 1`, après l'évaluation du signal de la bougie) :
- *cassée* à la première bougie qui clôture au-delà : `C_t < bas` (demande) ou `C_t > haut` (offre) ;
- *consommée* à son premier contact : `L_t ≤ haut` (demande) ou `H_t ≥ bas` (offre),
  qu'il y ait signal ou non. Une zone ne sert qu'une fois.
- Une zone cassée ou consommée n'est plus active.

## Signal acheteur à la clôture de la bougie `t`

1. `t ≥ n` (ATR disponible).
2. Au moins une zone de demande active est touchée : `L_t ≤ haut`. Si plusieurs, on retient
   celle dont le `haut` est le plus élevé (toutes les zones touchées sont consommées).
3. Rejet : `C_t > haut` de la zone retenue.
4. Stop : `SL = bas − b · ATR_t`. Risque estimé : `R_est = C_t − SL`.
5. Place jusqu'à la zone opposée : soit `S` = plus petit `bas` des zones d'offre actives
   au début de la bougie `t` avec `bas > C_t`. Condition : pas de telle zone, ou `S − C_t ≥ 2 · R_est`.

## Signal vendeur (symétrique)

Zone d'offre active touchée (`H_t ≥ bas`, on retient le `bas` le plus bas), rejet `C_t < bas`,
`SL = haut + b · ATR_t`, `R_est = SL − C_t`, place : plus grand `haut` des zones de demande
actives au début de la bougie `t` avec `haut < C_t` doit vérifier `C_t − haut ≥ 2 · R_est`.

Si un signal acheteur et un signal vendeur apparaissent sur la même bougie : aucun signal.

## Exécution (moteur commun)

- Heure du signal = clôture de la bougie `t`. Entrée à l'ouverture de la minute suivante
  (achat à l'ask, vente au bid, + 0,3 pip de glissement). Abandon si cette minute arrive plus
  de 15 min après le signal.
- Sortie simple : SL ci-dessus, TP = entrée réelle ± 2 × (distance entrée réelle → SL).
- Variante testée APRÈS : TP partiels 1 R / 2 R / 3 R (un tiers chacun) + stop au point d'entrée après TP1.
- Une seule position à la fois par paire. Pas de durée maximale.
- Filtre annonces : non appliqué (pas d'historique fiable du calendrier disponible) — limite notée.
