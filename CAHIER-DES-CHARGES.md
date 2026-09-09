# Cahier des charges — Application d'analyse de figures chartistes sur le forex

Document de référence unique. Remplace les notes de travail précédentes.
Version 1 — septembre 2026.

> **Comment lire ce document.** Chaque section technique commence par une ligne
> « *Pourquoi ça compte* ». Les termes sont définis au §16 (glossaire).
> Les décisions sont fermes : quand deux options existaient, une seule figure ici,
> avec son motif.

---

## 1. Le produit en une page

L'application détecte automatiquement les figures chartistes et les configurations
de marché sur le forex, explique **comment ce type de configuration se trade
habituellement**, puis **publie si l'objectif a été atteint ou non**.

Chaque détection est horodatée et publiée **avant** de connaître son issue. Elle est ensuite
résolue automatiquement. Au fil du temps se constitue une base de dizaines de milliers de
configurations documentées et mesurées **frais déduits** — c'est le cœur du produit.

L'utilisateur peut aussi importer son propre journal de trades et se comparer à cette base.

### Ce qui n'existe nulle part aujourd'hui

| Ce que font les autres | Ce que fait cette application |
|---|---|
| Un backtest fabriqué a posteriori | Un journal **prospectif** : publié avant l'issue, non modifiable |
| Un taux de réussite brut | Une **espérance en R, nette de frais** |
| Des chiffres invérifiables | Un historique chaîné par empreinte numérique, recalculable par n'importe qui |
| Du contenu pédagogique déconnecté des chiffres | **La méthode enseignée est exactement celle qui est mesurée** |
| « 90 % de réussite » | « Données insuffisantes : 37 occurrences, 100 nécessaires » |

### La phrase qui résume le positionnement

> Nous ne vous disons pas quoi acheter. Nous vous disons ce que cette configuration
> a réellement donné les 1 240 fois précédentes, frais compris — y compris quand
> le résultat nous dessert.

---

## 2. Objectif et proposition de valeur

**Objectif produit :** devenir la référence mondiale sur une seule question —
*« cette configuration chartiste, ça donne quoi réellement ? »*

**Trois avantages concurrentiels**, classés par solidité :

| Avantage | Copiable en combien de temps ? |
|---|---|
| **L'historique prospectif** | **Jamais rattrapable.** Un backtest se refait en une nuit ; deux ans de détections publiées à l'avance ne se fabriquent pas rétroactivement. Sa valeur augmente chaque jour, sans effort. |
| **L'écart comportemental** (journal de l'utilisateur comparé à la base) | 12-18 mois, et seulement après avoir accumulé la base. Crée un coût de sortie : l'utilisateur perd son historique s'il part. |
| Le moteur de détection | 3 mois. **Aucune valeur défensive.** Ne jamais bâtir l'argumentaire dessus. |

**Conséquence :** le produit n'est pas le moteur. Le produit est la base de résultats,
et ce qu'elle permet de dire à un utilisateur sur lui-même.

### L'honnêteté comme barrière à l'entrée

Le marché des outils forex vit de promesses invérifiables. Un produit dont le mécanisme
central est *« nous publions nos échecs »* est inimitable par les acteurs installés :
basculer vers la transparence détruirait les chiffres qu'ils affichent déjà.

**Cible assumée : non pas celui qui cherche des signaux, mais celui qui s'est déjà fait
avoir par des signaux.** Segment réel, atteignable uniquement en organique — ce qui tombe
bien, puisque la publicité payante est de toute façon fermée (§3).

---

## 3. Cadre juridique — les règles à ne jamais enfreindre

*Pourquoi ça compte : une seule de ces lignes franchie transforme un logiciel en activité
réglementée, avec obligation d'agrément.*

