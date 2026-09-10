# Spécification technique — Lot 2 : le range

Document d'implémentation. Complète le cahier des charges, ne le remplace pas.
Version de stratégie : **`range.v1`** — figée. Toute modification d'une valeur de ce document
crée `range.v2` et laisse `range.v1` et son historique intacts (cahier des charges §15, règle 4).

> **Règle de lecture.** Chaque constante est nommée et rassemblée au §1.3. Aucune valeur
> numérique ne doit apparaître en dur dans le code : toutes proviennent de la table
> `parametre_strategie`, ce qui rend le versionnement effectif et vérifiable.

---

## 1. Fondations

### 1.1 Conventions

| Élément | Règle |
|---|---|
| Horodatage | UTC en base, toujours. Les conversions en heure locale ne servent qu'au critère de séance (§4.7) |
| Bougie | Étiquetée par son **heure d'ouverture**. Une bougie H4 `12:00` couvre `[12:00, 16:00[` |
| Clôture journalière | **17:00 America/New_York**, convention figée. Le fuseau, pas un décalage fixe : le changement d'heure est donc absorbé par la base de fuseaux horaires |
| Semaine | Ouverture dimanche 17:00 New York, clôture vendredi 17:00 New York |
| Prix stockés | **Milieu (mid)**. Le spread est appliqué au moment du calcul de l'exécution (§6) |
| Valeur du pip | 0,0001, sauf paires cotées en JPY : 0,01 |
| Arrondi | Aucun arrondi intermédiaire. Calculs en `numeric`, arrondi au dernier moment pour l'affichage |
| Fuseau des données | Toute bougie est reconstruite depuis M1. Aucun agrégat n'est repris tel quel d'un fournisseur |

### 1.2 Indicateurs — définitions exactes

**True Range**

```
TR_i = max( H_i − L_i , |H_i − C_{i−1}| , |L_i − C_{i−1}| )
```

**ATR (méthode de Wilder, période n = 14)**

```
ATR_n     = moyenne arithmétique des n premiers TR      (amorçage)
ATR_i     = ( (n−1) × ATR_{i−1} + TR_i ) / n            (i > n)
```

L'ATR utilisé pour une détection au barreau `t` est **`ATR_t`**, jamais une valeur postérieure.

**EMA (période p)**

```
α       = 2 / (p + 1)
EMA_p   = moyenne arithmétique des p premières clôtures  (amorçage)
EMA_i   = α × C_i + (1 − α) × EMA_{i−1}
```

**RSI (Wilder, période 14)** — moyennes de gains et pertes lissées comme l'ATR.

**ADX (Wilder, période 14)** — implémentation standard, +DI / −DI puis lissage de DX.

**Amorçage.** Aucun indicateur n'est utilisable avant `AMORCAGE_MIN = 300` bougies clôturées
sur l'unité de temps concernée. Toute détection calculée avant ce seuil est **rejetée avec le
motif `amorcage_insuffisant`** et conservée (cahier des charges §8).

### 1.3 Constantes de `range.v1`

| Nom | Valeur | Rôle |
|---|---|---|
| `ATR_PERIODE` | 14 | Toutes les mesures en unités d'ATR |
| `ZZ_K` | 1,5 | Seuil ZigZag en multiples d'ATR |
| `PIVOTS_MIN` | 4 | Pivots alternés minimum pour un range |
| `TOLERANCE_BORNE` | 0,25 | Écart maximal d'un pivot à sa borne, en ATR |
| `HAUTEUR_MIN` | 1,0 | Hauteur minimale du range, en ATR |
| `HAUTEUR_MAX` | 6,0 | Hauteur maximale du range, en ATR |
| `DUREE_MIN` | 15 | Bougies entre premier et dernier pivot |
| `DUREE_MAX` | 200 | Idem, borne haute |
| `DEBORDEMENT_MAX` | 0,05 | Fraction de clôtures autorisées hors des bornes |
| `PENTE_MAX` | 0,50 | Dérive maximale sur la fenêtre, en fraction de la hauteur |
| `TOUCHE_ZONE` | 0,10 | Distance à une borne valant « touche », en ATR |
| `CASSURE_MIN` | 0,25 | Dépassement de clôture validant une cassure, en ATR |
| `STOP_MARGE` | 0,50 | Marge du stop au-delà de la borne, en ATR |
| `RETOUR_MAX` | 10 | Bougies pour qu'un retour post-cassure soit valide |
| `HORIZON` | 20 | Bougies avant classement en « sans issue » |
| `AMORCAGE_MIN` | 300 | Bougies minimales avant toute détection |
| `SEUIL_ANNONCE` | 0,70 | Fraction du score maximal atteignable requise pour annoncer |

