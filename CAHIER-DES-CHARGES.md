# Cahier des charges

## Application d'analyse statistique de configurations chartistes sur le marché des changes

Version 3 — septembre 2026. Document de référence, autoportant.

---

## Comment lire ce document

| | |
|---|---|
| **Destinataire** | Toute personne appelée à construire, financer ou évaluer le produit |
| **Prérequis** | Aucun. Les termes techniques sont définis au §32 |
| **Statut des décisions** | Toutes les décisions de ce document sont **arrêtées**. Les rares points encore ouverts sont regroupés au §31, et nulle part ailleurs |
| **Documents d'implémentation** | `SPEC-LOT2.md` · `SPEC-LOT3.md` · `SPEC-LOT5.md` · `SPEC-LOT11.md` · `SPEC-DESIGN.md` |
| **Règle de préséance** | Un document d'implémentation fait foi sur les formules. Ce cahier des charges fait foi sur les principes |

Les sections techniques commencent par une ligne *Pourquoi ça compte*.

---

## Sommaire

| Partie | Contenu | Sections |
|---|---|---|
| **I** | Le produit | 1 à 6 |
| **II** | La méthode — le cœur du dossier | 7 à 14 |
| **III** | La technique | 15 à 21 |
| **IV** | L'exploitation | 22 à 27 |
| **V** | L'exécution | 28 à 33 |

---
---

# PARTIE I — LE PRODUIT

## 1. Résumé exécutif

L'application détecte automatiquement les configurations chartistes sur le marché des changes,
explique **comment ce type de configuration se trade habituellement**, publie chaque détection
**avant d'en connaître l'issue** dans un registre infalsifiable ancré chez des tiers, puis
mesure le résultat **frais déduits** — y compris pour les configurations qu'elle a écartées.

L'utilisateur peut importer son propre relevé de courtier et se comparer à cette base.

### La proposition en une phrase

> Nous ne vous disons pas quoi acheter. Nous vous disons ce que cette configuration a
> réellement donné les 1 240 fois précédentes, frais compris — y compris quand le résultat
> nous dessert.

### Ce que fait ce produit et que personne ne fait

| L'existant | Ce produit |
|---|---|
| Un historique fabriqué après coup | Un registre **prospectif**, publié avant l'issue, horodaté par des tiers indépendants |
| Un taux de réussite brut | Une **espérance en R, nette de tous frais** — spread, glissement et portage |
| Seulement les configurations retenues | **Les configurations écartées aussi**, comme groupe témoin publié |
| Un contenu pédagogique déconnecté des chiffres | **La méthode enseignée est exactement celle qui est mesurée** |
| « 92 % de réussite » | « Données insuffisantes : 37 occurrences, 100 nécessaires » |

## 2. Les quinze décisions arrêtées

*Un développeur qui ne lirait que ce tableau saurait déjà à quoi il a affaire.*

| # | Décision | Motif |
|---|---|---|
| 1 | **Publier avant de savoir**, avec ancrage horaire chez trois tiers indépendants | Seule preuve qu'un concurrent ne peut pas fabriquer rétroactivement |
| 2 | **Conserver et publier les configurations écartées** | Sans groupe témoin, la valeur du filtrage est indémontrable |
| 3 | **Publier des comparaisons, jamais un chiffre seul** | Rend le produit robuste à l'absence d'avantage de marché — l'issue la plus probable |
| 4 | **Espérance nette en R** en indicateur principal, jamais le taux de réussite | 70 % de réussite à 0,3 R perd de l'argent ; 40 % à 2 R en gagne |
| 5 | **Aucune personnalisation** : jamais le capital ni le profil de risque | Seule chose qui évite le statut de conseiller en investissement financier |
| 6 | **Aucun contenu produit par un utilisateur** : ni figure, ni trade, ni commentaire publié | Une seule source, donc une seule vérité. Aucune modération, aucune exposition aux tiers |
| 7 | **Déterminisme absolu**, tout recalculable, versions figées | Le produit *est* ses chiffres. Un historique qui bouge détruit tout |
| 8 | **Les prix sont en direct, la mesure ne l'est pas** | Une détection recalculée à chaque tick serait non reproductible, donc invérifiable |
| 9 | **On apprend en H1, on annonce en H4** | La puissance statistique est en H1, la friction supportable en H4 |
| 10 | **Détecter tout le catalogue, ne publier qu'au-delà de 100 occurrences** | Sans seuil, tester 500 combinaisons fabrique une vingtaine de faux avantages |
| 11 | **Le score de confluence est déterministe et versionné**, son seuil fixé par les données | Une confluence non chiffrée réintroduit la subjectivité au cœur du système |
| 12 | **L'analyse comportementale est le produit payant**, la base de figures est l'acquisition | Elle ne dépend d'aucun avantage de marché et croît avec les utilisateurs |
| 13 | **Deux accès seulement : individuel et groupe**, le groupe s'administrant lui-même | Sert tous les publics sans ajouter de produit ni d'heure de support |
| 14 | **Aucune rémunération d'un courtier indexée sur le volume négocié** | Celui qui facture les coûts ne peut pas payer celui qui les mesure |
| 15 | **Publier les mauvais chiffres tels quels**, règle écrite avant tout revenu | Seule protection contre la tentation de les trafiquer |

## 3. Position concurrentielle

*Un cahier des charges qui revendique l'unicité sans nommer ses concurrents n'est pas sérieux.*

| Acteur | Ce qu'il fait | Ce qu'il ne fait pas |
|---|---|---|
| **Autochartist** — le concurrent réel | Reconnaissance automatique de figures, indice de qualité, statistiques historiques. Distribué en marque blanche par de nombreux courtiers | Aucun registre prospectif public et ancré, aucun groupe témoin, aucun résultat net de portage, aucun croisement avec le journal de l'utilisateur, aucun mode contrainte. Produit **vendu aux courtiers**, sans réputation propre auprès du public |
| TradingView | Graphiques, screener, communauté immense | Aucune statistique d'issue mesurée et publiée |
| Bulkowski, *Encyclopedia of Chart Patterns* | Statistiques de référence sur plus de 60 figures | Un livre. Actions américaines, rétrospectif, sans frais, figé, non interrogeable |
| Tradezella, Edgewonk, TraderVue | Journaux de trading et statistiques personnelles | Aucune base de référence à laquelle se comparer |
| Vendeurs de signaux | Des promesses | Aucune vérifiabilité. C'est le repoussoir — et le vivier de clients |

### Ce qu'il faut en conclure

**Le moteur de détection n'est pas un avantage : Autochartist prouve qu'il est une marchandise
banale, copiable en trois mois.** La différenciation tient entièrement à cinq choses que
personne ne fait : registre prospectif ancré, groupe témoin publié, résultats nets de tous
frais, croisement avec le journal personnel, mode contrainte.

Le positionnement n'est donc pas *« le premier à détecter des figures »* mais
**« le seul dont les chiffres sont vérifiables par un tiers »**.

### L'honnêteté comme barrière à l'entrée

Le marché des outils de trading vit de promesses invérifiables. Un produit dont le mécanisme
central est *« nous publions nos échecs »* est inimitable par les acteurs installés : basculer
vers la transparence détruirait les chiffres qu'ils affichent déjà.

**Cible assumée : non pas celui qui cherche des signaux, mais celui qui s'est déjà fait avoir
par des signaux.** Segment réel, atteignable uniquement en organique — ce qui tombe bien,
puisque la publicité payante est de toute façon fermée (§22).

## 4. Publics et accès

Le produit s'adresse à tous les publics. Il n'existe pourtant que **deux accès**, et c'est ce
qui le rend tenable pour une équipe d'une personne.

| Accès | Pour qui | Administration | Facturation |
|---|---|---|---|
| **Individuel** | Une personne | Elle-même | Mensuelle, par carte |
| **Groupe** | Société de financement, courtier, école, équipe, média | **Un administrateur désigné chez le client, qui crée et retire ses membres lui-même** | Facture unique, au siège |

> **Un seul moteur, une seule base, les mêmes chiffres. Les accès diffèrent par
> l'administration et la facturation — jamais par le contenu.**

Un membre d'un groupe voit exactement ce que voit un abonné individuel. Aucune version
professionnelle, aucun chiffre réservé, aucune marque blanche. Sans cette règle, chaque public
ajouterait un produit à maintenir et les chiffres finiraient par diverger d'un client à
l'autre — ce qui détruirait l'argument central.

### Qui achète quoi

