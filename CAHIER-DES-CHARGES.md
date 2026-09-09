# Cahier des charges — Application d'analyse de figures chartistes sur le forex

Document de référence unique. Version 2 — septembre 2026.

> **Comment lire.** Les sections techniques commencent par « *Pourquoi ça compte* ».
> Les termes sont définis au §29 (glossaire). Chaque décision est ferme : quand deux options
> existaient, une seule figure ici, avec son motif. Les points encore ouverts sont regroupés
> au §28 — et nulle part ailleurs.

**Sommaire**

| Partie | Sections |
|---|---|
| **I — Produit** | 1 à 6 |
| **II — Méthode** (le cœur) | 7 à 12 |
| **III — Technique** | 13 à 18 |
| **IV — Exploitation** | 19 à 24 |
| **V — Exécution** | 25 à 30 |

---
---

# PARTIE I — PRODUIT

## 1. Résumé exécutif

L'application détecte automatiquement les figures chartistes et les configurations de marché
sur le forex, explique **comment ce type de configuration se trade habituellement**, puis
**publie si l'objectif a été atteint ou non**.

Chaque détection est horodatée et publiée **avant** de connaître son issue, dans un journal
public infalsifiable. Elle est ensuite résolue automatiquement. Au fil du temps se constitue une
base de dizaines de milliers de configurations documentées et mesurées **frais déduits** —
c'est le cœur du produit.

L'utilisateur peut importer son propre journal de trades et se comparer à cette base.

### Ce qui n'existe nulle part aujourd'hui

| Ce que font les autres | Ce que fait cette application |
|---|---|
| Un backtest fabriqué a posteriori | Un journal **prospectif** : publié avant l'issue, ancré publiquement, non modifiable |
| Un taux de réussite brut | Une **espérance en R, nette de tous frais** |
| Seulement les configurations retenues | Les configurations **écartées aussi**, comme groupe témoin |
| Du contenu pédagogique déconnecté des chiffres | **La méthode enseignée est exactement celle qui est mesurée** |
| « 90 % de réussite » | « Données insuffisantes : 37 occurrences, 100 nécessaires » |

### La phrase qui résume le positionnement

> Nous ne vous disons pas quoi acheter. Nous vous disons ce que cette configuration a
> réellement donné les 1 240 fois précédentes, frais compris — y compris quand le résultat
> nous dessert.

---

## 2. Proposition de valeur et avantages concurrentiels

**Objectif produit :** devenir la référence mondiale sur une seule question —
*« cette configuration chartiste, ça donne quoi réellement ? »*

| Avantage | Copiable en combien de temps ? |
|---|---|
| **L'historique prospectif ancré publiquement** | **Jamais rattrapable.** Un backtest se refait en une nuit ; deux ans de détections publiées à l'avance et horodatées par un tiers ne se fabriquent pas rétroactivement. Sa valeur augmente chaque jour, sans effort |
| **Le groupe témoin** (configurations écartées, conservées et mesurées) | Impossible pour qui ne l'a pas fait dès le départ. Sans lui, aucun concurrent ne peut prouver que son filtrage sert à quelque chose |
| **L'écart comportemental** (journal de l'utilisateur × base) | 12-18 mois, et seulement après avoir accumulé la base. Crée un coût de sortie |
| Le moteur de détection | **3 mois — et il existe déjà chez un concurrent (§3). Aucune valeur défensive.** Ne jamais bâtir l'argumentaire dessus |

### Principe de conception fondamental : publier des **comparaisons**, jamais des absolus

*C'est la décision qui rend le produit robuste au seul risque qu'il ne contrôle pas :
l'absence d'avantage exploitable sur le marché.*

Un produit qui vend « cette figure gagne » s'effondre si l'espérance mesurée est nulle.
Un produit qui vend « cette figure gagne **0,14 R de plus que celle-là**, et **0,23 R de plus
en séance de Londres qu'en séance asiatique** » garde toute sa valeur, **même si les deux
espérances sont négatives**.

| Ce qu'on ne vend pas | Ce qu'on vend |
|---|---|
| « Le double creux est rentable » | « Le double creux fait 0,12 R de mieux que le triangle, mesuré sur 2 400 cas » |
| « Tradez cette configuration » | « En H1 les frais consomment 15 % du mouvement, contre 2 % en journalier » |
| « 62 % de réussite » | « L'entrée sur retour bat l'entrée sur cassure de 0,09 R » |

Deux raisons, la seconde étant technique :

1. **L'information relative reste actionnable même quand l'avantage absolu est nul.** Savoir
   où l'on perd le moins a de la valeur pour quelqu'un qui trade de toute façon.
2. **Les comparaisons sont statistiquement bien plus robustes.** Les biais communs aux deux
   termes — qualité de la source de prix, modèle de frais, choix de l'horizon — s'annulent en
   grande partie dans une différence, alors qu'ils faussent entièrement une valeur absolue.

**Conséquence sur l'interface : tout chiffre publié est accompagné de son terme de comparaison.
Aucune statistique n'est affichée seule.**

### L'honnêteté comme barrière à l'entrée

Le marché des outils forex vit de promesses invérifiables. Un produit dont le mécanisme central
est *« nous publions nos échecs »* est inimitable par les acteurs installés : basculer vers la
transparence détruirait les chiffres qu'ils affichent déjà.

**Cible assumée : non pas celui qui cherche des signaux, mais celui qui s'est déjà fait avoir
par des signaux.** Segment réel, atteignable uniquement en organique — ce qui tombe bien,
puisque la publicité payante est de toute façon fermée (§19).

---

## 3. Analyse concurrentielle

*Pourquoi ça compte : un cahier des charges qui revendique l'unicité sans nommer ses
concurrents n'est pas sérieux.*

| Acteur | Ce qu'il fait | Ce qu'il ne fait pas |
|---|---|---|
| **Autochartist** — le concurrent réel | Reconnaissance automatique de figures, niveaux clés, indice de qualité, statistiques historiques. Distribué en marque blanche par de nombreux courtiers | Pas de journal prospectif public et infalsifiable, pas de groupe témoin publié, pas de résultats nets de swap et slippage, pas de croisement avec le journal de l'utilisateur, pas de mode contrainte. C'est un produit **B2B vendu aux courtiers**, sans réputation propre auprès du public |
| TradingView | Graphiques, screener, quelques détections, communauté immense | Aucune statistique d'issue mesurée et publiée |
| Bulkowski (*Encyclopedia of Chart Patterns*) | Statistiques de référence sur 60+ figures | Un livre. Actions américaines, rétrospectif, sans frais, figé, non interrogeable |
| Tradezella, Edgewonk, TraderVue | Journaux de trading et statistiques personnelles | Aucune base de référence à laquelle se comparer |
| Vendeurs de signaux (Telegram, Discord) | Signaux, promesses | Aucune vérifiabilité. C'est le repoussoir, et le vivier de clients |

### Conclusion à retenir

**Le moteur de détection n'est pas un avantage : Autochartist prouve qu'il est une marchandise
banale.** La différenciation est entièrement dans ce que personne ne fait :

1. journal prospectif public et ancré chez un tiers ;
2. groupe témoin publié ;
3. résultats nets de **tous** les frais, swap compris ;
4. croisement avec le journal personnel ;
5. mode contrainte de perte maximale.

Le positionnement n'est donc pas « le premier à détecter des figures », mais
**« le seul dont les chiffres sont vérifiables par un tiers »**.

---

## 4. Utilisateurs et segments

| # | Segment | Ce qu'il cherche | Priorité |
|---|---|---|---|
| 1 | **Candidat en société de financement (*prop firm*)** | Savoir quelles configurations survivent à une limite de perte quotidienne. Paie déjà 100 à 600 $ par tentative, souvent plusieurs fois | **Segment principal.** Capacité à payer démontrée, besoin précis, dimension mondiale |
| 2 | Trader particulier déçu par les vendeurs de signaux | Des chiffres vérifiables plutôt que des promesses | Segment d'entrée, atteignable en organique |
| 3 | Société de financement, courtier, formateur | Statistiques agrégées : quelles configurations font sauter les comptes | Revenu B2B ultérieur, panier bien plus élevé |

**Cadrage :** 70 à 85 % des comptes de particuliers perdent de l'argent sur les CFD (mention
réglementaire obligatoire des courtiers). Ce public paie peu et part vite. Le produit doit être
conçu pour le segment 1, même si le segment 2 arrive en premier.

**Portée mondiale :** le forex est identique partout, les données sont universelles, il n'y a
aucun ancrage géographique. L'internationalisation se réduit à traduire l'interface — sous
réserve des exclusions de juridiction du §20.

---

## 5. Périmètre fonctionnel — les neuf modules

### Module A — Ingestion et stockage des données

*Pourquoi ça compte : si les données d'entrée sont fausses, tout le reste est faux.*