---

## 2. Détection des pivots

### 2.1 Algorithme

ZigZag à seuil adaptatif. Le seuil au barreau `i` vaut `θ_i = ZZ_K × ATR_i`.

```
état      ∈ { recherche_haut, recherche_bas }
extreme   = prix extrême courant
i_extreme = barreau de cet extrême

Pour chaque barreau i, dans l'ordre chronologique :

  si état = recherche_haut :
      si H_i > extreme :
          extreme = H_i ; i_extreme = i
      sinon si (extreme − L_i) ≥ θ_i :
          → confirmer un PIVOT HAUT en i_extreme, CONFIRMÉ AU BARREAU i
          état = recherche_bas ; extreme = L_i ; i_extreme = i

  si état = recherche_bas :  (symétrique, avec L_i et (H_i − extreme))
```

### 2.2 La règle qui décide de la validité de tout le système

> **Un pivot situé au barreau `p` n'existe qu'à partir du barreau `c` où il est confirmé,
> avec `c > p`. Aucun calcul effectué au barreau `t` ne peut utiliser un pivot dont
> `c > t`, même si `p ≤ t`.**

C'est le piège classique du ZigZag : le graphique affiche le pivot à `p`, ce qui donne
l'illusion qu'il était connu à ce moment. Il ne l'était pas.

Chaque pivot est donc stocké avec **deux barreaux** : `barreau_pivot` (`p`) et
`barreau_confirmation` (`c`). Toute requête de détection filtre sur `barreau_confirmation ≤ t`.
Le test point-in-time (§8.1) vérifie précisément ce point.

### 2.3 Amorçage de l'état

L'état initial est déterminé par les `AMORCAGE_MIN` premières bougies : si la clôture de la
dernière est supérieure à celle de la première, l'état démarre en `recherche_haut`, sinon en
`recherche_bas`. Ce choix est sans effet au-delà des premiers pivots et il est déterministe.

---

## 3. Définition du range

### 3.1 Conditions cumulatives

Au barreau `t`, soit `P` la liste des pivots confirmés (`barreau_confirmation ≤ t`) triés
chronologiquement. On considère les `PIVOTS_MIN` derniers pivots, notés `p₁…p₄`.

| # | Condition | Formule |
|---|---|---|
| C1 | **Alternance** | `p₁…p₄` alternent haut/bas ou bas/haut, sans répétition |
| C2 | **Bornes** | `borne_haute` = **maximum** des pivots hauts ; `borne_basse` = **minimum** des pivots bas |
| C3 | **Hauteur** | `HAUTEUR_MIN × ATR_t ≤ (borne_haute − borne_basse) ≤ HAUTEUR_MAX × ATR_t` |
| C4 | **Extension arrière** | `debut` recule tant que `borne_basse − tol ≤ clôture ≤ borne_haute + tol` |
| C5 | **Durée** | `DUREE_MIN ≤ (t − debut) ≤ DUREE_MAX`, mesurée sur la **fenêtre étendue** |
| C6 | **Confinement** | Sur `[debut, t]`, au plus `DEBORDEMENT_MAX` des **clôtures** hors des bornes élargies de `tol` |
| C7 | **Absence de dérive** | Régression linéaire des clôtures : `\|pente × longueur\| ≤ PENTE_MAX × hauteur` |
| C8 | **Touches** | Chaque borne touchée au moins **2 fois** à `TOUCHE_ZONE` près |

> **Correction de conception, issue de la construction.** La première rédaction de ce document
> définissait les bornes comme la **moyenne** des pivots, et exigeait que chacun soit à moins de
> `0,25 ATR` de cette moyenne. Mesuré à l'exécution : **cette condition rejette 62 candidats sur
> 67**, soit plus de 92 %. Elle ne décrivait pas un range.
>
> Un range n'est pas une zone où les sommets sont identiques — c'est une zone dont le prix ne
> parvient pas à sortir. D'où les bornes prises aux **extrêmes**, l'extension arrière de la
> fenêtre qui donne au range sa vraie durée, et la cohésion mesurée en **touches** plutôt qu'en
> égalité des pivots.
>
> Cette correction n'a pas été obtenue en assouplissant un seuil jusqu'à obtenir des résultats,
> mais en corrigeant une définition fausse. La distinction est le sujet même du §8.

