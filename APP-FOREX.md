# Application de détection de figures — Forex, paires majeures

Spécification v1. Décidé : périmètre **forex, paires majeures uniquement**.
Modèle : essai gratuit puis abonnement.

## 1. Ce que fait l'app (et ce qu'elle ne fait pas)

**Fait :** détecte des figures chartistes et des états de tendance sur 7 paires majeures,
horodate chaque détection **avant** l'issue, puis publie le résultat — gagnant ou perdant.

**Ne fait pas :** ne connaît ni le capital, ni le portefeuille, ni le profil de risque
de l'utilisateur. Ne dit jamais « adapté à toi ». Cette ligne ne doit jamais être franchie :
c'est elle qui évite le statut de conseiller en investissement financier.

## 2. Position juridique

| Point | Statut |
|---|---|
| Agrément CIF (ORIAS + association AMF) | **Non requis** si aucune personnalisation (MiFID II, règl. délégué 2017/565 art. 9) |
| MAR art. 20 (recommandations d'investissement) | Champ **incertain** sur le forex de détail : le spot FX n'est pas un instrument financier au sens de MiFID II annexe I section C. Appliquer la discipline MAR quand même : auteur identifié, date, méthode, historique publié, avertissement. |
| **Loi Sapin 2 — art. L.222-16-1 code de la consommation** | **Contrainte forte.** Interdit la publicité par voie électronique pour les contrats financiers hautement spéculatifs (forex, CFD) à destination du public en France. |
| Loi influenceurs (n° 2023-451) | Interdit la promotion de ces produits par des influenceurs. |
| Politiques Google Ads / Meta | Services de signaux forex : catégorie restreinte ou interdite. |

**Conséquence opérationnelle :** l'acquisition payante est fermée. Le canal doit être organique
(contenu, YouTube, communauté) et l'app doit se présenter comme **outil d'analyse statistique**,
jamais comme promesse de gain. À faire valider par un avocat avant la mise en ligne payante.

## 3. Objection à la décision de périmètre (à lire, la décision reste au propriétaire)

Le forex majeur est le marché **le plus liquide et le plus arbitré du monde** :
7 500 Md$ échangés par jour (enquête triennale BIS, avril 2022). EUR/USD en journalier
est le jeu de données le plus exploré de l'histoire de la finance quantitative.

Deux conséquences chiffrées :

1. **L'avantage attendu y est le plus proche de zéro.** Si l'objectif est d'afficher un bon
   pourcentage, c'est le marché où c'est le moins probable.
2. **Le volume de données est faible.** 7 paires seulement. Estimation : 40 à 120 occurrences
   par figure et par paire sur 10 ans en H4. Sur 50 occurrences, l'intervalle de confiance à 95 %
   d'un taux de réussite est de **± 14 points**. Il faut environ **2 400 occurrences** pour
   distinguer 52 % de 50 %. Un affichage par paire sera donc statistiquement muet ;
   seuls les agrégats toutes paires confondues auront un sens.

Contre-argument en faveur du forex : données historiques gratuites et propres, marché ouvert 24/5,
pas de dividendes ni de splits ni de titres radiés, 7 symboles à maintenir au lieu de 5 000.
La complexité technique est divisée par dix.

**Position retenue :** on garde le forex, mais l'unité statistique publiée est
**l'agrégat toutes paires**, jamais la cellule paire × figure.

## 4. Définition du résultat — à figer avant la première ligne de code

Sans définition écrite et immuable, le pourcentage publié ne vaut rien.

| Élément | Règle |
|---|---|
| Entrée | Clôture de la bougie qui valide la figure. Pas de prix intra-bougie. |
| Invalidation (perdant) | Niveau structurel de la figure (ex. sommet de la tête pour une ETE). |
| Objectif (gagnant) | Projection mesurée de la figure. |
| Horizon | 20 bougies. Ni objectif ni invalidation touchés → **neutre**, comptabilisé séparément. |
| Départage | Résolution en **données M1** pour savoir lequel de l'objectif ou de l'invalidation a été touché en premier dans la bougie. |
| Frais | Spread médian de la paire déduit à l'entrée et à la sortie. Le résultat publié est **net**. |

Le cas « neutre » doit être affiché. Une app qui n'affiche que gagnants/perdants ment par omission.

## 5. Le vrai actif du produit : le journal prospectif

Un backtest ne prouve rien — tout le monde peut en fabriquer un flatteur.
La crédibilité vient d'une seule chose : **la détection est publiée avant l'issue et ne peut pas
être modifiée après.**

- Chaque détection est écrite dans un journal public : horodatage, paire, figure, niveaux, source du prix.
- Chaînage par hachage : chaque entrée contient le hash de la précédente. Toute réécriture est détectable.
- Le résultat est calculé automatiquement à l'échéance, sans intervention humaine.
- Le taux de réussite affiché sur le site est **celui du journal prospectif**, pas celui du backtest.
  Les deux sont montrés côte à côte : l'écart entre les deux est en soi une information de qualité.

C'est ce que les concurrents ne font pas, et c'est gratuit à construire.

## 6. Pièges techniques spécifiques au forex

1. **Il n'existe pas de prix consolidé.** Le forex est de gré à gré : chaque courtier a son flux.
   Les chandeliers de l'utilisateur ne seront pas identiques aux tiens. Publier explicitement
   la source de prix retenue et s'y tenir. Ne jamais changer de source sans le signaler.
2. **Départage intra-bougie.** Sans données M1, impossible de savoir si l'objectif ou le stop
   a été touché en premier. C'est l'erreur qui gonfle artificiellement les taux de réussite.
3. **Heure de clôture.** La bougie journalière dépend du fuseau du courtier (17 h New York
   contre minuit UTC). Cela change les figures détectées. Choisir une convention et la documenter.
4. **Dimanche et roulement.** Les gaps du dimanche soir peuvent traverser un stop. À traiter.
5. **Détection déterministe.** Pivots par ZigZag à seuil ATR, puis règles géométriques.
   Aucun apprentissage automatique en v1 : non reproductible, non explicable, surapprentissage garanti.

## 7. Catalogue des figures et unité statistique

### On détecte tout, on ne publie pas tout

**Détection : catalogue complet.** La littérature chartiste documente plus de 60 figures
(référence : Bulkowski, *Encyclopedia of Chart Patterns*). Les détecter toutes est peu coûteux
une fois l'interface stratégie en place, et la couverture est un argument commercial réel.

**Publication des statistiques : sous condition.** C'est là que se joue la crédibilité.

Le danger n'est pas le temps de développement, c'est le **test multiple**. 60 figures × 3 unités
de temps = 180 combinaisons testées. Au seuil de 5 %, **on attend mécaniquement une dizaine de
résultats « significatifs » dus au seul hasard**. Un classement « les figures qui marchent le
mieux » établi sans correction ne classe pas des figures : il classe du bruit. C'est exactement
le mécanisme qui a produit toutes les fausses stratégies de l'histoire du trading.

### Seuils de publication

| Occurrences | Précision (IC 95 %) | Affichage |
|---|---|---|
| < 100 | pire que ± 10 pts | **« Données insuffisantes — 37 occurrences observées, 100 nécessaires »** |
| 100 - 399 | ± 5 à 10 pts | Résultat marqué **provisoire**, intervalle de confiance affiché |
| ≥ 400 | ± 5 pts | Résultat **établi** |
| ≥ 2 400 | ± 2 pts | Permet d'affirmer un avantage de 2 points |

Le classement des figures applique une **correction de tests multiples** (Benjamini-Hochberg),
jamais le taux de réussite brut.

Afficher « données insuffisantes » n'est pas un aveu de faiblesse : c'est la fonctionnalité que
personne n'offre, et la preuve visible que les autres chiffres sont sérieux.

### Le bon levier pour gagner en puissance : plus de paires, pas moins d'exigence

Pour faire monter les occurrences, on n'assouplit pas les seuils — on **ajoute des paires**.
Passer de 7 majeures à ~28 paires (mineures et croisées) multiplie les occurrences par environ 4,
**sans une ligne de code supplémentaire** : même moteur, même source de données, même format.
C'est la seule extension à faire quand une figure reste sous le seuil.

### L'unité statistique est la figure × la méthode, pas la figure

Une épaule-tête-épaule ne se trade pas d'une seule façon :

| Méthode | Entrée |
|---|---|
| A | Cassure de l'encolure |
| B | Retour sur l'encolure après cassure |
| C | Cassure confirmée par la clôture de la bougie suivante |

Ces trois méthodes ont des résultats différents. Les traiter comme une seule brouille tout.

**Conséquence d'architecture, essentielle :** la méthode affichée à l'utilisateur (« voici
comment se trade ce type de figure ») et la règle de résolution gagnant/perdant sont **le même
objet en base**. Une définition unique, deux usages : pédagogie et mesure. Sans cette unité, le
contenu explique une chose et les statistiques en mesurent une autre — c'est le défaut de tout
le contenu pédagogique existant, et de tous les backtests publiés.

C'est aussi ce qui produit la sortie la plus vendable du produit :
*« Sur l'épaule-tête-épaule, l'entrée sur retour a une espérance nette supérieure à l'entrée sur
cassure »* — une question que les traders se disputent depuis trente ans sans jamais l'avoir
chiffrée sur données prospectives.

### Périmètre v1

| Élément | Valeur |
|---|---|
| Paires | EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD — extensible à ~28 |
| Unités de temps | H1, H4, journalier |
| Figures détectées | Catalogue complet, ajouté par lots via l'interface stratégie |
| Figures **publiées** | Uniquement celles franchissant le seuil de 100 occurrences |
| Tendance et range | ADX + structure de sommets et creux. États : haussier, baissier, range |
| Fréquence de calcul | Traitement par lots à chaque clôture de bougie. Pas de temps réel |

### Position juridique de la couche pédagogique

Formuler « voici comment se trade ce type de figure » plutôt que « prenez ce trade » est la
bonne approche : c'est du contenu éducatif générique et non une suggestion d'opération.

Réserve honnête : afficher cette méthode **avec les niveaux concrets de cette paire à cet
instant** reste, en pratique, très proche d'une recommandation, quelle que soit la formulation.
Ce qui protège réellement reste l'**absence de personnalisation** (voir §2) — la formulation
pédagogique est une précaution supplémentaire, pas le rempart principal.

## 8. Architecture et coûts

- **Calcul par lots**, pas de flux temps réel. Précalcul à chaque clôture H4, résultats en cache.
- Stockage : PostgreSQL + TimescaleDB. Détection : Python + Polars. API : FastAPI. Front : rien de lourd.
- **Données historiques :** Dukascopy (tick, gratuit) ou HistData (M1, gratuit) pour la base ;
  flux courant via une API forex à 30-50 $/mois (estimation).
- **Hébergement :** un VPS à 20-40 €/mois suffit jusqu'à plusieurs milliers d'utilisateurs.
  Le coût par utilisateur est quasi nul : le calcul est mutualisé, il ne dépend pas du nombre d'abonnés.

Coût d'infrastructure total estimé avant le premier client : **moins de 100 €/mois.**

## 9. Critère d'arrêt honnête

Le journal prospectif dira la vérité au bout de 3 à 6 mois. Deux issues :

- **Taux net positif et stable** → le produit a une valeur démontrable, et une preuve que
  personne d'autre ne fournit.
- **Taux net autour de 50 % ou négatif** → ne pas maquiller le chiffre. Deux options :
  pivoter le discours vers « ce que l'analyse technique ne fait pas », ou arrêter.
  Publier un mauvais chiffre honnêtement reste un produit ; publier un bon chiffre fabriqué
  est une infraction.

Décider maintenant, par écrit, ce qui sera fait dans le second cas. C'est la seule protection
contre la tentation de trafiquer les résultats quand l'abonnement sera en jeu.
