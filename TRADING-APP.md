# Application de recherche de stratégies — EUR/USD

Statut : **cadrage, aucune ligne de code**. Document de spécification, à contredire avant de construire.
Dernière mise à jour : 2026-09-12.

---

## 1. Ce que tu as demandé, reformulé sans les angles morts

Une application qui :
1. rejoue 5 ans d'EUR/USD sur toutes les unités de temps ;
2. teste toutes les figures et stratégies connues ;
3. classe celles qui ont le plus fort « pourcentage de réussite » ;
4. garde en mémoire, évolue, se corrige.

**Les points 2, 3 et 4 tels qu'écrits produisent une machine à fabriquer de fausses découvertes.**
Ce document explique pourquoi, et ce qu'il faut construire à la place. Le point 1 est bon.

---

## 1 bis. Décisions actées — 2026-09-12

| Décision | Choix retenu | Conséquence |
|---|---|---|
| Périmètre | **EUR/USD seul**, extension envisagée plus tard | Coupe l'accès aux avantages transversaux (§5.1). Accepté comme coût d'apprentissage |
| Finalité | **Outil de recherche personnel. Aucun capital engagé, aucun trade réel** | Le risque financier tombe à zéro. Le risque restant est le temps (§7) |
| Validation | Damien examine les résultats lui-même | **Encadré par un protocole strict** — voir §6.3, sinon ce point ruine tout le dispositif |
| Traçabilité | Journal obligatoire dans tous les cas | §6.1 |
| Explicabilité | L'application doit justifier chaque signal | §6.2 — avec une contrainte contre-intuitive : l'explication vient **avant** le test, jamais après |
| Unités de temps | **Tranché : H1 minimum en génération de signal** | Voir ci-dessous |

**Sur les unités de temps, la raison a changé.** Sans trading réel, l'argument « les frais mangent
le gain » n'est plus un argument de perte d'argent — c'est un argument de **budget statistique**.
Tester M1-M15 revient à dépenser la moitié de ton budget de tests (§6.4) sur des hypothèses
arithmétiquement condamnées d'avance. Le coût n'est plus financier, il est méthodologique :
chaque test inutile rend les vrais résultats moins crédibles. La décision tient, pour une meilleure raison.

---

## 2. Quatre erreurs à corriger avant d'écrire du code

### 2.1 Le « pourcentage de réussite » est la mauvaise métrique

Fait mathématique. Ce qui décide du résultat, c'est l'espérance par trade :

```
E = (%gagnants × gain moyen) − (%perdants × perte moyenne) − coûts
```

Deux exemples, tous deux sur 100 trades EUR/USD :

| Stratégie | % réussite | Gain moyen | Perte moyenne | Résultat 100 trades |
|---|---|---|---|---|
| A — vendre la volatilité | **90 %** | +10 pips | −120 pips | **−300 pips** |
| B — suivi de tendance | **35 %** | +90 pips | −30 pips | **+1 200 pips** |

La stratégie à 90 % de réussite ruine le compte. Celle à 35 % gagne.
Un classement par taux de réussite sélectionne **systématiquement** le profil A :
les stratégies qui encaissent souvent peu et perdent rarement beaucoup.
C'est le mécanisme exact de la faillite de la plupart des comptes retail.

**Métrique retenue à la place :** espérance nette par trade en pips, puis ratio de Sharpe déflaté
(§4.3), profondeur et durée de la perte maximale. Le taux de réussite est affiché mais ne classe rien.

### 2.2 « Le RSI a un fort pourcentage de réussite » — faux tel quel

- Ce qui est vrai : le RSI 2 périodes en retour à la moyenne a un **taux de réussite** élevé
  (souvent 70-80 %) sur indices actions. C'est exactement le profil A ci-dessus.
- Ce qui est vrai aussi : les backtests publics qui l'affichent **ne modélisent ni le spread,
  ni le slippage** (le plus diffusé : Sharpe 0,39 moyen sur 20 symboles, coûts non modélisés).
