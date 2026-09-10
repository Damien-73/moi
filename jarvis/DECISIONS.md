# JARVIS — Décisions produit

Journal des arbitrages pris en conversation. Une ligne = une décision tranchée.
Mise à jour : 2026-09-10.

---

## D1 — Le produit est un journal, pas une conversation

**Décidé.** Le client raconte sa journée par tranches (matin / midi / soir),
plus un point hebdomadaire et une synthèse mensuelle.
C'est par là que les données réelles entrent dans le système.

Sans ce flux, il n'y a pas de produit : juste un chatbot avec de la mémoire.

**Origine :** correction apportée par Damien à l'objection « l'IA ne voit rien de ta vie ».
L'objection était fausse, la correction est retenue.

---

## D2 — C'est l'IA qui demande, jamais le client qui rédige

**Décidé.** Interdit : une page blanche « raconte-moi ta journée ».
Retenu : 4 questions courtes, choisies parce que le système ne connaît pas encore la réponse.

**Règle associée — l'effort doit décroître :**

| Moment | Nombre de questions |
|---|---|
| Semaine 1 | ~10 (le système ne sait rien) |
| Mois 3 | ~2 (il a déjà compris le reste) |

Si l'effort demandé reste constant, tout le monde part. C'est le point de conception
qui décide de la survie du produit.

---

## D3 — Le vocal est prioritaire, pas optionnel

**Décidé.** Personne n'écrit trois paragraphes par jour ; tout le monde peut parler 90 secondes.

**Règle :** l'app ne renvoie jamais la transcription. Elle renvoie **5 lignes structurées**
de ce qu'elle a retenu. C'est ce qui prouve qu'elle a écouté.

---

## D4 — Un seul domaine en profondeur au lancement

**Décidé.** Le journal est universel (il marche pour perdre du poids, dégager du temps,
écrire un business plan). Le **conseil** ne l'est pas : chaque domaine demande des
connaissances différentes.

Six domaines au lancement = superficiel partout = les « trucs bateaux » qu'on refuse.

Journal ouvert à tous dès le départ. Profondeur réelle sur **un seul domaine**,
les autres ajoutés un par un.

---

## D5 — La rétention est le produit, pas une conséquence

**Décidé, contre l'avis initial de Damien.** Dans un abonnement, un client qui n'utilise
plus l'app résilie sous 2 mois. Si 80 % abandonnent le rituel au mois 1, l'entreprise
passe son temps à remplacer ses clients.

La question centrale n'est pas « l'app est-elle bonne » mais **« les gens tiennent-ils le rituel »**.

---

## D6 — Notifications : conséquence, jamais reproche

**Décidé.** Interdit : « bouge-toi ». Marche 3 jours, puis désinstallation.

Retenu : *« Je n'ai rien de toi depuis 4 jours. Mon analyse de ta semaine sera fausse. »*

Le mode dur ne s'active que si le client l'a explicitement demandé.

---

## D7 — Les cinq fonctions retenues, par ordre de construction

| # | Fonction | Rôle |
|---|---|---|
| 1 | **Rapport mensuel « ton mois vu de l'extérieur »** | *« Tu as parlé de ton travail 23 fois, 19 fois négativement. Tes 4 meilleures journées avaient toutes du sport le matin. »* C'est du comptage, pas de l'IA. C'est ce qui justifie l'abonnement à lui seul. |
| 2 | **Corrélations personnelles** | *« Les semaines où tu dors moins de 6 h, tu abandonnes tes plans 3 fois plus. »* Produit de la durée, introuvable ailleurs. |
| 3 | **Bouton « pas envie aujourd'hui »** | L'absence devient une donnée au lieu d'une culpabilité. Supprime la honte, première cause d'abandon des journaux. |
| 4 | **« Toi il y a X mois »** | Meilleur verrou anti-résiliation : n'existe que si on est resté. |
| 5 | **Score de fiabilité affiché** | *« Mes 20 dernières estimations : 12 justes, 8 fausses. Je suis trop optimiste sur tes délais. »* Rend l'app croyable quand elle dit quelque chose de dur. |

