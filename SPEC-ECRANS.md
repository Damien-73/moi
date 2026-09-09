# Spécification des écrans

Complète `SPEC-DESIGN.md`, qui fixe le système visuel. Ce document fixe **la structure et le
contenu** de chaque écran. Les schémas sont des maquettes de structure, non des dessins :
la mise en forme suit `SPEC-DESIGN.md`.

> **Rappel de la règle du chiffre unique** : chaque écran répond à une seule question, par un
> seul chiffre en grand, **toujours accompagné de son terme de comparaison et de sa taille
> d'échantillon**.

---

## Écran 1 — Registre en direct  ·  page d'accueil  ·  public

```
┌───────────────────────────────────────────────────────────────────────┐
│  [logo]                              Registre  Écartées  Figures  Preuve │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   Nous publions chaque détection avant d'en connaître l'issue.        │
│   Y compris celles qui échouent.                                      │
│                                                                       │
│              7                    +0,08 R              −0,21 R        │
│     annoncées aujourd'hui      annoncées, net       groupe témoin     │
│                                 n = 1 840            n = 14 600       │
│                                                                       │
│   ─────────────────────────────────────────────────────────────────   │
│                                                                       │
│   ┌─ EUR/USD · H4 · Double creux ──────── ANNONCÉE · 82 % ─────────┐  │
│   │  [graphique : 3 lignes, aucun indicateur]                      │  │
│   │  Entrée 1,0812  Invalidation 1,0774  Objectif 1,0869           │  │
│   │  Publiée 14/03 12:00 UTC · empreinte a3f9… · ✓ ancrée          │  │
│   │  ● en cours — 14 bougies restantes                             │  │
│   └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│   ┌─ GBP/USD · D1 · Range ──────────────── ANNONCÉE · 71 % ────────┐  │
│   │  ✓ objectif atteint  ·  +0,97 R net  (+1,08 R brut)            │  │
│   └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│   ┌─ USD/JPY · H4 · ETE ────────────────── ANNONCÉE · 74 % ────────┐  │
│   │  ✗ invalidée  ·  −1,00 R net                                   │  │
│   └────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Règles** — les issues défavorables sont affichées **au même rang** que les favorables, jamais
repliées ni reléguées · l'empreinte et la mention d'ancrage sont toujours visibles · le
graphique ne porte **aucun indicateur** par défaut · défilement infini par ordre
antéchronologique · le bandeau d'avertissement de risque est présent en pied de page.

---

## Écran 2 — Détail d'une détection  ·  public

Reprend la carte, complétée de quatre blocs dépliables (divulgation progressive) :

| Niveau | Contenu | Déclencheur |
|---|---|---|
| 1 | Verdict, score, niveaux, issue | Immédiat |
| 2 | Les trois critères les plus déterminants | Visible, en petit |
| 3 | **Les 11 critères, avec les valeurs mesurées** | « Voir le détail du score » |
| 4 | Empreinte, preuve d'inclusion Merkle, ancrages, commande de vérification | Depuis le niveau 3 |

```
   Détail du score                                        9 / 11  =  82 %
   ────────────────────────────────────────────────────────────────────
   Qualité géométrique      2 touches nettes, symétrie 0,11 A      +2
   Tendance journalière     haussière, EMA200 pente 0,18 A         +2
   Zone support             — neutralisé : le creux est le support   —
   Niveau rond              1,0800, à 0,08 A                       +1
   Divergence RSI           RSI 34 → 41 sur creux décroissants      +1
   Faisabilité              D = 0,31                                +1
   Séance                   13:00 UTC, chevauchement Londres–NY     +1
   Calendrier               aucune annonce à fort impact             0
   Extension                0,8 A de l'EMA20                         0
   Régime                   ADX 17 — range, cohérent avec R1        +1
```

**Sous le graphique, toujours :** la statistique de la même configuration, celle du groupe
témoin, et l'écart entre les deux. **Jamais le résultat isolé de cette seule détection.**

---

## Écran 3 — Détections écartées  ·  public

Structure identique à l'écran 1, deux différences :

```
   ┌─ AUD/USD · H4 · ETE ──────────────────── ÉCARTÉE · 31 % ────────┐
   │  Motif : tendance journalière opposée (filtre)                  │
   │          objectif à 2,3 ATR, jugé irréaliste (filtre)           │
   │          aucune zone de support à proximité                     │
   │                                                                 │
   │  Sur 3 210 configurations écartées pour tendance opposée :      │
   │  espérance nette −0,26 R                                        │
   └─────────────────────────────────────────────────────────────────┘