Le range est **constitué** au barreau `t_c = barreau_confirmation(p₄)`.

### 3.2 Cycle de vie

| Événement | Effet |
|---|---|
| Constitution | Le range devient actif. Il est enregistré avec ses bornes, figées définitivement |
| Cassure confirmée (§4.2, méthode R2) | Le range passe à `rompu`. **Plus aucune entrée R1 n'est générée** |
| `DUREE_MAX` dépassée sans cassure | Le range passe à `expire` |
| Nouveau pivot hors tolérance | Le range passe à `invalide` |

**Les bornes ne sont jamais recalculées après constitution.** Un range dont les bornes bougent
n'est pas mesurable : ce serait un objet différent à chaque barreau.

---

## 4. Méthodes de trading — `figure × méthode`

Quatre méthodes mesurées séparément (cahier des charges §7). Chacune produit ses propres
détections, son propre score et sa propre statistique.

### 4.1 R1 — Retour sur borne (retour à la moyenne)

| Élément | Règle |
|---|---|
| Déclencheur, achat | Une bougie dont `L_i ≤ borne_basse + TOUCHE_ZONE × ATR`, avec `C_i > borne_basse` |
| Déclencheur, vente | Symétrique sur `borne_haute` |
| Entrée | Clôture de la bougie déclenchante |
| Invalidation | `borne_basse − STOP_MARGE × ATR` (achat) |
| Objectif R1a | Milieu du range : `(borne_haute + borne_basse) / 2` |
| Objectif R1b | Borne opposée |
| Condition | Range à l'état `actif` uniquement |
| Anti-doublon | Une seule détection R1 par borne et par range tant que le prix n'est pas repassé par le milieu |

### 4.2 R2 — Cassure confirmée

| Élément | Règle |
|---|---|
| Déclencheur, achat | `C_i ≥ borne_haute + CASSURE_MIN × ATR` |
| Entrée | Clôture de la bougie de cassure |
| Invalidation | `borne_haute − STOP_MARGE × ATR` — c'est-à-dire **de retour dans le range** |
| Objectif | Projection de la hauteur : `borne_haute + (borne_haute − borne_basse)` |
| Effet secondaire | Le range passe à `rompu` |

### 4.3 R3 — Cassure puis retour

| Élément | Règle |
|---|---|
| Préalable | Une cassure R2 a été déclenchée au barreau `b` |
| Déclencheur | Dans les `RETOUR_MAX` bougies suivant `b`, une bougie dont `L_i ≤ borne_haute + TOUCHE_ZONE × ATR` sans que `C_i < borne_haute` |
| Entrée | Clôture de cette bougie |
| Invalidation | `borne_haute − STOP_MARGE × ATR` |
| Objectif | Identique à R2 |
| Exclusivité | R3 est mesurée indépendamment de R2. Les deux coexistent dans les statistiques, jamais dans un même compte |

### 4.4 Objectifs à ratio fixe — double mesure obligatoire

Pour **chaque** détection des méthodes ci-dessus, deux objectifs supplémentaires sont calculés
et résolus séparément (cahier des charges §11) :

```
risque   = |entrée − invalidation|
objectif_1R5 = entrée ± 1,5 × risque
objectif_2R  = entrée ± 2,0 × risque
```

Une détection produit donc **trois lignes d'issue** : objectif de la méthode, objectif 1,5 R,
objectif 2 R. Même entrée, même invalidation, même horizon.

---

## 5. Score de confluence — formules exactes

Aucun critère ne peut rester en formulation littéraire : deux implémentations donneraient deux
résultats, et le déterminisme (§8.2) serait perdu.

### 5.1 Filtres durs — rejet immédiat

| Filtre | Condition exacte | Motif enregistré |
|---|---|---|
| Contre-tendance | `tendance_UTS = opposée au sens de la détection` (§5.2) | `contre_tendance` |
| Annonce économique | Un événement à fort impact concernant l'une des deux devises tombe dans `[t_entrée, t_entrée + HORIZON × durée_UT]` | `evenement_macro` |
| Objectif irréaliste | `D > 1,50` avec `D = |objectif − entrée| / (ATR_t × √HORIZON)` | `objectif_irrealiste` |
| Amorçage | Moins de `AMORCAGE_MIN` bougies disponibles | `amorcage_insuffisant` |
| Données incomplètes | Une bougie manquante dans la fenêtre de détection | `donnees_incompletes` |

