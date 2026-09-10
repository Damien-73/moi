# Spécification technique — Lot 11 : mode contrainte (*prop firm*)

Document d'implémentation. Complète le cahier des charges §5 module F.

> **C'est la fonction destinée au segment principal** (cahier des charges §4) : un public qui
> paie déjà 100 à 600 $ par tentative et dont la question n'a aujourd'hui aucune réponse
> chiffrée. Une stratégie à espérance positive peut échouer dans neuf cas sur dix sous
> contrainte de perte maximale — et aucun outil ne le dit.

---

## 1. La question à laquelle on répond

**Pas** : « cette approche est-elle rentable ? »
**Mais** : « quelle est la probabilité qu'elle atteigne l'objectif **avant** de franchir une
limite de perte ? »

Ce sont deux questions différentes, et la seconde ne se déduit pas de la première.
Une espérance de +0,05 R par trade est positive ; la même approche, avec 1,5 % de risque par
trade sous une limite de perte totale de 10 %, échoue dans la majorité des simulations.

---

## 2. Paramètres d'entrée

### 2.1 Contraintes de l'examen

| Paramètre | Type | Valeur usuelle |
|---|---|---|
| Objectif de gain, phase 1 | % du capital | 8 à 10 % |
| Objectif de gain, phase 2 | % du capital | 4 à 5 % |
| **Perte journalière maximale** | % | 4 à 5 % |
| **Perte totale maximale** | % | 6 à 12 % |
| Type de perte totale | `statique` ou `suiveuse` | Voir §2.2 |
| Référence de la perte journalière | `solde d'ouverture` ou `capital initial` | Selon l'organisme |
| Heure de réinitialisation journalière | Fuseau + heure | Souvent minuit heure de New York |
| Durée maximale | Jours, ou illimitée | 30 jours, ou sans limite |
| Jours de négociation minimaux | Nombre | 0 à 5 |

### 2.2 Perte totale statique contre suiveuse — distinction déterminante

| Type | Calcul | Effet |
|---|---|---|
| **Statique** | Seuil = `capital_initial × (1 − perte_max)`, fixe | Le gain accumulé constitue un coussin |
| **Suiveuse** | Seuil = `plus_haut_atteint × (1 − perte_max)`, remonte avec les gains | **Aucun coussin ne se constitue.** Un compte en gain de 6 % reste à 10 % de la rupture |

La variante suiveuse est nettement plus sévère et très répandue. Confondre les deux fausse
complètement le résultat. **Les deux sont implémentées, et le type retenu est affiché en
permanence dans le résultat.**

Variante à supporter également : seuil suiveur qui **se fige** une fois le capital initial
dépassé de l'objectif — pratique courante, intermédiaire entre les deux.

### 2.3 Paramètres de la stratégie simulée

Filtre de configurations (figure, méthode, unité de temps, tranche de score, paires),
**risque par trade en pourcentage**, nombre maximal de positions simultanées.

### 2.4 Contrainte juridique sur les entrées

Tout est exprimé **en pourcentage**. La taille de compte n'est qu'un confort d'affichage :
elle n'est **ni enregistrée, ni utilisée pour filtrer ou classer quoi que ce soit**
(cahier des charges §10.3). Le simulateur porte sur les règles d'un examen, jamais sur la
situation financière de l'utilisateur.

---

## 3. Méthode de simulation

### 3.1 Rééchantillonnage par blocs journaliers — le point technique décisif

*L'erreur qui invaliderait tout le module : rééchantillonner les trades un par un.*

Tirer des trades indépendamment détruit deux structures dont dépend entièrement le résultat :

1. **Le regroupement journalier.** La limite de perte journalière ne porte pas sur des trades
   isolés mais sur ce qui se produit **dans une même journée**. Un tirage indépendant disperse
   les pertes entre les jours et **sous-estime massivement** la probabilité de franchir la
   limite journalière.