- Ce qui est faux : transposer ça à l'EUR/USD. Le marché des changes est le marché le plus liquide
  et le plus arbitragé du monde. Neely, Weller & Ulrich (*Journal of Financial and Quantitative
  Analysis*, 2009) ont montré en test hors-échantillon réel que les rendements des règles techniques
  sur devises étaient **authentiques dans les années 1970-80 et avaient disparu au début des
  années 1990** pour les filtres et les moyennes mobiles.

Conclusion : le RSI n'est pas une hypothèse de départ privilégiée. C'est une hypothèse parmi
2 000 autres, et elle part avec un a priori défavorable.

### 2.3 « Toutes les figures × toutes les unités de temps » = fouille de données

Fait statistique. Si tu testes N stratégies **sans aucun avantage réel**, le meilleur Sharpe observé
par pur hasard vaut environ `√(2·ln N) / √(années de données)`.

Sur 5 ans de données :

| Nombre de variantes testées | Meilleur Sharpe attendu **avec zéro edge réel** |
|---|---|
| 100 | 1,36 |
| 1 000 | 1,66 |
| 10 000 | 1,93 |
| 100 000 | 2,16 |

« Toutes les figures » (20 motifs) × « toutes les unités de temps » (8) × paramètres (10 par motif)
× filtres (5) = **8 000 tests**. L'application te remontera une stratégie à Sharpe ~1,9,
courbe de capital lisse, 68 % de réussite. Elle sera **du bruit**, et elle perdra en réel.

Ce n'est pas un risque théorique : c'est le résultat attendu, avec une quasi-certitude.
Bailey & López de Prado ont formalisé la correction (ratio de Sharpe déflaté, 2014) précisément
parce que ce piège détruit des fonds professionnels.

### 2.4 « L'application évolue et se corrige » — amplificateur du problème 2.3

Une application qui réoptimise en permanence sur les mêmes 5 ans ne s'améliore pas :
elle augmente N. Chaque cycle d'auto-correction rend le meilleur résultat *plus* faux.

**L'apprentissage n'est légitime que si chaque nouvelle idée est testée sur des données
que l'application n'a jamais vues.** C'est la contrainte structurante de toute l'architecture (§4).

---

## 3. Le mur des coûts — la contrainte qui décide de tout

Estimation, à recalculer avec le vrai relevé du courtier retenu.

- Coût aller-retour EUR/USD, compte ECN : **0,6 à 1,0 pip** (spread + commission + slippage).
- Amplitude moyenne d'une bougie (ATR indicatif) :

| Unité de temps | ATR ≈ | Coût / ATR | Verdict |
|---|---|---|---|
| M1 | 2-3 pips | **30 %** | Éliminé |
| M5 | 5-8 pips | **13 %** | Éliminé |
| M15 | 10-14 pips | 7 % | Très défavorable |
| H1 | 20-30 pips | 3 % | Limite basse |
| H4 | 45-60 pips | 1,6 % | Exploitable |
| D1 | 70-100 pips | 1,0 % | Exploitable |
| W1 | 180-250 pips | 0,4 % | Exploitable |

Vérification par le volume annuel : une stratégie M5 à 10 trades/jour paie
`10 × 250 × 0,8 = 2 000 pips de frais par an`. L'amplitude annuelle totale de l'EUR/USD
est de l'ordre de 1 200 à 1 500 pips. **La stratégie doit capturer plus que le mouvement
total de l'année pour simplement rentrer dans ses frais.** C'est arithmétiquement perdu.

**Décision : l'application ne teste pas en dessous de H1.** Les unités M1 à M15 sont chargées
pour l'exécution et l'analyse de microstructure, jamais pour la génération de signal.
Cela contredit « toutes les unités de temps » — et c'est la contradiction la plus rentable
de ce document.

---

## 4. Ce qu'il faut construire : un moteur de **réfutation**, pas de découverte

Inversion du cahier des charges. L'application ne cherche pas ce qui marche.
Elle essaie de **tuer** chaque hypothèse, et ne garde que les survivantes.

### 4.1 Découpage des données — non négociable