| Public | Accès | Ce qu'il cherche |
|---|---|---|
| **Candidat en société de financement** | Individuel | Le mode contrainte : quelles configurations survivent à une limite de perte quotidienne. Il paie déjà 100 à 600 $ par tentative, souvent plusieurs fois |
| **Trader particulier** | Individuel | Des chiffres vérifiables, et le miroir de son propre comportement |
| **Société de financement** | Groupe | Équiper ses candidats, et savoir ce qui fait sauter les comptes |
| **Courtier** | Groupe | Offrir l'outil à ses clients — le modèle d'Autochartist, déjà prouvé |
| **École, formateur** | Groupe | Équiper une promotion, citer les statistiques dans ses supports |
| **Média, chercheur, régulateur** | Groupe gratuit | Le jeu de données ouvert, avec citation |

**Hors cible, explicitement :** la gestion d'actifs institutionnelle. Elle ne fonde pas ses
décisions sur l'analyse chartiste ; construire pour elle serait du travail perdu.

**Cadrage :** 70 à 85 % des comptes de détail perdent de l'argent sur les CFD — mention
réglementaire obligatoire des courtiers. Ce public paie peu et part vite. Il reste
indispensable : il alimente la base comportementale et la crédibilité publique. Il ne portera
pas le chiffre d'affaires seul. **Un groupe à 2 000 €/mois vaut environ 80 abonnés individuels,
avec une attrition dix fois moindre et un seul interlocuteur.**

## 5. Les modules

### Module A — Ingestion et stockage

*Pourquoi ça compte : si les données d'entrée sont fausses, tout le reste est faux.*

- Source de vérité : bougies **M1**, agrégées en H1, H4 et journalier. Aucun agrégat n'est
  jamais repris d'un fournisseur.
- Spread réel reconstruit depuis les données tick, **variable selon l'heure** : au roulement
  quotidien il est plusieurs fois supérieur à la normale. Personne ne modélise cela, et cela
  fausse tous les résultats de nuit.
- Clôture journalière figée à **17:00 America/New_York** — un fuseau, jamais un décalage fixe,
  pour que le changement d'heure soit absorbé automatiquement.
- Bougies H4 alignées sur l'ouverture de la journée : une bougie ne chevauche jamais deux
  journées.
- Gaps du dimanche soir traités : ils peuvent traverser un niveau d'invalidation.
- Valeur du pip : 0,0001, sauf paires en yen, 0,01.

### Module B — Détection et score

Chaque stratégie est un module indépendant respectant un contrat unique :

```
détecter(bougies_jusqu_à_t, paramètres)
  -> [ { sens, entrée, invalidation, objectif, horizon, score, détail_du_score } ]
```

- **Interdiction absolue d'accéder à une bougie postérieure à `t`.**
- Détection **déterministe** : pivots par ZigZag à seuil ATR, puis règles géométriques.
- **Aucun apprentissage automatique.** Non reproductible, non explicable, surapprentissage
  garanti sur des données de marché.
- Le score (§10) est stocké **avec son détail critère par critère** : sans lui, aucun rejet
  n'est explicable et aucune statistique n'est reconstructible.

### Module C — Registre prospectif public

*À la fois la preuve du produit et son principal outil d'acquisition.*

- Chaque détection est écrite dans un registre public : horodatage, paire, unité de temps,
  figure, méthode, niveaux, score détaillé, source de prix, version de stratégie, statut
  annoncée ou écartée avec son motif.
- **Arbre de Merkle par cycle horaire, chaîne des racines, ancrage chez trois tiers** (§17).
- L'issue est calculée automatiquement, sans intervention humaine.
- **Accessible gratuitement, sans compte.** C'est ce qui remplace la publicité interdite.
- Le backtest est affiché **à côté** du registre prospectif, jamais à sa place : l'écart entre
  les deux est lui-même une information de qualité.

### Module D — Base de résultats interrogeable

Filtres : paire, unité de temps, figure, méthode, tranche de score, heure, régime de marché,
période, statut annoncée ou écartée.

> Épaule-tête-épaule inversée, H4, entrée sur retour — 1 240 occurrences depuis 2015.
> Objectif atteint 46 % · invalidation 41 % · sans issue 13 %.
> **Espérance nette : +0,08 R.** Intervalle de confiance à 95 % : [+0,01 ; +0,15].
> Groupe témoin sur la même figure : −0,21 R.

### Module E — Journal de l'utilisateur

- Import d'un rapport MT4/MT5 ou d'un fichier CSV. **Aucune connexion au compte de courtage** :
  ni identifiants, ni jeton, ni lecture d'API.
- Statistiques personnelles : espérance, série de pertes maximale, résultats par paire, par
  heure, par jour.
- **L'écart comportemental**, fonction qui justifie l'abonnement :

> Vous avez pris 34 trades en range. La base donne 48 % net sur cette configuration.
> Vous êtes à 31 %. Écart principal : vous entrez en moyenne 2 bougies trop tôt.

Analyse rétrospective sur les données de l'utilisateur : aucune exposition réglementaire.

### Module F — Mode contrainte

Rejoue la base sous contrainte de perte maximale journalière et globale. Répond à la seule
question du segment principal : *« cette approche survit-elle à une limite de perte de 5 % par
jour ? »*

Une stratégie à espérance positive peut échouer dans neuf cas sur dix sous contrainte de perte
maximale. **Aucun outil existant ne le dit.**

Sortie : **probabilité de réussite de la contrainte**, jamais un rendement.

### Module G — Notifications

*Une annonce qui arrive six heures trop tard ne vaut rien. C'est un module à part entière.*

| Canal | Version |
|---|---|
| Courriel, notification navigateur | 1 |
| Telegram, webhook | 2 |

- **Latence exigée : moins de 60 secondes après la clôture de la bougie déclenchante.** Au-delà,
  l'annonce part **marquée comme retardée**, et le retard est inscrit au registre public.
- Filtres : paires, unités de temps, figures, score minimum.
- **Aucun filtre fondé sur le capital ou le profil de risque** (§22). Toute annonce est
  identique pour tous les abonnés au même filtre.

### Module H — Contenu pédagogique

Une fiche par figure : définition, construction, méthodes de trading, erreurs classiques, **et
les statistiques mesurées de cette figure, mises à jour automatiquement**. Une fiche par critère
du score. Glossaire accessible depuis n'importe quel terme de l'interface.

Ce module est aussi le moteur d'acquisition naturelle (§25).

## 6. Aucun contenu produit par un utilisateur

> **Personne n'écrit, ne saisit ni ne publie de figure, de trade ou de commentaire dans
> l'application. Tout ce qui est affiché est produit par le moteur.**

| Exclu définitivement | Pourquoi |
|---|---|
| Chat, forum, commentaires | Machine à opinions, aimant à escroqueries, modération impossible, conseil personnalisé public |
| Figures annotées ou soumises par des utilisateurs | Détruirait la reproductibilité : deux personnes ne dessinent pas la même figure |
| Signaux ou pronostics publiés par des tiers | Ferait de la plateforme un distributeur de recommandations de tiers |
| Notation ou vote sur les détections | Une opinion agrégée n'est pas une mesure |

### L'exception qui n'en est pas une : le journal personnel

| Contenu d'utilisateur | Import du journal (module E) |
|---|---|
| Publié, visible par d'autres | **Strictement privé**, visible du seul déposant |
| Influence ce que les autres voient | N'influence **aucun** chiffre public |
| Rédigé, donc opinion | Exporté d'un relevé, donc fait |

L'utilisateur ne contribue pas au produit : il confie une donnée pour obtenir **son propre
miroir**. Le principe est respecté.

### Bénéfice

Une seule source, donc une seule vérité. Aucune modération, aucune obligation d'hébergeur,
aucune exposition aux publications de tiers. Et un argument simple :

> Rien de ce que vous lisez ici n'a été écrit par quelqu'un qui avait un intérêt à ce que vous
> le lisiez.

**La communauté d'échange existe, mais à l'extérieur** : un espace Discord ou Telegram
clairement séparé du produit, modéré par un bénévole. Coût de développement nul, aucune
exposition sur la plateforme.

## 7. Écrans et parcours

| # | Écran | Accès | Contenu |
|---|---|---|---|
| 1 | **Registre en direct** | Public | Flux des détections annoncées, statut, issue. C'est la page d'accueil |
| 2 | Détail d'une détection | Public | Graphique, niveaux, méthode appliquée, score détaillé, issue |
| 3 | **Détections écartées** | Public | Le groupe témoin, motif de rejet et statistique associée |
| 4 | Fiche figure | Public | Pédagogie et statistiques à jour. **Cible du référencement naturel** |
| 5 | Preuve et intégrité | Public | Chaîne d'empreintes, ancrages, procédure de vérification, incidents |
| 6 | Explorateur de statistiques | Abonné | Base interrogeable, tous filtres, export |
| 7 | Mes alertes | Abonné | Filtres de notification |
| 8 | Mon journal | Abonné | Import et statistiques personnelles |
| 9 | **Écart comportemental** | Abonné | La comparaison journal × base |
| 10 | Mode contrainte | Abonné supérieur | Simulateur |
| 11 | Compte, abonnement, administration de groupe | Abonné | Facturation, sièges |
| 12 | Mentions légales, CGU, avertissement de risque | Public | §22 |