| Sujet | Position |
|---|---|
| **Agrément conseiller en investissement financier (CIF)** | **Non requis**, à une condition stricte : aucune personnalisation. L'application ne doit jamais connaître le capital, le portefeuille, ni le profil de risque de l'utilisateur pour produire une analyse (MiFID II, règl. délégué UE 2017/565, art. 9). |
| **Formulation** | Toujours « voici comment ce type de figure se trade habituellement », jamais « prenez ce trade ». C'est du contenu pédagogique générique. Réserve honnête : cette formulation est une précaution **supplémentaire**, pas le rempart principal. Le rempart, c'est l'absence de personnalisation. |
| **Règlement MAR (UE 596/2014, art. 20)** | Champ incertain sur le forex de détail : le change au comptant n'est pas un instrument financier au sens de MiFID II annexe I section C. **On applique la discipline quand même** : auteur identifié, date, méthodologie publiée, historique complet accessible, avertissement sur les performances passées. |
| **Loi Sapin 2 — art. L.222-16-1 code de la consommation** | **Interdit la publicité électronique** pour les contrats financiers hautement spéculatifs (forex, CFD) auprès du public en France. La loi influenceurs (n° 2023-451) l'interdit aussi aux influenceurs. Google Ads et Meta la restreignent ou l'interdisent. |
| **Données personnelles** | Le journal de l'utilisateur contient des données financières personnelles : RGPD, hébergement UE, export et suppression sur demande. |

### Les cinq interdits absolus dans le produit

1. Ne jamais demander le capital ou le profil de risque de l'utilisateur pour produire une analyse.
2. Ne jamais écrire « achetez », « vendez », « prenez ce trade », « recommandé pour vous ».
3. Ne jamais afficher une taille de position adaptée à l'utilisateur.
4. Ne jamais promettre un rendement, ni afficher un gain en euros.
5. Ne jamais supprimer ou corriger une détection publiée.

### Conséquence opérationnelle majeure

**L'acquisition payante est fermée.** Le canal doit être organique : contenu, vidéo,
communauté, référencement naturel. La page publique du journal prospectif (§5, module C)
est l'outil d'acquisition principal — pas une fonctionnalité annexe.

**À faire valider par un avocat spécialisé avant toute mise en ligne payante.**

---

## 4. Utilisateurs cibles

| # | Segment | Ce qu'il cherche | Priorité |
|---|---|---|---|
| 1 | **Candidat en société de financement (*prop firm*)** | Savoir quelles configurations survivent à une limite de perte quotidienne. Il paie déjà 100 à 600 $ par tentative, souvent plusieurs fois. | **Segment principal.** Capacité à payer démontrée, besoin précis, dimension mondiale. |
| 2 | Trader particulier déçu par les vendeurs de signaux | Des chiffres vérifiables plutôt que des promesses | Segment d'entrée, atteignable en organique |
| 3 | Société de financement, courtier, formateur | Statistiques agrégées : quelles configurations font sauter les comptes | Revenu B2B ultérieur, panier bien plus élevé |

**Rappel de cadrage :** 70 à 85 % des comptes de particuliers perdent de l'argent sur les CFD
(mention réglementaire obligatoire des courtiers). Ce public paie peu et part vite.
Le produit doit être conçu pour le segment 1, même si le segment 2 arrive en premier.

**Portée mondiale :** le forex est identique partout, les données sont universelles,
il n'y a aucun ancrage géographique. L'internationalisation se réduit à traduire l'interface.

---

## 5. Périmètre fonctionnel — les six modules

### Module A — Ingestion et stockage des données

*Pourquoi ça compte : si les données d'entrée sont fausses, tout le reste est faux.*

- Source de vérité : bougies **M1** (une minute), agrégées en H1, H4 et journalier.
- Spread réel reconstruit depuis les données tick, **variable selon l'heure**. À l'heure du
  roulement quotidien, il peut être plusieurs fois supérieur à la normale. Personne ne modélise
  ça, et ça fausse tous les résultats de nuit.
- Convention d'heure de clôture journalière **documentée et figée** (le fuseau change les figures
  détectées : une bougie journalière qui clôture à 17 h New York ne donne pas les mêmes figures
  qu'à minuit UTC).
- Traitement des gaps du dimanche soir, qui peuvent traverser un niveau d'invalidation.

### Module B — Moteur de détection

Chaque stratégie est un module indépendant respectant un contrat unique :

