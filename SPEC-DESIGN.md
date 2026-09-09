# Spécification d'interface, d'ergonomie et de temps réel

Complète le cahier des charges. S'applique à tous les écrans du §6 du cahier des charges.

---

## 1. Le principe directeur

> **Ici, le luxe c'est la retenue.**
> Chaque élément ajouté doit justifier sa présence. Un écran est fini quand on ne peut plus
> rien en retirer.

Ce n'est pas une préférence esthétique, c'est une conséquence du positionnement.
Le produit vend **la rigueur et la preuve**. Son apparence doit dire la même chose que son
contenu, sinon le message se contredit lui-même.

### La référence visuelle — et l'anti-référence

| On s'inspire de | On fuit |
|---|---|
| Recherche institutionnelle, presse financière de qualité, outils logiciels sobres et précis | Tableaux de bord de trading grand public |
| Blanc cassé chaud, noir profond, une seule couleur d'accent, typographie soignée, beaucoup de vide | Fonds noirs saturés de néon, dégradés, chandeliers clignotants, badges « 92 % WIN RATE » |
| Le chiffre au centre, l'ornement absent | L'ornement au centre, le chiffre noyé |

**Point stratégique :** l'esthétique « terminal de trading néon » est exactement celle des
vendeurs de signaux contre lesquels le produit se positionne. L'adopter reviendrait à se
déguiser en ce qu'on dénonce. Un utilisateur échaudé reconnaît cette apparence en une seconde
et se méfie.

---

## 2. Typographie

Deux familles, pas trois. Toutes deux libres et de qualité professionnelle.

| Usage | Police | Réglage |
|---|---|---|
| Interface, données, tableaux | **Inter** (variable) | `font-variant-numeric: tabular-nums` **obligatoire** partout où un chiffre apparaît |
| Titres éditoriaux, citations, pages publiques | **Newsreader** ou **Instrument Serif** | Uniquement pour les titres et les phrases de fond. Jamais dans un tableau |

**Les chiffres tabulaires ne sont pas un détail.** Sans eux, les colonnes de statistiques ne
s'alignent pas verticalement, les chiffres « dansent » quand une valeur se met à jour, et le
produit perd instantanément son air sérieux. C'est le premier signe qu'un professionnel repère.

### Échelle typographique

| Niveau | Taille | Usage |
|---|---|---|
| Display | 48 / 56 px | Le chiffre unique d'une page |
| Titre 1 | 32 px | Titre de page |
| Titre 2 | 22 px | Section |
| Corps | 16 px | Texte courant. **Jamais en dessous de 14 px** |
| Données | 15 px, tabulaire | Tableaux |
| Légende | 13 px | Taille d'échantillon, intervalles, notes |

Longueur de ligne : **65 à 75 caractères** maximum sur les pages de lecture.

---

## 3. Couleurs

### Base

| Rôle | Clair | Sombre |
|---|---|---|
| Fond | `#FAF9F7` (blanc cassé chaud, jamais blanc pur) | `#0E0F11` |
| Surface | `#FFFFFF` | `#17181B` |
| Texte principal | `#16181D` | `#EDEDEF` |
| Texte secondaire | `#5F6570` | `#9BA1AC` |
| Bordure | `#E6E3DE` | `#26282D` |
| Accent (interactif) | `#1F4FD8` | `#5B85F5` |

Le mode sombre est **de premier rang, pas une option** : ce public travaille la nuit.
Les deux thèmes sont conçus ensemble, jamais l'un dérivé de l'autre par inversion.

### Encodage des résultats — décision technique importante

**Le couple rouge/vert est écarté au profit de orange/bleu.**

Deux raisons :

1. **Accessibilité.** Environ 8 % des hommes présentent une déficience de perception du rouge
   et du vert. Dans un produit dont toute la valeur tient à la lecture de résultats, c'est un
   défaut fonctionnel, pas un détail de confort.
2. **Positionnement.** Le rouge et le vert sont le langage du gain immédiat. Le produit parle
   d'espérance mesurée, pas d'euphorie et de panique.

| Sens | Couleur | Usage |
|---|---|---|
| Favorable | `#1F6FEB` (bleu) | Objectif atteint, espérance supérieure à la référence |
| Défavorable | `#C2621A` (orange brûlé) | Invalidation, espérance inférieure |
| Neutre / sans issue | Gris | Ni l'un ni l'autre |

**Aucune information n'est portée par la seule couleur.** Chaque état porte aussi un libellé
ou un symbole. Contraste minimal AA (4,5:1) sur tout texte.

