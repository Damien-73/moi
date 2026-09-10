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