2. **La corrélation entre positions simultanées.** Trois positions ouvertes le même jour sur
   des paires corrélées perdent ensemble. Le tirage indépendant traite ces pertes comme trois
   événements distincts.

> **Règle : l'unité de rééchantillonnage est la journée de négociation complète, avec tous ses
> trades et leur ordre.** Les deux structures sont alors préservées sans avoir à les modéliser.

```
1. Constituer l'ensemble des journées historiques du filtre choisi
   (chaque journée = liste ordonnée des R nets de ses détections).
2. Pour chaque simulation :
   a. Tirer des journées avec remise jusqu'à atteindre l'objectif,
      franchir une limite, ou épuiser la durée maximale.
   b. Appliquer les trades de la journée dans l'ordre, en actualisant
      le capital après chacun (dimensionnement fractionnaire fixe).
   c. Après chaque trade : contrôler la perte totale.
      En fin de journée : contrôler la perte journalière.
   d. Enregistrer l'issue et le nombre de jours écoulés.
3. Répéter 10 000 fois.
```

### 3.2 Contrôles à l'intérieur d'une journée

La limite de perte **totale** peut être franchie en cours de journée : elle est donc contrôlée
**après chaque trade**, pas seulement en clôture. La limite **journalière** est évaluée sur le
cumul de la journée, à sa réinitialisation.

Cas particulier à traiter explicitement : lorsque plusieurs positions sont ouvertes
simultanément, la perte flottante peut franchir une limite avant que les trades ne soient
clôturés. Le modèle utilise les **excursions défavorables maximales** enregistrées avec chaque
détection (`SPEC-LOT2` §6.5) pour évaluer le pire point de la journée, et non son seul résultat
final. **Sans cela, le simulateur serait optimiste** — et un simulateur optimiste sur cette
question est pire qu'aucun simulateur.

### 3.3 Précision annoncée

10 000 simulations. La probabilité affichée porte son propre intervalle de confiance
binomial : une probabilité de 32 % sur 10 000 tirages vaut 32 % ± 0,9 point.

**Si l'historique du filtre choisi comporte moins de 60 journées distinctes, aucun résultat
n'est affiché** : « historique insuffisant — 41 journées sur 60 nécessaires ». Même discipline
que partout ailleurs dans le produit.

---

## 4. Sorties

### 4.1 Résultat principal

```
        31 %
        probabilité de réussite de la phase 1
        ────────────────────────────────────────────────────────
        Échec par perte totale     52 %
        Échec par perte journalière 11 %
        Délai dépassé               6 %
        Durée médiane si réussite  18 jours
        10 000 simulations · IC 95 % [30,1 % ; 31,9 %]
        Perte totale suiveuse · risque 1 % · score ≥ 70 %
```

La **répartition des causes d'échec** vaut autant que la probabilité : elle indique quoi
corriger. Un échec dominé par la limite journalière appelle une réduction du nombre de
positions simultanées ; un échec par perte totale appelle une réduction du risque unitaire.

### 4.2 La sortie la plus utile : probabilité en fonction du risque par trade

Simulation répétée pour chaque valeur de risque de 0,25 % à 3,00 %, par pas de 0,25 %.

```
risque    0,25%  0,50%  0,75%  1,00%  1,25%  1,50%  2,00%  2,50%  3,00%
réussite    18%    29%    34%    31%    25%    19%    10%     5%     2%
                          ▲ optimum
```

**La courbe n'est pas monotone, et c'est le résultat que personne ne montre.** En dessous de
l'optimum, on ne peut pas atteindre l'objectif dans le temps imparti ; au-dessus, on franchit
la limite avant. L'optimum se situe presque toujours **bien plus bas que ce que les traders
utilisent** — ce qui confirme par le calcul la décision du cahier des charges §10.2 d'écarter
le risque de 2 %.

Un seul graphique, une seule lecture, et il justifie à lui seul l'abonnement supérieur.