```
détecter(bougies_jusqu_à_t, paramètres)
  -> [ { sens, entrée, invalidation, objectif, horizon } ]
```

- **Interdiction absolue d'accéder à une bougie postérieure à `t`.**
- Détection **déterministe** : pivots par ZigZag à seuil ATR, puis règles géométriques.
- **Aucun apprentissage automatique en version 1** : non reproductible, non explicable,
  surapprentissage garanti sur des données de marché.
- Le catalogue complet des figures est visé (§6), ajouté par lots.

### Module C — Journal prospectif public

*C'est à la fois la preuve du produit et son principal outil d'acquisition.*

- Chaque détection est écrite dans un journal public : horodatage, paire, unité de temps,
  figure, méthode, niveaux, source de prix, version de la stratégie.
- **Chaînage par empreinte numérique** : chaque entrée contient l'empreinte de la précédente.
  Toute réécriture ultérieure devient détectable par n'importe qui.
- L'issue est calculée automatiquement, sans intervention humaine.
- **Accessible gratuitement, sans compte.** C'est ce qui remplace la publicité interdite.
- Le backtest est affiché **à côté** du journal prospectif, jamais à sa place :
  l'écart entre les deux est lui-même une information de qualité.

### Module D — Base de résultats interrogeable

Le cœur vendable. Filtres : paire, unité de temps, figure, méthode, heure de la journée,
état de tendance, période.

Sortie type :
> Épaule-tête-épaule inversée, H4, entrée sur retour — 1 240 occurrences depuis 2015.
> Objectif atteint : 46 %. Invalidation : 41 %. Sans issue à l'horizon : 13 %.
> **Espérance nette : +0,08 R.** Intervalle de confiance à 95 % : [+0,01 ; +0,15].

### Module E — Journal de trading de l'utilisateur

- Import par rapport MT4/MT5 ou fichier CSV. **Aucune connexion au courtier n'est nécessaire.**
- Statistiques personnelles : espérance, série de pertes maximale, résultats par paire,
  par heure, par jour de la semaine.
- **L'écart comportemental** — la fonction qui justifie l'abonnement :

> Vous avez pris 34 trades en range. La base donne 48 % net sur cette configuration.
> Vous êtes à 31 %. Écart principal : vous entrez en moyenne 2 bougies trop tôt.

C'est de l'analyse rétrospective sur les données de l'utilisateur : aucune exposition
réglementaire, contrairement au signal.

### Module F — Mode contrainte (*prop firm*)

Rejoue la base sous contrainte de perte maximale journalière et globale.

Répond à la seule question de ce public : *« cette approche survit-elle à une limite de perte
de 5 % par jour ? »* Une stratégie à espérance positive peut échouer dans 90 % des cas sous
contrainte de drawdown — **aucun outil existant ne le dit.**

Paramètres : objectif de gain, perte journalière maximale, perte totale maximale, durée.
Sortie : probabilité de réussite de la contrainte, et non simple rendement.

---

## 6. Catalogue des figures et unité de mesure

### On détecte tout, on ne publie pas tout

**Détection : catalogue complet.** La littérature documente plus de 60 figures
(référence : Bulkowski, *Encyclopedia of Chart Patterns*). Les détecter toutes coûte peu une
fois l'interface du module B en place, et la couverture est un argument commercial réel.

**Publication : sous condition.** C'est là que se joue toute la crédibilité.

> *Le danger n'est pas le temps de développement, c'est le **test multiple**.
> 60 figures × 3 unités de temps × 3 méthodes = plus de 500 combinaisons testées.
> Au seuil habituel de 5 %, on attend mécaniquement **une vingtaine de résultats
> « significatifs » dus au seul hasard**. Un classement « les figures qui marchent le mieux »
> établi sans correction ne classe pas des figures : il classe du bruit.
> C'est le mécanisme qui a produit toutes les fausses stratégies de l'histoire du trading.*

### Seuils de publication

