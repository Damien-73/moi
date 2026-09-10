# Spécification technique — Évolution du moteur

Comment le système apprend de ses échecs **sans détruire la propriété qui fait toute sa
valeur** : la reproductibilité.

---

## 1. Ce que la version naïve détruirait

L'intention — « une détection échoue, on comprend pourquoi, on retient la leçon » — est juste.
Son implémentation directe est fatale. Quatre raisons, dans l'ordre de gravité.

| # | Effet | Conséquence |
|---|---|---|
| 1 | **Surapprentissage** | Un moteur qui s'ajuste après chaque échec apprend le bruit. En six mois, historique magnifique, avantage réel nul. C'est la façon dont se fabriquent toutes les fausses stratégies |
| 2 | **Destruction de l'historique** | On ne peut pas dire « cette stratégie fait +0,12 R sur deux ans » si elle a changé quarante fois. L'actif de l'entreprise disparaît |
| 3 | **Perte de reproductibilité** | Un tiers ne peut plus recalculer. Le vérificateur public devient inutile |
| 4 | **Superstition** | Voir ci-dessous : un échec isolé ne contient presque aucune information |

### La vérité mathématique qu'il faut avoir en tête

> **Dans un système à 45 % de réussite, une perte isolée est l'issue la plus probable.
> Elle ne contient strictement aucune information de diagnostic.**

Chercher « pourquoi ce trade a échoué » est exactement ce que fait un trader qui construit des
superstitions. Le système doit être conçu pour ne jamais le faire.

**Ton observation « des fois c'est juste le marché » n'est pas une excuse : c'est l'hypothèse
par défaut, et elle est vraie dans la grande majorité des cas.** Tout le mécanisme ci-dessous
consiste à prouver le contraire avant d'agir.

---

## 2. Le partage fondamental : la mesure et la règle

*Deux choses évoluent, et elles n'obéissent pas au même régime.*

| | **La mesure** | **La règle** |
|---|---|---|
| Quoi | Modèle de spread, portage, résolution intra-bougie, complétude, correction de bug | Conditions géométriques, critères du score, pondérations, seuils |
| Évolution | **Toujours permise, et encouragée** | **Fortement contrainte** |
| Effet | Recalcul complet de l'historique sous une nouvelle version de mesure. Les anciens chiffres restent consultables, l'écart est publié | Nouvelle version de stratégie, historique de l'ancienne intact, période de comparaison obligatoire (§6) |
| Justification exigée | Un défaut démontré | Un défaut démontré **statistiquement**, sur une population, hors bruit (§4) |

**Améliorer la mesure améliore la vérité. Changer la règle change ce qu'on mesure.**
Confondre les deux est l'erreur qui ruinerait le projet.

---

## 3. L'unité d'apprentissage n'est pas le trade

> **On n'apprend jamais d'une détection. On apprend d'une cellule.**

Une **cellule** = figure × méthode × unité de temps × tranche de score, éventuellement croisée
avec une séance ou un régime. Une cellule n'entre dans le processus d'évaluation qu'à partir de
**100 occurrences résolues**, et n'autorise une décision qu'à **400**.

Toute analyse d'une détection isolée est **interdite dans le moteur**. Elle reste possible dans
l'interface, à titre pédagogique, avec la mention :

> Ce résultat isolé n'a aucune valeur statistique. Voir la cellule complète : 1 240 cas.

---

## 4. Les quatre causes d'un écart, et ce que chacune autorise

Quand une cellule sous-performe par rapport à son historique, l'ordre d'examen est fixe.
**On ne passe à la cause suivante qu'après avoir écarté la précédente.**

### Cause 1 — Le bruit *(hypothèse par défaut)*

L'écart observé tombe dans l'intervalle de confiance de la cellule.

**Autorisé : rien.** On enregistre l'observation, on ne touche à rien.
C'est le verdict le plus fréquent, et de loin. **Un système sain conclut au bruit dans plus de
80 % des cas examinés** ; si ce n'est pas le cas, c'est le seuil d'alerte qui est mal réglé.

### Cause 2 — Un défaut de mesure ou de données

Bug, période à données trouées, spread estimé au lieu de mesuré, résolution intra-bougie
défaillante, portage mal appliqué.

**Autorisé : correction, et recalcul complet sous une nouvelle version de mesure.**
Ce n'est **pas** un changement de stratégie. L'écart entre l'avant et l'après est publié.