- Source de vérité : bougies **M1**, agrégées en H1, H4 et journalier.
- Spread réel reconstruit depuis les données tick, **variable selon l'heure**. À l'heure du
  roulement quotidien il peut être plusieurs fois supérieur à la normale — personne ne modélise
  ça, et cela fausse tous les résultats de nuit.
- Convention d'heure de clôture journalière **documentée et figée** : une bougie qui clôture à
  17 h New York ne donne pas les mêmes figures qu'à minuit UTC.
- **Gestion du changement d'heure (été/hiver).** Les séances de Londres et New York se décalent
  deux fois par an. Un critère de séance codé en heure UTC fixe devient faux deux fois par an :
  les séances sont définies **par rapport à l'heure locale des places**, jamais en UTC constant.
- Traitement des gaps du dimanche soir, qui peuvent traverser un niveau d'invalidation.
- **Valeur du pip par paire** : 0,0001 en général, **0,01 sur les paires en yen**.

### Module B — Moteur de détection et score de confluence

Chaque stratégie est un module indépendant respectant un contrat unique :

```
détecter(bougies_jusqu_à_t, paramètres)
  -> [ { sens, entrée, invalidation, objectif, horizon, score, détail_du_score } ]
```

- **Interdiction absolue d'accéder à une bougie postérieure à `t`.**
- Détection **déterministe** : pivots par ZigZag à seuil ATR, puis règles géométriques.
- **Aucun apprentissage automatique en version 1** : non reproductible, non explicable,
  surapprentissage garanti sur des données de marché.
- Le score de confluence (§9) est calculé et **stocké avec son détail critère par critère**,
  pour que tout rejet soit explicable et toute statistique reconstructible.
- Catalogue complet des figures visé (§7), ajouté par lots.

### Module C — Journal prospectif public

*À la fois la preuve du produit et son principal outil d'acquisition.*

- Chaque détection est écrite dans un journal public : horodatage, paire, unité de temps,
  figure, méthode, niveaux, score et son détail, source de prix, version de la stratégie,
  statut annoncée / écartée avec motif.
- **Chaînage par empreinte numérique**, et **ancrage quotidien chez un tiers** (§15).
- L'issue est calculée automatiquement, sans intervention humaine.
- **Accessible gratuitement, sans compte.** C'est ce qui remplace la publicité interdite.
- Le backtest est affiché **à côté** du journal prospectif, jamais à sa place : l'écart entre
  les deux est lui-même une information de qualité.

### Module D — Base de résultats interrogeable

Le cœur vendable. Filtres : paire, unité de temps, figure, méthode, tranche de score, heure,
régime de marché, période, statut annoncée/écartée.

> Épaule-tête-épaule inversée, H4, entrée sur retour — 1 240 occurrences depuis 2015.
> Objectif atteint : 46 %. Invalidation : 41 %. Sans issue : 13 %.
> **Espérance nette : +0,08 R.** Intervalle de confiance à 95 % : [+0,01 ; +0,15].

### Module E — Journal de trading de l'utilisateur

- Import par rapport MT4/MT5 ou fichier CSV. **Aucune connexion au courtier n'est nécessaire.**
- Statistiques personnelles : espérance, série de pertes maximale, résultats par paire, par
  heure, par jour.
- **L'écart comportemental** — la fonction qui justifie l'abonnement :

> Vous avez pris 34 trades en range. La base donne 48 % net sur cette configuration.
> Vous êtes à 31 %. Écart principal : vous entrez en moyenne 2 bougies trop tôt.

Analyse rétrospective sur les données de l'utilisateur : aucune exposition réglementaire.

### Module F — Mode contrainte (*prop firm*)

Rejoue la base sous contrainte de perte maximale journalière et globale.

Répond à la seule question de ce public : *« cette approche survit-elle à une limite de perte de
5 % par jour ? »* Une stratégie à espérance positive peut échouer dans 90 % des cas sous
contrainte de drawdown — **aucun outil existant ne le dit.**

Entrées : objectif de gain, perte journalière maximale, perte totale maximale, durée, risque par
trade. Sortie : **probabilité de réussite de la contrainte**, jamais un rendement.

### Module G — Notifications

*Pourquoi ça compte : une annonce qui arrive six heures trop tard ne vaut rien. C'est un module
à part entière, pas un détail d'implémentation.*

| Canal | Priorité |
|---|---|
| Courriel | v1 |
| Notification navigateur (web push) | v1 |
| Telegram | v2 — canal dominant du public visé |
| Webhook | v2 — pour les utilisateurs outillés |

- **Exigence de latence : annonce envoyée en moins de 60 secondes après la clôture de la bougie
  déclenchante.** Au-delà, l'annonce est envoyée **marquée comme retardée**, et le retard est
  enregistré dans le journal public.
- Filtres utilisateur : paires, unités de temps, figures, score minimum.
- **Aucun filtre fondé sur le capital ou le profil de risque** (§19).
- Toute annonce envoyée est identique pour tous les abonnés au même filtre — jamais
  individualisée.

### Module H — Contenu pédagogique

- Une fiche par figure : définition, construction, méthodes de trading, erreurs classiques,
  **et les statistiques mesurées de cette figure**, mises à jour automatiquement.
- Une fiche par critère du score, expliquant ce qu'il mesure et sa contribution mesurée.
- Glossaire intégré, accessible depuis n'importe quel terme de l'interface.

Ce module est aussi le moteur d'acquisition naturelle (§22).

### Module I — Commentaires horodatés et verrouillés (v2)

*Un chat en direct est **refusé**. Les commentaires horodatés sont retenus. Les deux ne
répondent pas au même besoin, et un seul est compatible avec le produit.*

#### Pourquoi le chat en direct est refusé

| Motif | Détail |
|---|---|
| **Il contredit la raison d'être du produit** | Tout l'édifice repose sur *« des chiffres vérifiables, pas des opinions »*. Un chat est une machine à opinions. En quelques semaines il devient la fonction la plus utilisée, saturée de « je pense que l'euro va monter » — exactement le bruit que le produit existe pour remplacer. L'identité du produit se dissout |
| **Exposition réglementaire** | Un utilisateur qui écrit « achetez l'euro maintenant » publie une recommandation **sur votre plateforme**. Le régime d'hébergeur protège tant qu'il n'y a pas d'intervention éditoriale — mais toute modération active brouille cette frontière |
| **Aimant à escroqueries** | Les salons de discussion forex attirent les vendeurs de signaux, les parrainages vers des courtiers non régulés et les systèmes d'affiliation. Le produit deviendrait le canal d'acquisition de ceux contre qui il se positionne |
| **Publicité interdite** | Un message promotionnel pour un courtier CFD posté par un utilisateur peut relever de l'interdiction du §19 |
| **Conseil personnalisé public** | « Dois-je prendre ce trade avec 3 000 € ? » recevra une réponse d'un autre utilisateur, publiquement, sur votre plateforme. C'est le §19 franchi en permanence |
| **Modération impossible à cette échelle** | Un salon forex non modéré dégénère en quelques semaines. La modération est un travail à temps plein, 24 h sur 5 jours, sur plusieurs fuseaux |

**Précision de vocabulaire :** la transparence recherchée est déjà assurée par le journal
prospectif, l'ancrage externe et le groupe témoin (§15). Ce qu'un chat apporte, c'est de la
**conversation**, pas de la transparence. Deux besoins distincts, à traiter séparément.

#### Ce qui est retenu à la place : le commentaire horodaté et verrouillé

Un fil de commentaires **attaché à une détection précise**, avec une règle unique :

> **Tout commentaire publié avant la résolution est horodaté et verrouillé définitivement.
> Il reste affiché à côté de l'issue réelle.**

C'est le principe fondateur du produit — publier avant de savoir — **étendu à la communauté**.

| Conséquence | Effet |
|---|---|
| On voit ce que les gens disaient **avant** de connaître le résultat | Personne d'autre ne montre ça |
| Impossible de réécrire son avis après coup | Auto-régulation : chacun devient prudent quand son opinion reste attachée au résultat |
| Le fil se ferme à la résolution | Pas de flux permanent à modérer, volume borné |
| Aucune promotion possible | Un commentaire ne peut porter que sur la détection à laquelle il est attaché |