| Occurrences | Précision (intervalle de confiance à 95 %) | Affichage |
|---|---|---|
| < 100 | pire que ± 10 points | **« Données insuffisantes — 37 occurrences observées, 100 nécessaires »** |
| 100 - 399 | ± 5 à 10 points | Résultat **provisoire**, intervalle affiché |
| ≥ 400 | ± 5 points | Résultat **établi** |
| ≥ 2 400 | ± 2 points | Permet d'affirmer un avantage de 2 points |

Le classement des figures applique une **correction de tests multiples**
(procédure de Benjamini-Hochberg), jamais le taux de réussite brut.

Afficher « données insuffisantes » n'est pas un aveu de faiblesse : c'est la fonctionnalité
que personne n'offre, et la preuve visible que les autres chiffres sont sérieux.

### Pour gagner en puissance statistique : ajouter des paires, jamais assouplir les seuils

Passer de 7 paires majeures à environ 28 paires (mineures et croisées) multiplie les occurrences
par 4, **sans une ligne de code supplémentaire** : même moteur, même source, même format.
C'est la seule extension autorisée quand une figure reste sous le seuil.

### L'unité statistique est **figure × méthode**, jamais la figure seule

Une épaule-tête-épaule ne se trade pas d'une seule façon :

| Méthode | Entrée |
|---|---|
| A | Cassure de l'encolure |
| B | Retour sur l'encolure après cassure |
| C | Cassure confirmée par la clôture de la bougie suivante |

Ces méthodes donnent des résultats différents. Les confondre invalide tout.

**Règle d'architecture essentielle : la méthode affichée à l'utilisateur (« voici comment se
trade ce type de figure ») et la règle qui décide gagnant/perdant sont le même objet en base.**
Une définition unique, deux usages : pédagogie et mesure. Sans cette unité, le contenu explique
une chose et les statistiques en mesurent une autre — c'est le défaut de tout le contenu
pédagogique existant et de tous les backtests publiés.

C'est aussi ce qui produit la sortie la plus vendable du produit :
*« sur l'épaule-tête-épaule, l'entrée sur retour a une espérance nette supérieure à l'entrée
sur cassure »* — une question débattue depuis trente ans, jamais chiffrée sur données prospectives.

---

## 7. Règles de mesure — à figer avant la première ligne de code

*Pourquoi ça compte : sans définition écrite et immuable, le pourcentage publié ne vaut rien
et devient manipulable — et il le sera, le jour où l'abonnement en dépendra.*

| Élément | Règle |
|---|---|
| Entrée | Selon la méthode déclarée, au prix défini par la méthode. Jamais un prix intra-bougie arbitraire |
| Invalidation | Niveau structurel de la figure (ex. sommet de la tête pour une épaule-tête-épaule) |
| Objectif | Projection mesurée de la figure |
| Horizon | Défini par méthode (par défaut 20 bougies). Ni objectif ni invalidation atteints → **sans issue**, comptabilisé à part |
| Départage | **Résolution en données M1** pour savoir lequel de l'objectif ou de l'invalidation a été touché en premier à l'intérieur d'une bougie |
| Frais | Spread horaire réel déduit à l'entrée et à la sortie. Le résultat publié est **net** |
| Indicateur principal | **Espérance en R, nette de frais** |

### Décision d'affichage qui sépare un outil sérieux d'un produit marketing

Un taux de réussite de **70 % avec un objectif à 0,3 R perd de l'argent**.
Un taux de **40 % avec un objectif à 2 R en gagne**.

**L'espérance nette en R est l'indicateur mis en avant partout.** Le taux de réussite est
affiché en second, parce que c'est ce que les gens cherchent — mais jamais en titre.

Les trois issues (objectif, invalidation, sans issue) sont toujours affichées ensemble.
Une application qui n'affiche que gagnants/perdants ment par omission.

---

## 8. Données

| Besoin | Source | Coût |
|---|---|---|
| Historique M1 et tick | Dukascopy (tick, gratuit) ou HistData (M1, gratuit) | 0 € |
| Flux courant | API forex (Polygon, TraderMade, OANDA) | ~30-50 $/mois (estimation) |

**Piège spécifique au forex : il n'existe pas de prix consolidé.** Le change est de gré à gré,
chaque courtier a son propre flux. Les chandeliers de l'utilisateur ne seront jamais
strictement identiques aux tiens.

