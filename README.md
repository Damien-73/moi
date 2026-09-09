# Dossier de conception — application d'analyse de figures chartistes sur le forex

État au 9 septembre 2026. Branche `claude/trading-app-discussion-jzalrz`.

---

## En une phrase

Une application qui détecte les figures chartistes sur le forex, explique comment ce type de
configuration se trade habituellement, **publie chaque détection avant d'en connaître l'issue**
dans un journal infalsifiable et ancré chez des tiers, puis mesure le résultat frais déduits —
y compris les configurations qu'elle a écartées.

**Le produit n'est pas le moteur de détection**, qui existe déjà ailleurs et se copie en trois
mois. Le produit est la base de résultats vérifiables, et ce qu'elle permet de dire à un
utilisateur sur son propre comportement.

---

## Les documents

| Document | Rôle | Lignes |
|---|---|---|
| **`CAHIER-DES-CHARGES.md`** | Référence unique : produit, méthode, technique, exploitation, exécution. **À lire en premier** | ~1 270 |
| `SPEC-LOT2.md` | Détection du range et calcul du score, au niveau formule | 587 |
| `SPEC-LOT3.md` | Journal prospectif, arbre de Merkle, ancrage externe, vérificateur public | 224 |
| `SPEC-LOT5.md` | Import du journal utilisateur et écart comportemental | 228 |
| `SPEC-LOT11.md` | Mode contrainte pour les sociétés de financement | 201 |
| `SPEC-DESIGN.md` | Interface, ergonomie, système visuel, périmètre du temps réel | 285 |

**Ordre de lecture recommandé pour un novice :** le glossaire (`CAHIER-DES-CHARGES.md` §29),
puis le §1, puis le §2. Le reste se lit dans l'ordre.

**Règle de préséance :** en cas de divergence, un document d'implémentation fait foi sur les
formules, le cahier des charges fait foi sur les principes.

---

## Les onze décisions qui structurent tout

| # | Décision | Pourquoi |
|---|---|---|
| 1 | **Publier avant de savoir**, avec ancrage horaire chez trois tiers | Seule preuve qu'un concurrent ne peut pas fabriquer rétroactivement. C'est l'unique avantage durable |
| 2 | **Conserver et publier les configurations écartées** | Sans groupe témoin, impossible de prouver que le filtrage sert à quelque chose |
| 3 | **Publier des comparaisons, jamais des chiffres seuls** | Rend le produit robuste au cas où aucun avantage de marché n'existe — l'issue la plus probable |
| 4 | **Espérance nette en R** comme indicateur principal, pas le taux de réussite | 70 % de réussite à 0,3 R perd de l'argent ; 40 % à 2 R en gagne |
| 5 | **Aucune personnalisation** : jamais le capital ni le profil de risque | C'est la seule chose qui évite l'agrément de conseiller en investissement financier |
| 6 | **Déterminisme absolu**, tout recalculable, versions figées | Le produit *est* ses chiffres. Un historique qui bouge détruit tout |
| 7 | **Les prix sont en direct, la mesure ne l'est pas** | Une détection recalculée à chaque tick serait non reproductible, donc invérifiable |
| 8 | **L'analyse comportementale est le produit payant**, la base de figures est l'acquisition | Elle ne dépend d'aucun avantage de marché et croît avec les utilisateurs, pas avec le temps |
| 9 | **Deux accès seulement — individuel et groupe** ; le groupe s'administre lui-même | Sert tous les publics sans ajouter de produit ni d'heure de support |
| 10 | **Aucun contenu produit par un utilisateur** : ni figure, ni trade, ni commentaire publié | Une seule source, donc une seule vérité. Aucune modération, aucune exposition aux publications de tiers |
| 11 | **Publier les mauvais chiffres tels quels**, règle écrite avant tout revenu | Seule protection contre la tentation de les trafiquer quand l'abonnement en dépendra |

---

## Ce qui est prêt et ce qui ne l'est pas

| État | Éléments |
|---|---|
| **Spécifié, constructible** | Lots 0 à 5, lot 11, système d'interface |
| **Spécifié au niveau principe seulement** | Lots 6 à 10, 12 et 13 : notifications, abonnement, catalogue étendu, référencement programmatique, comptes groupe, API |
| **Hors compétence, à faire valider** | Validation juridique des CGU et du positionnement (avocat), structure et TVA (comptable) — `CAHIER-DES-CHARGES.md` §28 |
| **Non décidé, et ce n'est pas un oubli** | Le seuil d'annonce du score : il sera fixé **par les données**, après 400 occurrences, jamais à l'avance |

---

## Le premier pas

**Lot 0 — avant toute ligne de code :** ouvrir le compte Stripe en décrivant l'activité comme
*logiciel d'analyse statistique*, et vérifier qu'elle est acceptée. Le forex est classé
activité à risque par les processeurs de paiement, et un refus après des mois de développement
rendrait le produit invendable.

---

## L'avertissement à garder en vue

Sur les paires majeures — le marché le plus liquide et le plus arbitré du monde — **l'avantage
attendu est proche de zéro**. Le dossier est construit pour que le produit ait de la valeur
même dans ce cas : mesures comparatives, analyse comportementale, mode contrainte, et une règle
écrite d'avance qui impose de publier les mauvais résultats tels quels.

Le pari n'est pas « je trouve un avantage sur le marché ». Il est **« je suis le seul à mesurer
honnêtement, et je vends cette mesure à ceux qui achètent sur preuve »**. Le second pari peut
se gagner sans que le marché coopère.