**Parcours d'entrée type :** un visiteur arrive par une fiche figure depuis un moteur de
recherche → il voit une statistique réelle → il ouvre le registre en direct → il constate que
les échecs sont publiés aussi → il crée un compte pour les alertes → il importe son journal →
il découvre son écart comportemental → il s'abonne.

**Tout est gratuit jusqu'à l'écart comportemental.** Le mur payant est placé là parce que c'est
la seule fonction dont la valeur est personnelle et immédiate.

**Interface, ergonomie, système visuel et périmètre du temps réel : `SPEC-DESIGN.md`.**

---
---

# PARTIE II — LA MÉTHODE

## 8. Les six principes de mesure

*Le produit **est** ses chiffres. Ces six principes ne sont pas des bonnes pratiques : ce sont
les conditions sans lesquelles le produit n'a aucune valeur.*

### 8.1 Publier avant de savoir

Une détection est écrite, horodatée et ancrée **avant** que son issue soit connue. Un backtest
se refait en une nuit ; deux ans de registre prospectif ne se fabriquent pas rétroactivement.
C'est le seul actif dont la valeur augmente mécaniquement avec le temps.

### 8.2 Conserver ce qu'on écarte

**Sans groupe témoin, on ne peut pas prouver que le filtrage sert à quelque chose.**
« Les configurations annoncées donnent +0,19 R » n'a aucun sens sans point de comparaison.
Et filtrer puis mesurer sur le résultat filtré ne mesure pas le marché : cela mesure
l'optimisme du filtre. C'est le mécanisme exact qui fabrique les faux avantages.

C'est aussi le meilleur argument commercial du produit, et il n'existe qu'à cette condition :

> Annoncées : **+0,19 R** (n = 1 840) · Écartées : **−0,21 R** (n = 14 600).
> Voilà pourquoi nous les écartons.

### 8.3 Ne jamais publier un chiffre seul

Un produit qui vend « cette figure gagne » s'effondre si l'espérance mesurée est nulle. Un
produit qui vend « cette figure fait **0,14 R de mieux** que celle-là » garde toute sa valeur
**même si les deux espérances sont négatives**.

Deux raisons, la seconde étant technique :

1. L'information relative reste actionnable pour qui tradera de toute façon.
2. **Les comparaisons sont bien plus robustes** : les biais communs aux deux termes — source de
   prix, modèle de frais, choix d'horizon — s'annulent dans une différence, alors qu'ils
   faussent entièrement une valeur absolue.

**Conséquence d'interface : tout chiffre publié est accompagné de son terme de comparaison.**

### 8.4 Mesurer en R, net de tout

Un taux de réussite de **70 % avec un objectif à 0,3 R perd de l'argent**. Un taux de **40 % à
2 R en gagne**. L'espérance nette en R est l'indicateur mis en avant partout ; le taux de
réussite est affiché en second, jamais en titre. Les trois issues — objectif, invalidation,
sans issue — sont toujours montrées ensemble : n'afficher que gagnants et perdants ment par
omission.

### 8.5 Tout doit être recalculable par un tiers

Sérialisation canonique, versions de stratégie figées, aucune constante en dur, recalcul complet
nocturne comparé aux empreintes stockées. **Un historique qui bouge silencieusement détruit
tout.** Une divergence bloque la compilation et impose une nouvelle version.

### 8.6 Se protéger de soi-même

Toute stratégie est **déclarée et publiée avant d'être observée**. Interdiction absolue de
publier le résultat d'une stratégie testée en privé puis retenue parce qu'elle donnait un bon
chiffre. C'est la protection contre le test multiple — et contre la tentation.

## 9. Catalogue et unité de mesure

### 9.1 Détecter tout, publier sous condition

**Détection : catalogue complet.** La littérature documente plus de 60 figures. Les détecter
toutes coûte peu une fois l'interface du module B en place, et la couverture est un argument
commercial réel.

**Publication : sous condition d'occurrences.** C'est là que se joue toute la crédibilité.

> Le danger n'est pas le temps de développement, c'est le **test multiple**. 60 figures × 3
> unités de temps × 3 méthodes dépassent 500 combinaisons. Au seuil habituel de 5 %, on attend
> mécaniquement **une vingtaine de résultats « significatifs » dus au seul hasard**. Un
> classement des figures établi sans correction ne classe pas des figures : il classe du bruit.

| Occurrences | Précision (IC 95 %) | Affichage |
|---|---|---|
| < 100 | pire que ± 10 points | **« Données insuffisantes — 37 occurrences, 100 nécessaires »** |
| 100 à 399 | ± 5 à 10 points | Résultat **provisoire**, intervalle affiché |
| ≥ 400 | ± 5 points | Résultat **établi** |
| ≥ 2 400 | ± 2 points | Permet d'affirmer un avantage de 2 points |

Classement des figures avec **correction de tests multiples** (Benjamini-Hochberg), jamais le
taux brut. Afficher « données insuffisantes » n'est pas une faiblesse : c'est la fonctionnalité
que personne n'offre, et la preuve visible que les autres chiffres sont sérieux.

### 9.2 Gagner en puissance : plus de paires, jamais moins d'exigence

Passer de 7 paires majeures à environ **28 paires** — mineures et croisées — multiplie les
occurrences par 4, **sans une ligne de code supplémentaire** : même moteur, même source, même
format. C'est la seule extension autorisée quand une figure reste sous le seuil.

### 9.3 L'unité mesurée est **figure × méthode**

| Méthode, exemple de l'épaule-tête-épaule | Entrée |
|---|---|
| A | Cassure de l'encolure |
| B | Retour sur l'encolure après cassure |
| C | Cassure confirmée par la clôture suivante |
| D | Cassure avec sortie partielle à 1 R et suivi du reste |

Ces méthodes donnent des résultats différents ; les confondre invalide tout. La méthode D montre
que **les modes de sortie sont des méthodes à part entière**, mesurées séparément.

> **Règle d'architecture : la méthode affichée à l'utilisateur — « voici comment se trade ce
> type de figure » — et la règle qui décide gagnant ou perdant sont le même objet en base.**

Une définition, deux usages : pédagogie et mesure. Sans cette unité, le contenu explique une
chose et les statistiques en mesurent une autre — c'est le défaut de tout le contenu
pédagogique existant et de tous les backtests publiés.

Cela produit aussi la sortie la plus vendable : *« sur l'épaule-tête-épaule, l'entrée sur retour
a une espérance nette supérieure à l'entrée sur cassure »* — question débattue depuis trente
ans, jamais chiffrée sur données prospectives.

## 10. Détection, annonce, conservation : trois choses distinctes

*Point le plus important du document. S'y tromper vide le produit de sa valeur.*

| Étape | Périmètre |
|---|---|
| **Détection** | **Toutes** les figures, même celles ne remplissant aucun critère |
| **Conservation** | **Toutes**, définitivement, avec leur score et le détail de leur évaluation |
| **Annonce** | **Uniquement** celles franchissant les filtres durs et le seuil de score |
| Statistiques mises en avant | Celles des configurations **annoncées** |
| Statistiques de contrôle | Celles des configurations **écartées**, publiées à part |

**Rien n'est jamais supprimé.** Ce qui est écarté est marqué comme écarté, avec son motif.
Une erreur se corrige par une **détection d'annulation ajoutée à la suite**, jamais par une
suppression : le registre est un livre comptable, pas un document révisable.

### Ce que voit l'utilisateur

Il reçoit **uniquement les configurations annoncées**. Mais il peut ouvrir une configuration
écartée et lire le motif :

> Épaule-tête-épaule détectée — **non annoncée**. Score 4/13.
> Manquant : tendance journalière opposée (−2), objectif à 2,3 ATR jugé irréaliste (−2),
> aucune zone de support à proximité.
> *Sur les 3 210 configurations écartées pour tendance opposée, l'espérance nette est de −0,26 R.*

Fonction pédagogique unique sur le marché, et démonstration permanente que le filtrage a une
valeur mesurée.

## 11. Le score de confluence

### 11.1 Pourquoi un score, et non une liste de conditions

Exiger que **tous** les critères soient remplis ne produit presque aucune configuration : onze
critères remplis chacun 70 % du temps donnent 0,70¹¹ ≈ **2 % de survie**. Sur dix ans et sept
paires, une poignée d'annonces par an — trop peu pour trader, trop peu pour prouver.

**Structure retenue : trois filtres durs, puis un seuil de score.**

| Filtres durs — rejet automatique |
|---|
| Configuration à contre-tendance journalière |
| Annonce économique à fort impact dans l'horizon du trade |
| Objectif irréaliste : `\|objectif − entrée\| > 1,5 × ATR × √horizon` |