→ **Obligation : publier la source de prix retenue, et ne jamais en changer sans l'annoncer
et sans reconstruire l'historique sous une nouvelle version.**

---

## 9. Architecture et pile technique

Choisie pour un développeur seul assisté par IA : peu de pièces, un seul langage,
tout reproductible.

| Couche | Choix | Motif |
|---|---|---|
| Traitement et API | Python (Polars, FastAPI) | Un seul langage, une seule surface de débogage |
| Base de données | PostgreSQL + TimescaleDB | **Une seule base.** Ni Kafka, ni Redis, ni microservices |
| Graphiques | TradingView Lightweight Charts | Gratuit, libre, conçu exactement pour cet usage. **Ne jamais coder son propre moteur graphique** |
| Interface | SvelteKit ou Next.js | Indifférent. Ne pas y passer de temps en v1 |
| Hébergement | Un VPS (Hetzner, 15-40 €/mois), Docker Compose, Caddy | Kubernetes serait une erreur à ce stade |
| Paiement | Stripe | Essai puis abonnement gérés nativement |

### Modèle de données (tables principales)

| Table | Rôle |
|---|---|
| `instrument` | Les paires |
| `bougie` | Chandeliers M1 et agrégats, avec spread estimé |
| `version_strategie` | **Version figée** d'une figure × méthode : code, empreinte, paramètres, dates d'activation et de retrait |
| `detection` | Une détection publiée : horodatage, niveaux, version, empreinte de l'entrée précédente, empreinte propre |
| `issue` | Résultat : atteint / invalidé / sans issue, excursions maximales favorable et défavorable, résultat brut et net |
| `trade_utilisateur` | Journal importé, éventuellement rapproché d'une détection |

---

## 10. Fiabilité — les six règles non négociables

*Pourquoi ça compte : le produit **est** ses chiffres. Une seule erreur méthodologique
invalide l'ensemble et détruit le seul avantage concurrentiel.*

1. **Point-in-time strict.** La fonction de détection ne reçoit qu'une tranche en lecture seule
   des bougies jusqu'à `t`. Un test automatisé injecte des données futures et vérifie que le
   résultat ne change pas. **C'est le test le plus important du projet.**
2. **Test de déterminisme en intégration continue.** Chaque nuit : recalcul complet de
   l'historique, comparaison des empreintes avec les détections stockées. Toute divergence fait
   échouer la compilation et impose la création d'une nouvelle version de stratégie.
   *Coût : une journée de travail. Sans ça, l'historique se réécrit silencieusement à chaque
   correction de bug, et les chiffres publiés deviennent faux sans que personne ne le voie.*
3. **Versionnement des stratégies.** Une stratégie modifiée est une stratégie **nouvelle**.
   L'ancienne conserve son historique publié. On ne supprime jamais, on remplace.
4. **Résolution intra-bougie en M1** obligatoire. C'est l'erreur qui gonfle artificiellement
   tous les taux de réussite amateurs.
5. **Frais réels** : spread horaire modélisé depuis les données tick, jamais une constante.
6. **Pré-enregistrement.** Toute nouvelle stratégie est déclarée et publiée **avant** d'être
   observée. Interdiction de publier le résultat d'une stratégie qu'on a d'abord testée en
   privé et retenue parce qu'elle donnait un bon chiffre. C'est la protection contre le test
   multiple — et contre soi-même.

---

## 11. Performance et coûts

*Pourquoi ça compte : c'est le point sur lequel les projets de ce type surinvestissent
alors qu'il n'y a aucun problème.*

- Volume : 7 paires × 3 unités de temps × 20 ans ≈ **1,1 million de bougies**. Cela tient en
  mémoire vive. Une passe complète de détection se compte en secondes ou en minutes.
- **Le calcul est identique pour tous les utilisateurs** : on précalcule une fois à chaque
  clôture de bougie, on sert depuis le cache. **Le coût marginal par abonné est proche de zéro.**
  Seul le journal personnel est calculé par utilisateur, et il est minuscule.
