# Spécification technique — Lots 6 à 15

Complète le cahier des charges §28. Les lots 1 à 5 et 11 ont leurs documents dédiés ;
les figures ont le leur (`SPEC-FIGURES.md`). Ce document couvre tout le reste.

---

## Lot 6 — Comptes, abonnement, obligations légales

### 6.1 Modèle de compte

```sql
CREATE TABLE organisation (
    id            bigserial PRIMARY KEY,
    nom           text NOT NULL,
    type          text NOT NULL CHECK (type IN ('individuel','groupe','gratuit')),
    sieges_payes  integer NOT NULL DEFAULT 1,
    admin_id      bigint,                    -- NULL pour un compte individuel
    stripe_client text,
    cree_le       timestamptz NOT NULL
);

CREATE TABLE utilisateur (
    id              bigserial PRIMARY KEY,
    organisation_id bigint NOT NULL REFERENCES organisation(id),
    courriel        citext NOT NULL UNIQUE,
    role            text NOT NULL CHECK (role IN ('membre','admin')),
    pays_declare    char(2) NOT NULL,        -- contrôle de juridiction, §22
    actif           boolean NOT NULL DEFAULT true,
    cree_le         timestamptz NOT NULL
);
```

**Un compte individuel est une organisation d'un siège.** Un seul chemin de code, jamais deux.

### 6.2 Administration déléguée

| Action | Qui |
|---|---|
| Inviter, retirer, réattribuer un siège | **L'administrateur du groupe, sans notre intervention** |
| Dépasser le nombre de sièges payés | Refusé, avec invitation à en ajouter |
| Retirer un membre | Le siège est libéré immédiatement, l'historique du membre conservé et inaccessible |
| Changer d'administrateur | L'administrateur en place uniquement |

**Aucun support de premier niveau sur les sièges.** C'est la condition qui rend le multi-public
tenable pour une personne seule.

### 6.3 Abonnement

- Stripe Checkout, essai de 14 jours sans prélèvement.
- **Stripe Tax activé dès le premier abonnement** : TVA au taux du pays du client, guichet
  unique européen (cahier des charges §23).
- Échec de paiement : trois relances automatiques sur 14 jours, puis rétrogradation au niveau
  public. **Aucune donnée n'est supprimée** ; le journal importé reste accessible en lecture
  et exportable.
- Résiliation en un clic, sans justification, effet en fin de période payée.

### 6.4 Contrôle de juridiction

Pays déclaré à l'inscription. **Les résidents des États-Unis sont refusés** au niveau du
formulaire, avec le motif affiché (cahier des charges §23). Le contrôle est déclaratif ; il
matérialise l'exclusion contractuelle, il ne prétend pas être infaillible.

### 6.5 Documents obligatoires

Mentions légales · CGU · CGV · politique de confidentialité · politique de cookies ·
**avertissement de risque affiché sur toute page portant une statistique**.
Le pare-feu contractuel (cahier des charges §24) est publié, ainsi que **la liste des clients
professionnels**.

### 6.6 Critères d'acceptation

Un paiement de bout en bout avec TVA correcte · un administrateur crée et retire un membre sans
notre intervention · un dépassement de sièges est refusé proprement · un résident déclaré
états-unien ne peut pas s'inscrire · l'avertissement de risque est présent sur toutes les pages
statistiques.

---

## Lot 7 — Notifications

### 7.1 Chaîne d'envoi

```
clôture de bougie → détections calculées → annonce sélectionnée
   → destinataires résolus (filtres) → file d'envoi → envoi → latence journalisée
```

**Cible : moins de 60 secondes entre la clôture et l'envoi.** Au-delà, l'annonce part
**marquée « retardée »**, et le retard est inscrit au registre public : la promesse tenue ou
non fait partie des chiffres publiés.

### 7.2 Canaux

| Canal | Version | Contrainte |
|---|---|---|
| Courriel | 1 | Service tiers avec authentification du domaine d'envoi. La délivrabilité est critique |
| Notification navigateur | 1 | Aucune dépendance externe |
| Telegram | 2 | Canal dominant du public visé |
| Webhook | 2 | Charge utile JSON identique au format du jeu de données ouvert |

### 7.3 Filtres, et ce qu'ils ne peuvent pas être