> **Note sur la faisabilité.** Le déplacement typique d'un actif sur `N` bougies évolue comme
> `ATR × √N`, non comme `ATR × N`. La formulation « 1,5 × ATR cumulé » du cahier des charges
> §9.2 est ici précisée en `1,5 × ATR × √HORIZON`, seule forme correcte.

### 5.2 Critères et calculs

**Unité de temps supérieure (UTS) :** H1 → H4 ; H4 → D1 ; D1 → hebdomadaire.

| # | Critère | Calcul exact | Points |
|---|---|---|---|
| 1 | **Tendance UTS** | Haussière si `C > EMA200` **et** `(EMA200_t − EMA200_{t−20}) / ATR_t ≥ 0,10` **et** deux derniers pivots confirmés en sommets et creux croissants. Baissière : symétrique. Sinon neutre | Alignée +2 · Neutre 0 · Opposée → filtre dur |
| 2 | **Zone S/R** | **Neutralisé pour le range** : les bornes *sont* les niveaux (cahier des charges §9.7) | — |
| 3 | **Niveau rond** | `min over k` de `|entrée − k × PAS|` ≤ `0,10 × ATR`, avec `PAS = 0,0050` (`0,50` en JPY) | +1 |
| 4 | **Niveaux de référence** | `entrée` à moins de `0,15 × ATR` du plus haut, plus bas ou clôture de la veille, du plus haut ou plus bas de la semaine précédente, ou de l'ouverture du jour | +1 |
| 5 | **Divergence RSI** | Achat : deux creux pivots confirmés dans les 50 dernières bougies avec `prix₂ < prix₁` et `RSI₂ > RSI₁ + 2` | +1 |
| 6 | **Faisabilité** | `D ≤ 0,75` → +1 ; `0,75 < D ≤ 1,50` → 0 ; `D > 1,50` → filtre dur | +1 / 0 |
| 7 | **Séance** | Heure d'ouverture de la bougie d'entrée convertie en `Europe/London` et `America/New_York`. **+1** si dans l'intersection des séances (Londres 08:00–16:30 locale, New York 08:00–17:00 locale). **−1** si séance de Tokyo (`Asia/Tokyo` 09:00–15:00) ou fenêtre de roulement (`America/New_York` 16:45–18:15) | +1 / −1 |
| 8 | **Calendrier** | Voir filtre dur | — |
| 9 | **Extension** | `|entrée − EMA20| / ATR_t > 2,0` | −1 |
| 10 | **Qualité géométrique** | +1 si ≥ 3 touches sur chaque borne (au-delà du minimum de 2) ; +1 si l'écart maximal des pivots à leur borne ≤ `0,15 × ATR` | 0 à +2 |
| 11 | **Régime** | `ADX(14)` sur l'UT de la détection. **R1** : +1 si `ADX < 20`. **R2/R3** : +1 si `ADX > 25` | +1 |

### 5.3 Normalisation et seuil

```
maximum_atteignable(range) = 2 + 1 + 1 + 1 + 1 + 1 + 2 + 1 = 10
score_normalise            = max(0, points_obtenus) / maximum_atteignable
annoncée                   ⇔ aucun filtre dur ET score_normalise ≥ SEUIL_ANNONCE
```

Le critère 2 est exclu du maximum puisqu'il est neutralisé : c'est l'application directe de la
règle du cahier des charges §9.7, sans laquelle le range serait mécaniquement mieux noté que
les figures qui ne contiennent pas leur propre support.

**Le détail critère par critère est stocké en JSON avec chaque détection.** Sans lui, aucun
rejet n'est explicable à l'utilisateur et aucune statistique n'est reconstructible.

---

## 6. Résolution et coûts

### 6.1 Prix d'exécution

| Opération | Prix |
|---|---|
| Entrée à l'achat | `mid + spread_horaire / 2` |
| Sortie à la vente | `mid − spread_horaire / 2` |
| Vente à découvert | Symétrique |
| Franchissement de l'invalidation | Prix de l'invalidation, **dégradé de `0,5 × spread_horaire`** au titre du glissement |