**Extension possible (v3, sous réserve d'avis juridique) :** l'utilisateur peut enregistrer son
propre pronostic avant l'issue, et son historique devient public. Même mécanique, appliquée aux
personnes. Aucun élément monétaire, aucun classement mis en avant tant que l'avis juridique
n'est pas rendu.

#### Obligations si des contenus d'utilisateurs sont hébergés

Conditions d'utilisation spécifiques, procédure de signalement et de retrait, point de contact
publié, journal des retraits, modération a posteriori. Ces obligations existent dès le premier
commentaire — elles sont une raison de plus de limiter le périmètre au fil verrouillé.

#### La communauté, elle, se fait à l'extérieur

Un espace de discussion ouvert (Discord ou Telegram), **hébergé hors du produit et clairement
séparé de lui**, modéré par un bénévole issu de la communauté. Coût de développement nul,
aucune exposition sur la plateforme, et le besoin d'échange est satisfait.


---

## 6. Parcours et écrans

*Pourquoi ça compte : sans liste d'écrans, un cahier des charges n'est pas constructible.*

| # | Écran | Accès | Contenu |
|---|---|---|---|
| 1 | **Journal en direct** | Public, sans compte | Flux des détections annoncées, statut, issue. La page d'accueil |
| 2 | Détail d'une détection | Public | Graphique, niveaux, méthode appliquée, score détaillé critère par critère, issue, **fil de commentaires verrouillés (v2)** |
| 3 | **Détections écartées** | Public | Le groupe témoin, avec motif de rejet et statistique associée |
| 4 | Fiche figure | Public | Pédagogie + statistiques à jour. **Cible du référencement naturel (§22)** |
| 5 | Preuve et intégrité | Public | Explication de la chaîne d'empreintes, ancrages publics, procédure de vérification par un tiers |
| 6 | Explorateur de statistiques | Abonné | Base interrogeable, tous filtres, export |
| 7 | Mes alertes | Abonné | Filtres de notification |
| 8 | Mon journal | Abonné | Import, statistiques personnelles |
| 9 | **Écart comportemental** | Abonné | La comparaison journal × base |
| 10 | Mode contrainte | Abonné supérieur | Simulateur prop firm |
| 11 | Compte et abonnement | Abonné | Facturation Stripe |
| 12 | Mentions légales, CGU, avertissement de risque | Public | §19 |

**Interface, ergonomie, design et temps réel : voir `SPEC-DESIGN.md`.**

**Parcours d'entrée type :** un visiteur arrive par une fiche figure via un moteur de recherche →
il voit une statistique réelle → il clique sur le journal en direct → il constate que les échecs
sont publiés aussi → il crée un compte pour les alertes → il importe son journal → il découvre
son écart comportemental → il s'abonne.

**Chaque étape de ce parcours est gratuite jusqu'à l'écart comportemental.** C'est là qu'est
placé le mur payant, parce que c'est la seule fonction dont la valeur est personnelle et immédiate.

---
---

# PARTIE II — MÉTHODE

## 7. Catalogue des figures et unité de mesure

### On détecte tout, on ne publie pas tout

**Détection : catalogue complet.** La littérature documente plus de 60 figures (Bulkowski).
Les détecter toutes coûte peu une fois l'interface du module B en place, et la couverture est un
argument commercial réel.

**Publication : sous condition.** C'est là que se joue toute la crédibilité.

> *Le danger n'est pas le temps de développement, c'est le **test multiple**. 60 figures × 3
> unités de temps × 3 méthodes = plus de 500 combinaisons testées. Au seuil habituel de 5 %,
> on attend mécaniquement **une vingtaine de résultats « significatifs » dus au seul hasard**.
> Un classement « les figures qui marchent le mieux » établi sans correction ne classe pas des
> figures : il classe du bruit. C'est le mécanisme qui a produit toutes les fausses stratégies
> de l'histoire du trading.*

### Seuils de publication

| Occurrences | Précision (IC 95 %) | Affichage |
|---|---|---|
| < 100 | pire que ± 10 points | **« Données insuffisantes — 37 occurrences observées, 100 nécessaires »** |
| 100 - 399 | ± 5 à 10 points | Résultat **provisoire**, intervalle affiché |
| ≥ 400 | ± 5 points | Résultat **établi** |
| ≥ 2 400 | ± 2 points | Permet d'affirmer un avantage de 2 points |

Classement des figures avec **correction de tests multiples** (Benjamini-Hochberg),
jamais le taux de réussite brut.

Afficher « données insuffisantes » n'est pas un aveu de faiblesse : c'est la fonctionnalité que
personne n'offre, et la preuve visible que les autres chiffres sont sérieux.

### Pour gagner en puissance : ajouter des paires, jamais assouplir les seuils

Passer de 7 paires majeures à environ 28 paires (mineures et croisées) multiplie les occurrences
par 4, **sans une ligne de code supplémentaire** : même moteur, même source, même format.
C'est la seule extension autorisée quand une figure reste sous le seuil.

### L'unité statistique est **figure × méthode**, jamais la figure seule

| Méthode (exemple : épaule-tête-épaule) | Entrée |
|---|---|
| A | Cassure de l'encolure |
| B | Retour sur l'encolure après cassure |
| C | Cassure confirmée par la clôture suivante |
| D | Cassure avec sortie partielle à 1 R et suivi du reste |

Ces méthodes donnent des résultats différents. Les confondre invalide tout.
La méthode D montre que **les modes de sortie** (sortie partielle, stop suiveur) sont des
méthodes à part entière, mesurées séparément — et non des variantes informelles.

**Règle d'architecture essentielle : la méthode affichée à l'utilisateur (« voici comment se
trade ce type de figure ») et la règle qui décide gagnant/perdant sont le même objet en base.**
Une définition unique, deux usages : pédagogie et mesure. Sans cette unité, le contenu explique
une chose et les statistiques en mesurent une autre — défaut de tout le contenu pédagogique
existant et de tous les backtests publiés.

Sortie la plus vendable du produit : *« sur l'épaule-tête-épaule, l'entrée sur retour a une
espérance nette supérieure à l'entrée sur cassure »* — question débattue depuis trente ans,
jamais chiffrée sur données prospectives.

---

## 8. Détection, annonce et conservation sont trois choses distinctes

*Point le plus important du document. S'y tromper vide le produit de sa valeur.*

| Étape | Périmètre |
|---|---|
| **Détection** | **Toutes** les figures, même celles ne remplissant aucun critère |
| **Conservation** | **Toutes**, définitivement, avec leur score et le détail de leur évaluation |
| **Annonce** | **Uniquement** celles franchissant les filtres durs et le seuil de score |
| **Statistiques mises en avant** | Celles des configurations **annoncées** |
| **Statistiques de contrôle** | Celles des configurations **écartées** — conservées et publiées à part |

### Pourquoi les configurations écartées doivent être gardées

1. **Sans elles, on ne peut pas prouver que le filtre sert à quelque chose.** « Les
   configurations annoncées donnent +0,19 R » n'a aucun sens sans point de comparaison :
   +0,19 R **par rapport à quoi ?**
2. **C'est le meilleur argument commercial du produit**, et il n'existe que si on garde le
   groupe témoin :

   > Configurations annoncées : **+0,19 R** (n = 1 840).
   > Configurations écartées : **−0,21 R** (n = 14 600).
   > Voilà pourquoi nous les écartons.

3. **Filtrer puis mesurer sur le résultat filtré ne mesure pas le marché, ça mesure l'optimisme
   du filtre.** C'est le mécanisme exact qui fabrique les faux avantages.
4. **Les critères évolueront.** Sans historique complet, impossible de réévaluer le passé —
   donc impossible de savoir si un ajustement améliore ou dégrade.

**Règle : rien n'est jamais supprimé. Ce qui est écarté est marqué comme écarté, avec son motif.**

### Ce que voit l'utilisateur

Il reçoit **uniquement les configurations annoncées**. Mais il peut ouvrir une configuration
écartée et lire le motif :

> Épaule-tête-épaule détectée — **non annoncée**. Score 4/13.
> Manquant : tendance journalière opposée (−2), objectif à 2,3 ATR jugé irréaliste sur
> l'horizon (−2), aucune zone de support à proximité.
> *Sur les 3 210 configurations écartées pour tendance opposée, l'espérance nette est de −0,26 R.*

Fonction pédagogique unique sur le marché, et démonstration permanente que le filtrage a une
valeur mesurée.

---

## 9. Le score de confluence

### 9.1 Pourquoi un score, et pas une liste de conditions

Exiger que **tous** les critères soient remplis ne produit presque aucune configuration.
Onze critères remplis chacun 70 % du temps donnent 0,70¹¹ ≈ **2 % de survie** : sur dix ans et
sept paires, une poignée d'annonces par an — trop peu pour trader, trop peu pour prouver quoi
que ce soit.

**Structure retenue : trois filtres durs, puis un seuil de score.**

| Filtres durs — rejet automatique |
|---|
| Configuration à contre-tendance journalière |
| Annonce économique à fort impact dans l'horizon du trade |
| Objectif irréaliste : au-delà de 1,5 × ATR cumulé sur l'horizon |

Puis **score ≥ 7 sur 13** pour l'annonce — seuil initial, **à recalibrer sur les données une
fois 400 occurrences accumulées**, jamais fixé définitivement à l'avance. Le seuil est versionné :
le modifier crée une nouvelle version de stratégie (§15), et l'ancien historique reste intact.

### 9.2 Les critères

| # | Critère | Points | Calcul |
|---|---|---|---|
| 1 | **Tendance supérieure alignée** | +2 aligné D1 / +1 aligné H4 / **−2 à contre-tendance D1** | Pente MM200 + structure de sommets et creux |
| 2 | **Zone support/résistance** | +2 | À moins de 0,25 ATR d'un niveau touché ≥ 3 fois |
| 3 | **Niveau rond** | +1 | Prix en 00 ou 50. Effet documenté : les ordres stop se concentrent sur ces niveaux (Osler, 2003) |
| 4 | **Niveaux de référence** | +1 | Plus haut/bas de la veille ou de la semaine, ouverture journalière |
| 5 | **Divergence de momentum** | +1 | RSI divergent au sommet ou creux de la figure |
| 6 | **Objectif atteignable** | +1 / **−2 si irréaliste** | Objectif ≤ 1,5 × ATR cumulé sur l'horizon |
| 7 | **Séance horaire** | +1 chevauchement Londres–New York / **−1 séance asiatique ou heure de roulement** | Heure locale des places, changement d'heure pris en compte |
| 8 | **Calendrier économique** | **−2** | Annonce à fort impact prévue dans l'horizon |
| 9 | **Extension du mouvement** | **−1** | Prix à plus de 2 ATR de la MM20 : mouvement déjà mûr |
| 10 | **Qualité géométrique** | 0 à +2 | Symétrie, durée, nombre de touches, propreté des bornes |
| 11 | **Régime de marché** | +1 si cohérent | Continuation en tendance, retournement en range |

L'application publie l'espérance nette **par tranche de score** :

> Score 0-3 : −0,21 R · Score 4-6 : −0,04 R · Score 7+ : **+0,19 R** (n = 1 840)

Si le score ne sépare pas les résultats, **on le publie aussi**.

### 9.3 Redondance : une famille d'information, un seul représentant

*C'est le point où un score mal conçu compte plusieurs fois la même information et fabrique une
fausse certitude.*

| Constat vérifiable | Conséquence |
|---|---|
| **La bande centrale de Bollinger *est* la moyenne mobile 20** | Les compter tous deux, c'est compter deux fois la même chose |
| **MACD = moyenne exponentielle 12 − moyenne exponentielle 26** | Autre lecture du croisement de moyennes mobiles |
| RSI et MACD mesurent tous deux le momentum | Deux votes fortement corrélés |
| Largeur des bandes de Bollinger et ATR | Deux mesures de la même volatilité |

| Famille | Représentant retenu | Rôle |
|---|---|---|
| **Structure de prix** | Sommets et creux, cassures, bornes | **Autorité maximale** |
| **Tendance supérieure** | Pente MM200 + structure journalière | Fort |
| **Localisation** | S/R, niveaux ronds, références | Fort |
| **Momentum** | **RSI seul.** MACD écarté | Faible |
| **Volatilité** | **ATR seul.** Bollinger écarté | **Jamais directionnel** — faisabilité et dimensionnement uniquement |
| **Volume, VWAP** | **Écartés** | Aucun |

**Volume et VWAP : écartés.** Il n'existe pas de volume réel sur le change au comptant, marché
de gré à gré. Ce qu'affichent les plateformes est un **volume de ticks**, propre à chaque
courtier. L'utiliser rendrait les résultats non reproductibles par un tiers — ce qui contredit
frontalement le principe fondateur du produit. Affichables en information secondaire, jamais
dans le score.

### 9.4 Hiérarchie d'autorité en cas de désaccord réel

> **1. Structure de prix → 2. Tendance de l'unité de temps supérieure → 3. Zones →
> 4. Momentum → 5. Volatilité**

**Un indicateur ne prime jamais sur la structure.** Les indicateurs sont dérivés du prix ;
le prix n'est pas dérivé des indicateurs. Un RSI en surachat contre une structure haussière
intacte retire des points — il ne renverse rien.

### 9.5 On enregistre les contradictions, on ne les arbitre pas

**Interdit : écrire une règle faite à la main pour trancher une contradiction.** C'est ainsi
qu'on injecte une opinion invérifiable au cœur du système.

1. Les éléments contradictoires s'annulent naturellement dans le score. Une configuration
   contradictoire tombe à un score bas et n'est pas annoncée — sans règle spéciale.
2. La contradiction est **étiquetée** comme un état nommé et conservée
   (ex. *figure haussière + tendance journalière baissière + RSI en surachat*).
3. Au bout de 400 occurrences, **les données tranchent**.

### 9.6 Asymétrie : une contradiction retire plus qu'une confirmation n'ajoute

Une figure haussière contient **déjà** l'information « haussier ». Un indicateur qui confirme
répète ce que la figure dit. Un élément qui contredit apporte une information **absente** de la
figure : c'est là qu'est la surprise, donc la valeur.

| Type | Amplitude |
|---|---|
| Contradiction | **−2**, ou filtre dur |
| Confirmation | +1 à +2 |

Un score symétrique surévaluerait les configurations les plus évidentes — donc les plus déjà
intégrées dans le prix.

### 9.7 Neutraliser les critères contenus dans la définition de la figure

| Figure | Critère automatiquement satisfait | Problème |
|---|---|---|
| Drapeau, fanion | « Aligné avec la tendance » | La figure n'existe que dans une tendance : +2 gratuits |
| Double creux, ETE inversée | « Sur un support » | Le creux **est** le support |
| Cassure de range | « Niveau de référence » | La borne **est** le niveau |

**Sans correction, les figures de continuation obtiendraient mécaniquement de meilleurs scores
que les figures de retournement — pour une raison purement comptable.** Le classement
« quelles figures marchent le mieux », sortie principale du produit, serait faux.

**Règle : chaque figure déclare les critères que sa construction satisfait d'office. Ils sont
neutralisés, et le score s'exprime en pourcentage du maximum atteignable par cette figure**,
jamais en points bruts, afin que deux figures restent comparables.

### 9.8 Admission d'un nouvel indicateur

**Aucun indicateur n'entre dans le score sans que sa contribution marginale ait été mesurée**
sur un échantillon réservé, non utilisé pour le réglage. S'il n'améliore pas la séparation
d'espérance entre tranches de score, il est retiré.

Les pondérations initiales sont fixées à la main et **transparentes**. Elles ne seront
recalibrées **qu'une seule fois**, sur données suffisantes, par une méthode documentée et sur
échantillon réservé, puis figées dans une nouvelle version. Un score recalibré en continu sur
ses propres résultats est surajusté : excellent en historique, sans valeur en réel.

### 9.9 Exemple complet de calcul

**Double creux, EUR/USD, H4 — annoncée**

| Critère | Évaluation | Points |
|---|---|---|
| Qualité géométrique | 2 touches nettes, symétrie correcte | +2 |
| Tendance journalière | Haussière, alignée | +2 |
| Zone support | *Neutralisé — contenu dans la définition* | — |
| Niveau rond | Creux sur 1,0800 | +1 |
| Divergence de momentum | RSI divergent au second creux | +1 |
| Faisabilité de l'objectif | 1,1 × ATR cumulé | +1 |
| Séance | Cassure pendant le chevauchement Londres–New York | +1 |
| Calendrier économique | Aucune annonce à fort impact | 0 |
| Extension | Prix à 0,8 ATR de la MM20 | 0 |
| Régime | Retournement en régime de range : cohérent | +1 |
| **Total** | | **9 / 11 atteignables = 82 %** |

→ **Annoncée.** Confluence élevée : ratio minimum 1,5 R.

**Même figure, contexte différent :** tendance journalière opposée + objectif à 2,4 ATR →
**deux filtres durs → écartée**, motif affiché avec la statistique du groupe témoin.

### 9.10 La confluence renforce-t-elle vraiment ? C'est mesurable

L'hypothèse « un indicateur qui va dans le sens de la figure renforce le trade » est
**universellement admise et rarement vérifiée**. Trois résultats possibles, **les trois
publiables** :

1. La confirmation améliore l'espérance → le score est validé, argument commercial majeur.
2. Elle ne change rien → la confluence serait une croyance sans effet mesurable.
3. Elle la dégrade → les configurations les plus évidentes sont les plus déjà intégrées dans le
   prix. Contre-intuitif, et le plus vendable des trois.

Aucun outil existant ne permet de répondre sur données prospectives. C'est la contribution la
plus originale du produit.

---

## 10. Ratio, risque et dimensionnement

### 10.1 Règles retenues

| Contexte | Ratio minimum | Risque par trade |
|---|---|---|
| Score de confluence **élevé** | **1,5 R** | 1 % (2 % en variante, §10.2) |
| Score **normal** | **2 R** | 1 % |
| **Mode contrainte prop firm** | selon score | **0,5 %** |

| Ratio | Taux de réussite requis pour l'équilibre |
|---|---|
| 1,5 R | **40,0 %** |
| 2 R | **33,3 %** |
| 3 R | 25,0 % |

**Effet mécanique à assumer :** exiger 2 R fait baisser le taux de réussite affiché, car
beaucoup de figures n'ont pas 2 R d'espace avant l'obstacle structurel suivant. Le filtre de
ratio est lui-même un choix de stratégie, avec un coût mesurable — l'application le mesure,
elle ne le suppose pas.

### 10.2 Pourquoi 2 % de risque est écarté comme règle par défaut

*Calcul, pas opinion.* À 40 % de réussite, la plus longue série de pertes attendue sur 200
trades est d'environ **10 pertes consécutives**. Résultat normal, pas accident.

| Risque par trade | Perte après 10 pertes consécutives |
|---|---|
| 2 % | **− 18,3 %** |
| 1 % | − 9,6 % |
| 0,5 % | − 4,9 % |

Les sociétés de financement imposent typiquement **10 % de perte maximale totale et 5 % par
jour**. À 2 %, le compte saute avant la fin d'une série normale. À 1 %, il la frôle.

Le 2 % reste **affichable en variante**, avec la perte simulée correspondante affichée à côté.

### 10.3 Limite juridique absolue sur le dimensionnement

| Autorisé | Interdit |
|---|---|
| « Cette configuration se traite habituellement avec un risque de 1 % du capital » | « Vous avez 5 000 € : risquez 50 €, soit 0,11 lot » |
| Calculatrice exécutée **dans le navigateur**, valeur jamais transmise ni stockée | Capital enregistré dans le compte utilisateur |
| Statistiques identiques pour tous | Configurations filtrées ou classées selon le capital |

**Ligne rouge : dès que le capital de l'utilisateur influence *ce qui lui est montré*,
l'application devient une activité réglementée (§19).**

---

## 11. Règles de mesure du résultat

*Sans définition écrite et immuable, le pourcentage publié ne vaut rien et devient manipulable —
et il le sera, le jour où l'abonnement en dépendra.*

| Élément | Règle |
|---|---|
| Entrée | Au prix défini par la méthode déclarée. Jamais un prix intra-bougie arbitraire |
| Invalidation | Niveau structurel de la figure |
| **Objectif — double mesure** | **(a)** projection mesurée de la figure **et (b)** objectif fixe à 1,5 R / 2 R, calculés et publiés séparément |
| Horizon | Par défaut 20 bougies. Ni objectif ni invalidation atteints → **sans issue**, comptabilisé à part |
| Départage | **Résolution en données M1** pour savoir lequel de l'objectif ou de l'invalidation a été touché en premier dans une bougie |
| Frais déduits | Spread horaire réel **+ slippage sur invalidation + swap de portage** |
| Indicateur principal | **Espérance en R, nette de frais** |

La double mesure de l'objectif répond à « quelle stratégie marche le mieux » : elle dit si la
projection de la figure bat le ratio fixe, ou l'inverse.

**Le swap de portage est l'oubli le plus fréquent.** Sur une figure journalière tenue 20 jours,
les intérêts peuvent dépasser plusieurs fois le coût du spread. Tout résultat qui l'ignore est
faux sur les unités de temps longues.

### Décision d'affichage

Un taux de réussite de **70 % avec un objectif à 0,3 R perd de l'argent**. Un taux de **40 % à
2 R en gagne**. **L'espérance nette en R est mise en avant partout.** Le taux de réussite est
affiché en second, jamais en titre. Les trois issues (objectif, invalidation, sans issue) sont
toujours affichées ensemble : n'afficher que gagnants/perdants ment par omission.

---

## 12. Trois protections à afficher, que les autres outils omettent

1. **Série de pertes maximale attendue.** À 40 % de réussite, environ 10 pertes consécutives sur
   200 trades sont normales. Les utilisateurs abandonnent pendant ces séries en croyant que la
   méthode est cassée. L'afficher **avant** est la fonction de rétention la plus efficace du
   produit.
2. **Corrélation entre paires.** EUR/USD et GBP/USD évoluent ensemble à ~0,85. Deux positions de
   2 % dans le même sens ne font pas 4 % de risque mais **environ 3,8 % concentrés sur un seul
   pari**. L'application signale les détections corrélées simultanées.
3. **Écart entre résultat brut et net**, toujours côte à côte. C'est ce qui montre à
   l'utilisateur ce que les frais lui coûtent réellement.

---
---

# PARTIE III — TECHNIQUE

## 13. Données

| Besoin | Source | Coût |
|---|---|---|
| Historique M1 et tick | Dukascopy (tick, gratuit) ou HistData (M1, gratuit) | 0 € |
| Flux courant | API forex (Polygon, TraderMade, OANDA) | ~30-50 $/mois (estimation) |
| Calendrier économique | API de calendrier économique | 0-30 $/mois (estimation) |

**Piège spécifique au forex : il n'existe pas de prix consolidé.** Le change est de gré à gré,
chaque courtier a son flux. Les chandeliers de l'utilisateur ne seront jamais strictement
identiques aux tiens.

→ **Obligation : publier la source de prix retenue, et ne jamais en changer sans l'annoncer et
sans reconstruire l'historique sous une nouvelle version.**

**Politique de révision.** Les fournisseurs corrigent parfois des données passées. Règle : une
bougie déjà utilisée pour une détection publiée **n'est jamais modifiée**. Une correction reçue
est enregistrée à part et signalée sur les détections concernées, jamais appliquée
rétroactivement.

**Complétude.** Toute bougie manquante est détectée et journalisée. Une détection calculée sur
une période incomplète est marquée comme telle et **exclue des statistiques**, mais conservée.

---

## 14. Architecture et modèle de données

Pile choisie pour un développeur seul assisté par IA : peu de pièces, un seul langage, tout
reproductible.

| Couche | Choix | Motif |
|---|---|---|
| Traitement et API | Python (Polars, FastAPI) | Un seul langage, une seule surface de débogage |
| Base de données | PostgreSQL + TimescaleDB | **Une seule base.** Ni Kafka, ni Redis, ni microservices |
| Graphiques | TradingView Lightweight Charts | Gratuit, libre, conçu pour cet usage. **Ne jamais coder son propre moteur graphique** |
| Interface | SvelteKit ou Next.js | Indifférent. Ne pas y passer de temps en v1 |
| Hébergement | Un VPS (15-40 €/mois), Docker Compose, Caddy | Kubernetes serait une erreur à ce stade |
| Paiement | Stripe + Stripe Tax | Voir §20 et §25, lot 0 |
| Courriel transactionnel | Service tiers (Postmark, Resend) | La délivrabilité des alertes est critique |

### Modèle de données

| Table | Rôle |
|---|---|
| `instrument` | Paires, valeur du pip, horaires de séance |
| `bougie` | M1 et agrégats, spread estimé, indicateur de complétude |
| `version_strategie` | Version figée d'une figure × méthode : code, empreinte, paramètres, seuils, dates d'activation et de retrait |
| `detection` | Horodatage, niveaux, score et **détail critère par critère**, statut annoncée/écartée + motif, version, empreinte précédente, empreinte propre |
| `issue` | Atteint / invalidé / sans issue, excursions maximales favorable et défavorable, résultat brut et net, détail des frais |
| `ancrage` | Empreinte quotidienne publiée à l'extérieur, avec sa preuve (§15) |
| `trade_utilisateur` | Journal importé, éventuellement rapproché d'une détection |
| `notification` | Envois, canal, horodatage, latence mesurée |

---

## 15. Fiabilité, intégrité et preuve

*Le produit **est** ses chiffres. Une seule erreur méthodologique invalide l'ensemble et détruit
le seul avantage concurrentiel.*

### 15.1 Faille corrigée : le chaînage seul ne prouve rien

**Une chaîne d'empreintes détenue par celui qui la produit ne prouve rien** : il peut recalculer
toute la chaîne après coup. Le chaînage seul, tel que spécifié en version 1 de ce document,
était insuffisant.

**Correction obligatoire — ancrage externe quotidien.** Chaque jour, l'empreinte de tête de la
chaîne est publiée à un endroit que l'éditeur ne contrôle pas et qui est horodaté par un tiers :

- dépôt public versionné (commit horodaté et signé), **et**
- service d'horodatage qualifié, ou toute autre source tierce vérifiable.

À partir de là, réécrire l'histoire supposerait de réécrire aussi des enregistrements tiers
horodatés. **C'est ce qui transforme une affirmation en preuve** — et c'est le fondement de tout
l'argumentaire du produit. La procédure de vérification est publiée (écran 5, §6) pour que
n'importe qui puisse la refaire.

### 15.2 Les sept règles non négociables

1. **Point-in-time strict.** La fonction de détection ne reçoit qu'une tranche en lecture seule
   des bougies jusqu'à `t`. Un test automatisé injecte des données futures et vérifie que le
   résultat ne change pas. **Test le plus important du projet.**
2. **Test de déterminisme en intégration continue.** Chaque nuit : recalcul complet de
   l'historique, comparaison des empreintes. Toute divergence fait échouer la compilation et
   impose une nouvelle version de stratégie. *Coût : une journée. Sans ça, l'historique se
   réécrit silencieusement à chaque correction de bug.*
3. **Ancrage externe quotidien** (§15.1).
4. **Versionnement des stratégies.** Une stratégie modifiée est une stratégie **nouvelle**.
   L'ancienne conserve son historique. On ne supprime jamais, on remplace.
5. **Résolution intra-bougie en M1** obligatoire. C'est l'erreur qui gonfle artificiellement
   tous les taux de réussite amateurs.
6. **Frais réels** : spread horaire modélisé depuis les données tick, slippage, swap.
   Jamais de constante.
7. **Pré-enregistrement.** Toute nouvelle stratégie est déclarée et publiée **avant** d'être
   observée. Interdiction de publier le résultat d'une stratégie testée en privé puis retenue
   parce qu'elle donnait un bon chiffre. Protection contre le test multiple — et contre soi-même.

---

## 16. Sécurité, sauvegarde et supervision

*Pourquoi ça compte : le journal prospectif est l'unique actif de l'entreprise. Le perdre, ou
le laisser se trouer sans s'en apercevoir, détruit la valeur accumulée — et elle n'est pas
reconstituable.*

### Sauvegarde

- Sauvegarde quotidienne chiffrée, **hors du serveur de production**, chez un autre fournisseur.
- **Test de restauration mensuel effectif.** Une sauvegarde jamais restaurée n'est pas une
  sauvegarde.
- Conservation : quotidienne 30 jours, mensuelle 12 mois, annuelle sans limite.
- L'ancrage externe (§15.1) constitue une seconde ligne : même en cas de perte totale, les
  empreintes publiées permettent de prouver ce qui avait été publié.

### Supervision — ce qui doit déclencher une alerte immédiate

| Événement | Pourquoi c'est grave |
|---|---|
| Flux de données interrompu ou bougie manquante | Détections manquantes → journal incomplet → crédibilité perdue |
| Traitement par lots échoué ou en retard | Idem |
| Latence de notification > 60 s | Promesse produit non tenue (§5, module G) |
| Ancrage quotidien non publié | La preuve du jour est absente |
| Échec du test de déterminisme | L'historique a peut-être bougé |

**Page publique d'intégrité** (écran 5) : taux de complétude des données, ancrages publiés,
incidents passés. Publier ses propres pannes est cohérent avec le positionnement — et
personne ne le fait.

### Sécurité

- Authentification déléguée, mots de passe jamais stockés en clair, second facteur proposé.
- Secrets hors du dépôt, chiffrés.
- Dépendances mises à jour, analyse automatique des vulnérabilités.
- Accès administrateur nominatif et journalisé.
- Données du journal utilisateur chiffrées au repos.

---

## 17. Tests et qualité

| Type de test | Contenu |
|---|---|
| **Point-in-time** | Injection de données futures : le résultat doit être identique |
| **Déterminisme** | Recalcul complet nocturne, comparaison des empreintes |
| **Jeu de référence annoté** | 100 configurations étiquetées à la main par figure : le détecteur doit les retrouver, et ne pas en inventer |
| **Résolution** | Cas construits où objectif et invalidation sont touchés dans la même bougie : le départage M1 doit trancher correctement |
| **Frais** | Un trade de contrôle dont le résultat net est calculé à la main |
| **Changement d'heure** | Les critères de séance restent corrects de part et d'autre des bascules |
| **Complétude** | Une période à données trouées produit des détections marquées et exclues des statistiques |
| **Non-régression** | Toute correction de bug ajoute le cas qui l'a révélée |

Environnements séparés développement / production, migrations de base versionnées,
déploiement automatisé et réversible.

---

## 18. Performance et coûts

- Volume : 7 paires × 3 unités de temps × 20 ans ≈ **1,1 million de bougies**. Cela tient en
  mémoire vive. Une passe complète de détection se compte en secondes ou minutes.
- **Le calcul est identique pour tous les utilisateurs** : précalcul à chaque clôture de bougie,
  service depuis le cache. **Coût marginal par abonné proche de zéro.**
- **Traitement par lots, jamais de flux tick en temps réel.** C'est le seul moyen de créer un
  problème de performance, et il n'apporte rien : les figures en H1, H4 et journalier ne bougent
  pas à la seconde.

**Coût d'infrastructure total avant le premier client : moins de 150 €/mois** (hébergement,
données, courriel, sauvegarde). Ce n'est pas là qu'est le risque.