| Autorisé | Interdit |
|---|---|
| Paires, unités de temps, figures, méthodes, score minimum | **Tout filtre fondé sur le capital, le profil de risque ou l'historique personnel** |

Deux utilisateurs ayant le même filtre reçoivent **exactement** le même message.
C'est ce qui maintient l'absence de personnalisation (cahier des charges §22).

### 7.4 Anti-saturation

Plafond par défaut de 10 annonces par jour et par utilisateur, modifiable par lui.
Au-delà, regroupement en un message unique. Une application qui sature ses utilisateurs les
perd, et un plafond élevé n'est pas un service.

### 7.5 Critères d'acceptation

Latence médiane inférieure à 60 s sur 1 000 envois · une annonce retardée est marquée comme
telle en base et au registre · deux comptes au même filtre reçoivent un contenu identique au
caractère près · un filtre fondé sur le capital est rejeté par le schéma.

---

## Lot 9 — Moteur statistique

*Le cœur de ce que le produit vend. Toute erreur ici est une erreur publiée.*

### 9.1 Agrégat élémentaire

Pour un ensemble de détections résolues, avec `n` = nombre d'issues :

```
p_atteint    = nb(atteint) / n
p_invalide   = nb(invalide) / n
p_sans_issue = nb(sans_issue) / n
esperance_R  = moyenne(r_net)
ecart_type   = écart-type d'échantillon(r_net)
ic95_esp     = esperance_R ± 1,96 × ecart_type / √n
ic95_taux    = p ± 1,96 × √(p(1−p)/n)
```

**L'espérance est l'indicateur mis en avant ; le taux de réussite est secondaire.**
Les trois issues sont toujours affichées ensemble.

### 9.2 Seuils de publication

| `n` | Affichage |
|---|---|
| < 100 | **« Données insuffisantes — 37 occurrences, 100 nécessaires »**. Aucun chiffre |
| 100 à 399 | **Provisoire**, intervalle affiché |
| ≥ 400 | **Établi** |

Le seuil est appliqué **dans la couche de données**, jamais dans l'interface : un chiffre sous
le seuil ne doit pas exister côté client, même caché.

### 9.3 Correction de tests multiples

Tout classement — figures, méthodes, critères, tranches de score — applique **Benjamini-Hochberg**
sur l'ensemble des séries comparées simultanément :

```
1. Calculer la p-valeur de chaque série (test bilatéral, H0 : espérance nulle).
2. Trier par p-valeur croissante, rang i sur m séries.
3. Seuil : p(i) ≤ i/m × 0,05.
4. Ne marquer « significatif » que les séries sous le seuil.
```

**Le nombre `m` de séries testées est affiché à côté du classement.** Un lecteur doit pouvoir
juger de l'ampleur du test multiple. Personne ne fait cela.

### 9.4 Comparaisons obligatoires

> **Aucune statistique n'est servie seule par l'API.**

Toute réponse contient la valeur, son intervalle, `n`, **et au moins un terme de comparaison** :
groupe témoin de la même figure, moyenne toutes figures, ou la même figure sur une autre unité
de temps. Le schéma de réponse rend le champ `comparaison` obligatoire — la règle est ainsi
imposée par le code, pas par la discipline.

### 9.5 Critères d'acceptation

Une série de 87 occurrences ne renvoie aucun chiffre · un classement affiche le nombre de séries
testées · une réponse sans terme de comparaison est rejetée par le schéma · les intervalles sont
vérifiés contre un calcul manuel sur trois séries.

---

## Lot 10 — Fiches, référencement programmatique, outils gratuits

### 10.1 Pages générées

| Motif d'adresse | Volume |
|---|---|
| `/figures/{figure}` | ~16 |
| `/figures/{figure}/{paire}` | ~450 |
| `/figures/{figure}/{paire}/{unite}` | ~1 350 |
| `/methodes/{figure}/{methode}` | ~48 |
| `/criteres/{critere}` | 11 |
| `/paires/{paire}` | 28 |

Environ **1 900 pages en v1, plus de 5 000 après l'extension à 28 paires**, chacune répondant à
une requête réellement formulée, chacune bâtie sur des données propriétaires.

### 10.2 Règles de génération

- **Une page dont la série est sous le seuil de publication affiche « données insuffisantes »
  et n'est pas indexée** (`noindex`). Publier des milliers de pages vides détruirait la
  crédibilité du domaine entier auprès des moteurs.