`spread_horaire` = médiane du spread observé dans les données tick pour cette paire et ce
**créneau horaire de la semaine** (168 créneaux d'une heure). Calculé une fois, versionné,
jamais recalculé après publication d'une détection.

### 6.2 Algorithme de résolution — parcours en M1

```
Entrée  : entrée E, invalidation S, objectif T, sens, t_entrée, HORIZON, unité de temps
Fenêtre : de t_entrée + 1 minute à fin(barreau t_entrée + HORIZON)

Pour chaque bougie M1 dans l'ordre chronologique :
    achat :
        touche_S = (L_m1 ≤ S)
        touche_T = (H_m1 ≥ T)
    vente : symétrique

    si touche_S et touche_T  → issue = "invalide"     (règle conservatrice, §6.3)
    sinon si touche_S        → issue = "invalide"
    sinon si touche_T        → issue = "atteint"
    → sortir de la boucle dès qu'une issue est fixée

Si aucune issue : issue = "sans_issue", sortie à la clôture de la dernière bougie de l'horizon
```

### 6.3 La règle conservatrice, et pourquoi elle est non négociable

Quand invalidation et objectif sont touchés à l'intérieur de la **même bougie M1**, l'ordre réel
est inconnaissable sans données tick. **L'issue est alors toujours comptée comme invalidation.**

Choisir l'inverse, ou tirer au sort, gonflerait les taux de réussite d'une manière invérifiable.
C'est exactement le mécanisme qui rend flatteurs la quasi-totalité des backtests amateurs.
La fréquence de ce cas est **enregistrée et publiée** : c'est une mesure de l'incertitude
résiduelle du système.

### 6.4 Swap de portage

Appliqué à chaque passage de `17:00 America/New_York` où la position est encore ouverte,
**triplé le mercredi** (valeur de règlement du week-end). Taux par paire et par sens, issus
d'une grille versionnée.

```
swap_total = Σ taux_journalier(paire, sens) × jours_portés × facteur_mercredi
```

Sur une détection journalière tenue 20 jours, le swap peut dépasser plusieurs fois le spread.
L'omettre fausse le signe du résultat sur les unités de temps longues.

### 6.5 Résultat

```
risque_prix     = |E − S|
resultat_brut   = (sortie − E) × sens
resultat_net    = resultat_brut − cout_spread − cout_glissement − swap_total
R_brut          = resultat_brut / risque_prix
R_net           = resultat_net  / risque_prix
```

`R_net` est **l'indicateur publié**. `R_brut` n'est affiché qu'à côté de lui (cahier des
charges §12).

Sont également enregistrées les excursions maximales favorable et défavorable en unités de R,
qui permettront plus tard d'évaluer des sorties partielles sans recalculer l'historique.

---

## 7. Schéma de base de données