```

En tête de page, le chiffre unique :

```
        −0,21 R                          contre  +0,19 R  pour les annoncées
        écartées, espérance nette                 écart : 0,40 R
        n = 14 600                                n = 1 840
```

**C'est l'écran le plus persuasif du produit.** Il doit être atteignable depuis l'accueil en un
clic, et lisible sans compte.

---

## Écran 4 — Fiche figure  ·  public  ·  cible du référencement

```
   Le double creux
   ───────────────────────────────────────────────────────────────
   [schéma de la figure]

   Ce qu'elle est · Comment elle se construit · Comment elle se trade
   habituellement · Les trois erreurs classiques

   ┌── Ce que nos mesures montrent ────────────────────────────────┐
   │                                                              │
   │              +0,08 R                                         │
   │        espérance nette, entrée sur cassure                   │
   │        groupe témoin −0,21 R · n = 1 240 · IC [+0,01;+0,15]  │
   │                                                              │
   │   Par méthode        cassure  +0,08 R    retour  +0,17 R     │
   │   Par unité de temps    H4    +0,12 R    D1      +0,03 R     │
   │   Par tranche de score  0-3   −0,19 R    7+      +0,21 R     │
   │                                                              │
   │   Mis à jour le 14/03/2026 · 12 nouvelles occurrences ce mois│
   └──────────────────────────────────────────────────────────────┘

   Cette figure sur : EUR/USD · GBP/USD · USD/JPY · …
```

**Une page dont la série est sous 100 occurrences affiche « données insuffisantes » et porte
`noindex`.** Publier des milliers de pages vides détruirait la crédibilité du domaine entier.

---

## Écran 5 — Preuve et intégrité  ·  public

```
   Comment vérifier nos chiffres vous-même
   ───────────────────────────────────────────────────────────────
   1. Téléchargez le jeu de données          [CSV]  [Parquet]
   2. Téléchargez le vérificateur            [code source]
   3. Exécutez :   verifier --du 2026-01-01 --au 2026-06-30

   Il recalcule les empreintes, les racines de Merkle, la continuité
   de la chaîne, l'antériorité des ancrages — et les issues elles-mêmes,
   depuis les données de marché.

   ┌── État ──────────────────────────────────────────────────────┐
   │  Cycles ancrés          4 344 / 4 344                        │
   │  Complétude des données 99,97 %                              │
   │  Dernier ancrage        14/03 13:00 UTC   ✓ 3 supports       │
   │  Incidents (12 mois)    2 — voir le détail                   │
   └──────────────────────────────────────────────────────────────┘

   Vous trouvez une divergence ? Écrivez-nous.
   Nous nous engageons à publier toute divergence confirmée,
   avec son explication.
```

**Les incidents passés sont listés, datés, expliqués.** Un trou d'ancrage n'est jamais comblé
rétroactivement : il reste visible définitivement.

---

## Écran 6 — Explorateur de statistiques  ·  abonné  ·  densité « analyse »

Filtres persistants en colonne gauche : paire, unité de temps, figure, méthode, tranche de
score, séance, régime, période, statut. Tableau dense à droite, 36 px par ligne, chiffres
tabulaires, tri par colonne, export CSV.

```
   Figure          Méthode   UT   n      Atteint  Espérance    Témoin    Écart
   ─────────────────────────────────────────────────────────────────────────────
   Double creux    retour    H4   1 240   46 %    +0,17 R     −0,21 R   +0,38
   Range           borne     H4   3 812   51 %    +0,09 R     −0,18 R   +0,27
   Triangle asc.   cassure   D1     287   38 %    −0,04 R     −0,22 R   +0,18  ⚠ provisoire
   ETE serrée      cassure   H4      87    —      données insuffisantes (87/100)
   ─────────────────────────────────────────────────────────────────────────────
   4 séries affichées sur 144 testées · correction de tests multiples appliquée