- Contenu régénéré à chaque mise à jour statistique, date de mise à jour affichée.
- Données structurées `Dataset` sur chaque fiche.
- Aucun texte de remplissage. Une phrase de définition, les chiffres, les comparaisons.

### 10.3 Outils gratuits

Calculatrice de position **exécutée dans le navigateur, aucune valeur transmise ni stockée**
(cahier des charges §12.2) · valeur du pip · horloge des séances avec changement d'heure ·
matrice de corrélation calculée sur nos données · calendrier économique.

Aucun avantage de marché n'est nécessaire pour les construire, ils répondent à de forts volumes
de recherche, et ils portent l'autorité du domaine.

### 10.4 Critères d'acceptation

Une page sous le seuil renvoie `noindex` · aucune page ne contient de texte généré sans chiffres ·
la calculatrice n'émet aucune requête réseau · les pages se régénèrent automatiquement après
recalcul.

---

## Lot 12 — Ouverture des données

| Élément | Règle |
|---|---|
| Contenu | Toute détection **résolue depuis plus de 90 jours**, annoncée ou écartée, avec score détaillé, issue, coûts et empreintes |
| Formats | CSV et Parquet, plus les preuves d'ancrage et le vérificateur |
| Fréquence | Republication mensuelle, à date fixe |
| Licence | Réutilisation libre avec citation |
| Exclusion absolue | **Aucune donnée d'utilisateur, jamais**, même agrégée et anonymisée, sans consentement explicite distinct |

Un identifiant stable est attribué à chaque détection dès sa publication, pour que les citations
externes restent valides indéfiniment.

---

## Lot 13 — Accès groupe et démarche professionnelle

### 13.1 Fonctionnel

Le modèle du lot 6 suffit. **Rien à développer de plus** : ni marque blanche, ni portail dédié,
ni rapport sur mesure. Un accès groupe est un ensemble de sièges et un administrateur.

**Règle : aucun développement professionnel spéculatif.** Un rapport produit à la main pour un
premier client vaut mieux qu'une plateforme construite pour des clients qui n'existent pas.

### 13.2 Le rapport d'intelligence du risque

Produit **manuellement** pour les trois premiers clients, automatisé seulement après.
Contenu : configurations et comportements associés aux plus fortes pertes sous contrainte,
répartition des causes d'échec, comparaison entre la population du client et la base globale.

### 13.3 Prérequis avant tout démarchage

Six mois de registre prospectif · le vérificateur public en ligne · le mode contrainte
opérationnel. **Le registre public est l'argumentaire de vente** : la démarche est entrante,
fondée sur la preuve, pas sur la prospection.

---

## Lot 15 — API et extension crypto

### 15.1 API

| Point d'accès | Contenu |
|---|---|
| `GET /detections` | Filtres, pagination, format identique au jeu de données ouvert |
| `GET /detections/{id}` | Détail, score, issue, empreinte, **preuve d'inclusion Merkle** |
| `GET /statistiques` | Agrégats, **terme de comparaison obligatoire** (§9.4) |
| `GET /integrite` | Ancrages, complétude, incidents |

Authentification par jeton, quotas par niveau d'abonnement, versionnement dans l'adresse.
**La preuve d'inclusion est servie avec chaque détection** : c'est ce qui permet à un tiers de
vérifier un élément isolé sans télécharger la base.

### 15.2 Extension crypto

**Aucune ligne de moteur à écrire.** Ce qui change :

| Élément | Adaptation |
|---|---|
| Calendrier | Marché ouvert en continu : le concept de séance disparaît, le critère 7 est **neutralisé** et le score maximal ajusté |
| Portage | Financement des contrats à terme perpétuels, positif ou négatif selon le sens, appliqué toutes les 8 heures |
| Journée | Convention UTC, pas de bascule à 17:00 New York |
| Volume | **Réel et vérifiable** sur les places centralisées, contrairement au change. Il redevient donc admissible — après mesure de sa contribution marginale (cahier des charges §11.8) |
| Données | API publiques gratuites des places d'échange |

**À n'ouvrir qu'une fois le forex prouvé** (cahier des charges §31, point 8). C'est la couverture
la moins chère contre l'hypothèse « aucun avantage nulle part sur le change », et c'est aussi le
premier terrain où le volume peut entrer dans le score.