| Période | Rôle | Règle |
|---|---|---|
| 2020-2023 (4 ans) | Développement | Tests illimités, compteur N incrémenté à chaque test |
| 2024-2025 (2 ans) | Validation | **Un seul passage par hypothèse.** Échec = hypothèse morte, définitivement |
| 2026 → | Réel simulé | Jamais utilisé pour optimiser. Uniquement pour mesurer la dégradation |

Les données de validation sont chiffrées / verrouillées par le code. On ne peut pas y accéder
sans enregistrer le test dans le journal. C'est une contrainte technique, pas une discipline
personnelle — la discipline personnelle ne tient pas.

### 4.2 Pré-enregistrement des hypothèses

Avant tout test, l'hypothèse est écrite en base : nom, mécanisme économique supposé,
règle d'entrée, de sortie, paramètres, unité de temps, date. **Sans mécanisme économique
plausible, l'hypothèse est refusée.**

Raison : un motif sans cause est un motif sans avenir. « Le RSI passe sous 30 » n'est pas une cause.
« Les gérants actions rééquilibrent leur couverture de change en fin de mois » en est une.

### 4.3 Le compteur N est la variable d'état la plus importante

C'est *ça*, la « mémoire » que tu demandes. Pas une collection de stratégies gagnantes :
un **journal complet de tous les tests, échecs inclus**, qui permet de calculer le Sharpe déflaté
et donc de savoir si un résultat est réel ou tiré au sort.

Une base qui ne garde que les gagnantes est pire qu'une absence de mémoire :
elle donne une confiance fausse.

### 4.4 Validation en cascade — 5 filtres, éliminatoires dans l'ordre

1. **Coûts réels** : spread horaire réel (données bid/ask tick), pas un spread moyen.
2. **Walk-forward ancré** avec purge et embargo (empêche la fuite d'information entre train et test).
3. **Sharpe déflaté** > 0 en tenant compte du N réel du journal.
4. **Robustesse paramétrique** : la performance doit survivre à ±30 % sur chaque paramètre.
   Un pic isolé dans la grille de paramètres = surapprentissage, rejet automatique.
5. **Cohérence par régime** : le résultat doit tenir sur au moins 3 des 4 régimes
   (volatilité haute/basse × tendance/range). Une stratégie qui ne gagne que sur 2022 est morte.

Estimation : **moins de 3 % des hypothèses testées passeront les 5 filtres.** C'est normal, et
c'est le signe que le moteur fonctionne. Un moteur qui valide 30 % des idées est cassé.

### 4.5 Suivi de dégradation

Une fois une stratégie validée, l'application compare en continu le réel simulé au backtest.
Écart significatif (test séquentiel) → mise à l'arrêt automatique. Les avantages en devises
ne meurent pas brutalement, ils s'érodent — voir §2.2.

---

## 5. Ce que la recherche documente réellement comme ayant un avantage

Recherche effectuée le 2026-09-11. Classement par solidité de la preuve.

### 5.1 Prouvé, mais **inaccessible sur une seule paire**

| Effet | Preuve | Blocage |
|---|---|---|
| **Carry** (portage) | Robuste sur 200 ans d'historique | Nécessite un panier de devises, pas une paire |
| **Momentum de devises** | Documenté, publié | Transversal : classement de 8-10 paires |
| **Basis-momentum** | Fan (2025), *European Financial Management* : rendements significatifs, risque plus faible que le carry | Transversal |
| **Value / PPP** | Documenté | Transversal, horizon pluriannuel |

**Conséquence directe sur ton cahier des charges :** les avantages les mieux établis du marché
des changes sont *transversaux* — ils viennent de la comparaison entre devises, pas de l'analyse
d'une seule. Se limiter à l'EUR/USD **t'interdit l'accès aux quatre meilleures sources d'avantage
documentées.**

Recommandation : garder l'EUR/USD comme paire pilote pour construire le moteur (données les plus
propres, spread le plus faible), puis **étendre à 8 majeures dès que le moteur tourne.**
L'extension multiplie le coût de développement par ~1,2 et l'espace d'avantages exploitables par ~10.