*Indice diagnostique :* un défaut de mesure affecte **plusieurs cellules à la fois**, souvent
sur une même période ou une même paire. Un écart isolé sur une seule cellule n'est presque
jamais un bug.

### Cause 3 — Un changement de régime

La cellule fonctionnait, ne fonctionne plus, et la rupture est **datable**. Elle coïncide
souvent avec un changement identifiable : politique monétaire, niveau de volatilité, liquidité.

**Autorisé :** ajouter un **critère de contexte** au score — jamais modifier la définition de la
figure. Le régime devient une variable mesurée, pas une exclusion décrétée.

**Interdit :** supprimer la cellule, ou restreindre sa période d'application a posteriori.
Restreindre après coup, c'est choisir la période où ça marchait : c'est du test multiple déguisé.

### Cause 4 — Une erreur de conception

La règle capture autre chose que ce qu'on croyait. Rare, et grave.

**Autorisé : une nouvelle version de stratégie**, avec la procédure complète du §6.
L'ancienne conserve son historique et **reste publiée** : elle documente l'erreur.

---

## 5. Surveillance automatique, décision jamais automatique

> **Le système détecte tout seul. Il ne se corrige jamais tout seul.**

### 5.1 Détection de dérive

Pour chaque cellule publiée, suivi séquentiel de l'écart cumulé entre l'espérance observée hors
échantillon et l'espérance de référence :

```
S_0 = 0
S_k = max( 0 , S_{k−1} + (esperance_reference − r_net_k) − marge )
alerte  ⇔  S_k > SEUIL_DERIVE
```

`marge` et `SEUIL_DERIVE` sont calibrés sur l'historique pour produire **au plus une fausse
alerte par cellule et par an**. Une surveillance trop sensible génère du bruit administratif et
pousse à modifier ce qui n'a pas besoin de l'être.

### 5.2 Ce que déclenche une alerte

Une alerte **ouvre un dossier** dans le registre d'enseignements (§7). Elle ne modifie rien,
ne désactive rien, ne masque rien. La cellule continue d'être publiée pendant l'instruction,
**avec la mention « sous surveillance » et la date d'ouverture du dossier.**

Masquer une cellule pendant qu'on l'examine reviendrait à retirer discrètement un résultat
gênant. C'est exactement ce que le produit reproche à ses concurrents.

---

## 6. Le mode fantôme — comment on prouve qu'un changement est une amélioration

*Sans ce mécanisme, « on a amélioré le moteur » est une affirmation invérifiable.*

Toute nouvelle version de stratégie passe par quatre étapes obligatoires :

| Étape | Contenu |
|---|---|
| 1 — **Pré-enregistrement** | La modification, son motif et **le résultat attendu** sont publiés au registre d'enseignements **avant** toute observation |
| 2 — **Fantôme** | `vN+1` tourne en parallèle de `vN`, ses détections sont publiées et ancrées **mais marquées `fantome = vrai`** et non annoncées |
| 3 — **Comparaison** | Après **400 détections résolues** en mode fantôme, comparaison des deux versions **sur les mêmes périodes** |
| 4 — **Bascule ou abandon** | `vN+1` remplace `vN` uniquement si son espérance nette est supérieure **et** que l'écart sort de l'intervalle de confiance. Sinon, elle est abandonnée — **et l'abandon est publié** |

**Les versions abandonnées restent au registre.** Publier ses tentatives ratées d'amélioration
est l'exact prolongement du principe de publier ses détections ratées.

```sql
ALTER TABLE detection ADD COLUMN fantome boolean NOT NULL DEFAULT false;
ALTER TABLE detection ADD COLUMN sous_surveillance boolean NOT NULL DEFAULT false;
```

---

## 7. Le registre d'enseignements

*L'évolution du moteur est aussi transparente que ses détections. Personne ne fait cela.*

```sql
CREATE TABLE enseignement (
    id                bigserial PRIMARY KEY,
    ouvert_le         timestamptz NOT NULL,
    cellule           text        NOT NULL,
    declencheur       text        NOT NULL,   -- 'derive','revue_periodique','defaut_signale'
    observation       text        NOT NULL,
    hypothese         text        NOT NULL,   -- formulée AVANT l'examen
    cause_retenue     text,                   -- 'bruit','mesure','regime','conception'
    decision          text,                   -- 'aucune','correction_mesure','nouvelle_version'
    version_creee     text REFERENCES version_strategie(id),
    resultat_fantome  jsonb,
    clos_le           timestamptz,
    empreinte_prec    char(64) NOT NULL,
    empreinte         char(64) NOT NULL UNIQUE
);
```