Puis **score ≥ 70 % du maximum atteignable** pour l'annonce — seuil initial, **recalibré sur les
données une fois 400 occurrences accumulées**, jamais fixé définitivement à l'avance. Le seuil
est versionné : le modifier crée une nouvelle version de stratégie, et l'historique reste intact.

### 11.2 Les critères

| # | Critère | Points | Calcul |
|---|---|---|---|
| 1 | **Tendance supérieure alignée** | +2 D1 · +1 H4 · **opposée → filtre dur** | Pente EMA200 rapportée à l'ATR, plus structure de sommets et creux |
| 2 | **Zone support/résistance** | +2 | À moins de 0,25 ATR d'un niveau touché au moins 3 fois |
| 3 | **Niveau rond** | +1 | Prix en 00 ou 50. Effet documenté : les ordres stop s'y concentrent (Osler, 2003) |
| 4 | **Niveaux de référence** | +1 | Plus haut ou bas de la veille ou de la semaine, ouverture du jour |
| 5 | **Divergence de momentum** | +1 | RSI divergent au sommet ou creux de la figure |
| 6 | **Objectif atteignable** | +1 · **filtre dur si irréaliste** | `D = \|objectif − entrée\| / (ATR × √horizon)` ; `D ≤ 0,75` → +1 |
| 7 | **Séance** | +1 chevauchement Londres–New York · **−1** séance asiatique ou heure de roulement | Heure locale des places, changement d'heure pris en compte |
| 8 | **Calendrier économique** | filtre dur | Annonce à fort impact dans l'horizon |
| 9 | **Extension du mouvement** | **−1** | Prix à plus de 2 ATR de l'EMA20 : mouvement déjà mûr |
| 10 | **Qualité géométrique** | 0 à +2 | Symétrie, durée, nombre de touches, propreté des bornes |
| 11 | **Régime de marché** | +1 si cohérent | Continuation en tendance, retournement en range |

L'espérance nette est publiée **par tranche de score** :

> Score 0-3 : −0,21 R · Score 4-6 : −0,04 R · Score 7+ : **+0,19 R** (n = 1 840)

**Si le score ne sépare pas les résultats, on le publie aussi.** C'est une information de
premier ordre : elle dirait que la confluence est une croyance confortable sans effet mesurable.

### 11.3 Redondance : une famille d'information, un seul représentant

*C'est le point où un score mal conçu compte plusieurs fois la même information et fabrique une
fausse certitude.*

| Constat vérifiable | Conséquence |
|---|---|
| **La bande centrale de Bollinger *est* la moyenne mobile 20** | Les compter tous deux, c'est compter deux fois la même chose |
| **MACD = moyenne exponentielle 12 − moyenne exponentielle 26** | Autre lecture du croisement de moyennes mobiles |
| RSI et MACD mesurent tous deux le momentum | Deux votes fortement corrélés |
| Largeur des bandes de Bollinger et ATR | Deux mesures de la même volatilité |

| Famille | Représentant | Rôle |
|---|---|---|
| **Structure de prix** | Sommets, creux, cassures, bornes | **Autorité maximale** |
| **Tendance supérieure** | Pente EMA200 et structure journalière | Fort |
| **Localisation** | Support/résistance, niveaux ronds, références | Fort |
| **Momentum** | **RSI seul.** MACD écarté | Faible |
| **Volatilité** | **ATR seul.** Bollinger écarté | **Jamais directionnel** — faisabilité et dimensionnement |
| **Volume, VWAP** | **Écartés** | Aucun |

**Volume et VWAP sont écartés.** Il n'existe pas de volume réel sur le change au comptant,
marché de gré à gré. Ce qu'affichent les plateformes est un **volume de ticks**, propre à chaque
courtier : l'utiliser rendrait les résultats non reproductibles par un tiers, ce qui contredit
frontalement le principe fondateur du produit.

### 11.4 Hiérarchie en cas de désaccord réel

> **Structure de prix → Tendance de l'unité supérieure → Zones → Momentum → Volatilité**

**Un indicateur ne prime jamais sur la structure.** Les indicateurs sont dérivés du prix ; le
prix n'est pas dérivé des indicateurs. Un RSI en surachat contre une structure haussière intacte
retire des points — il ne renverse rien.

### 11.5 On enregistre les contradictions, on ne les arbitre pas

**Interdit : écrire une règle faite à la main pour trancher une contradiction.** C'est ainsi
qu'on injecte une opinion invérifiable au cœur du système.

Les éléments contradictoires s'annulent naturellement dans le score : la configuration tombe bas
et n'est pas annoncée, sans règle spéciale. La contradiction est **étiquetée** comme un état
nommé et conservée. Au bout de 400 occurrences, **les données tranchent**.

### 11.6 Asymétrie : une contradiction retire plus qu'une confirmation n'ajoute

Une figure haussière contient **déjà** l'information « haussier ». Un indicateur qui confirme
répète ce que la figure dit ; un élément qui contredit apporte une information **absente** de la
figure — c'est là qu'est la surprise, donc la valeur.

Contradictions : **−2 ou filtre dur**. Confirmations : +1 à +2. Un score symétrique
surévaluerait les configurations les plus évidentes, donc les plus déjà intégrées dans le prix.

### 11.7 Neutraliser les critères contenus dans la définition d'une figure

| Figure | Critère satisfait d'office | Problème |
|---|---|---|
| Drapeau, fanion | « Aligné avec la tendance » | La figure n'existe que dans une tendance : +2 gratuits |
| Double creux, ETE inversée | « Sur un support » | Le creux **est** le support |
| Cassure de range | « Niveau de référence » | La borne **est** le niveau |

**Sans correction, les figures de continuation obtiendraient mécaniquement de meilleurs scores
que les figures de retournement, pour une raison purement comptable.** Le classement des
figures — sortie principale du produit — serait faux.

**Règle : chaque figure déclare les critères que sa construction satisfait d'office ; ils sont
neutralisés, et le score s'exprime en pourcentage du maximum atteignable par cette figure**,
jamais en points bruts, afin que deux figures restent comparables.

### 11.8 Admission d'un indicateur

**Aucun indicateur n'entre dans le score sans que sa contribution marginale ait été mesurée** sur
un échantillon réservé. S'il n'améliore pas la séparation d'espérance entre tranches de score, il
est retiré.

Les pondérations initiales sont fixées à la main et transparentes. Elles ne seront recalibrées
**qu'une seule fois**, par une méthode documentée, sur échantillon réservé, puis figées dans une
nouvelle version. Un score recalibré en continu sur ses propres résultats est surajusté :
excellent en historique, sans valeur en réel.

## 12. Ratio, risque, dimensionnement

| Contexte | Ratio minimum | Risque par trade |
|---|---|---|
| Score de confluence **élevé** | **1,5 R** | 1 % |
| Score **normal** | **2 R** | 1 % |
| **Mode contrainte** | selon score | **0,5 %** |
| Variante affichable, avec sa perte simulée | — | 2 % |

| Ratio | Taux de réussite requis pour l'équilibre |
|---|---|
| 1,5 R | **40,0 %** |
| 2 R | **33,3 %** |
| 3 R | 25,0 % |

**Effet mécanique à assumer :** exiger 2 R fait baisser le taux de réussite affiché, car beaucoup
de figures n'ont pas 2 R d'espace avant l'obstacle structurel suivant. Le filtre de ratio est
lui-même un choix de stratégie, avec un coût mesurable — l'application le mesure, elle ne le
suppose pas.

### 12.1 Pourquoi 2 % de risque n'est pas la règle par défaut

*Calcul, pas opinion.* À 40 % de réussite, la plus longue série de pertes attendue sur 200
trades est d'environ **10 pertes consécutives**. Résultat normal, pas accident.

| Risque par trade | Perte après 10 pertes consécutives |
|---|---|
| 2 % | **− 18,3 %** |
| 1 % | − 9,6 % |
| 0,5 % | − 4,9 % |

Les sociétés de financement imposent typiquement 10 % de perte maximale totale et 5 % par jour.
**À 2 %, le compte saute avant la fin d'une série normale.** À 1 %, il la frôle.

### 12.2 Limite juridique sur le dimensionnement

| Autorisé | Interdit |
|---|---|
| « Cette configuration se traite habituellement avec un risque de 1 % du capital » | « Vous avez 5 000 € : risquez 50 €, soit 0,11 lot » |
| Calculatrice exécutée **dans le navigateur**, valeur jamais transmise ni stockée | Capital enregistré dans le compte |
| Statistiques identiques pour tous | Configurations filtrées ou classées selon le capital |

> **Ligne rouge : dès que le capital de l'utilisateur influence *ce qui lui est montré*,
> l'application devient une activité réglementée.**