### 5.2 Exploitable sur EUR/USD seul — les vraies pistes

| Piste | Nature de la preuve | Réserve |
|---|---|---|
| **Momentum temporel** (D1/W1) | Publié, deux siècles de données | Performance **quasi nulle depuis 2011** sur l'indice SG Trend. Encombrement. Sharpe réaliste 0,3-0,5 |
| **Flux de fin de mois / fixing 16h Londres** | Melvin & Prins (*Journal of Empirical Finance*, 2015) : effet significatif, prévisible à partir des mouvements actions relatifs | Effet atténué depuis la réforme du fixing (fenêtre 5 min, 2015). À re-tester sur 2020-2025 |
| **Saisonnalité intrajournalière / chevauchement Londres-New York** | Effet documenté, mais **conditionnel aux annonces macro US** | Sur M15 ou moins → détruit par les coûts (§3) |
| **Volatilité autour des annonces programmées** (NFP, CPI, FOMC, BCE) | La volatilité est prévisible, **la direction ne l'est pas** | Impose des stratégies d'options ou de straddle, pas du directionnel |
| **Différentiel de taux Fed / BCE (swap)** | Mécanique, pas statistique : c'est un flux de trésorerie contractuel | Faible, mais c'est le seul rendement non aléatoire de la liste |

### 5.3 Ce que la recherche **ne** soutient pas

- **Figures chartistes** (épaule-tête-épaule, triangles, drapeaux). Les statistiques de Bulkowski
  sont sérieuses mais portent sur les **actions américaines**, mesurent le mouvement *après*
  cassure sans coûts ni stop réaliste, et la définition d'une figure est elle-même un paramètre
  libre qui gonfle N (§2.3). À traiter comme hypothèses à réfuter, jamais comme référence.
- **Le RSI comme avantage autonome.** Voir §2.2.
- **Toute combinaison d'indicateurs classiques sur EUR/USD sous H1.** Éliminée par les coûts (§3).

---

## 6. Journal, explicabilité et rôle humain

C'est la partie que tu as ajoutée, et c'est la plus délicate des trois. Chacune des trois exigences
est bonne, et chacune a une version naïve qui produit l'inverse de l'effet recherché.

### 6.1 Le journal — trois propriétés non négociables

Un journal n'a de valeur que s'il est impossible à embellir. Trois contraintes techniques :

1. **Ajout seul (append-only), haché en chaîne.** Chaque ligne contient le hachage de la précédente.
   Une modification rétroactive casse la chaîne et se voit. Sans ça, tu réécriras l'histoire
   sans même t'en rendre compte — tout le monde le fait.
2. **Horodatage du signal avant le prix suivant.** Le signal est écrit en base, scellé, *puis*
   la bougie suivante est lue. Un journal qui enregistre le signal après avoir vu le résultat
   ne prouve rien. C'est l'erreur qui invalide 90 % des journaux de trading personnels.
3. **Les échecs y sont, au même titre que les succès.** Hypothèses rejetées, stratégies abandonnées,
   tests interrompus. Un journal qui ne garde que ce qui a marché est un outil d'auto-persuasion.

Contenu minimal par entrée : identifiant d'hypothèse, horodatage UTC, prix bid et ask au signal,
direction, taille, stop, objectif, régime détecté, et l'intégralité des valeurs d'indicateurs
au moment de la décision.

### 6.2 L'explicabilité — le piège de l'explication a posteriori

Ton exigence : « l'application devra expliquer ses choix ». Bonne exigence, piège sérieux.

**Une explication générée après coup sur une stratégie issue de fouille de données est une
rationalisation, pas une explication.** Elle rend le bruit convaincant. C'est strictement pire
que pas d'explication du tout : tu auras une courbe de capital fausse *et* un récit crédible
pour y croire.

La seule forme honnête : **l'explication est écrite avant le test, pas après.**

L'application n'explique donc jamais *pourquoi elle a choisi une stratégie*. Elle rapporte
une seule chose : **le mécanisme déclaré à l'avance s'est-il vérifié, oui ou non.**