**Chaîné et ancré comme le registre des détections** (`SPEC-LOT3.md`) : l'historique des
décisions d'évolution est aussi infalsifiable que celui des résultats.

Publié sur une page dédiée : chaque dossier, son hypothèse, sa cause retenue, sa décision.
**Y compris les dossiers clos sur « bruit — aucune action », qui seront les plus nombreux.**

C'est le contenu le plus rare que le produit puisse offrir : la démonstration publique qu'on
résiste à la tentation de modifier ce qui n'a pas besoin de l'être.

---

## 8. À quelle vitesse peut-on réellement apprendre

*Chiffres, pour éviter toute illusion.*

Avec un écart-type des résultats d'environ 1 R par trade :

| Question | Occurrences nécessaires |
|---|---|
| Mesurer une espérance à ± 0,10 R près | **~ 384** |
| Détecter avec fiabilité qu'une espérance de +0,10 R est tombée à zéro | **~ 780** |
| Distinguer 52 % de 50 % de réussite | ~ 2 400 |

> **Conclusion : on ne peut pas savoir qu'une stratégie s'est dégradée en moins de plusieurs
> centaines d'occurrences.** Toute « leçon » tirée plus vite est du bruit interprété.

Sur une cellule produisant 30 détections par mois, cela représente **un an d'observation**.
C'est la vitesse réelle d'apprentissage de ce type de système. La reconnaître est ce qui sépare
un instrument de mesure d'un outil qui se raconte des histoires.

**C'est aussi un argument commercial :** un concurrent qui annonce un moteur « qui s'améliore en
continu » annonce, sans le savoir, un moteur surajusté.

---

## 9. Ce qui, en revanche, apprend vite et sans risque

| Domaine | Pourquoi c'est sans risque |
|---|---|
| **L'analyse comportementale** (module E) | Chaque utilisateur est sa propre population. Aucun chiffre public n'en dépend, aucune version de stratégie n'est touchée. Elle peut s'affiner en continu |
| **Le modèle de coûts** | Améliorer l'estimation du spread ou du portage améliore la **vérité**, pas la règle. Recalcul versionné, écart publié |
| **La qualité des données** | Combler un trou, ajouter une source, affiner la résolution intra-bougie |
| **L'interface et la pédagogie** | Aucun effet sur les chiffres |

**Le produit s'améliore donc réellement et rapidement — mais sur la mesure, pas sur la règle.**
C'est la lecture juste de ta demande.

---

## 10. Ce qui reste interdit, sans exception

| Interdit | Motif |
|---|---|
| Modifier une règle après une détection perdante | Une perte isolée ne contient aucune information |
| Recalibrer les pondérations du score en continu | Surajustement garanti |
| Introduire de l'apprentissage automatique dans la détection ou le score | Non reproductible, non explicable |
| Désactiver ou masquer une cellule pendant son instruction | Retirer un résultat gênant |
| Restreindre a posteriori la période d'application d'une stratégie | Choisir la période où ça marchait : test multiple déguisé |
| Basculer sur une nouvelle version sans période fantôme | « Amélioration » invérifiable |
| Supprimer un dossier du registre d'enseignements | Même règle que pour les détections |

---

## 11. Critères d'acceptation

| # | Critère |
|---|---|
| 1 | Une détection perdante isolée ne déclenche aucun traitement automatique |
| 2 | La surveillance de dérive produit au plus une fausse alerte par cellule et par an, vérifié sur l'historique |
| 3 | Une alerte ouvre un dossier et ne modifie rien d'autre |
| 4 | Une cellule sous surveillance reste publiée, avec sa mention |
| 5 | Aucune nouvelle version ne peut être activée sans 400 détections en mode fantôme |
| 6 | Les versions abandonnées et les dossiers clos sur « bruit » sont publiés |
| 7 | Le registre d'enseignements est chaîné et ancré comme celui des détections |
| 8 | Un changement de mesure déclenche un recalcul complet et la publication de l'écart |