## 13. Règles de mesure du résultat

| Élément | Règle |
|---|---|
| Entrée | Au prix défini par la méthode déclarée. Jamais un prix intra-bougie arbitraire |
| Invalidation | Niveau structurel de la figure |
| **Objectif — double mesure** | **(a)** projection de la figure **et (b)** objectif fixe à 1,5 R et 2 R, calculés et publiés séparément |
| Horizon | 20 bougies par défaut. Ni objectif ni invalidation atteints → **sans issue**, comptabilisé à part |
| Départage | **Résolution en données M1.** Si les deux sont touchés dans la même bougie M1 : **compté comme invalidation**, toujours |
| Frais déduits | Spread horaire réel **+ glissement sur invalidation + portage** |
| Indicateur principal | **Espérance en R, nette** |

La règle conservatrice sur les bougies ambiguës est non négociable : choisir l'inverse, ou tirer
au sort, gonflerait les taux de réussite d'une manière invérifiable. C'est le mécanisme qui rend
flatteurs la quasi-totalité des backtests amateurs. **La fréquence de ce cas est enregistrée et
publiée** : c'est la mesure de l'incertitude résiduelle du système.

**Le portage est l'oubli le plus fréquent.** Sur une figure journalière tenue 20 jours, il peut
dépasser plusieurs fois le coût du spread. Tout résultat qui l'ignore est faux sur les unités de
temps longues.

### Trois protections à afficher, que les autres outils omettent

1. **Série de pertes maximale attendue.** À 40 % de réussite, environ 10 pertes consécutives sur
   200 trades sont normales. Les utilisateurs abandonnent pendant ces séries en croyant la
   méthode cassée. L'afficher **avant** est la fonction de rétention la plus efficace du produit.
2. **Corrélation entre paires.** EUR/USD et GBP/USD évoluent ensemble à environ 0,85. Deux
   positions de 2 % dans le même sens ne font pas 4 % de risque mais **environ 3,8 % concentrés
   sur un seul pari**. Les détections corrélées simultanées sont signalées.
3. **Écart brut / net**, toujours côte à côte : c'est ce qui montre à l'utilisateur ce que les
   frais lui coûtent réellement.

## 14. Coût de friction et unités de temps

*Section décisive : elle détermine ce qu'on annonce.*

Un coût en pips ne dit rien. Rapporté à la distance d'invalidation, il donne **le seuil que
l'avantage brut doit franchir pour rapporter quoi que ce soit**.

Ordres de grandeur EUR/USD, à confirmer sur données réelles : spread aller-retour et glissement
≈ 1,4 pip, distance d'invalidation ≈ 1 ATR, horizon 20 bougies.

| Unité | ATR typique | Coût de spread | Portage sur l'horizon | **Coût total** |
|---|---|---|---|---|
| **H1** | ~12 pips | 0,117 R | ~20 h, négligeable | **~0,12 R** |
| **H4** | ~35 pips | 0,040 R | ~3,3 jours | **0,07 à 0,13 R** |
| **D1** | ~75 pips | 0,019 R | **~28 jours, 6 à 20 pips** | **0,10 à 0,29 R** |

### Le résultat contre-intuitif

Le raisonnement habituel — « plus l'unité est longue, moins les frais pèsent » — est **faux dès
qu'on intègre le portage**. Le spread se dilue quand l'amplitude augmente, mais le portage
s'accumule avec la durée : les deux effets vont en sens inverse.

> **Le H4 est très probablement le meilleur compromis.** Le journalier n'est préférable que sur
> les paires dont le portage est favorable ou neutre — ce qui dépend du sens de la position et
> change avec les taux directeurs.

C'est **une hypothèse à mesurer**, et elle constitue à elle seule un résultat publiable que
personne n'a chiffré.

### Politique du H1

| Usage | Décision |
|---|---|
| **Détection et mesure** | **Conservé.** Le H1 fournit 4 fois plus d'occurrences que le H4 et 24 fois plus que le journalier : c'est là qu'est la puissance statistique |
| **Annonce** | **Désactivée par défaut**, activable avec l'avertissement de coût affiché |
| Affichage | Coût de friction indiqué en R sur chaque statistique H1 |

> **On apprend en H1, on annonce en H4.**

### Où chercher l'avantage — cinq leviers, par ordre de fiabilité

**1. Réduire le coût — seul avantage certain.** Ce n'est pas un pari, c'est de l'arithmétique.
Passer du H1 au H4 économise ~0,08 R par trade, de façon acquise. Éviter la fenêtre de
roulement, les annonces macro, les portages défavorables : tout cela est gagné d'avance.

> **Le gain le plus important accessible n'est pas de trouver une meilleure figure, c'est de
> cesser de payer pour une moins bonne.** Et c'est ce que le produit mesure sans effort.

**2. Chercher l'avantage dans les critères, pas dans les figures.** La littérature ne documente
aucun avantage persistant pour les figures chartistes sur les majeures. Elle documente en
revanche des effets de microstructure réels, parce qu'ils proviennent de flux véritables et non
d'une erreur de prix arbitrable : concentration des ordres stop sur les niveaux ronds (critère 3),
saisonnalité intrajournalière et flux de fixing (critère 7), persistance de tendance (critère 1).

**Hypothèse de travail, publiée comme telle : si un avantage apparaît, il viendra du contexte,
pas de la forme des figures.** Prédiction testable, et le produit est l'instrument qui permet de
la trancher. Si elle se vérifie, elle renverse la hiérarchie habituelle de l'analyse technique.

**3. Étendre la mesure au crypto une fois le moteur éprouvé.** Marché nettement moins arbitré,
plus retail, ouvert en continu, données gratuites, **et le même code sans une ligne à écrire**.
Couverture la moins chère contre l'hypothèse « aucun avantage nulle part sur le change ». Le
forex reste le produit ; le crypto est une extension de mesure.

**4. L'avantage comportemental, qui n'exige aucune inefficience de marché.** Faire passer un
trader de −0,30 R à −0,05 R en corrigeant son dimensionnement et ses sorties prématurées est une
amélioration considérable et vérifiable, obtenue sans que le marché ait à coopérer. C'est le
seul avantage que le produit peut garantir.

**5. Les quatre impasses, interdites.**

| Tentation | Pourquoi c'est une impasse |
|---|---|
| Apprentissage automatique | Surapprentissage garanti, résultats non reproductibles |
| Empiler des indicateurs | Redondance : la même information comptée plusieurs fois |
| Abaisser les seuils d'occurrences | Fabrique des avantages qui n'existent pas |
| Étendre le catalogue en espérant qu'une figure marche | C'est la définition du test multiple |

Ces quatre chemins produisent le même résultat : un système magnifique en historique, sans
valeur en réel. **L'interdiction est le produit.**

---
---

# PARTIE III — LA TECHNIQUE

## 15. Données

| Besoin | Source | Coût |
|---|---|---|
| Historique M1 et tick | Dukascopy ou HistData | 0 € |
| Flux courant | API forex (Polygon, TraderMade, OANDA) | ~30-50 $/mois |
| Calendrier économique | API dédiée | 0-30 $/mois |

**Piège majeur : il n'existe pas de prix consolidé sur le change.** Le marché est de gré à gré,
chaque courtier a son flux. Les chandeliers de l'utilisateur ne seront jamais strictement
identiques aux nôtres.

→ **Obligation : publier la source de prix retenue, et n'en jamais changer sans l'annoncer et
sans reconstruire l'historique sous une nouvelle version.**

**Révisions.** Les fournisseurs corrigent parfois des données passées. Une bougie ayant servi à
une détection publiée **n'est jamais modifiée** : la correction est enregistrée à part et
signalée, jamais appliquée rétroactivement.

**Complétude.** Toute bougie manquante est détectée et journalisée. Une détection calculée sur
une période incomplète est marquée et **exclue des statistiques**, mais conservée.

## 16. Architecture

Pile choisie pour un développeur seul assisté par IA : peu de pièces, un seul langage, tout
reproductible.

| Couche | Choix | Motif |
|---|---|---|
| Traitement et API | Python (Polars, FastAPI) | Un seul langage, une seule surface de débogage |
| Base, lots 1-2 | **SQLite** | Aucune installation. 1,1 million de bougies, c'est peu |
| Base, à partir du lot 3 | PostgreSQL + TimescaleDB | Service public et multi-utilisateur. SQL standard, migration mécanique |
| Graphiques | TradingView Lightweight Charts | Gratuit, libre, conçu pour cet usage. **Ne jamais coder son propre moteur graphique** |
| Interface | SvelteKit ou Next.js | Indifférent. Ne pas y passer de temps en v1 |
| Hébergement | Un VPS, 15-40 €/mois, Docker Compose, Caddy | Kubernetes serait une erreur à ce stade |
| Paiement | Stripe + Stripe Tax | Voir §23 et §28, lot 0 |
| Courriel | Service tiers (Postmark, Resend) | La délivrabilité des alertes est critique |