---
---

# PARTIE IV — EXPLOITATION

## 19. Cadre juridique et interdits

*Une seule de ces lignes franchie transforme un logiciel en activité réglementée.*

| Sujet | Position |
|---|---|
| **Agrément conseiller en investissement financier (CIF)** | **Non requis**, à une condition stricte : aucune personnalisation. L'application ne doit jamais connaître le capital, le portefeuille ni le profil de risque de l'utilisateur pour produire une analyse (MiFID II, règl. délégué UE 2017/565, art. 9) |
| **Formulation** | Toujours « voici comment ce type de figure se trade habituellement », jamais « prenez ce trade ». Réserve honnête : c'est une précaution **supplémentaire**, pas le rempart principal. Le rempart, c'est l'absence de personnalisation |
| **Règlement MAR (UE 596/2014, art. 20)** | Champ incertain sur le forex de détail : le change au comptant n'est pas un instrument financier au sens de MiFID II annexe I section C. **On applique la discipline quand même** : auteur identifié, date, méthodologie publiée, historique complet accessible, avertissement |
| **Loi Sapin 2 — art. L.222-16-1 code de la consommation** | **Interdit la publicité électronique** pour les contrats financiers hautement spéculatifs auprès du public en France. Loi influenceurs (n° 2023-451) : même interdiction. Google Ads et Meta : restreint ou interdit |
| **RGPD** | Le journal utilisateur contient des données financières personnelles : hébergement UE, registre des traitements, contrats de sous-traitance, export et suppression sur demande, durée de conservation définie |