### 4.3 Autres sorties

Probabilité combinée des deux phases · courbe de capital des simulations médiane, du premier
et du dernier décile · distribution de la perte maximale atteinte · nombre médian de trades
avant l'issue.

---

## 5. Ce que le simulateur ne dit pas — affiché à l'écran

*L'avertissement fait partie du produit. Le masquer contredirait tout le reste.*

| Limite | Formulation affichée |
|---|---|
| Hypothèse de stationnarité | « Cette simulation suppose que l'avenir ressemble au passé mesuré. Ce n'est pas garanti. » |
| Exécution parfaite supposée | « Elle suppose que chaque configuration est prise, sans exception ni improvisation. Aucun trader ne fait cela. » |
| Résultat probabiliste | « 31 % de réussite ne signifie pas que vous réussirez à 31 %. Cela signifie que sur 100 tentatives conduites ainsi, environ 31 aboutiraient. » |
| Aucune personnalisation | « Ce calcul ne tient aucun compte de votre situation. Il porte sur des règles d'examen, pas sur vous. » |

**Cohérence avec le §27 du cahier des charges :** si les probabilités calculées sont faibles —
ce qui est l'issue la plus probable — elles sont affichées telles quelles. Un outil qui
annonce honnêtement 31 % à quelqu'un qui s'apprête à payer 300 $ lui rend un service que
personne d'autre ne lui rend, et il s'en souviendra.

---

## 6. Critères d'acceptation

| # | Critère |
|---|---|
| 1 | Perte totale statique, suiveuse et suiveuse figée sont implémentées et distinguées à l'écran |
| 2 | Le rééchantillonnage se fait par journée complète, jamais par trade isolé — vérifié par test |
| 3 | La limite totale est contrôlée après chaque trade, la limite journalière à la réinitialisation |
| 4 | Les excursions défavorables maximales sont utilisées pour les positions simultanées |
| 5 | Sous 60 journées d'historique, aucun résultat n'est affiché |
| 6 | La probabilité est accompagnée de son intervalle de confiance |
| 7 | La courbe risque / réussite est produite sur toute la plage 0,25 % à 3 % |
| 8 | Les quatre avertissements du §5 sont visibles sans avoir à faire défiler la page |
| 9 | Aucune taille de compte n'est enregistrée en base |


---

## 7. Constat de construction : espérance négative et risque optimal

*Mesuré à l'exécution, sur un jeu où l'espérance nette est de −0,19 R.*

```
risque      0,25%  0,50%  0,75%  1,00%  1,25%  1,50%  2,00%  2,50%  3,00%
réussite       3%    12%    15%    17%    19%    20%    19%    20%    20%
```

**La courbe ne redescend pas. L'optimum est au risque maximal.**

Ce n'est pas une anomalie, c'est la conséquence logique d'une espérance
négative : quand chaque trade fait perdre en moyenne, atteindre un objectif de
gain ne peut venir que de la **variance**. Augmenter le risque augmente la
variance, donc la probabilité — faible — d'atteindre l'objectif avant de sauter.

> **Autrement dit : lorsque l'espérance est négative, le simulateur recommande
> mécaniquement de jouer gros. C'est le comportement d'un billet de loterie,
> pas d'une méthode.**

### Conséquence sur le produit

Le mode contrainte **doit afficher le signe de l'espérance avant la courbe**,
et, lorsqu'elle est négative, remplacer l'« optimum » par un avertissement :

> Espérance nette de cette sélection : −0,19 R. Aucune taille de position ne
> rend cette approche viable. La probabilité affichée augmente avec le risque
> parce que seule la chance peut atteindre l'objectif — ce n'est pas une
> recommandation, c'est la description d'un pari.

Sans cette règle, un utilisateur lirait « optimum à 3 % » et prendrait le
chiffre pour un conseil. Ce serait le contraire exact de ce que le produit
prétend faire.