### Tables principales

| Table | Rôle |
|---|---|
| `instrument` | Paires, valeur du pip, horaires de séance |
| `bougie` | M1 et agrégats, spread estimé, indicateur de complétude |
| `version_strategie` | Version figée d'une figure × méthode : code, empreinte, paramètres, seuils, dates |
| `detection` | Horodatage, niveaux, score et **détail critère par critère**, statut et motif, version, empreintes |
| `issue` | Atteint / invalidé / sans issue, excursions extrêmes, résultat brut et net, détail des frais |
| `ancrage` | Racine de Merkle et tête de chaîne, avec les trois preuves externes |
| `organisation`, `siege` | Comptes de groupe et administration déléguée |
| `trade_utilisateur` | Journal importé, éventuellement rapproché d'une détection |
| `notification` | Envois, canal, horodatage, latence mesurée |

Schéma au niveau colonne : `SPEC-LOT2.md` §7.

## 17. Intégrité et preuve

### 17.1 Le chaînage seul ne prouve rien

Une chaîne d'empreintes détenue par celui qui la produit peut être entièrement recalculée après
coup. **Ce qui vaut preuve, c'est l'ancrage chez un tiers.** D'où la question qui décide de tout :

> **Combien de temps une détection existe-t-elle sans être ancrée ?**
> Pendant cette fenêtre, elle peut disparaître sans laisser de trace.

**Règle de dimensionnement : la fenêtre d'ancrage doit être strictement inférieure au délai
minimal de résolution d'une détection.** Si aucune détection ne peut se résoudre avant d'avoir
été ancrée, la suppression opportuniste devient impossible.

**Décision : ancrage à chaque cycle de traitement, soit toutes les heures.**

### 17.2 Structure et supports

Arbre de Merkle par cycle, chaîne des racines. Un arbre permet de prouver l'inclusion d'**une
seule** détection avec une poignée d'empreintes, au lieu d'exiger toute la base.

| Support | Ce qu'il apporte | Coût |
|---|---|---|
| Dépôt public versionné, commit signé | Lisible par tous, historique hébergé par un tiers | 0 € |
| Horodatage RFC 3161 | Jeton signé par une autorité indépendante, opposable | ~0 € |
| OpenTimestamps | Preuve d'antériorité ne dépendant d'aucune organisation | ≈ 0 € |

**Les cycles vides sont ancrés comme les autres** : un cycle manquant serait indistinguable d'un
cycle supprimé. **Un cycle non ancré laisse un trou visible définitivement**, jamais comblé
rétroactivement — un ancrage produit après coup prouverait le contraire de ce qu'il prétend.

### 17.3 Le vérificateur public

Un programme autonome, publié et documenté, qui ne dépend d'aucun service de l'éditeur autre que
le jeu de données public. Il recalcule les empreintes, les racines, la continuité de la chaîne,
l'antériorité des ancrages — **et les issues elles-mêmes depuis les données de marché**. Il
vérifie donc le contenu, pas seulement l'intégrité.

Une page publique invite explicitement à contester, avec engagement écrit de publier toute
divergence confirmée. Sur un marché saturé de résultats fabriqués, c'est l'argument le plus
difficile à ignorer, et il coûte une page de documentation.

Détail complet : `SPEC-LOT3.md`.

## 18. Sécurité, sauvegarde, supervision

*Le registre prospectif est l'unique actif de l'entreprise. Le perdre, ou le laisser se trouer
sans s'en apercevoir, détruit une valeur non reconstituable.*

**Sauvegarde** — quotidienne, chiffrée, hors du serveur de production, chez un autre
fournisseur. **Test de restauration mensuel effectif** : une sauvegarde jamais restaurée n'est
pas une sauvegarde. Conservation : 30 jours, 12 mois, puis annuelle sans limite.

**Alertes immédiates** — flux interrompu ou bougie manquante · traitement échoué ou en retard ·
latence de notification supérieure à 60 s · ancrage non publié · échec du test de déterminisme.

**Page publique d'intégrité** — complétude des données, ancrages publiés, incidents passés.
Publier ses propres pannes est cohérent avec le positionnement, et personne ne le fait.

**Sécurité** — authentification déléguée, second facteur proposé, secrets hors du dépôt,
dépendances analysées, accès administrateur nominatif et journalisé, journal utilisateur chiffré
au repos.

## 19. Tests et qualité

| Test | Contenu |
|---|---|
| **Point-in-time** | Injection de données futures, y compris aberrantes : le résultat doit être identique. **Test le plus important du projet** |
| **Contre-épreuve** | Un calcul volontairement fautif doit faire échouer le harnais. Un test qui ne peut pas échouer ne prouve rien |
| **Déterminisme** | Recalcul complet nocturne, comparaison des empreintes. Divergence → compilation en échec |
| **Jeu de référence annoté** | 60 fenêtres étiquetées à la main : le détecteur doit retrouver les valides et n'en inventer aucune |
| **Résolution** | Cas construits où objectif et invalidation tombent dans la même bougie |
| **Frais** | Un trade calculé à la main. Écart toléré : zéro |
| **Changement d'heure** | Les critères de séance restent corrects de part et d'autre des quatre bascules annuelles |
| **Complétude** | Une période trouée produit des détections marquées et exclues |
| **Non-régression** | Toute correction ajoute le cas qui l'a révélée |

Environnements séparés, migrations versionnées, déploiement automatisé et réversible.

## 20. Performance et coûts

- Volume : 7 paires × 3 unités × 20 ans ≈ **1,1 million de bougies**. Cela tient en mémoire vive ;
  une passe complète se compte en secondes.
- **Le calcul est identique pour tous les utilisateurs** : précalcul à chaque clôture, service
  depuis le cache. **Coût marginal par abonné proche de zéro.**
- **Traitement par lots. Jamais de flux tick en temps réel** pour la mesure.

**Coût d'infrastructure avant le premier client : moins de 150 €/mois.** Ce n'est pas là qu'est
le risque.

## 21. Interface et temps réel

Système visuel, ergonomie, langage et accessibilité : **`SPEC-DESIGN.md`**, dont ces trois règles
structurantes :

- **Le luxe ici, c'est la retenue.** L'esthétique « terminal de trading néon » est celle des
  vendeurs de signaux : l'adopter reviendrait à se déguiser en ce qu'on dénonce.
- **Un seul chiffre par écran**, en grand, toujours accompagné de son terme de comparaison et de
  sa taille d'échantillon.
- **Encodage bleu / orange**, jamais rouge / vert : environ 8 % des hommes ont une déficience de
  perception du rouge et du vert, ce qui serait un défaut fonctionnel dans un produit dont toute
  la valeur tient à la lecture de résultats.

### Périmètre du temps réel

| En direct | Par lots, à la clôture |
|---|---|
| Prix affichés sur les graphiques | **Détection** |
| Distance du prix aux niveaux d'une détection ouverte | **Score** |
| Compte à rebours avant clôture | **Résolution** |
| Aperçu provisoire, **affiché en gris, non enregistré** | |
| Envoi de l'annonce : **moins de 60 s** | |

> **Les prix sont en direct, la mesure ne l'est pas. C'est ce qui rend la mesure vérifiable.**

Une détection recalculée à chaque tick donnerait un résultat différent à chaque tick : elle
serait non reproductible, ce qui détruirait le déterminisme, donc la chaîne d'empreintes, donc
la preuve. Le flux de prix ne touche **jamais** la base de détections : deux systèmes séparés,
et cette séparation est une exigence d'architecture.

---
---

# PARTIE IV — L'EXPLOITATION

## 22. Cadre juridique

*Une seule de ces lignes franchie transforme un logiciel en activité réglementée.*

| Sujet | Position |
|---|---|
| **Agrément de conseiller en investissement financier** | **Non requis**, à une condition stricte : aucune personnalisation. L'application ne connaît jamais le capital, le portefeuille ni le profil de risque de l'utilisateur pour produire une analyse (MiFID II, règl. délégué UE 2017/565, art. 9) |
| **Formulation** | Toujours « voici comment ce type de figure se trade habituellement », jamais « prenez ce trade ». Réserve honnête : c'est une précaution **supplémentaire**, pas le rempart principal. Le rempart est l'absence de personnalisation |
| **Règlement MAR** (UE 596/2014, art. 20) | Champ incertain sur le change de détail : le change au comptant n'est pas un instrument financier au sens de MiFID II annexe I section C. **La discipline s'applique quand même** : auteur identifié, date, méthodologie publiée, historique accessible, avertissement |
| **Loi Sapin 2** — art. L.222-16-1 code de la consommation | **Interdit la publicité électronique** pour les contrats financiers hautement spéculatifs auprès du public en France. Loi influenceurs (n° 2023-451) : même interdiction. Google et Meta : restreint ou interdit |
| **RGPD** | Le journal utilisateur contient des données financières personnelles : hébergement UE, registre des traitements, contrats de sous-traitance, export et suppression sur demande |