- **Traitement par lots, jamais de flux tick en temps réel.** C'est le seul moyen de créer un
  problème de performance, et il n'apporte rien : les figures en H1, H4 et journalier ne
  bougent pas à la seconde.

**Coût d'infrastructure total avant le premier client : moins de 100 €/mois.**
Ce n'est pas là qu'est le risque.

---

## 12. Modèle économique

| Niveau | Contenu | Prix recommandé |
|---|---|---|
| **Public, gratuit, sans compte** | Journal prospectif en direct, statistiques agrégées principales | 0 € — **c'est l'outil d'acquisition, pas une version bridée** |
| **Abonnement standard** | Base interrogeable complète, tous les filtres, alertes, journal personnel et écart comportemental | **19 €/mois** |
| **Abonnement contrainte** | Mode *prop firm*, export, accès API | **39 €/mois** |

Essai de 14 jours sur les niveaux payants.

Repère de volume : **165 abonnés à 19 €** ou **100 abonnés à 29 €** pour 2 500 €/mois brut.

Le niveau gratuit n'est pas une concession commerciale : la publicité étant fermée (§3),
c'est la seule mécanique d'acquisition dont dispose le produit, et elle se renforce
mécaniquement avec le temps.

---

## 13. Ordre de construction

*L'ordre compte plus que le contenu : chaque lot doit produire quelque chose de vérifiable.*

| Lot | Contenu | Critère d'acceptation |
|---|---|---|
| **0** | Ouvrir le compte Stripe, décrire l'activité comme **logiciel d'analyse statistique**, obtenir la validation | Compte validé. **À faire avant d'écrire du code** : un refus bloquerait toute monétisation après des mois de travail |
| **1** | Ingestion, stockage, **harnais de déterminisme et test point-in-time** | Le test qui injecte des données futures échoue si on triche. Recalcul complet reproductible à l'identique |
| **2** | **Une seule stratégie : le range**, de bout en bout, résolution M1 comprise | 500 détections historiques résolues, résultat net calculé, backtest reproductible deux fois à l'identique |
| **3** | **Page publique du journal prospectif, gratuite, sans compte** | En ligne et accumulant des détections **pendant** que le reste se développe. C'est l'actif qui prend de la valeur avec le temps : il doit démarrer le plus tôt possible |
| **4** | Interface stratégie + premier lot de figures (10 à 15) | Ajouter une figure ne demande aucune modification du moteur |
| **5** | Base interrogeable + seuils de publication + correction de tests multiples | Une figure sous 100 occurrences affiche « données insuffisantes » et non un pourcentage |
| **6** | Import du journal utilisateur + écart comportemental | Un rapport MT5 réel s'importe et produit un écart chiffré |
| **7** | Mode contrainte *prop firm* | Réponse en probabilité de réussite de la contrainte, pas en rendement |
| **8** | Catalogue complet des figures, extension à 28 paires | Occurrences multipliées, seuils franchis |
| **9** | API et licence de la base (B2B) | — |

### Pourquoi commencer par le range et non par l'épaule-tête-épaule

Le range se définit **objectivement** (bornes, nombre de touches, durée), il est **fréquent**
— donc il donne une puissance statistique exploitable en quelques mois au lieu de plusieurs
années — et les paires majeures passent la majorité de leur temps en range.
L'épaule-tête-épaule est subjective et rare : c'est le pire premier cas possible.

---

## 14. Ce qui tuera le projet si on l'ignore