---

## 4. Espace et grille

- Échelle d'espacement en multiples de **4 px** : 4, 8, 12, 16, 24, 32, 48, 64, 96.
- Rayon d'angle unique : **8 px**. Jamais deux rayons différents sur un même écran.
- **Aucune ombre portée décorative.** Séparation par la bordure et par le vide.
- Largeur de contenu maximale : 1 200 px, sauf explorateur de statistiques (pleine largeur).

### Deux densités

| Mode | Où | Interligne |
|---|---|---|
| **Lecture** | Pages publiques, fiches figures, journal | Généreux, respirant |
| **Analyse** | Explorateur de statistiques, journal utilisateur | Dense, lignes de 36 px, comparaison à l'œil facilitée |

Basculer de l'un à l'autre est une décision par écran, jamais un réglage utilisateur : c'est au
produit de savoir ce que l'écran sert à faire.

---

## 5. La règle du chiffre unique

> **Chaque écran répond à une seule question, et cette réponse tient en un seul chiffre,
> immédiatement visible.**

| Écran | Le chiffre |
|---|---|
| Journal en direct | Nombre de détections annoncées aujourd'hui |
| Détail d'une détection | Le score, en pourcentage |
| Fiche figure | Espérance nette en R |
| Écart comportemental | L'écart entre l'utilisateur et la base |
| Mode contrainte | Probabilité de réussite de la contrainte |

Ce chiffre est en taille Display. **Il est toujours accompagné, en légende, de son terme de
comparaison et de sa taille d'échantillon** — application directe du principe comparatif du
cahier des charges §2.

```
        + 0,08 R
        espérance nette
        ─────────────────────────────────
        Groupe témoin : −0,21 R  ·  n = 1 840  ·  IC 95 % [+0,01 ; +0,15]
```

Jamais un chiffre nu. Jamais deux chiffres en concurrence pour l'attention.

---

## 6. Divulgation progressive

L'interface montre d'abord la réponse, puis, sur demande, le raisonnement.

| Niveau | Contenu | Déclencheur |
|---|---|---|
| 1 | Le verdict : annoncée / écartée, le score, l'issue | Immédiat |
| 2 | Le résumé : les 3 critères les plus déterminants | Toujours visible, en petit |
| 3 | Le détail complet des 11 critères, avec valeurs mesurées | Un clic sur « Voir le détail du score » |
| 4 | Les données brutes, l'empreinte, la vérification | Un clic depuis le niveau 3 |

**Le niveau 4 existe pour n'être presque jamais ouvert.** Sa seule présence est l'argument :
tout est là, vérifiable, pour qui veut regarder.

---

## 7. Le composant central : la carte de détection

```
┌──────────────────────────────────────────────────────────┐
│  EUR/USD · H4 · Double creux            ANNONCÉE   82 %  │
│                                                          │
│  ▸ graphique, 3 lignes seulement : entrée, invalidation, │
│    objectif. Aucun indicateur affiché par défaut.        │
│                                                          │
│  Entrée 1,0812   Invalidation 1,0774   Objectif 1,0869   │
│  Ratio 1,5 R · horizon 20 bougies                        │
│                                                          │
│  Tendance journalière alignée · sur niveau rond ·        │
│  divergence RSI                          Voir le détail  │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│  Publiée le 14/03 à 12:00 UTC · empreinte a3f9…  ✓ ancré │
└──────────────────────────────────────────────────────────┘
```

Règles :

- **Le graphique ne montre par défaut aucun indicateur.** Trois lignes horizontales, un
  chandelier sobre. Les indicateurs s'affichent à la demande, un par un.
- L'empreinte et la mention d'ancrage sont **toujours visibles**, en petit. C'est le rappel
  permanent de ce qui distingue le produit.
- Une carte écartée est **identique en structure**, avec le motif de rejet à la place de
  la liste de confluences, et la statistique du groupe témoin en légende.

---

## 8. Langage

*L'ergonomie commence par les mots. La moitié des utilisateurs ne connaît pas le vocabulaire.*

| Règle | Application |
|---|---|
| **Aucun jargon sans définition à la première occurrence** | Terme souligné en pointillés, définition du glossaire au survol et au toucher |
| Français simple, phrases courtes | « L'objectif a été atteint », pas « target hit » |
| **Aucun anglicisme évitable** | Invalidation, non « stop loss ». Espérance, non « expectancy » |
| Les nombres sont écrits, pas seulement affichés | « 1 840 cas mesurés », pas « n=1840 » seul |
| **Aucune formulation impérative** | « Cette configuration se trade habituellement ainsi », jamais « prenez ce trade » (cahier des charges §19) |