### Les cinq interdits absolus

1. Ne jamais demander le capital ou le profil de risque pour produire une analyse.
2. Ne jamais écrire « achetez », « vendez », « prenez ce trade », « recommandé pour vous ».
3. Ne jamais afficher une taille de position adaptée à l'utilisateur.
4. Ne jamais promettre un rendement, ni afficher un gain en euros.
5. Ne jamais supprimer ou corriger une détection publiée.

**Documents obligatoires avant mise en ligne :** mentions légales, CGU, CGV, politique de
confidentialité et de cookies, **avertissement de risque visible sur chaque page affichant une
statistique**. Le tout validé par un avocat spécialisé.

**Conséquence opérationnelle majeure : l'acquisition payante est fermée.** Le canal est
organique (§25), et la page publique du registre en est l'outil principal — pas une
fonctionnalité annexe.

## 23. Juridictions, structure, fiscalité

| Zone | Position de départ |
|---|---|
| France et UE | Marché principal |
| **États-Unis** | **Exclus au lancement.** L'encadrement du conseil sur le change y est strict (CFTC, NFA) et les exemptions applicables demandent un avis juridique |
| Autres | Ouverts, sauf pays sous sanctions |

Blocage par les CGU et déclaration de résidence à l'inscription.

**Structure :** micro-entreprise au démarrage, passage en société à examiner selon le chiffre
d'affaires et la responsabilité.

**TVA — point technique à ne pas rater.** La vente d'un service numérique à un particulier de
l'UE est taxée **au taux du pays du client**. Au-delà de 10 000 € de ventes transfrontalières
annuelles, déclaration via le **guichet unique (OSS)**. **Solution retenue : Stripe Tax dès le
premier abonnement**, ~0,5 % du volume — sans commune mesure avec le coût d'une régularisation.

## 24. Modèle économique

### Accès individuel

| Niveau | Contenu |
|---|---|
| **Public, sans compte** | Registre en direct, groupe témoin, fiches figures, statistiques agrégées — **outil d'acquisition, pas version bridée** |
| **Analyse** | Base interrogeable, tous filtres, alertes, journal personnel, écart comportemental |
| **Contrainte** | Mode contrainte, export, API |

### Accès groupe

Par siège, dégressif, minimum 10 sièges. Options : rapport mensuel d'intelligence du risque,
accès API. Médias, chercheurs et régulateurs : **gratuit, avec citation**.

Le siège de groupe est moins cher que l'abonnement individuel, et c'est voulu : le client
apporte le volume, gère son administration, ne génère aucun support.

**Niveaux de prix : §31, point 4.**

### Contrainte de marché à connaître

**La détection de figures a un prix de marché proche de zéro** : Autochartist est distribué
gratuitement par de nombreux courtiers. Ce qui se vend, c'est l'analyse comportementale et le
mode contrainte, pas la détection.

### Pare-feu contractuel — clause non négociable

*Vendre à un courtier crée un conflit d'intérêts évident : celui qui facture les coûts de
transaction paierait celui qui les mesure.*

1. **Aucune rémunération liée au volume négocié, aucun apport d'affaires rémunéré.**
2. **Aucun client ne peut faire modifier, retirer ou adoucir un chiffre publié.**
3. **La liste des clients professionnels est publique.**

Un client qui refuse ces clauses est un client qu'on refuse. **Le premier contrat signé au prix
de la crédibilité coûterait plus qu'il ne rapporte** : l'indépendance est l'actif.

### Projection, hypothèses pessimistes

> **Abonnés à l'équilibre = nouveaux abonnés par mois ÷ attrition mensuelle.**
> À 12 % d'attrition, 10 nouveaux par mois plafonnent à 83 abonnés, définitivement.

| | Mois 12 | Mois 24 | Mois 36 |
|---|---|---|---|
| Visiteurs par mois, organique seul | 800 | 2 500 | 6 000 |
| Conversion visiteur → payant | 0,10 % | 0,10 % | 0,12 % |
| Attrition mensuelle | 13 % | 12 % | 11 % |
| **Abonnés à l'équilibre** | ~8 | ~21 | ~65 |
| Revenu individuel, net | ~230 € | ~600 € | ~1 700 € |
| Un accès groupe | — | +1 000 € | +2 000 € |
| **Total** | ~230 € | **~1 600 €** | **~3 700 €** |

**Conclusion : la voie individuelle seule n'atteint pas 2 500 €/mois avant le mois 26 à 30, et
jamais en scénario pessimiste. Le premier accès groupe change cela à lui seul.** D'où sa
position au lot 13, dès que le registre totalise six mois.

## 25. Acquisition

*La publicité payante étant interdite, l'acquisition est une contrainte de conception, pas une
activité qui viendra après.*

### Moteur principal : le référencement programmatique

La base **génère elle-même** des milliers de pages de contenu unique, chiffré, constamment mis à
jour :

> *Double creux EUR/USD en H4 : 1 240 cas mesurés, 46 % d'objectifs atteints, espérance nette
> +0,08 R — contre −0,21 R pour le groupe témoin.*

60 figures × 28 paires × 3 unités de temps = **plus de 5 000 pages**, chacune répondant à une
requête réellement tapée, impossibles à copier puisqu'elles proviennent de la base. Coût marginal
nul, qualité croissante avec les occurrences. **C'est le meilleur atout de croissance du produit,
et il découle directement de son architecture.**

### Canaux complémentaires

| Canal | Rôle |
|---|---|
| Registre public | Preuve permanente, motif de retour régulier |
| **Ouverture des données de plus de 90 jours** | Devenir la source que les autres citent. Chaque citation est un lien et une preuve qu'il n'y a rien à cacher |
| **Vérificateur publié, invitation à contester** | L'argument le plus difficile à ignorer sur un marché saturé de résultats fabriqués |
| **Outils gratuits** : calculatrice de position, valeur du pip, horloge des séances, matrice de corrélation | Aucun avantage de marché nécessaire, fort volume de recherche |
| Rapport public mensuel, **date et format fixes, publié même quand les chiffres sont mauvais** | Le rituel qui construit la réputation |
| Vidéo, communautés | Contribution par les chiffres, jamais par la promotion |
| Espace communautaire hébergé **hors du produit** | Satisfait le besoin d'échange sans exposer la plateforme |

### Revenus interdits

**Aucune rémunération d'apport d'affaires versée par un courtier, jamais.** C'est le revenu le
plus facile de ce marché, et le seul qui détruirait instantanément le positionnement.

## 26. Métriques

| Métrique | Cible |
|---|---|
| Taux de création de compte | > 3 % des visiteurs |
| **Taux d'import du journal** (activation) | **> 40 % des comptes** — meilleur prédicteur d'abonnement |
| Conversion essai → abonnement | > 25 % |
| **Rétention à 3 mois** | **> 60 %** — la métrique qui décide de la viabilité |
| Attrition mensuelle | < 8 % |
| Latence médiane des notifications | < 60 s |
| Complétude des données | > 99,9 % |

**Métrique de vérité produit, publiée :** espérance nette des configurations annoncées, comparée
au groupe témoin. Si l'écart disparaît, le produit change de discours (§30).

## 27. Support

Asynchrone, par écrit, français et anglais, 48 h ouvrées. Base de connaissances alimentée par
les questions reçues. Les groupes s'administrent seuls : aucun support de premier niveau sur les
sièges.

**Aucune réponse individuelle ne doit jamais contenir de conseil personnalisé.** C'est le canal
par lequel l'interdit du §22 est le plus facile à franchir par inadvertance : réponses types
préparées pour les questions du type « dois-je prendre ce trade ? ».

---
---

# PARTIE V — L'EXÉCUTION

## 28. Ordre de construction

*L'ordre compte plus que le contenu : chaque lot doit produire quelque chose de vérifiable.*