```

**La dernière ligne est obligatoire.** Un lecteur doit pouvoir juger de l'ampleur du test
multiple. **Aucune colonne « espérance » ne s'affiche sans sa colonne « témoin ».**

---

## Écran 7 — Mes alertes  ·  abonné

Filtres : paires, unités de temps, figures, méthodes, score minimum, canaux, plafond quotidien.

Un encart fixe, non masquable :

> Les alertes sont identiques pour tous les abonnés ayant les mêmes filtres.
> Nous ne connaissons ni votre capital, ni vos positions, et nous ne voulons pas les connaître.

**Aucun champ de capital ou de profil de risque n'existe sur cet écran.**

---

## Écran 8 — Mon journal  ·  abonné

Import en trois étapes, avec un point de contrôle explicite :

```
   1. Déposez votre relevé            [MT4]  [MT5]  [CSV]

   2. Vérification
      ✓ 428 trades lus, 3 lignes ignorées (voir le détail)
      ⚠ Décalage horaire du serveur détecté : UTC+3
        Estimé sur 14 semaines de fermeture hebdomadaire.
        Sans cette correction, votre analyse horaire serait
        décalée de trois heures.                    [corriger]
      ⚠ Aucun stop enregistré : le risque sera estimé à partir
        de vos propres pertes.  Résultats marqués « risque estimé ».

   3. Analyse                                        [lancer]
```

Puis : espérance, série de pertes maximale, résultats par paire, par séance, par jour.

---

## Écran 9 — Écart comportemental  ·  abonné  ·  l'écran qui fait payer

```
        0,61 R
        ce que vos écarts vous coûtent, par trade
        sur 128 trades · base de comparaison : 1 840 configurations

   ─────────────────────────────────────────────────────────────────

   1.  Vous sortez trop tôt de vos gagnants.
       Capture moyenne du mouvement favorable : 41 %.
       Coût estimé : 0,34 R par trade                    [128 trades →]

   2.  Vous augmentez votre mise après une perte.
       Corrélation risque / résultat précédent : −0,38.
       Coût estimé : 0,19 R par trade                     [41 trades →]

   3.  Vos trades du vendredi après-midi perdent.
       Espérance −0,44 R, contre +0,02 R le reste de la semaine.
       Coût estimé : 0,08 R par trade                     [21 trades →]
```

**Trois constats au maximum**, classés par coût décroissant, **chacun cliquable vers la liste
exacte des trades concernés**. Sans cette liste, un constat n'est qu'une affirmation.

Sous les seuils : « pas encore assez de trades pour conclure — 12 sur 30 ».

---

## Écran 10 — Mode contrainte  ·  abonné supérieur

```
   Paramètres                      Résultat
   ─────────────────────           ──────────────────────────────────
   Objectif        10 %                    31 %
   Perte / jour     5 %            probabilité de réussite, phase 1
   Perte totale    10 %            10 000 simulations · IC [30,1 ; 31,9]
   Type       suiveuse
   Durée        30 jours           Échec par perte totale        52 %
   Risque/trade     1 %            Échec par perte journalière   11 %
   Filtre    score ≥ 70 %          Délai dépassé                  6 %
                                   Durée médiane si réussite  18 jours

   Probabilité selon le risque par trade
   0,25%  0,50%  0,75%  1,00%  1,25%  1,50%  2,00%  2,50%  3,00%
    18%    29%    34%    31%    25%    19%    10%     5%     2%
                   ▲ optimum
```

**Les quatre avertissements du `SPEC-LOT11.md` §5 sont visibles sans faire défiler la page.**

---

## Écran 11 — Compte et administration de groupe

Compte individuel : abonnement, facturation, export, suppression.

Groupe, vue administrateur : liste des membres, sièges utilisés sur sièges payés, invitation par
courriel, retrait, transfert du rôle d'administrateur, facture unique.
**Aucune action n'exige notre intervention.**

Un administrateur **ne voit jamais** le journal de trading de ses membres. Il voit qui occupe un
siège, rien d'autre.

---

## Écran 12 — Mentions légales et avertissement

Mentions légales, CGU, CGV, confidentialité, cookies, **pare-feu contractuel publié**, **liste
des clients professionnels**.

Bandeau d'avertissement de risque en pied de **toute page portant une statistique** :

> Les performances passées ne préjugent pas des performances futures. 70 à 85 % des comptes de
> particuliers perdent de l'argent sur les contrats financiers. Ce service fournit des analyses
> statistiques impersonnelles et ne constitue pas un conseil en investissement.

---

## Ordre de construction des écrans

| Lot | Écrans |
|---|---|
| 3 | 1, 2, 3, 5 — **le registre public avant tout le reste** |
| 6 | 11, 12 |
| 7 | 7 |
| 9 | 6 |
| 10 | 4 |
| 5 | 8, 9 |
| 11 | 10 |

Les écrans 1, 2, 3 et 5 sont publics et gratuits : ce sont eux qui font l'acquisition, et ils
doivent tourner pendant que le reste se construit.