Rapport type pour un signal :

```
Hypothèse H-047  (déclarée le 2026-09-20, avant tout test)
Mécanisme déclaré : les gérants actions couvrent leur exposition change en fin de mois
                    -> pression vendeuse sur la devise du marché actions surperformant,
                       concentrée avant le fixing de 16h Londres.
Condition remplie : dernier jour ouvré du mois, T-90 min avant fixing,
                    écart de performance S&P500 / EuroStoxx sur le mois = +3,1 %
Régime détecté   : volatilité basse, absence d'annonce macro a moins de 4 h
Base statistique : 58 occurrences (2020-2023). Hors-echantillon 2024-2025 : 24 occurrences
Espérance        : +11 pips  [IC 95 % : -2 a +24]
Ce qui invaliderait : espérance hors-echantillon negative sur 20 occurrences consecutives
```

Trois règles de présentation, à imposer dans le code :

- **Toute statistique est affichée en intervalle de confiance, jamais en valeur ponctuelle.**
  « +11 pips » est malhonnête. « +11 pips [IC 95 % : −2 à +24] » dit la vérité : le résultat
  est compatible avec zéro.
- **Le nombre d'occurrences est affiché à côté de chaque chiffre.** Une espérance calculée
  sur 12 trades ne veut rien dire, quelle que soit sa valeur.
- **La condition de falsification est affichée avec le signal**, pas dans une annexe.

### 6.3 Ton rôle — protocole d'examen humain

Tu as écrit : « je regarde moi-même si c'est juste ou pas ». **Tel quel, ça détruit le dispositif.**

Raison : si l'application te remonte 50 stratégies et que tu gardes celles qui « te semblent justes »,
tu viens d'exécuter 50 tests supplémentaires non comptabilisés, avec un filtre humain opaque.
Le compteur N est faussé, le Sharpe déflaté ne vaut plus rien, et tu auras sélectionné
les stratégies **les plus convaincantes**, qui ne sont pas les plus vraies — juste les mieux
racontées.

Ton jugement a pourtant une valeur réelle, mais à un seul endroit : **avant le test, sur le
mécanisme économique.** Un humain sait dire « cette règle n'a aucune cause plausible ».
Aucune machine ne sait le faire.

D'où le protocole :

| Moment | Ce que tu fais | Ce que tu n'as pas le droit de faire |
|---|---|---|
| **Avant le test** | Valider ou refuser le mécanisme économique déclaré. C'est ton vrai apport | — |
| **Avant de voir le résultat** | **Noter ta prédiction** : marchera / ne marchera pas, et ton niveau de confiance | — |
| **Pendant** | Rien | Ajuster les paramètres, prolonger la période, relancer |
| **Après** | Lire. Éventuellement déclarer une **nouvelle** hypothèse, qui incrémente N | Choisir les gagnantes dans une liste de résultats |

L'étape « noter ta prédiction avant de voir » est le point le plus utile du projet pour toi.
Au bout de 50 hypothèses, l'application calcule ta **calibration** : quand tu dis « 80 % sûr »,
as-tu raison 80 % du temps ? C'est la seule façon de transformer « je regarde moi-même si c'est juste »
en donnée mesurable au lieu d'une impression. Réponse probable la première année : tu es
mal calibré, comme tout le monde. La valeur est de le savoir.

Le journal enregistre donc **deux** flux : les décisions de l'application, et les tiennes.

### 6.4 Le budget de tests — à fixer maintenant, pas à découvrir plus tard

Puisque N détermine si un résultat est réel (§2.3), il doit être une **décision consciente**,
pas un compteur qu'on découvre à la fin.

Seuil de Sharpe en dessous duquel un résultat est indiscernable du hasard, sur 5 ans de données :

| Budget de tests | Sharpe minimal crédible |
|---|---|
| 50 hypothèses | **1,25** |
| 200 hypothèses | **1,45** |
| 1 000 hypothèses | **1,66** |
| 10 000 hypothèses | **1,93** |