### Les cinq interdits absolus dans le produit

1. Ne jamais demander le capital ou le profil de risque pour produire une analyse.
2. Ne jamais écrire « achetez », « vendez », « prenez ce trade », « recommandé pour vous ».
3. Ne jamais afficher une taille de position adaptée à l'utilisateur.
4. Ne jamais promettre un rendement, ni afficher un gain en euros.
5. Ne jamais supprimer ou corriger une détection publiée.

### Documents obligatoires avant mise en ligne

Mentions légales · CGU · CGV · politique de confidentialité · politique de cookies ·
**avertissement de risque visible sur chaque page affichant une statistique**.

**Le tout à faire valider par un avocat spécialisé avant toute mise en ligne payante.**

### Conséquence opérationnelle majeure

**L'acquisition payante est fermée.** Le canal doit être organique (§22). La page publique du
journal prospectif est l'outil d'acquisition principal — pas une fonctionnalité annexe.

---

## 20. Juridictions, structure et fiscalité

*Pourquoi ça compte : un abonnement vendu dans le monde entier déclenche des obligations
fiscales dès le premier client étranger. C'est l'oubli le plus courant des projets logiciels.*

### Juridictions

| Zone | Position de départ |
|---|---|
| France et UE | Marché principal |
| **États-Unis** | **Exclus au lancement.** L'encadrement du conseil sur le change y est strict (CFTC / NFA) et les exemptions applicables demandent un avis juridique. Exclusion par les CGU tant que cet avis n'est pas obtenu |
| Autres pays | Ouverts par défaut, sauf pays sous sanctions |