**Ordre de construction retenu :** vocal (D3) et rapport mensuel (n°1) avant tout le reste.
Le premier rend le rituel tenable, le second le rend payant.

---

## D8 — Les rétrospectives se déclenchent sur le contraste, pas sur le calendrier

**Décidé.** Une rétrospective à date fixe devient du papier peint en trois passages.

Déclencheurs retenus : un fait s'est inversé, une peur a disparu des conversations,
une prédiction s'est révélée fausse dans le bon sens.

**Garde-fou :** l'app ne montre jamais un passé qui rend le présent humiliant,
sauf si elle en nomme aussi la cause. *« Tu allais mieux en mars. Depuis tu dors moins
et tu as arrêté le sport. C'est peut-être ça, pas toi. »*

---

## D9 — Mois 1 : la synthèse, présentée comme un brouillon

**Décidé.** Au mois 1, le système ne montre pas l'évolution (il n'y en a pas encore)
mais **l'accumulation** : *« en 30 jours je sais 47 choses de toi, voici les 5 plus importantes »*.
Le mois 1 est le moment où les gens abandonnent : c'est là qu'il faut leur montrer
ce qu'ils perdraient en partant.

**Formulation obligatoire :**

> « Voici ce que je crois avoir compris de toi après un mois. Dis-moi ce que j'ai faux. »

Jamais un verdict. Un brouillon à corriger.

**Pourquoi la validation compte plus qu'elle n'en a l'air :** une correction vaut dix
déclarations. *« Non, ce n'est pas la sécurité que je cherche, c'est de ne plus avoir
de compte à rendre »* est l'information la plus précieuse du produit, et aucune question
ne l'aurait sortie.

---

## D10 — L'électrochoc, c'est le mois 3

**Décidé.** À 30 jours le système peut encore se tromper. Une IA qui frappe fort
avec 20 % d'erreurs perd son client.

| Moment | Effet visé |
|---|---|
| Mois 1 | « Il m'a vraiment compris » — précision, pas dureté |
| Mois 3+ | Confrontation — l'app a eu raison deux ou trois fois, elle l'a gagnée |

---

## D11 — Données émotionnelles = contrainte juridique dès le départ

**Constaté, non négociable.** Collecter les peurs, le mal-être au travail, l'état d'esprit
fait entrer le produit dans les **données de santé**, la catégorie la plus protégée en Europe.

Conséquences à intégrer dès la conception, pas après :
- consentement explicite et séparé pour ces données ;
- protocole obligatoire quand quelqu'un écrit qu'il va très mal ;
- liste fermée de ce qui ne peut jamais être inféré (diagnostic, pathologie).

Rattraper cela après le lancement coûte très cher.

---

## Points encore ouverts

| # | Question | Décision requise |
|---|---|---|
| O1 | Quel domaine unique au lancement ? | Damien |
| O2 | Prix de l'abonnement (coût réel : 15-60 €/mois pour un client très actif) | Damien |
| O3 | Associé technique : quand le chercher ? | Damien |
| O4 | Calendrier de construction | Damien |

---

# Mise à jour — produit reprécisé par Damien

## D12 — Le produit : un assistant personnel pour particuliers, tous objectifs

**Décidé, contre ma recommandation initiale d'un domaine unique.**

L'app sert n'importe quel objectif : vie privée, quotidien, carrière, investissement,
projets. Y compris les gens qui n'ont **aucun objectif** — l'app les aide à le trouver.

**Pourquoi ça tient malgré tout :** l'avantage ne vient pas de la connaissance du domaine,
il vient de la connaissance de la personne. Sur l'immobilier, ChatGPT donne le même plan
à tout le monde ; l'app sait que le client épargne réellement 300 € et pas les 600 annoncés,
qu'il a lâché deux projets quand ça s'est compliqué, et qu'il veut pouvoir bouger.