| # | Risque | Parade |
|---|---|---|
| 1 | **Publier un chiffre non reproductible.** Un utilisateur recalculera. Un seul écart inexpliqué détruit l'unique argument du produit | Règles §10, sans exception |
| 2 | **Embellir les résultats** le jour où l'abonnement en dépend | §15 : écrire la règle **maintenant**, avant tout revenu |
| 3 | **Refus du processeur de paiement** (le forex est classé activité à risque) | Lot 0, avant le code |
| 4 | **Élargir avant d'avoir prouvé.** Vingt figures médiocres valent moins qu'une seule documentée sur trois ans | Seuils du §6 |
| 5 | **Le H1 est un piège.** Spread aller-retour ~1,2-2 pips contre une amplitude horaire typique de 10-15 pips : le coût de transaction consomme **~15 % du mouvement en H1, contre ~2 % en journalier** | Garder le H1, mais afficher systématiquement le résultat **net à côté du brut**. L'écart est en soi une information que les utilisateurs ignorent |
| 6 | Attente d'un avantage important sur les paires majeures | Marché le plus liquide du monde : 7 500 Md$/jour (BIS 2022). L'avantage attendu y est proche de zéro. **Le produit doit avoir de la valeur même quand les chiffres sont mauvais** — c'est le sens du §15 |

---

## 15. Règle d'honnêteté — à signer avant le premier euro encaissé

Le journal prospectif dira la vérité au bout de 3 à 6 mois. Deux issues possibles :

- **Espérance nette positive et stable** → le produit a une valeur démontrable que
  personne d'autre ne fournit.
- **Espérance nette nulle ou négative** → **on publie le chiffre tel quel.** Le produit
  bascule alors sur ce qu'il est réellement : *l'outil qui montre, chiffres à l'appui,
  ce que l'analyse technique ne fait pas.* C'est un produit vendable, et une position
  unique sur ce marché.

**Décision prise par écrit maintenant, avant tout revenu : dans le second cas, le chiffre
est publié sans retouche.** C'est la seule protection contre la tentation de le trafiquer
quand l'abonnement en dépendra.

---

## 16. Glossaire

| Terme | Définition |
|---|---|
| **R** | Unité de risque. 1 R = la distance entre l'entrée et l'invalidation. Un gain de 2 R rapporte deux fois ce qu'on risquait |
| **Espérance en R** | Gain moyen par trade exprimé en R. Seul indicateur qui dit si une approche gagne de l'argent |
| **Spread** | Écart entre prix d'achat et prix de vente. Coût payé à chaque opération |
| **Slippage** | Écart entre le prix attendu et le prix réellement obtenu |
| **Pip** | Plus petite variation usuelle d'une paire de devises |
| **M1 / H1 / H4 / D1** | Bougies de 1 minute / 1 heure / 4 heures / 1 jour |
| **ATR** | Amplitude moyenne récente. Sert à fixer des seuils qui s'adaptent à la volatilité |
| **Pivot / ZigZag** | Méthode de repérage automatique des sommets et creux significatifs |
| **Point-in-time** | Principe garantissant qu'un calcul n'utilise que l'information disponible à l'instant simulé |
| **Look-ahead bias** | Erreur consistant à utiliser une information future. Rend tout backtest faussement excellent |
| **Test multiple** | Le fait d'essayer beaucoup d'hypothèses fait apparaître des résultats « significatifs » par pur hasard |
| **Intervalle de confiance** | Fourchette dans laquelle se situe probablement la vraie valeur. Se resserre quand les occurrences augmentent |
| **Drawdown** | Perte maximale subie depuis un sommet de capital |
| **Prop firm** | Société qui finance un trader après un examen payant, sous contrainte stricte de perte maximale |
| **Prospectif** | Publié **avant** de connaître le résultat. Contraire de rétrospectif, seul mode qui prouve quelque chose |

---

## 17. Sources et références

- Bulkowski, *Encyclopedia of Chart Patterns* — catalogue de référence des figures chartistes
- Lo, Mamaysky & Wang (2000), *Foundations of Technical Analysis*, Journal of Finance
- Sullivan, Timmermann & White (1999) — correction du biais de sélection sur les règles techniques
- Bajgrowicz & Scaillet (2012) — rentabilité des règles techniques après frais et test multiple
- Bailey & López de Prado — *Deflated Sharpe Ratio*, correction du test multiple
- Enquête triennale BIS, avril 2022 — volumes du marché des changes
- Règlement (UE) 596/2014 (MAR), art. 20 ; règlement délégué (UE) 2016/958
- Directive MiFID II ; règlement délégué (UE) 2017/565, art. 9
- Code de la consommation, art. L.222-16-1 (loi Sapin 2)