Le blocage se fait par les CGU et par une déclaration de résidence à l'inscription.

### Structure

Micro-entreprise au démarrage. Passage en société à examiner dès que le chiffre d'affaires ou
la responsabilité le justifient. Question à trancher avec un comptable (§28).

### TVA — point technique à ne pas rater

La vente d'un **service numérique à un particulier dans l'UE** est taxée **au taux du pays du
client**, et non au taux français. Au-delà de 10 000 € de ventes transfrontalières annuelles,
cela impose une déclaration via le **guichet unique (OSS)**.

**Solution retenue : activer Stripe Tax dès le premier abonnement.** Le calcul et la collecte
sont automatisés pour un coût de l'ordre de 0,5 % du volume — sans commune mesure avec le coût
d'une régularisation.

**À confirmer avec un comptable** avant la première facture (§28).

---

## 21. Modèle économique

| Niveau | Contenu | Prix |
|---|---|---|
| **Public, sans compte** | Journal prospectif en direct, groupe témoin, fiches figures, statistiques agrégées principales | **0 €** — outil d'acquisition, pas version bridée |
| **Standard** | Base interrogeable complète, tous filtres, alertes, journal personnel, écart comportemental | **19 €/mois** |
| **Contrainte** | Mode prop firm, export, accès API | **39 €/mois** |

Essai de 14 jours sur les niveaux payants. Remise annuelle à examiner une fois la rétention
mesurée (§28).

Repère de volume : **165 abonnés à 19 €**, ou **100 abonnés à 29 €**, pour 2 500 €/mois brut.

Le niveau gratuit n'est pas une concession commerciale : la publicité étant fermée (§19), c'est
la seule mécanique d'acquisition dont dispose le produit, et elle se renforce avec le temps.

---

## 22. Acquisition et croissance