| Lot | Contenu | Critère d'acceptation |
|---|---|---|
| **0** | Compte Stripe validé, activité décrite comme **logiciel d'analyse statistique**. Consultation juridique de cadrage | **Avant d'écrire du code.** Un refus bloquerait toute monétisation après des mois de travail |
| **1** | Ingestion, stockage, agrégation, indicateurs, pivots, **harnais de déterminisme et test point-in-time** | Le test d'injection de données futures échoue si on triche. Recalcul reproductible à l'identique. **✅ livré** |
| **2** | **Une stratégie : le range**, de bout en bout, résolution M1 et frais complets. **Backtest walk-forward avec correction de tests multiples** | 500 détections résolues, reproductibles deux fois à l'identique. **Point de décision, §28.1** |
| **3** | Registre + Merkle + **ancrage horaire sur trois supports** + page publique + **vérificateur publié** | Un tiers vérifie la chaîne sans aide. Doit démarrer **le plus tôt possible** : c'est l'actif qui prend de la valeur avec le temps |
| **4** | Score de confluence, filtres durs, **conservation du groupe témoin** | Une détection écartée est conservée avec motif et score détaillé |
| **5** | **Import du journal et écart comportemental** | Un rapport MT5 réel produit un écart chiffré |
| **6** | Abonnement Stripe, Stripe Tax, documents légaux | Un paiement de bout en bout, TVA correcte |
| **7** | Notifications, supervision de la latence | Annonce en moins de 60 s, latence journalisée |
| **8** | Interface stratégie, premier lot de 10 à 15 figures | Ajouter une figure ne modifie pas le moteur |
| **9** | Base interrogeable, seuils, correction de tests multiples, **comparaisons systématiques** | Aucun chiffre affiché sans terme de comparaison |
| **10** | Fiches figures, **référencement programmatique**, outils gratuits | Les pages se génèrent et se mettent à jour seules |
| **11** | Mode contrainte | Réponse en probabilité de réussite, pas en rendement |
| **12** | **Ouverture des données de plus de 90 jours** | Jeu téléchargeable, republié mensuellement |
| **13** | **Comptes groupe** et premiers contacts professionnels | Un administrateur crée et retire ses membres sans notre intervention |
| **14** | Catalogue complet, extension à 28 paires | Occurrences multipliées, seuils franchis |
| **15** | API contractualisée, extension crypto | — |

### 28.1 Le lot 2 est un point de décision

Le backtest honnête donne, **en quelques semaines au lieu de six mois**, une première indication
sur l'existence d'un avantage. Il ne prouve rien pour un client, mais il oriente le positionnement.

| Résultat | Conséquence |
|---|---|
| Espérance nette clairement positive après correction | Le discours « quelles configurations gagnent » est tenable |
| Espérance proche de zéro | **Basculer immédiatement** sur le discours comparatif (§8.3) et le comportemental |
| Espérance nettement négative | Le produit devient *l'outil qui chiffre ce que l'analyse technique coûte* — position unique et vendable |

### 28.2 Pourquoi commencer par le range

Il se définit **objectivement** — bornes, nombre de touches, durée —, il est **fréquent**, donc
il donne une puissance statistique exploitable en quelques mois au lieu de plusieurs années, et
les paires majeures passent la majorité de leur temps en range. L'épaule-tête-épaule est
subjective et rare : c'est le pire premier cas possible.

## 29. Risques et parades

| # | Risque | Parade |
|---|---|---|
| 1 | **Publier un chiffre non reproductible.** Un seul écart inexpliqué détruit l'unique argument du produit | §8, §17, §19, sans exception |
| 2 | **Embellir les résultats** le jour où l'abonnement en dépend | §30 : règle écrite **avant** tout revenu |
| 3 | **Refus du processeur de paiement** — le change est classé activité à risque | Lot 0, avant le code |
| 4 | **Perte de la base** | §18 : sauvegardes hors site, restauration testée, ancrage externe |
| 5 | **Trous de données non détectés** | §18 : supervision, marquage et exclusion des périodes incomplètes |
| 6 | **Élargir avant d'avoir prouvé** | Seuils du §9.1 |
| 7 | **Coût de friction sous-estimé** | §14 : coûts exprimés en R, H1 hors annonce par défaut |
| 8 | **Avantage attendu proche de zéro sur les majeures** | §8.3 et §14 : le produit garde sa valeur sans avantage de marché |
| 9 | **Dépendance à une source de données unique** | Seconde source prévue ; tout changement crée une version |
| 10 | **Exposition juridique hors UE** | §23 : États-Unis exclus au lancement |
| 11 | **Contenus de tiers** | §6 : aucun contenu produit par un utilisateur, sans exception |
| 12 | **Conflit d'intérêts avec un courtier** | §24 : pare-feu contractuel publié |

## 30. Règle d'honnêteté — à signer avant le premier euro encaissé

Le registre prospectif dira la vérité au bout de trois à six mois.

- **Espérance nette positive et stable** → le produit a une valeur démontrable que personne
  d'autre ne fournit.
- **Espérance nulle ou négative** → **on publie le chiffre tel quel.** Le produit bascule sur ce
  qu'il est réellement : *l'outil qui montre, chiffres à l'appui, ce que l'analyse technique ne
  fait pas.* C'est un produit vendable, et une position unique sur ce marché.

**Décision prise par écrit maintenant, avant tout revenu : dans le second cas, le chiffre est
publié sans retouche.** Seule protection contre la tentation de le trafiquer quand l'abonnement
en dépendra.

## 31. Points ouverts

*Regroupés ici, et nulle part ailleurs. Aucun ne bloque le lot 2.*

| # | Question | Qui tranche | Quand |
|---|---|---|---|
| 1 | Validation juridique du positionnement et des CGU | Avocat spécialisé | Avant le lot 6 |
| 2 | Statut des États-Unis : exclusion définitive ou ouverture encadrée | Avocat | Année 1 |
| 3 | Structure juridique et régime de TVA | Comptable | Avant la première facture |
| 4 | **Niveaux de prix** individuels et par siège | Le propriétaire, après mesure de la rétention | Avant le lot 6 |
| 5 | Source de prix de référence définitive | Décision technique, après essai de deux fournisseurs | Lot 2 |
| 6 | **Seuil de score pour l'annonce** | **Les données**, après 400 occurrences. Le fixer d'avance serait la première entorse au principe fondateur | Après le lot 9 |
| 7 | Priorité Telegram par rapport au webhook | La demande des utilisateurs | Après le lot 7 |
| 8 | Extension crypto | À n'envisager qu'une fois le forex prouvé | Après le lot 14 |

## 32. Glossaire

| Terme | Définition |
|---|---|
| **R** | Unité de risque. 1 R = distance entre l'entrée et l'invalidation. Un gain de 2 R rapporte deux fois ce qu'on risquait |
| **Espérance en R** | Gain moyen par trade en R. Seul indicateur qui dit si une approche gagne de l'argent |
| **Spread** | Écart entre prix d'achat et de vente. Coût payé à chaque opération |
| **Glissement** | Écart entre le prix attendu et le prix réellement obtenu |
| **Portage (swap)** | Intérêts payés ou reçus pour conserver une position d'un jour sur l'autre |
| **Pip** | Plus petite variation usuelle d'une paire. 0,0001, sauf paires en yen : 0,01 |
| **M1 / H1 / H4 / D1** | Bougies de 1 minute, 1 heure, 4 heures, 1 jour |
| **ATR** | Amplitude moyenne récente. Sert à fixer des seuils qui s'adaptent à la volatilité |
| **Pivot, ZigZag** | Repérage automatique des sommets et creux significatifs |
| **Confluence** | Convergence de plusieurs éléments favorables. Doit être chiffrée pour être exploitable |
| **Corrélation** | Degré auquel deux paires bougent ensemble. Deux positions corrélées sont un seul pari |
| **Série de pertes** | Nombre de pertes consécutives. Des séries longues sont normales et prévisibles |
| **Régime de marché** | État dominant : tendance ou range. Conditionne quelles figures fonctionnent |
| **Volume de ticks** | Nombre de changements de prix. Remplace sur le change le volume réel, qui n'existe pas — et diffère d'un courtier à l'autre |
| **Point-in-time** | Principe garantissant qu'un calcul n'utilise que l'information disponible à l'instant simulé |
| **Look-ahead bias** | Utilisation d'une information future. Rend tout backtest faussement excellent |
| **Test multiple** | Essayer beaucoup d'hypothèses fait apparaître des résultats « significatifs » par pur hasard |
| **Intervalle de confiance** | Fourchette dans laquelle se situe probablement la vraie valeur. Se resserre quand les occurrences augmentent |
| **Drawdown** | Perte maximale subie depuis un sommet de capital |
| **Groupe témoin** | Configurations écartées, conservées pour mesurer ce que vaut le filtrage |
| **Ancrage externe** | Publication chez un tiers horodateur d'une empreinte, rendant toute réécriture détectable |
| **Arbre de Merkle** | Structure permettant de prouver qu'un élément appartient à un ensemble sans fournir l'ensemble |
| **Société de financement (prop firm)** | Société qui finance un trader après un examen payant, sous contrainte stricte de perte maximale |
| **Prospectif** | Publié **avant** de connaître le résultat. Seul mode qui prouve quelque chose |
| **OSS, guichet unique** | Régime européen de déclaration de la TVA sur les services numériques vendus à des particuliers d'autres pays de l'UE |

## 33. Sources

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