```sql
CREATE TABLE instrument (
    id                  smallserial PRIMARY KEY,
    symbole             text        NOT NULL UNIQUE,   -- 'EURUSD'
    devise_base         char(3)     NOT NULL,
    devise_cotation     char(3)     NOT NULL,
    valeur_pip          numeric(12,8) NOT NULL,        -- 0.0001 / 0.01
    pas_niveau_rond     numeric(12,8) NOT NULL,        -- 0.0050 / 0.50
    actif               boolean     NOT NULL DEFAULT true
);

CREATE TABLE bougie (
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    unite_temps         text        NOT NULL,          -- 'M1','H1','H4','D1'
    ouverture_ts        timestamptz NOT NULL,
    o                   numeric(12,6) NOT NULL,
    h                   numeric(12,6) NOT NULL,
    l                   numeric(12,6) NOT NULL,
    c                   numeric(12,6) NOT NULL,
    complete            boolean     NOT NULL DEFAULT true,
    source              text        NOT NULL,
    PRIMARY KEY (instrument_id, unite_temps, ouverture_ts)
);
SELECT create_hypertable('bougie','ouverture_ts');

CREATE TABLE spread_horaire (
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    creneau             smallint    NOT NULL CHECK (creneau BETWEEN 0 AND 167),
    spread_median       numeric(12,8) NOT NULL,
    version             text        NOT NULL,
    PRIMARY KEY (instrument_id, creneau, version)
);

CREATE TABLE swap (
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    sens                smallint    NOT NULL CHECK (sens IN (-1,1)),
    taux_journalier     numeric(12,8) NOT NULL,        -- en prix, par unité
    valide_du           date        NOT NULL,
    valide_au           date,
    PRIMARY KEY (instrument_id, sens, valide_du)
);

CREATE TABLE version_strategie (
    id                  text        PRIMARY KEY,       -- 'range.v1'
    figure              text        NOT NULL,          -- 'range'
    methode             text        NOT NULL,          -- 'R1a','R1b','R2','R3'
    empreinte_code      char(64)    NOT NULL,          -- SHA-256 du module de détection
    parametres          jsonb       NOT NULL,
    score_max           smallint    NOT NULL,
    criteres_neutralises text[]     NOT NULL,
    active_le           timestamptz NOT NULL,
    retiree_le          timestamptz
);

CREATE TABLE pivot (
    id                  bigserial   PRIMARY KEY,
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    unite_temps         text        NOT NULL,
    type                text        NOT NULL CHECK (type IN ('haut','bas')),
    barreau_ts          timestamptz NOT NULL,          -- p : où se situe le pivot
    confirmation_ts     timestamptz NOT NULL,          -- c : où il devient connaissable
    prix                numeric(12,6) NOT NULL,
    version_zigzag      text        NOT NULL,
    CHECK (confirmation_ts > barreau_ts)
);
CREATE INDEX ON pivot (instrument_id, unite_temps, confirmation_ts);

CREATE TABLE range_detecte (
    id                  bigserial   PRIMARY KEY,
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    unite_temps         text        NOT NULL,
    constitue_ts        timestamptz NOT NULL,
    borne_haute         numeric(12,6) NOT NULL,        -- figée définitivement
    borne_basse         numeric(12,6) NOT NULL,
    atr_constitution    numeric(12,8) NOT NULL,
    pivots              bigint[]    NOT NULL,
    touches_haut        smallint    NOT NULL,
    touches_bas         smallint    NOT NULL,
    etat                text        NOT NULL CHECK (etat IN ('actif','rompu','expire','invalide')),
    etat_ts             timestamptz
);

CREATE TABLE detection (
    id                  bigserial   PRIMARY KEY,
    version_strategie   text        NOT NULL REFERENCES version_strategie(id),
    range_id            bigint      REFERENCES range_detecte(id),
    instrument_id       smallint    NOT NULL REFERENCES instrument(id),
    unite_temps         text        NOT NULL,
    sens                smallint    NOT NULL CHECK (sens IN (-1,1)),
    entree_ts           timestamptz NOT NULL,
    publiee_ts          timestamptz NOT NULL,          -- horodatage de publication effective
    prix_entree         numeric(12,6) NOT NULL,        -- mid, avant frais
    invalidation        numeric(12,6) NOT NULL,
    objectif_methode    numeric(12,6) NOT NULL,
    objectif_1r5        numeric(12,6) NOT NULL,
    objectif_2r         numeric(12,6) NOT NULL,
    horizon_barreaux    smallint    NOT NULL,
    atr_entree          numeric(12,8) NOT NULL,
    score_points        smallint    NOT NULL,
    score_max           smallint    NOT NULL,
    score_normalise     numeric(4,3) NOT NULL,
    score_detail        jsonb       NOT NULL,          -- critère → points → valeurs mesurées
    statut              text        NOT NULL CHECK (statut IN ('annoncee','ecartee')),
    motif_rejet         text,
    empreinte_prec      char(64)    NOT NULL,
    empreinte           char(64)    NOT NULL UNIQUE,
    CHECK ((statut = 'ecartee') = (motif_rejet IS NOT NULL))
);
CREATE INDEX ON detection (version_strategie, statut, entree_ts);

CREATE TABLE issue (
    detection_id        bigint      NOT NULL REFERENCES detection(id),
    cible               text        NOT NULL CHECK (cible IN ('methode','1r5','2r')),
    resolue_ts          timestamptz NOT NULL,
    resultat            text        NOT NULL CHECK (resultat IN ('atteint','invalide','sans_issue')),
    sortie_ts           timestamptz NOT NULL,
    prix_sortie         numeric(12,6) NOT NULL,
    ambigu_m1           boolean     NOT NULL DEFAULT false,  -- §6.3
    cout_spread         numeric(12,8) NOT NULL,
    cout_glissement     numeric(12,8) NOT NULL,
    cout_swap           numeric(12,8) NOT NULL,
    r_brut              numeric(8,4) NOT NULL,
    r_net               numeric(8,4) NOT NULL,
    excursion_fav       numeric(8,4) NOT NULL,
    excursion_def       numeric(8,4) NOT NULL,
    PRIMARY KEY (detection_id, cible)
);

CREATE TABLE ancrage (
    jour                date        PRIMARY KEY,
    empreinte_tete      char(64)    NOT NULL,
    nb_detections       integer     NOT NULL,
    preuve_externe      jsonb       NOT NULL,          -- références tierces horodatées
    publie_ts           timestamptz NOT NULL
);

CREATE TABLE parametre_strategie (
    version_strategie   text        NOT NULL REFERENCES version_strategie(id),
    nom                 text        NOT NULL,
    valeur              numeric     NOT NULL,
    PRIMARY KEY (version_strategie, nom)
);
```

