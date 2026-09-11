# Application de recherche de stratégies — EUR/USD

Statut : **cadrage, aucune ligne de code**. Document de spécification, à contredire avant de construire.
Dernière mise à jour : 2026-09-11.

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

## 6. Architecture technique proposée

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

## 7. Objection de fond, à trancher avant de commencer

`STRATEGIE.md` élimine explicitement le trading, motif « espérance négative ».
Les données confirment ce classement :

- **74 à 89 %** des comptes retail CFD perdent de l'argent (obligation de publication ESMA,
  affichée par chaque courtier).
- Étude AMF sur **14 799 clients actifs sur 4 ans : 89 % en perte, perte moyenne 10 887 €**
  par client perdant.
- Ton épargne est de **3 000 €**. Une perte de 10 887 € est hors de portée ; une perte de 3 000 €
  repousse le départ de **deux mois**.

Il faut donc séparer deux projets qui n'ont pas le même verdict :

| Projet | Verdict |
|---|---|
| **Trader l'EUR/USD avec ton épargne** | **Non.** Contredit `FEUILLE-DE-ROUTE.md`, engage le capital de départ, espérance négative documentée |
| **Construire le moteur de recherche décrit ici** | **Oui, sous conditions.** Aucun capital risqué, et tu construis exactement les compétences vendables de la priorité 4 : Python, données, statistiques, automatisation |

**Conditions :**
1. Zéro euro engagé sur les marchés tant que le moteur n'a pas produit une stratégie survivant
   aux 5 filtres **et** à 6 mois de réel simulé.
2. Le temps passé dessus sort des ~20 h/semaine. Chaque heure ici est une heure de moins
   sur la certification Klaviyo (`PLAN-MOIS-1.md`), qui est le seul chemin chiffré vers
   2 000 €/mois en 12 mois.
3. Si tu vends un jour des signaux ou du conseil en investissement, c'est une activité
   réglementée en France (statut CIF, AMF). À vérifier avant toute monétisation.

**Recommandation unique :** construis-le comme projet technique et projet de preuve de compétence,
en dehors des 20 h. Ne l'insère pas dans la feuille de route de revenu.
Si tu veux l'y insérer, alors il faut le dire — et arbitrer explicitement contre la priorité 2,
pas en plus d'elle.

---

## 8. Prochaine étape

Aucune ligne de code. Trois décisions à prendre, dans cet ordre :

1. **EUR/USD seul, ou EUR/USD puis extension à 8 majeures ?** (§5.1 — l'extension conditionne l'architecture)
2. **Projet technique hors feuille de route, ou arbitrage contre la priorité 2 ?** (§7)
3. **Acceptes-tu la suppression des unités M1-M15 en génération de signal ?** (§3)

Tant que ces trois points ne sont pas tranchés, écrire du code produit du code à jeter.

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