Estimation (approximation `√(2·ln N) / √années`, tests supposés indépendants et rendements normaux).
Les stratégies réelles sont corrélées entre elles, donc le seuil effectif est un peu plus bas —
mais l'ordre de grandeur tient, et c'est une borne prudente.

**Recommandation : budget de 200 hypothèses, seuil de crédibilité fixé à Sharpe 1,45.**
Tout ce qui sort en dessous est classé « non concluant », jamais « prometteur ».
À titre de repère : les meilleurs gérants de suivi de tendance tournent autour de **0,75**
de Sharpe (§5.2). Un résultat à 1,45 sur EUR/USD seul doit donc être considéré
comme **suspect par défaut**, pas comme une découverte.

L'application affiche en permanence : `tests consommés / budget`. Budget épuisé =
plus aucun accès aux données de validation. C'est verrouillé dans le code.

---

## 7. Architecture technique proposée

| Couche | Choix | Motif |
|---|---|---|
| Données | **Dukascopy** (tick bid/ask, 15+ ans, gratuit) ; HistData en secours | Le bid/ask réel est indispensable : un spread moyen falsifie tous les résultats |
| Stockage | Parquet + DuckDB | 5 ans de ticks EUR/USD ≈ 10-20 Go. SQLite ne tient pas |
| Balayage | **vectorbt** (NumPy + Numba) | Milliers de variantes en secondes, pour la phase exploratoire |
| Validation | **NautilusTrader** | Moteur événementiel, exécution fidèle. Les survivants du balayage y repassent |
| Journal | PostgreSQL ou SQLite | Hypothèses, tests, N, résultats, échecs. C'est le cœur, pas un accessoire |
| Statistiques | Sharpe déflaté, probabilité de surapprentissage (PBO) | Implémentation directe des papiers Bailey & López de Prado |

Règle : **balayage vectoriel pour éliminer, moteur événementiel pour valider.** Jamais l'inverse.
Un backtest vectoriel ment sur la microstructure ; il sert à écarter, pas à confirmer.

---

## 8. Objection de fond — état au 2026-09-12

`STRATEGIE.md` élimine le trading, motif « espérance négative ». Les données le confirment :
**74 à 89 %** des comptes retail CFD perdent de l'argent (publication obligatoire ESMA) ;
étude AMF sur **14 799 clients actifs sur 4 ans : 89 % en perte, 10 887 € de perte moyenne**
par client perdant. Ton épargne est de 3 000 €.

### 8.1 Risque financier — **levé**

Tu as tranché : outil de recherche, aucun capital engagé, aucun trade réel. L'objection
principale de `STRATEGIE.md` ne s'applique plus. Le projet est légitime sous cette forme.

Condition maintenue, sans exception : **zéro euro engagé tant que le moteur n'a pas produit
une stratégie survivant aux 5 filtres (§4.4) *et* à 6 mois de réel simulé.** Le jour où cette
question se reposera, elle se reposera avec des données, pas avec une envie.

### 8.2 Risque de temps — **ouvert, c'est la seule décision qui reste**

Estimation : **80 à 150 h** pour construire ce moteur correctement en partant novice en Python,
soit 2 à 4 mois à 10 h/semaine. Sur un horizon de 12 mois, c'est un quart du chemin vers
2 000 €/mois récurrents.

| Option | Conséquence |
|---|---|
| **A — hors des 20 h/semaine** (recommandée) | La feuille de route de revenu est intacte. Le projet avance plus lentement. C'est le seul scénario où les deux tiennent |
| **B — dedans, en arbitrage assumé contre la priorité 2** | Repousse la première vente de 2 à 4 mois, donc la démission d'autant. Acceptable **si** tu le décides explicitement |
| **C — dedans, sans le dire** | Le scénario par défaut, et le seul vraiment mauvais. La priorité 2 s'érode sans décision, et tu ne t'en apercevras qu'au mois 6 |

**Recommandation unique : option A.** Ce projet construit de vraies compétences vendables
(Python, données, statistiques, automatisation) — ce sont exactement celles de la priorité 4
de `FEUILLE-DE-ROUTE.md`. Mais elles ne paient qu'une fois vendues à un client, et ce moteur
n'a pas de client. Il ne remplace pas la priorité 2, il s'y ajoute.

