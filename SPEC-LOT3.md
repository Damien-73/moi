# Spécification technique — Lot 3 : journal prospectif, chaînage et ancrage

Document d'implémentation. Complète le cahier des charges §15.

> **Ce lot porte l'unique avantage concurrentiel durable du produit.** Une erreur ici ne
> dégrade pas une fonctionnalité : elle annule la valeur de tout ce qui est accumulé depuis
> le premier jour. C'est le lot où la rigueur prime sur la vitesse.

---

## 1. Ce qu'il faut prouver, et à qui

| Affirmation | Preuve exigée |
|---|---|
| « Cette détection a été publiée avant de connaître son issue » | Un horodatage **produit par un tiers**, antérieur à la résolution |
| « Nous n'avons rien retiré » | Chaque enregistrement est lié aux autres ; retirer l'un casse la vérification de tous les suivants |
| « Nous n'avons rien modifié » | Le recalcul par un tiers redonne exactement les mêmes empreintes |
| « Nous ne publions pas que nos réussites » | Les configurations écartées sont **dans la même chaîne** que les annoncées |

**Le destinataire de la preuve n'est pas l'utilisateur moyen** — il ne vérifiera jamais.
C'est le sceptique compétent : le journaliste, le concurrent, le partenaire B2B qui fait sa
diligence. Il suffit qu'**un seul** vérifie publiquement pour que l'argument devienne acquis.

---

## 2. La faille à refermer

Le chaînage par empreinte, seul, ne prouve rien : l'éditeur peut recalculer toute la chaîne.
Ce qui vaut preuve, c'est **l'ancrage chez un tiers**. D'où la question qui décide de tout :

> **Quelle est la durée pendant laquelle une détection existe sans être ancrée ?**
> Pendant cette fenêtre, elle peut être supprimée sans laisser de trace.

### Règle de dimensionnement

> **La fenêtre d'ancrage doit être strictement inférieure au délai minimal de résolution
> d'une détection.**

Si aucune détection ne peut se résoudre avant d'avoir été ancrée, la suppression opportuniste
devient impossible : au moment où l'éditeur apprend le résultat, l'engagement est déjà public.

| Unité de temps | Horizon | Délai minimal de résolution | Fenêtre d'ancrage exigée |
|---|---|---|---|
| H1 | 20 bougies | ≥ 1 heure | **≤ 1 heure** |
| H4 | 20 bougies | ≥ 4 heures | ≤ 1 heure |
| D1 | 20 bougies | ≥ 1 jour | ≤ 1 heure |

**Décision : ancrage à chaque cycle de traitement, soit toutes les heures.** L'ancrage
quotidien du cahier des charges v1 était insuffisant — il laissait une fenêtre de 24 heures
pendant laquelle une détection H1 pouvait naître, se résoudre et disparaître.

---

## 3. Structure : arbre de Merkle par cycle, chaîne de racines

Une chaîne linéaire pure oblige à détenir tous les enregistrements pour vérifier l'un d'eux.
Un arbre de Merkle permet de prouver l'inclusion d'**une seule** détection avec une poignée
d'empreintes.

```
Cycle horaire n :
    feuilles  = empreintes des détections du cycle, triées par (entree_ts, instrument, version)
    racine_n  = racine de Merkle des feuilles
    tete_n    = SHA256( tete_{n−1} ‖ racine_n ‖ n ‖ horodatage_cycle ‖ nb_feuilles )

Ancré à l'extérieur : tete_n
```

### Conséquences

| Propriété | Effet |
|---|---|
| Preuve d'inclusion compacte | Prouver qu'une détection est dans le cycle demande `log₂(n)` empreintes, pas la base entière |
| Chaînage des têtes | Retirer un cycle entier casse tous les suivants |
| Cycle vide | **Ancré quand même**, avec `nb_feuilles = 0`. Un cycle manquant serait indistinguable d'un cycle supprimé |

---

## 4. Sérialisation canonique — la condition de reproductibilité

*Deux implémentations doivent produire la même empreinte pour la même détection. Sans règle
de sérialisation stricte, c'est faux, et toute la vérification s'effondre.*

| Règle | Valeur |
|---|---|
| Encodage | UTF-8, sans marque d'ordre d'octets |
| Structure | Champs concaténés dans l'ordre fixé, séparateur `\x1f` (séparateur d'unité) |
| Horodatages | ISO 8601 en UTC, à la seconde, suffixe `Z` — `2026-03-14T12:00:00Z` |
| Nombres décimaux | Notation décimale simple, point décimal, **sans zéros de queue**, sans notation exponentielle. `1.0812`, jamais `1.08120` ni `1.0812e0` |
| Entiers | Sans signe superflu, sans zéros de tête |
| Valeur absente | Chaîne vide, jamais `null` ni `None` |
| Booléens | `true` / `false` en minuscules |
| Fonction d'empreinte | SHA-256, sortie en hexadécimal minuscule |

**Ordre des champs d'une feuille de détection** — figé, toute modification crée une nouvelle
version de format :

```
version_strategie · instrument · unite_temps · sens · entree_ts · prix_entree ·
invalidation · objectif_methode · objectif_1r5 · objectif_2r · horizon_barreaux ·
score_points · score_max · statut · motif_rejet
```

**Un jeu de vecteurs de test est publié** : 20 détections fictives avec leur empreinte
attendue. Toute implémentation tierce doit les reproduire avant d'être considérée valide.

---

## 5. Ancrage externe — trois supports indépendants

Un seul support est un point de défaillance unique, et un support contrôlable par l'éditeur
n'est pas une preuve.

