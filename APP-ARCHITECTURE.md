# Architecture et vision — application de détection forex

Comment je construirais cette application si l'objectif est un produit défendable à l'échelle
mondiale, et pas un service de signaux de plus.

---

## 1. Ce qui rend l'app unique — et pourquoi c'est copiable ou non

Trois avantages, classés par solidité.

| Avantage | Copiable en combien de temps ? |
|---|---|
| **Historique prospectif horodaté** — chaque détection publiée avant son issue, chaînée par hachage | **Impossible à rattraper.** Un backtest se refait en une nuit ; deux ans de détections publiées à l'avance ne se fabriquent pas. C'est le seul actif dont la valeur augmente mécaniquement avec le temps. |
| **Écart comportemental (journal utilisateur × base statistique)** | 12-18 mois, et seulement après avoir accumulé la base. Crée un coût de sortie : l'utilisateur perd son historique s'il part. |
| **Moteur de détection** | 3 mois. Aucune valeur défensive. Ne jamais construire l'argumentaire dessus. |

Le produit n'est donc **pas** le moteur. Le produit est **la base de résultats** et ce qu'elle
permet de dire à un utilisateur sur lui-même.

### L'angle stratégique : l'honnêteté comme fossé

Le marché des outils forex de détail est bâti sur des promesses invérifiables.
Un produit dont le mécanisme central est *« nous publions nos échecs »* est structurellement
inimitable par les acteurs en place : ils ne peuvent pas basculer vers la transparence
sans détruire les chiffres qu'ils affichent déjà.

Conséquence sur le positionnement, à assumer : **la cible n'est pas celui qui cherche des signaux,
c'est celui qui s'est déjà fait avoir par des signaux.** C'est un segment réel, atteignable
uniquement en organique — ce qui tombe bien, puisque la loi Sapin 2 ferme de toute façon
la publicité payante en France.

### Pourquoi l'échelle mondiale est crédible ici

Contrairement à un commerce physique ou à une prestation de service, ce produit n'a
**aucun ancrage géographique** : le forex est le même marché partout, les données sont universelles,
et l'internationalisation se réduit à traduire l'interface. Les 7 paires majeures intéressent
autant un utilisateur brésilien qu'un français.

### Le plafond honnête

Mention réglementaire obligatoire des courtiers : **70 à 85 % des comptes de particuliers
perdent de l'argent** sur les CFD. Ce public paie peu, part vite, et sa taille est contrainte
par la réglementation européenne depuis les limites de levier ESMA de 2018.

**Le segment qui paie réellement est ailleurs : les candidats aux sociétés de financement
(*prop firms*).** Ils paient déjà 100 à 600 $ par tentative, souvent plusieurs fois, et ont un
objectif chiffré et mesurable : atteindre l'objectif de gain sans franchir la perte maximale
journalière. C'est exactement ce que la base de données peut mesurer et que personne ne mesure.
Voir le module F.

---

## 2. Les modules

### A — Ingestion et stockage
Bougies M1 en source de vérité, agrégées en H1, H4, D1. Spread réel reconstruit depuis les
données tick, **variable selon l'heure** (à l'heure du roulement, il peut être plusieurs fois
supérieur à la normale — c'est un facteur que personne ne modélise et qui fausse tous les
résultats de nuit).

### B — Moteur de détection
Chaque stratégie est un module indépendant respectant un contrat unique :

```
detect(bougies_jusqu_a_t, params) -> [ { sens, entrée, invalidation, objectif, horizon } ]
```

Interdit d'accéder à une bougie postérieure à `t`. Aucun apprentissage automatique en v1.

### C — Résolution et journal prospectif
Chaque détection devient un trade virtuel, publié **avant** son issue, chaîné par hachage,
puis résolu automatiquement en données M1 (pour savoir qui de l'objectif ou de l'invalidation
a été touché en premier). Résultat stocké brut **et** net de spread.

### D — Base de résultats interrogeable
C'est le cœur vendable. « Le range en D1 sur GBP/USD, à quelle heure, avec quel écart-type,
quelle espérance nette ? » — des dizaines de milliers de trades documentés, filtrables.

### E — Journal de l'utilisateur
Import par rapport MT4/MT5 ou CSV. Aucune connexion au courtier n'est nécessaire en v1.
Puis **l'écart comportemental** : ce que l'utilisateur a fait, comparé à ce que la base dit
de la même configuration.

### F — Mode contrainte (*prop firm*)
Rejoue la base sous contrainte de perte maximale journalière et globale.
Répond à la seule question que ce public se pose : *« cette approche survit-elle à une limite
de perte de 5 % par jour ? »* Une stratégie à espérance positive peut échouer à 90 % sous
contrainte de drawdown — et aucun outil actuel ne le dit.

---

## 3. Décision produit qui change tout : afficher l'espérance, pas le taux de réussite

Un taux de réussite de 70 % avec un objectif à 0,3 R **perd** de l'argent.
Un taux de 40 % avec un objectif à 2 R en gagne.

L'indicateur mis en avant partout dans l'interface doit être **l'espérance en R, nette de frais**.
Le taux de réussite est affiché en second, parce que c'est ce que les gens cherchent —
mais jamais en titre. C'est le point qui sépare un outil sérieux d'un produit marketing.

---

## 4. Fiabilité : les six règles non négociables