Un seul ton : **factuel, sobre, jamais enthousiaste.** Le produit ne se réjouit pas d'un
objectif atteint et ne s'excuse pas d'une invalidation. Il constate.

---

## 9. Mobile et bureau

| Support | Usage prioritaire | Conception |
|---|---|---|
| **Mobile** | Consulter le journal, recevoir une annonce, ouvrir une carte | **Conçu en premier.** Une colonne, carte pleine largeur, graphique 16:9 |
| **Bureau** | Explorer les statistiques, importer et analyser son journal | Tableaux denses, filtres persistants, comparaisons côte à côte |

Les tableaux ne sont **jamais** transposés tels quels sur mobile : ils deviennent des listes de
cartes. Un tableau à défilement horizontal sur téléphone est un aveu de paresse.

---

## 10. Mouvement

- Transitions de **150 à 200 ms**, courbe standard, uniquement sur changement d'état.
- **Aucune animation décorative.** Aucun compteur qui s'incrémente, aucun élément qui « respire ».
- Une valeur qui se met à jour change **sans animation de position** — d'où l'obligation de
  chiffres tabulaires (§2).
- `prefers-reduced-motion` respecté : toutes les transitions deviennent instantanées.

---

## 11. Accessibilité — exigences minimales

Contraste AA sur tout texte · navigation complète au clavier · focus toujours visible ·
libellés de formulaire explicites · aucune information portée par la seule couleur ·
zones tactiles de 44 px minimum · textes redimensionnables jusqu'à 200 % sans perte.

---

## 12. Temps réel : ce qui est en direct, et ce qui ne peut pas l'être

*Distinction essentielle. Confondre les deux détruirait la propriété qui fonde tout le produit.*

### Ce qui est en direct

| Élément | Latence visée | Moyen |
|---|---|---|
| **Prix affichés sur les graphiques** | < 1 seconde | Flux permanent sur les paires suivies |
| **Distance du prix aux niveaux d'une détection ouverte** | < 1 seconde | Calcul côté navigateur, aucun enregistrement |
| **Compte à rebours avant la clôture de la bougie** | Continu | Horloge locale |
| **Aperçu provisoire des conditions** avant clôture | Continu | Affiché en gris, avec la mention **« provisoire — non enregistré »** |
| **Envoi de l'annonce après clôture** | **< 60 secondes** | Cahier des charges §5, module G |
| Issue d'une détection résolue | < 60 s après le franchissement | Suivi en M1 |

### Ce qui n'est pas — et ne sera jamais — recalculé en direct

**La détection elle-même.** Une figure n'est constituée qu'à la **clôture** d'une bougie.
Trois raisons, la troisième étant rédhibitoire :

1. **Par définition.** Toutes les règles de la spécification technique portent sur des
   clôtures. Une figure « en cours de formation » n'est pas une figure : c'est une hypothèse
   qui peut disparaître à la bougie suivante.
2. **Par honnêteté.** Une détection qui apparaît puis disparaît en cours de bougie produirait
   des alertes contradictoires — exactement le comportement des outils que le produit dénonce.
3. **Par nécessité méthodologique.** Une détection intra-bougie donne un résultat différent à
   chaque tick reçu. Elle serait donc **non reproductible** : deux personnes recalculant
   l'historique obtiendraient deux résultats. **Cela détruirait le déterminisme, donc la chaîne
   d'empreintes, donc la preuve, donc le produit.**

> **Formulation à retenir : les prix sont en direct, la mesure ne l'est pas.
> C'est ce qui rend la mesure vérifiable.**

L'aperçu provisoire donne à l'utilisateur toute la sensation du direct — il voit la
configuration se former et le compte à rebours défiler — sans qu'aucune de ces valeurs
provisoires n'entre dans le journal. Rien n'est enregistré avant la clôture.

### Conséquence technique

| Couche | Nature | Coût |
|---|---|---|
| Affichage des prix | Flux continu vers le navigateur, sans stockage | Faible : 7 à 28 symboles |
| Détection, score, résolution | **Traitement par lots à chaque clôture** | Précalculé une fois pour tous les utilisateurs |

Le flux de prix ne touche **jamais** la base de détections. Ce sont deux systèmes séparés, et
cette séparation est une exigence d'architecture, pas une commodité.