| # | Support | Ce qu'il apporte | Coût |
|---|---|---|---|
| 1 | **Dépôt public versionné**, un commit signé par cycle contenant `tete_n`, `racine_n`, `n`, le nombre de feuilles | Lisible par tous, sans outil. L'historique est public et hébergé par un tiers | 0 € |
| 2 | **Horodatage RFC 3161** auprès d'une autorité d'horodatage | Jeton cryptographique signé par un tiers indépendant, opposable | 0 à quelques euros/mois |
| 3 | **OpenTimestamps** (ancrage dans une chaîne de blocs publique) | Preuve d'antériorité qui ne dépend d'aucune organisation, vérifiable dans vingt ans | ≈ 0 € |

Les trois preuves sont stockées dans `ancrage.preuve_externe` et **republiées sur la page
publique d'intégrité**. Un ancrage qui échoue déclenche une alerte immédiate (cahier des
charges §16).

### Règle de transparence sur les défaillances

Si un cycle n'a pas pu être ancré, **le trou reste visible définitivement**. Il n'est jamais
comblé rétroactivement : un ancrage produit après coup porterait un horodatage postérieur et
prouverait le contraire de ce qu'il prétend. L'incident est décrit sur la page d'intégrité.

**Publier ses propres défaillances est cohérent avec le positionnement. Les masquer
détruirait le produit.**

---

## 6. Séquence d'un cycle

```
1. Clôture de bougie détectée (fin du cycle horaire)
2. Vérification de complétude des données          → sinon : cycle marqué incomplet, poursuivi
3. Calcul des détections (annoncées ET écartées)
4. Sérialisation canonique, empreinte de chaque feuille
5. Tri déterministe des feuilles
6. Construction de l'arbre de Merkle → racine_n
7. Calcul de tete_n depuis tete_{n−1}
8. Écriture en base, dans UNE transaction unique
9. Publication des ancrages 1, 2, 3
10. Publication publique des détections annoncées
11. Envoi des notifications                        → cible : < 60 s depuis l'étape 1
```

**Les étapes 8 et 9 ne sont pas réversibles.** Aucune procédure d'administration ne permet de
supprimer une détection publiée. Une erreur se corrige par une **détection d'annulation**
ajoutée à la suite, jamais par une suppression — le journal est un registre comptable, pas un
document révisable.

### Mesures publiées à chaque cycle

`délai clôture → écriture` · `délai écriture → ancrage` · `nombre de feuilles` ·
`complétude des données`. Ces quatre valeurs constituent la preuve continue que la machine
tourne comme annoncé.

---

## 7. Le vérificateur public

Un programme autonome, **publié, documenté et versionné**, qui ne dépend d'aucun service de
l'éditeur autre que le jeu de données public.

```
verifier --du 2026-01-01 --au 2026-06-30

  ✓ 4 344 cycles trouvés, 0 manquant
  ✓ 61 208 détections, dont 7 842 annoncées et 53 366 écartées
  ✓ Empreintes de feuilles recalculées : 61 208 / 61 208 conformes
  ✓ Racines de Merkle recalculées : 4 344 / 4 344 conformes
  ✓ Chaîne des têtes continue, aucune rupture
  ✓ Ancrages : 4 344 commits signés · 4 344 jetons RFC 3161 · 4 344 preuves OpenTimestamps
  ✓ Antériorité : aucune résolution antérieure à son ancrage
  ✓ Issues recalculées depuis les données M1 : 61 208 / 61 208 conformes
```

La dernière ligne est la plus importante : **le vérificateur ne se contente pas de contrôler
les empreintes, il recalcule les issues** depuis les données de marché publiques. Il vérifie
donc le contenu, pas seulement l'intégrité.

### L'invitation

Une page publique invite explicitement à contester : commande à exécuter, jeu de données à
télécharger, adresse pour signaler une divergence, et engagement écrit de publier toute
divergence confirmée avec son explication.

Sur un marché saturé de résultats fabriqués, c'est l'argument le plus difficile à ignorer,
et il coûte une page de documentation.

---

## 8. Jeu de données ouvert

| Élément | Règle |
|---|---|
| Contenu | Toute détection **résolue depuis plus de 90 jours**, annoncée ou écartée, avec score détaillé, issue, coûts et empreintes |
| Formats | CSV et Parquet, plus les preuves d'ancrage |
| Fréquence | Republication mensuelle, à date fixe |
| Licence | Réutilisation libre avec citation de la source |
| Exclusion | Aucune donnée d'utilisateur, jamais |

*Pourquoi c'est un gain net :* la valeur commerciale est dans le flux courant et dans
l'analyse, pas dans des lignes vieilles de trois mois. En les ouvrant, on devient la source
que les autres citent — et chaque citation est un lien, une autorité, et une preuve
supplémentaire qu'il n'y a rien à cacher.

---

## 9. Critères d'acceptation

| # | Critère |
|---|---|
| 1 | Un cycle est ancré sur les trois supports en moins de 5 minutes après la clôture |
| 2 | Aucune détection ne peut se résoudre avant son ancrage — vérifié par un test automatisé sur l'historique complet |
| 3 | Les cycles vides sont ancrés comme les autres |
| 4 | Le vérificateur, exécuté sur une machine vierge sans accès à la base, valide l'intégralité de l'historique |
| 5 | Les 20 vecteurs de test de sérialisation sont reproduits par une implémentation indépendante |
| 6 | Aucune commande d'administration ne permet de supprimer une détection publiée |
| 7 | Un cycle manquant apparaît sur la page d'intégrité et n'est jamais comblé rétroactivement |