*Pourquoi ça compte : la publicité payante étant interdite, l'acquisition est une contrainte de
conception, pas une activité qui viendra après.*

### Le moteur principal : le référencement naturel programmatique

La base de données **génère elle-même** des milliers de pages de contenu unique, chiffré et
constamment mis à jour :

> *« Double creux EUR/USD en H4 : 1 240 cas mesurés, 46 % d'objectifs atteints,
> espérance nette +0,08 R »*

- 60 figures × 28 paires × 3 unités de temps = **plus de 5 000 pages** possibles, chacune
  répondant à une requête que des gens tapent réellement.
- Contenu impossible à copier : il provient de la base propriétaire.
- Coût marginal nul, et la qualité s'améliore automatiquement à mesure que les occurrences
  s'accumulent.

**C'est le meilleur atout de croissance du produit, et il découle directement de son
architecture.** À traiter comme une fonctionnalité de premier plan, pas comme du marketing.

### Canaux complémentaires

| Canal | Rôle |
|---|---|
| Journal prospectif public | Preuve permanente, motif de retour régulier |
| Vidéo (résultats mensuels commentés, échecs compris) | Le format le plus crédible pour ce public |
| Communautés (forums, Reddit, Discord de traders) | Contribution par les chiffres, jamais par la promotion |
| **Espace communautaire propre, hébergé à l'extérieur** (Discord ou Telegram) | Satisfait le besoin d'échange sans exposer la plateforme (§5, module I) |
| Sociétés de financement | Partenariats de contenu — leur intérêt est que leurs candidats réussissent |

### Revenus interdits

**Aucune rémunération d'apport d'affaires versée par un courtier, jamais.** C'est le revenu le
plus facile à obtenir sur ce marché, et le seul qui détruirait instantanément le positionnement :
un produit qui mesure les coûts de transaction ne peut pas être payé par ceux qui les facturent.
Refus inscrit dans les conditions d'utilisation et publié.

### Ouverture des données anciennes

Les détections **résolues depuis plus de 90 jours** sont publiées en jeu de données ouvert,
téléchargeable et réutilisable avec citation.

*Pourquoi c'est un gain net :* la valeur commerciale est dans le flux courant et dans l'analyse,
pas dans des lignes vieilles de trois mois. En les ouvrant, on devient **la source que les autres
citent** — chercheurs, formateurs, vidéastes, journalistes. Chaque citation est un lien, une
autorité, et une preuve supplémentaire qu'il n'y a rien à cacher. Aucun concurrent de ce marché
ne peut se le permettre.

### Outils gratuits à fort volume de recherche

Calculatrice de position, valeur du pip, horloge des séances, matrice de corrélation, calendrier
économique. Aucun avantage de marché n'est nécessaire pour les construire, ils répondent à des
requêtes très recherchées, et ils alimentent le référencement du reste du site.

### Publication mensuelle des résultats

Un rapport public mensuel, **à date fixe et format fixe**, publié même quand les chiffres sont
mauvais : espérance du mois, écarts par rapport à l'historique, incidents techniques.
C'est le rituel qui construit la réputation, et c'est exactement ce qu'aucun concurrent ne peut
imiter.

### L'invitation à la vérification

Le script de vérification de la chaîne d'empreintes et des ancrages est **publié et documenté**.
N'importe qui est invité à recalculer l'historique et à contester un chiffre.
Sur un marché saturé de résultats fabriqués, c'est l'argument le plus difficile à ignorer —
et il ne coûte qu'une page de documentation.

---

## 23. Métriques et pilotage

| Métrique | Cible initiale |
|---|---|
| Visiteurs uniques mensuels | Croissance mensuelle continue |
| Taux de création de compte | > 3 % des visiteurs |
| **Taux d'import du journal** (activation) | **> 40 % des comptes créés** — meilleur prédicteur d'abonnement |
| Conversion essai → abonnement | > 25 % |
| **Rétention à 3 mois** | **> 60 %** — la métrique qui décide de la viabilité |
| Attrition mensuelle | < 8 % |
| Revenu mensuel récurrent | Suivi hebdomadaire |
| Latence médiane des notifications | < 60 s |
| Complétude des données | > 99,9 % |

**Métrique de vérité produit, à publier :** espérance nette des configurations annoncées,
comparée au groupe témoin. Si l'écart disparaît, le produit doit changer de discours (§27).

---

## 24. Support

- **Asynchrone par écrit**, en français et en anglais. Délai annoncé : 48 h ouvrées.
- Base de connaissances alimentée par les questions reçues.
- **Aucune réponse individuelle ne doit jamais contenir de conseil personnalisé** : c'est le
  canal par lequel l'interdit du §19 est le plus facile à franchir par inadvertance.
  Réponses types préparées pour les questions du type « dois-je prendre ce trade ? ».

---
---

# PARTIE V — EXÉCUTION

## 25. Ordre de construction

*L'ordre compte plus que le contenu : chaque lot doit produire quelque chose de vérifiable.*