### 7.1 Calcul de l'empreinte

```
empreinte = SHA256(
    empreinte_prec ‖ version_strategie ‖ instrument ‖ unite_temps ‖ sens ‖
    entree_ts(ISO-8601 UTC) ‖ prix_entree ‖ invalidation ‖ objectif_methode ‖
    score_points ‖ statut ‖ motif_rejet(ou chaîne vide)
)
```

Champs concaténés dans cet ordre exact, séparés par `\x1f`, valeurs numériques en notation
décimale non arrondie. **Les configurations écartées entrent dans la chaîne au même titre que
les annoncées** : sans cela, on pourrait retirer un rejet gênant sans que la chaîne ne le montre.

---

## 8. Tests exigés avant mise en service

### 8.1 Test point-in-time — le plus important du projet

```
1. Calculer l'ensemble des détections sur [T0, T1].
2. Concaténer aux données une période [T1, T2] de bougies réelles.
3. Recalculer les détections sur [T0, T1] uniquement.
4. Les deux ensembles doivent être identiques, empreintes comprises.
```

Variante d'attaque, à exécuter aussi : remplacer `[T1, T2]` par des données **aberrantes**
(prix multipliés par 10). Si une seule détection de `[T0, T1]` change, il existe une fuite
d'information future. Le test échoue et la mise en service est bloquée.

### 8.2 Test de déterminisme

Recalcul complet nocturne de l'historique, comparaison des empreintes stockées.
Toute divergence : **échec de la compilation**, et création obligatoire d'une nouvelle version
de stratégie. Aucune correction silencieuse n'est possible.

### 8.3 Jeu de référence annoté

**60 fenêtres annotées à la main** : 20 ranges valides, 20 quasi-ranges à rejeter (dérive trop
forte, hauteur hors bornes, débordements), 20 sans structure. Le détecteur doit retrouver les 20
premiers et n'en inventer aucun sur les 40 autres. Ce jeu est versionné avec le code.

### 8.4 Cas de résolution construits

| Cas | Attendu |
|---|---|
| Objectif touché, invalidation jamais | `atteint` |
| Invalidation touchée avant l'objectif | `invalide` |
| Les deux dans la même bougie M1 | `invalide`, `ambigu_m1 = true` |
| Ni l'un ni l'autre à l'horizon | `sans_issue`, sortie à la clôture |
| Gap de week-end traversant l'invalidation | `invalide` au **prix de réouverture**, pas au prix de l'invalidation |
| Position tenue un mercredi | Swap triplé ce jour-là |

### 8.5 Test de changement d'heure

Une détection dont l'entrée tombe la semaine précédant et la semaine suivant chaque bascule
horaire, en mars et en novembre : le critère de séance (§5.2, n° 7) doit rester correct dans
les quatre cas. Les décalages entre Londres, New York et Tokyo ne coïncident pas — c'est
précisément là que les implémentations naïves se trompent.

### 8.6 Test de coûts

Un trade construit à la main, coûts calculés sur papier, comparé au calcul du programme.
Écart toléré : zéro.

---

## 9. Critères d'acceptation du lot 2

| # | Critère | Vérification |
|---|---|---|
| 1 | Tous les tests du §8 passent | Intégration continue |
| 2 | ≥ 500 détections historiques résolues sur les 7 paires majeures | Requête |
| 3 | Deux exécutions complètes produisent des empreintes identiques | §8.2 |
| 4 | Chaque détection écartée porte un motif et un score détaillé | Contrainte de base + revue |
| 5 | Aucune constante numérique en dur dans le code | Revue + recherche automatisée |
| 6 | Le backtest walk-forward est produit avec correction de tests multiples | Rapport écrit |
| 7 | Le rapport de décision du §25.1 du cahier des charges est rédigé | Document |

**Le lot 2 n'est pas terminé quand le code fonctionne. Il est terminé quand le résultat est
reproductible par un tiers.**

---

## 10. Ce qui est délibérément exclu de `range.v1`