### 8.3 Risque réglementaire — à vérifier avant toute monétisation

Tant que l'outil reste personnel, aucun sujet. Si un jour tu vends des signaux, un abonnement
ou du conseil en investissement en France, c'est une activité réglementée (statut CIF, AMF).
À vérifier **avant** d'en parler à qui que ce soit, pas après.

---

## 9. Prochaine étape

Une seule décision reste ouverte, et c'est la plus importante : **§8.2 — ce projet sort-il
des 20 h/semaine, ou mange-t-il la priorité 2 ?**

Le risque financier est désormais nul : tu ne trades pas. Le risque restant est entièrement
un risque de temps, et il est réel — construire ce moteur correctement représente une
estimation de **80 à 150 h** pour un novice en Python, soit 2 à 4 mois à 10 h/semaine.
Sur 12 mois, c'est le quart du chemin vers 2 000 €/mois.

Ce n'est pas un argument pour renoncer. C'est un arbitrage à poser à voix haute, pas à subir.

Ordre de construction, une fois la question tranchée :

| Étape | Livrable | Estimation |
|---|---|---|
| 1 | Chargeur Dukascopy + stockage Parquet/DuckDB, EUR/USD H1 à W1, 2020-2026 | 10-15 h |
| 2 | Journal append-only haché + schéma d'hypothèses pré-enregistrées | 10-15 h |
| 3 | Moteur de backtest avec spread bid/ask réel, une seule stratégie de référence triviale | 15-25 h |
| 4 | Verrou sur les données de validation + compteur de budget de tests | 5-10 h |
| 5 | Sharpe déflaté, walk-forward purgé, robustesse paramétrique | 20-30 h |
| 6 | Rapport explicable + suivi de calibration humaine | 15-25 h |

**L'étape 3 ne teste qu'une stratégie volontairement banale** (croisement de moyennes mobiles,
par exemple), dont on attend qu'elle échoue. Objectif : vérifier que le moteur sait dire non.
Un moteur validé sur une stratégie gagnante ne prouve rien.

---

## Sources

- Neely, Weller & Ulrich, *The Adaptive Markets Hypothesis: Evidence from the Foreign Exchange Market*, Journal of Financial and Quantitative Analysis — https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/adaptive-markets-hypothesis-evidence-from-the-foreign-exchange-market/9D336CDCA83233819EB5CDD0F4BC0DAA
- Bailey & López de Prado, *The Deflated Sharpe Ratio* — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Bailey, Borwein, López de Prado & Zhu, *The Probability of Backtest Overfitting* — https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
- Fan, *Understanding the Performance of Currency Basis-Momentum*, European Financial Management 2025 — https://onlinelibrary.wiley.com/doi/full/10.1111/eufm.12555
- Fan, *Optimizing Currency Factors*, Financial Review 2025 — https://onlinelibrary.wiley.com/doi/10.1111/fire.70000
- Melvin & Prins, *Equity hedging and exchange rates at the London 4 p.m. fix*, Journal of Empirical Finance — https://www.sciencedirect.com/science/article/abs/pii/S1386418114000779
- *Did the Reform Fix the London Fix Problem?*, NBER — https://www.nber.org/system/files/working_papers/w23327/w23327.pdf
- *Two centuries of trend following* — https://arxiv.org/pdf/1404.3274
- Statistiques de pertes des comptes CFD (publications ESMA) — https://goodmoneyguide.com/trading/risk-warning-loss-percentages/
- Étude AMF sur les clients actifs forex/CFD — https://www.traderslog.com/what-percentage-of-traders-lose-money
- Rapports de performance suivi de tendance 2025 — https://www.toptradersunplugged.com/trend-following-performance-report-april-2025/
- Comparatif des moteurs de backtest Python 2026 — https://bullalert.ai/blog/best-python-backtest-engines-2026/
- Données historiques Dukascopy — https://www.dukascopy-node.app/instrument/eurusd
