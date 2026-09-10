# Spécification technique — Données de référence

Comble quatre dépendances que les autres documents supposaient résolues. Chacune bloquerait
la construction, et trois d'entre elles menaçaient la reproductibilité.

> **Principe directeur, valable pour les quatre :** une donnée de référence n'est admissible
> que si **un tiers peut la reconstituer à l'identique**. Une valeur fournie par un prestataire,
> révisable et non historisée, ne l'est pas — quelle que soit sa qualité apparente.

---

## 1. Calendrier économique

`SPEC-LOT2.md` §5.1 fait de l'annonce macroéconomique un **filtre dur** sans jamais définir
« fort impact ». C'est le trou le plus grave : la moitié des rejets seraient arbitraires.

### 1.1 Pourquoi ne pas utiliser l'étiquette d'un fournisseur

Les calendriers commerciaux marquent les événements « faible / moyen / fort impact ». Cette
étiquette est **subjective, révisable après coup, et non historisée**. L'utiliser reviendrait à
filtrer une détection de 2019 avec un jugement porté en 2026 : c'est une fuite d'information
future, exactement ce que le harnais point-in-time est censé interdire.

### 1.2 Classification par liste de types, figée et versionnée

**On ne classe pas par étiquette, on classe par type d'événement.** La liste est fixe, publiée,
et son évolution crée une nouvelle version de stratégie.

| Catégorie | Événements retenus | Devises concernées |
|---|---|---|
| **Décisions de taux** | Réunions de politique monétaire des banques centrales : Fed, BCE, BoE, BoJ, BoC, RBA, RBNZ, SNB | La devise de la banque |
| **Emploi** | Emploi non agricole américain et taux de chômage américain · rapport sur l'emploi canadien · rapport sur l'emploi australien | USD, CAD, AUD |
| **Inflation** | Indice des prix à la consommation, publication mensuelle principale | Devise du pays |
| **Croissance** | Produit intérieur brut, première estimation uniquement | Devise du pays |
| **Activité** | Indices des directeurs d'achat, estimation flash uniquement | Devise du pays |
| **Discours** | Auditions et discours programmés du président de la Fed et de la présidente de la BCE | USD, EUR |

**Sont exclus** : les révisions, les publications secondaires, les indicateurs régionaux, les
annonces non programmées. Une annonce non programmée ne peut pas être filtrée à l'avance ; la
prétendre filtrée serait mentir.

### 1.3 Fenêtre de rejet

```
rejet ⇔ un événement de la liste, concernant l'une des deux devises de la paire,
        tombe dans [t_entrée − 30 minutes, t_entrée + HORIZON × durée_unité_de_temps]
```

La marge amont de 30 minutes couvre le positionnement qui précède l'annonce.

### 1.4 Sources et historisation

| Usage | Source |
|---|---|
| Historique | Calendriers publics des banques centrales et instituts statistiques — dates connues et publiées à l'avance, non révisables |
| Courant | Toute interface de calendrier économique, **filtrée par notre liste de types**, jamais par son étiquette d'impact |

Les dates retenues sont **stockées en base** au moment de leur première connaissance, avec leur
date de saisie. Le calendrier devient ainsi lui-même point-in-time.

---

## 2. Portage (swap)

`SPEC-LOT2.md` §6.4 donne la formule et la table, jamais la source des taux.

### 2.1 Pourquoi ne pas utiliser la grille d'un courtier

Les grilles de portage des courtiers sont **propres à chacun, modifiées sans préavis, et
quasiment jamais archivées**. Aucun tiers ne pourrait reconstituer un résultat calculé avec
elles. Elles sont donc inadmissibles comme donnée de référence.

### 2.2 Reconstruction à partir des taux courts publics

Le portage est, dans son principe, le différentiel de taux d'intérêt à un jour entre les deux
devises, augmenté d'une marge de courtier prélevée dans les deux sens.

```
differentiel_annuel = taux_court(devise_base) − taux_court(devise_cotation)
portage_journalier  = ( sens × differentiel_annuel − MARGE_COURTIER ) / 360 × prix
```

| Constante | Valeur | Rôle |
|---|---|---|
| `MARGE_COURTIER` | **1,0 % annuel** | Prélevée **contre le trader dans les deux sens** : elle est donc soustraite quel que soit le signe du différentiel |
| `BASE_JOURS` | 360 | Convention du marché monétaire |
| `FACTEUR_MERCREDI` | 3 | Le portage du mercredi couvre le règlement du week-end |