**Réserve maintenue :** la personnalisation est universelle, **les faits ne le sont pas**
(voir D14).

---

## D13 — Ordre de construction : C, A, puis B, puis D

| Bloc | Contenu | Rang |
|---|---|---|
| A | L'assistant qui comprend (modèle de la personne) | 2 |
| C | Les connexions (agenda d'abord, puis mails) | **1** |
| B | Les agents qui exécutent | 3 |
| D | La couche ludique / visuelle (Sims) | 4 |

**L'agenda en premier** parce qu'il règle l'erreur du journal-corvée : c'est une donnée
que le client n'a pas à taper, elle donne de la valeur dès le premier jour, et elle
alimente le modèle en continu et gratuitement.

Le journal ne disparaît pas : il devient 2-3 questions glissées **dans** l'aide du jour.

Les agents (B) restent en mode « je prépare, tu valides » longtemps. Un agent qui se
plante dans la vie privée de quelqu'un coûte un client définitivement.

---

## D14 — L'IA ne calcule jamais

**Règle absolue.** Un modèle de langage devine l'arithmétique, il ne la fait pas.

L'IA choisit la formule et les paramètres. **Du code testé exécute le calcul.**
Capacité d'emprunt, mensualités, rendement, plus-value, projections : tout passe
par du code, jamais par le modèle.

Sans cette règle, l'app produit des plans financiers faux avec assurance.

---

## D15 — Ligne rouge investissement et santé

**L'app informe, simule et structure. Elle ne recommande jamais un produit précis.**

| Autorisé | Interdit |
|---|---|
| Types de placements, avantages, inconvénients, horizons, risques | « Achète ce bien », « achète cette action » |
| « Voici les options, voici ce que chacune donne dans ta situation » | « À ta place, je ferais ça » (sur de l'argent) |

Le conseil en investissement est un métier réglementé en France (statut CIF,
immatriculation). À faire valider par un juriste **avant** de coder cette partie.

Même logique pour tout ce qui touche la santé.

---

## D16 — Ce que vend l'abonnement : la continuité

**Constat central.** Aucune action isolée de l'app ne vaut 19 €/mois — ChatGPT fait
gratuitement le plan, l'analyse et le conseil ponctuels. Ce qui les vaut, c'est ce que
l'app fait sur 200 jours.

Les quatre choses qui n'existent nulle part, et qui ont toutes la même cause :

1. Se souvenir du plan de mars et en reparler en septembre.
2. Un chiffre qui bouge seul : *« ton objectif passe de 40 à 47 ans »*.
3. Une vue sur **tous** les objectifs à la fois, y compris quand ils se contredisent.
4. Un système qui a un avis sur la personne et qui a déjà eu raison.

**Elles n'existent que si le client est resté.**

### Deux conséquences

- **Le seul indicateur qui compte est le taux de résiliation.** Ni les inscriptions,
  ni l'usage.
- **Le mois 1 est le mois le plus faible** (l'app ne sait rien). Donc dès le jour 1,
  montrer un exemple concret de ce qu'elle pourra dire dans 3 mois. On vend l'avenir
  pendant que le présent se construit.

---

## D17 — Le plan long qui se recalcule

Horizon tenu par l'app, recalculé quand la réalité bouge, à des rythmes différents :

| Horizon | Fréquence de recalcul |
|---|---|
| Court terme | 6 mois à 1 an |
| Moyen terme | 2 à 3 ans |
| Long terme | 3 à 5 ans |

Plus un recalcul déclenché par tout événement réel : augmentation, taux, étape ratée,
changement de situation.

Complément retenu (idée de Damien) : quand un retard est constaté, l'app ne se contente
pas de le signaler — elle propose comment le rattraper, y compris en comparant
des placements sûrs à faible rendement plutôt que de l'épargne dormante.
Dans les limites de D15.
