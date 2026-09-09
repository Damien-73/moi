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

## 7. Périmètre v1

| Élément | Valeur |
|---|---|
| Paires | EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD |
| Unités de temps | H4 et journalier |
| Figures | Épaule-tête-épaule et inversée, double sommet et double creux, triangle symétrique, drapeau |
| Tendance | ADX + structure de sommets et creux. Trois états : haussier, baissier, indéterminé |
| Fréquence de calcul | Traitement par lots à chaque clôture de bougie H4. Pas de temps réel |

« Toutes les stratégies de trading » n'est pas une spécification. Six figures livrées et mesurées
valent mieux que quarante annoncées.

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