Le produit **est** ses chiffres. Une seule erreur méthodologique invalide tout.

1. **Point-in-time strict.** La fonction de détection ne reçoit qu'une tranche en lecture seule
   des bougies jusqu'à `t`. Un test automatisé injecte des données futures et vérifie que le
   résultat ne change pas. C'est le test le plus important du projet.
2. **Test de déterminisme en intégration continue.** Chaque nuit, recalcul complet de l'historique
   et comparaison des empreintes avec les détections stockées. Toute divergence fait échouer la
   compilation et impose la création d'une nouvelle version de stratégie. Coût de mise en place :
   une journée. Sans ça, l'historique se réécrit silencieusement à chaque correction de bug.
3. **Versionnement des stratégies.** Une stratégie modifiée est une stratégie nouvelle.
   L'ancienne conserve son historique publié. On ne supprime jamais, on remplace.
4. **Résolution intra-bougie en M1** obligatoire. C'est l'erreur qui gonfle artificiellement
   tous les taux de réussite amateurs.
5. **Frais réels** : spread horaire modélisé depuis les données tick, pas une constante.
6. **Pré-enregistrement.** Toute nouvelle stratégie est déclarée et publiée **avant** d'être
   observée. Interdiction de publier le résultat d'une stratégie qu'on a d'abord testée.
   C'est la protection contre le test multiple — et contre soi-même.

---

## 5. Performance : ce n'est pas le sujet

Volume total : 7 paires × 3 unités de temps × 20 ans ≈ **1,1 million de bougies**.
Cela tient en mémoire vive. Une passe de détection complète sur tout l'historique se compte
en secondes ou en minutes.

**Le calcul est identique pour tous les utilisateurs** : on précalcule une fois à chaque clôture
de bougie, on sert depuis le cache. Le coût marginal par abonné est proche de zéro — seul le
journal personnel est calculé par utilisateur, et il est minuscule.

Le seul moyen de créer un problème de performance est de traiter le flux tick en temps réel.
Ne pas le faire.

---

## 6. Pile technique

Choisie pour un développeur seul assisté par IA : peu de pièces, un seul langage, tout
reproductible.

| Couche | Choix | Motif |
|---|---|---|
| Traitement et API | Python (Polars, FastAPI) | Un seul langage, une seule surface de débogage |
| Base | PostgreSQL + TimescaleDB | Une seule base. Ni Kafka, ni Redis, ni microservices |
| Graphiques | TradingView Lightweight Charts | Gratuit, libre, conçu exactement pour ça. **Ne jamais coder son propre moteur graphique** |
| Interface | SvelteKit ou Next.js | Indifférent. Ne pas y passer de temps en v1 |
| Hébergement | Un VPS (Hetzner, ~15-40 €/mois), Docker Compose, Caddy | Kubernetes serait une erreur à ce stade |
| Paiement | Stripe (essai puis abonnement natif) | Voir le risque ci-dessous |

**Risque à vérifier tôt, avant d'écrire du code :** les processeurs de paiement classent souvent
les produits liés au forex en activité à risque. Un refus de Stripe bloque toute la monétisation.
Ouvrir le compte et décrire l'activité comme **logiciel d'analyse statistique** dès le début,
et obtenir la validation avant d'investir des mois de développement.

---

## 7. Ordre de construction

L'ordre compte plus que le contenu : chaque étape doit produire quelque chose de vérifiable.

| # | Étape | Pourquoi à cette place |
|---|---|---|
| 1 | Ingestion, stockage, **harnais de déterminisme** | Avant toute stratégie. Construire les garde-fous d'abord, jamais après |
| 2 | **Une seule stratégie : le range**, de bout en bout, résolution comprise | Voir ci-dessous |
| 3 | **Page publique du journal prospectif, gratuite, sans compte** | C'est l'outil marketing, pas une fonctionnalité. Elle doit tourner et accumuler pendant qu'on développe le reste |
| 4 | Interface stratégie + 5 stratégies supplémentaires | Une fois le contrat validé sur un cas réel |
| 5 | Import du journal utilisateur + écart comportemental | Le moment où l'abonnement devient justifiable |
| 6 | Mode contrainte *prop firm* | Le déblocage de la valeur : un public qui paie déjà |
| 7 | API et licence de la base | Revenu B2B : sociétés de financement et courtiers |

**Pourquoi commencer par le range et non par l'épaule-tête-épaule :** le range se définit
objectivement (bornes, nombre de touches, durée), il est **fréquent** — donc il donne une
puissance statistique exploitable en quelques mois au lieu de plusieurs années — et les paires
majeures passent la majorité de leur temps en range. L'épaule-tête-épaule est subjective et rare :
c'est le pire premier cas possible.

---

## 8. Ce qui tuera le projet si on l'ignore

1. **Publier un chiffre qu'on ne peut pas reproduire.** Un utilisateur recalculera. Un seul écart
   non explicable détruit l'unique argument du produit.
2. **Céder à la tentation d'embellir** le jour où l'abonnement en dépend. Écrire maintenant,
   avant tout revenu, ce qui sera publié si les chiffres sont mauvais.
3. **Élargir avant d'avoir prouvé.** Vingt stratégies médiocres valent moins qu'une seule
   documentée sur trois ans.
4. **Le refus du processeur de paiement.** À tester en premier, pas en dernier.