**Taux courts retenus** : taux à un jour publiés par les banques centrales, ou indices de
référence à un jour — séries historiques gratuites, publiques, non révisées.

### 2.3 Ce que cette approximation vaut

Elle **sous-estime** légèrement le coût réel : les courtiers de détail appliquent souvent une
marge supérieure à 1 %. C'est délibérément conservateur dans le mauvais sens, et **c'est signalé
sur chaque page portant un résultat sur unité de temps longue** :

> Portage estimé à partir des taux courts publics, marge de courtier de 1 % annuel.
> Votre courtier applique probablement davantage : votre résultat réel sera inférieur.

Conforme à la règle du `BRIEF.md` §9 : quand deux interprétations sont défendables, retenir
celle qui dégrade le chiffre publié — et quand on ne peut pas, le dire.

---

## 3. Spread et données bid/ask

`SPEC-LOT2.md` §6.1 fonde le spread sur « les données tick ». Or **tous les jeux gratuits n'en
contiennent pas**, et le sujet n'était nulle part traité.

| Source | Contenu | Utilisable pour le spread |
|---|---|---|
| **Dukascopy, tick** | Bid et ask horodatés | **Oui** — source de référence |
| HistData, M1 « ASCII » | Prix uniquement, sans bid/ask | Non |
| Flux courant d'une interface de marché | Bid et ask | Oui |

### 3.1 Deux modes, et leur conséquence sur l'affichage

| Mode | Condition | Marquage |
|---|---|---|
| **Mesuré** | Données bid/ask disponibles sur la période | Résultat normal |
| **Estimé** | Absentes : on applique la grille `spread_defaut` versionnée, par paire et par créneau horaire | **Détection marquée `spread_estime = vrai`**, et l'indication figure sur toute statistique en contenant |

```sql
ALTER TABLE detection ADD COLUMN spread_estime boolean NOT NULL DEFAULT false;
```

Les statistiques **séparent** les deux populations. Si l'écart entre elles est significatif, il
est publié : c'est en soi une mesure de la fiabilité du modèle de coûts.

### 3.2 Reconstruction du spread mesuré

Pour chaque paire et chacun des **168 créneaux horaires de la semaine** : médiane de
`(ask − bid)` sur l'ensemble des ticks du créneau, calculée une fois, versionnée, **jamais
recalculée après publication d'une détection l'ayant utilisée**.

---

## 4. Comptes et authentification

Nécessaire dès le journal personnel, **indépendamment de toute facturation** : ce sont des
données financières personnelles.

| Élément | Décision |
|---|---|
| Identifiant | Adresse de courriel, unique |
| Méthode | **Lien à usage unique envoyé par courriel** (validité 15 minutes, une seule utilisation). Aucun mot de passe |
| Motif | Pas de mot de passe stocké, pas de fuite possible, pas de réinitialisation à développer. C'est le choix le plus sûr **et** le plus simple |
| Second facteur | Proposé, par application d'authentification, obligatoire pour un rôle d'administrateur de groupe |
| Session | Cookie signé, `HttpOnly`, `Secure`, `SameSite=Lax`, 30 jours glissants |
| Fermeture | Révocation de toutes les sessions depuis l'écran de compte |
| Fournisseur externe | **Aucun.** Une dépendance d'authentification externe ajoute une pièce à maintenir et un tiers dans le parcours |

**Aucun champ de capital, de patrimoine ou de profil de risque n'existe dans le modèle de
compte** (cahier des charges §22). Cette absence est vérifiée par un test automatisé sur le
schéma : c'est l'interdit le plus facile à franchir par inadvertance.

---

## 5. Ce que ces quatre décisions ont en commun

Dans les quatre cas, la source la plus **pratique** a été écartée au profit de la plus
**reconstituable** :

| Écarté | Retenu |
|---|---|
| Étiquette d'impact d'un fournisseur | Liste de types d'événements, figée et publiée |
| Grille de portage d'un courtier | Taux courts publics et marge constante |
| Spread supposé disponible | Deux modes explicites, dont un marqué comme estimé |
| Fournisseur d'authentification externe | Lien à usage unique, sans dépendance |

C'est l'application directe du principe du `BRIEF.md` §2 : *le produit **est** ses chiffres*.
Une donnée qu'un tiers ne peut pas reconstituer rend invérifiable tout chiffre qui en dépend.