| Lot | Contenu | Critère d'acceptation |
|---|---|---|
| **0** | Compte Stripe (activité décrite comme **logiciel d'analyse statistique**) validé. Consultation juridique de cadrage | **Avant d'écrire du code** : un refus bloquerait toute monétisation après des mois de travail |
| **1** | Ingestion, stockage, **harnais de déterminisme et test point-in-time** | Le test d'injection de données futures échoue si on triche. Recalcul complet reproductible à l'identique |
| **2** | **Une seule stratégie : le range**, de bout en bout, résolution M1 et frais complets. **Backtest honnête walk-forward avec correction de tests multiples** | 500 détections résolues, résultat net calculé, reproductible deux fois à l'identique. **Ce lot est un point de décision** (§25.1) |
| **3** | Journal prospectif + chaînage + **ancrage externe quotidien** + page publique gratuite + **script de vérification publié** | En ligne et accumulant des détections **pendant** que le reste se développe. Un tiers doit pouvoir vérifier la chaîne sans aide |
| **4** | Score de confluence + filtres durs + **conservation du groupe témoin** | Une détection écartée est conservée avec motif et score détaillé |
| **5** | **Import du journal utilisateur + écart comportemental** | Un rapport MT5 réel s'importe et produit un écart chiffré. **Remonté du lot 9 : voir §25.2** |
| **6** | Abonnement Stripe + Stripe Tax + documents légaux | Un paiement de bout en bout, TVA correcte, CGU en ligne |
| **7** | Notifications (courriel, web push) + supervision de la latence | Annonce envoyée en moins de 60 s, latence journalisée |
| **8** | Interface stratégie + premier lot de figures (10 à 15) | Ajouter une figure ne demande aucune modification du moteur |
| **9** | Base interrogeable + seuils de publication + correction de tests multiples + **affichage systématique des comparaisons** | Une figure sous 100 occurrences affiche « données insuffisantes ». Aucun chiffre affiché sans terme de comparaison |
| **10** | Fiches figures + **référencement programmatique** + **outils gratuits** (calculatrice de position, corrélations, séances) | Les pages se génèrent depuis la base et se mettent à jour seules |
| **11** | Mode contrainte prop firm | Réponse en probabilité de réussite de la contrainte, pas en rendement |
| **12** | **Ouverture des données de plus de 90 jours + premiers contacts sociétés de financement** | Jeu de données téléchargeable. **Remonté de la fin : voir §25.3** |
| **13** | Catalogue complet, extension à 28 paires | Occurrences multipliées, seuils franchis |
| **14** | Commentaires horodatés et verrouillés + obligations d'hébergeur | Un commentaire publié avant l'issue ne peut plus être modifié |
| **15** | API et licence de la base (B2B contractualisé) | — |

### 25.1 Le lot 2 est un point de décision, pas une étape

Le backtest honnête du lot 2 donne, **en quelques semaines au lieu de six mois**, une première
indication sur l'existence d'un avantage. Il ne prouve rien pour un client — mais il informe la
décision de positionnement :

| Résultat du lot 2 | Conséquence |
|---|---|
| Espérance nette clairement positive après correction | Le discours « quelles configurations gagnent » est tenable |
| Espérance proche de zéro | **Basculer immédiatement sur le discours comparatif** (§2) et sur l'analyse comportementale. Ne pas attendre six mois pour l'apprendre |
| Espérance nettement négative | Le produit devient *l'outil qui chiffre ce que l'analyse technique coûte* — position unique et vendable, mais qui change les fiches produit et l'argumentaire |

Coût de cette information : quelques semaines. Valeur : elle oriente tout le reste.

### 25.2 Pourquoi l'analyse comportementale remonte au lot 5

Décision structurante, motivée par trois faiblesses du plan initial :

1. **Elle ne dépend pas de l'existence d'un avantage de marché.** Dire à quelqu'un qu'il entre
   deux bougies trop tôt garde toute sa valeur même si aucune figure n'est rentable.
   C'est la seule fonction robuste au risque principal du projet.
2. **Sa valeur est personnelle et immédiate**, donc c'est la fonction qui convertit en
   abonnement. La base de figures attire ; le miroir comportemental fait payer.
3. **Elle compose avec le nombre d'utilisateurs, pas avec le calendrier.** Le journal prospectif
   met deux ans à devenir un fossé ; la base comportementale grandit dès le premier import.

**Position retenue : la base de figures est le moteur d'acquisition, l'analyse comportementale
est le produit payant.** Aucun concurrent ne peut la reproduire, car un journal de trading sans
base de référence ne peut comparer à rien.

### 25.3 Pourquoi le B2B remonte au lot 12

Le référencement met 12 à 24 mois à composer et la publicité est interdite : la distribution est
le vrai goulot du projet, pas le produit.

Une société de financement compte des dizaines de milliers de candidats. **Un seul partenariat
apporte en un mois ce que le référencement met deux ans à construire.** Et ce public achète
sur preuve, pas sur promesse — ce qui transforme la principale faiblesse commerciale du produit
en avantage. Les premiers contacts n'exigent qu'un journal prospectif de six mois et le mode
contrainte : ils sont possibles bien avant la fin du développement.

### Pourquoi commencer par le range

Le range se définit **objectivement** (bornes, nombre de touches, durée), il est **fréquent** —
donc il donne une puissance statistique exploitable en quelques mois au lieu de plusieurs années
— et les paires majeures passent la majorité de leur temps en range. L'épaule-tête-épaule est
subjective et rare : c'est le pire premier cas possible.

---

## 26. Risques et parades

| # | Risque | Parade |
|---|---|---|
| 1 | **Publier un chiffre non reproductible.** Un utilisateur recalculera. Un seul écart inexpliqué détruit l'unique argument du produit | §15, sans exception |
| 2 | **Embellir les résultats** le jour où l'abonnement en dépend | §27 : règle écrite **maintenant**, avant tout revenu |
| 3 | **Refus du processeur de paiement** (le forex est classé activité à risque) | Lot 0, avant le code |
| 4 | **Perte de la base** | §16 : sauvegardes hors site, restauration testée, ancrage externe |
| 5 | **Trous de données non détectés** | §16 : supervision de complétude, marquage et exclusion des périodes incomplètes |
| 6 | **Élargir avant d'avoir prouvé** | Seuils du §7 |
| 7 | **Le H1 est un piège.** Spread aller-retour ~1,2-2 pips contre une amplitude horaire typique de 10-15 pips : le coût consomme **~15 % du mouvement en H1, contre ~2 % en journalier** | Garder le H1 mais afficher le net à côté du brut. L'écart est une information que les utilisateurs ignorent |
| 8 | **Attente d'un avantage important sur les majeures** | Marché le plus liquide du monde : 7 500 Md$/jour (BIS 2022). Avantage attendu proche de zéro. **Le produit doit avoir de la valeur même quand les chiffres sont mauvais** (§27) |
| 9 | **Dépendance à une source de données unique** | Prévoir une seconde source, et documenter que tout changement crée une nouvelle version |
| 10 | **Exposition juridique hors UE** | §20 : exclusion des États-Unis au lancement |
| 11 | **Contenus d'utilisateurs** : recommandations publiées par des tiers, promotion de courtiers, escroqueries, conseil personnalisé public | §5 module I : **pas de chat en direct**. Uniquement des commentaires verrouillés attachés à une détection, plus une communauté externe au produit |

---

## 27. Règle d'honnêteté — à signer avant le premier euro encaissé

Le journal prospectif dira la vérité au bout de 3 à 6 mois. Deux issues :

- **Espérance nette positive et stable** → le produit a une valeur démontrable que personne
  d'autre ne fournit.
- **Espérance nette nulle ou négative** → **on publie le chiffre tel quel.** Le produit bascule
  sur ce qu'il est réellement : *l'outil qui montre, chiffres à l'appui, ce que l'analyse
  technique ne fait pas.* C'est un produit vendable, et une position unique sur ce marché.

**Décision prise par écrit maintenant, avant tout revenu : dans le second cas, le chiffre est
publié sans retouche.** Seule protection contre la tentation de le trafiquer quand l'abonnement
en dépendra.

---

## 28. Ce qui reste à décider

*Regroupé ici, et nulle part ailleurs. Aucun de ces points ne bloque le lot 1.*

| # | Question | Qui tranche | Quand |
|---|---|---|---|
| 1 | Validation juridique complète du positionnement et des CGU | Avocat spécialisé | Avant le lot 8 |
| 2 | Statut des États-Unis : exclusion définitive ou ouverture encadrée | Avocat | Année 1 |
| 3 | Structure juridique et régime de TVA | Comptable | Avant la première facture |
| 4 | Source de prix de référence définitive | Décision technique, après essai de deux fournisseurs | Lot 1 |
| 5 | Seuil de score pour l'annonce | **Les données**, après 400 occurrences | Après le lot 6 |
| 6 | Prix définitifs et remise annuelle | Après mesure de la rétention | Après le lot 9 |
| 7 | Priorité Telegram par rapport au webhook | Demande des utilisateurs | Après le lot 7 |
| 8 | Ouverture à d'autres classes d'actifs | À n'envisager qu'une fois le forex prouvé | Année 2 |

---

## 29. Glossaire

| Terme | Définition |
|---|---|
| **R** | Unité de risque. 1 R = distance entre l'entrée et l'invalidation. Un gain de 2 R rapporte deux fois ce qu'on risquait |
| **Espérance en R** | Gain moyen par trade en R. Seul indicateur qui dit si une approche gagne de l'argent |
| **Spread** | Écart entre prix d'achat et de vente. Coût payé à chaque opération |
| **Slippage** | Écart entre le prix attendu et le prix réellement obtenu |
| **Swap de portage** | Intérêts payés ou reçus pour conserver une position d'un jour sur l'autre |
| **Pip** | Plus petite variation usuelle d'une paire. 0,0001, sauf paires en yen : 0,01 |
| **M1 / H1 / H4 / D1** | Bougies de 1 minute / 1 heure / 4 heures / 1 jour |
| **ATR** | Amplitude moyenne récente. Sert à fixer des seuils qui s'adaptent à la volatilité |
| **Pivot / ZigZag** | Repérage automatique des sommets et creux significatifs |
| **Confluence** | Convergence de plusieurs éléments favorables. Doit être chiffrée pour être exploitable |
| **Corrélation** | Degré auquel deux paires bougent ensemble. Deux positions corrélées sont un seul pari |
| **Série de pertes** | Nombre de pertes consécutives. Des séries longues sont normales et prévisibles |
| **Régime de marché** | État dominant : tendance ou range. Conditionne quelles figures fonctionnent |
| **Volume de ticks** | Nombre de changements de prix. Remplace sur le forex le volume réel qui n'existe pas — et diffère d'un courtier à l'autre |
| **Point-in-time** | Principe garantissant qu'un calcul n'utilise que l'information disponible à l'instant simulé |
| **Look-ahead bias** | Utilisation d'une information future. Rend tout backtest faussement excellent |
| **Test multiple** | Essayer beaucoup d'hypothèses fait apparaître des résultats « significatifs » par pur hasard |
| **Intervalle de confiance** | Fourchette dans laquelle se situe probablement la vraie valeur. Se resserre quand les occurrences augmentent |
| **Drawdown** | Perte maximale subie depuis un sommet de capital |
| **Groupe témoin** | Ensemble des configurations écartées, conservées pour mesurer ce que vaut le filtrage |
| **Ancrage externe** | Publication chez un tiers horodateur d'une empreinte, rendant toute réécriture ultérieure détectable |
| **Prop firm** | Société qui finance un trader après un examen payant, sous contrainte stricte de perte maximale |
| **Prospectif** | Publié **avant** de connaître le résultat. Seul mode qui prouve quelque chose |
| **OSS (guichet unique)** | Régime européen de déclaration de la TVA sur les services numériques vendus à des particuliers d'autres pays de l'UE |

---

## 30. Sources et références

- Bulkowski, *Encyclopedia of Chart Patterns* — catalogue de référence des figures
- Lo, Mamaysky & Wang (2000), *Foundations of Technical Analysis*, Journal of Finance
- Sullivan, Timmermann & White (1999) — biais de sélection sur les règles techniques
- Bajgrowicz & Scaillet (2012) — rentabilité des règles techniques après frais et test multiple
- Bailey & López de Prado — *Deflated Sharpe Ratio*
- Osler (2003), *Currency Orders and Exchange Rate Dynamics*, Journal of Finance — concentration
  des ordres sur les niveaux ronds
- Benjamini & Hochberg (1995) — contrôle du taux de fausses découvertes
- Enquête triennale BIS, avril 2022 — volumes du marché des changes
- Règlement (UE) 596/2014 (MAR), art. 20 ; règlement délégué (UE) 2016/958
- Directive MiFID II ; règlement délégué (UE) 2017/565, art. 9
- Code de la consommation, art. L.222-16-1 (loi Sapin 2)
- Règlement (UE) 2016/679 (RGPD)