| Exclu | Motif |
|---|---|
| Apprentissage automatique | Non reproductible, non explicable, surapprentissage garanti |
| Recalibrage automatique des paramètres | Un score qui s'ajuste sur ses propres résultats est surajusté |
| Volume, VWAP | Inexistants sur le change au comptant (cahier des charges §9.3) |
| Sorties partielles, stop suiveur | Méthodes à part entière, à mesurer séparément en `range.v2` |
| Temps réel infra-bougie | Traitement par lots uniquement |
| Bornes de range recalculées | Un objet dont la définition change n'est pas mesurable |


---

## 12. Constats de construction

*Ce que l'exécution a révélé, et qui n'était pas visible sur le papier.*

### 12.1 Le seuil d'annonce de 0,70 est inatteignable

Distribution des scores mesurée sur 232 détections :

```
     0%  ████████████████████ 38
    10%  ██████████████████████████████████ 63
    20%  ████████████████████████████████████████ 73
    30%  ██████████████████ 33
    40%  ██████████ 19
    50%  ███ 6
    ≥70%  aucune
```

**Aucune détection n'atteint 70 % du maximum atteignable.**

La cause est structurelle et elle contredit une décision prise plus tôt dans ce même dossier.
Le cahier des charges §11.1 démontre qu'exiger l'unanimité des critères est stérile — 0,70¹¹ ≈
2 % de survie — puis fixe un seuil de 70 % qui, avec des critères individuellement rares
(niveau rond, divergence, références, régime cohérent), **réintroduit exactement la
quasi-unanimité qu'il venait d'écarter**.

**Aucun seuil n'est ajusté ici.** L'ajuster pour faire apparaître des annonces serait
précisément le geste interdit par le §8.6 : choisir un paramètre au vu de ses résultats.
La conduite prescrite est celle du cahier des charges §31 point 6 — **le seuil est calibré
sur les données réelles, après 400 occurrences**, et cette distribution est la première mesure
qui y servira.

**Réserve honnête :** ce constat porte sur des données synthétiques, où la tendance, les
divergences et les niveaux ronds sont plus rares que sur un marché réel. L'ordre de grandeur
du problème est établi ; son ampleur exacte ne le sera que sur données réelles.

### 12.2 Un critère négatif doit afficher les points qu'il retire

Le critère de séance pouvait retirer un point tout en affichant `0` dans le détail montré à
l'utilisateur. L'explication donnée était donc fausse.

**Règle : le détail du score affiche les points RÉELLEMENT appliqués, négatifs compris.**
Un produit dont l'argument est l'explicabilité ne peut pas se permettre une explication
approximative — c'est la même exigence que pour les chiffres publiés.


### 12.3 La dégradation absolue ne mesure pas le surajustement

*Constat d'exécution, sur validation séquentielle en 5 plis.*

| Jeu | Espérance calibrée | Hors échantillon | Dégradation |
|---|---|---|---|
| Score **de bruit** | +0,081 R | **+0,034 R** | +0,047 |
| Score **réellement prédictif** | +0,337 R | **+0,166 R** | **+0,171** |

**Le score prédictif dégrade quatre fois plus en valeur absolue que le score de
bruit.** Retenir la dégradation comme critère de surajustement aurait donc conduit
à écarter le seul score qui fonctionne.

La raison est mécanique : un score réellement prédictif part de plus haut, il a
donc plus de marge pour retomber. La dégradation mesure la hauteur du départ
autant que la fragilité.

> **Critère retenu : lire l'espérance HORS ÉCHANTILLON, jamais la dégradation.**
> Un score de bruit retombe à zéro (+0,03 R) ; un score prédictif conserve une
> valeur nette (+0,17 R). C'est la seule séparation propre.

La dégradation reste affichée pour information, jamais comme critère de décision.

### 12.4 Ce que le backtest honnête produit

Sur données synthétiques, la chaîne complète donne :

```
espérance nette          −0,190 R sur 2 239 détections
Sharpe par trade         −0,134
seuil dû au test multiple  0,039  (18 séries testées)
Sharpe déflaté             0,0 %  — NON significatif
validation séquentielle  calibré −0,078 R → hors échantillon −0,172 R
seuils par pli           0,15 · 0,35 · 0,20 · 0,35 · 0,35  (INSTABLES)
VERDICT                  NÉGATIF
```

L'instabilité des seuils retenus d'un pli à l'autre est en soi un signal :
un seuil qui change à chaque période n'est pas un seuil, c'est du bruit calibré.
