# JARVIS — Analyse critique du cahier des charges

Date : 2026-09-10. Auteur : Claude, à la demande de Damien.
Aucune ligne de code. Analyse préalable uniquement.

**Convention de fiabilité** utilisée partout dans ce document :
`[FAIT]` vérifiable · `[EST.]` estimation raisonnée · `[HYP.]` hypothèse à tester.

---

## 0. Verdict en trois phrases

La vision décrit un produit réel et cohérent, pas un fantasme : un système de décision
longitudinal dont l'unité de valeur n'est pas la réponse mais **la décision enregistrée
et confrontée à son résultat**.

Environ 80 % de ce qui est décrit sera absorbé par les plateformes IA généralistes
d'ici 12 à 24 mois `[EST.]`. Les 20 % restants — la boucle prédiction → réalité → recalibration —
constituent un avantage réel, étroit, et c'est exactement la partie que le document
laisse dans le flou.

Le projet est faisable. Il n'est pas faisable **dans ta situation actuelle telle qu'elle est
documentée dans `PROFIL.md`**. Ce point est traité en §16, et c'est la partie la plus importante
de ce document.

---

## 1. Ce que je comprends réellement du produit

Ce n'est pas une application de conversation. C'est **une machine à états sur une personne**.

Trois objets, et trois seulement, forment le produit :

1. **Le Twin** — un ensemble d'assertions typées sur une personne, chacune portant
   une nature (fait / observation / hypothèse), une confiance, une provenance
   et une période de validité.
2. **Le Ledger** — l'historique des décisions importantes : contexte, options,
   recommandation, décision prise, **prédiction datée**, résultat réel, leçon.
3. **La Boucle** — le mécanisme qui écrit dans les deux : comprendre → objectif réel →
   options → décision → action → résultat → mise à jour.

La conversation est le **capteur** et l'**interface** de ces trois objets. Elle n'est pas le produit.

Le critère de vérité que je retiens de §67 et que j'utiliserai comme test permanent :

> **Si un échange n'a modifié ni le Twin ni le Ledger, c'était un échange de chatbot.**

C'est la règle de conception la plus utile du projet. Elle est opérationnalisable :
on peut la mesurer (taux d'échanges produisant une écriture d'état), donc elle
empêche la dérive vers « ChatGPT avec une jolie interface ».

**Le vrai produit, en une ligne :** un système qui se souvient de ce qu'il a prédit
sur ta vie, découvre qu'il s'est trompé, et corrige sa compréhension de toi.

---

## 2. Ce qui le différencie fondamentalement d'un chatbot avec mémoire et agents

Je sépare les différences **réelles** des différences **illusoires**. Le document mélange les deux.

### Différences réelles (structurelles)

| # | Différence | Pourquoi c'est structurel |
|---|---|---|
| 1 | **Mémoire typée et contestable** vs mémoire textuelle | Une mémoire en prose ne peut être ni auditée, ni corrigée finement, ni versionnée, ni raisonnée dessus. Une assertion typée avec confiance et provenance, si. |
| 2 | **Falsifiabilité** | Le système écrit ce qu'il croit qu'il va se passer, avec une date. Puis il vérifie. Aucun assistant grand public ne fait cela aujourd'hui `[FAIT]`. |
| 3 | **Bitemporalité** | Le système sait non seulement qui tu es, mais ce qu'il croyait de toi en mars et pourquoi il a changé d'avis (§16, §98). Cela demande un modèle de données spécifique, pas un prompt. |
| 4 | **Capture des résultats réels** | La valeur ne vient pas du modèle mais de données que personne d'autre ne possède : ce qui s'est réellement passé après la décision. |

### Différences illusoires (elles se répliquent en un prompt système)

- Le ton, la personnalité adaptative, le mode dur (§49, §50).
- Le Board of Directors (§31) : cinq perspectives jouées par le même modèle sur les mêmes
  données produisent cinq reformulations, pas cinq analyses. **Contradiction assumée :
  tel que décrit, le Board est majoritairement cosmétique.** Il ne devient réel que si
  chaque perspective est adossée à des *données différentes* (le Financier lit tes chiffres
  réels, le Réaliste lit ton historique d'abandons), pas à des *instructions différentes*.
- La capacité à dire non (§90), l'exploration de scénarios (§28), le refus de la complaisance (§71).
  Tout cela tient dans un prompt système de 2 000 mots.
- Le fait d'orchestrer des agents (§34).

**Conséquence directe :** si tu construis d'abord la personnalité, le Board et les agents,
tu construis un chatbot déguisé. Si tu construis d'abord le Twin typé et le Ledger,
tu construis autre chose. L'ordre n'est pas un détail d'implémentation, c'est **le** choix produit.

---

## 3. Le véritable avantage produit

Le document dit (§94) que l'avantage est « la profondeur du modèle personnel ».
C'est presque juste. Je précise, parce que la nuance décide de l'architecture.

**La profondeur ne protège pas. La longitudinalité vérifiée protège.**

Un concurrent peut recopier ton schéma de Twin en une semaine. Il ne peut pas recopier :

1. **L'historique des prédictions résolues d'un utilisateur.** Après 18 mois, le système
   sait que tes estimations de délai sont optimistes de 40 % et que tu abandonnes les plans
   au-delà de 45 min/jour. Cette connaissance est produite par le temps, pas par le modèle.
2. **L'apprentissage inter-utilisateurs sur les résultats réels** : « pour des personnes
   dans une situation comparable, les plans à 20 min/jour ont survécu dans 70 % des cas,
   ceux à 2 h/jour dans 12 % ». C'est le seul actif qui devienne meilleur avec l'échelle.
   C'est aussi le seul qui justifie une ambition mondiale.
3. **Le rituel** qui capture les résultats. Un concurrent peut copier une fonctionnalité ;
   il copie beaucoup plus difficilement une habitude installée chez l'utilisateur.

**Contradiction avec le document :** §95 affirme que l'expérience devient « difficile à remplacer »,
alors que §63 et §62 exigent l'export intégral. Les deux sont justes moralement, mais
il faut assumer que **l'export détruit une partie du verrouillage**. L'avantage doit donc
venir de la qualité de la boucle, pas de la captivité des données. C'est plus exigeant,
et c'est le bon choix.

**Point aveugle du document :** l'avantage décrit se forme entre 18 et 36 mois `[EST.]`.
Aucune section ne dit comment on survit jusque-là. C'est la faiblesse stratégique n°1.

---

## 4. Ce qui est techniquement réalisable aujourd'hui (2026)

Réalisable = un développeur compétent peut le livrer, avec une qualité acceptable, sans recherche.

| Élément | Statut | Réserve |
|---|---|---|
| Onboarding conversationnel adaptatif piloté par une liste de trous d'information | ✅ | Le « adaptatif » est un algorithme de sélection sur une liste de créneaux, pas de la magie. |
| Extraction structurée en assertions typées (sortie contrainte par schéma) | ✅ | Fiable en 2026. Exige une validation stricte : le modèle n'écrit jamais de prose en base. |
| Faits / observations / hypothèses + confiance + provenance | ✅ | C'est du modèle de données, pas de l'IA. |
| Écran « ce que JARVIS sait de moi », éditable, avec « pourquoi tu penses ça ? » | ✅ | Trivial si la provenance est stockée dès le jour 1. Impossible à rattraper sinon. |
| Synthèse personnalisée (WOW 1, §21) | ✅ | C'est aujourd'hui la partie la plus facile et la plus impressionnante. Attention : c'est aussi la plus copiable. |
| Objectif déclaré vs objectif profond hypothétique | ✅ | Sous forme d'hypothèse soumise à confirmation, comme le document l'exige. |
| Conflits d'objectifs (§27) | ✅ | Détectable par règles simples sur un petit nombre de paires (liberté/sécurité, argent/temps). |
| 2-3 trajectoires comparées avec hypothèses explicites | ✅ | **À condition d'assumer que ce n'est pas une simulation** (voir §5 ci-dessous). |
| Ledger de décisions avec prédiction datée | ✅ | C'est une table SQL. La difficulté est d'ordre UX, pas technique. |
| Détection d'écart dire/faire (§24) | ⚠️ | Réalisable si les événements sont journalisés. Bruité, et socialement le plus risqué du produit. |
| Reconnaissance d'erreur (§42) | ✅ | Découle mécaniquement du Ledger. Aucune intelligence supplémentaire requise. |
| Routage multi-modèles par coût (§58) | ✅ | Modèle économique pour extraction/classification, modèle puissant pour synthèse. |

---

## 5. Réalisable mais difficile ou coûteux

| Élément | Difficulté réelle | Coût `[EST.]` |
|---|---|---|
| **Capture des résultats réels (Reality Engine, §37)** | **Le problème n°1 non résolu du document.** Soit l'utilisateur déclare (déclaratif → décroissance rapide de l'assiduité), soit on intègre des sources externes (email, agenda, banque) → complexité, permissions, RGPD, maintenance. | Élevé, permanent |
| Trajectory Engine réellement calculatoire | Comparer des scénarios avec des chiffres exige un modèle de domaine (marché du travail, finances). Sans cela, ce sont des récits comparés. Avec cela, c'est un produit par domaine. | Élevé, par domaine |
| Actions à effet réel (envoyer, réserver, payer) | Fiabilité, authentification, casse permanente des intégrations, responsabilité juridique. §61 (ne jamais prétendre avoir agi) exige des accusés de réception vérifiés, donc une couche d'exécution avec états. | Élevé |
| Calibration des prédictions (§41) | Statistiquement, il faut ~30 prédictions résolues par utilisateur pour dire quoi que ce soit `[EST.]`. Soit 12-18 mois d'usage. | Faible en code, énorme en temps |
| Indépendance fournisseur (§88) | Une couche d'abstraction se code en 2 jours. **L'équivalence de comportement entre modèles ne s'obtient que par une suite d'évaluations**, à maintenir. C'est le vrai coût, et il est récurrent. | Moyen, récurrent |
| Savoir ne pas intervenir (§48) | Problème de décision sous incertitude avec coût d'erreur asymétrique : une notification inutile coûte plus qu'une notification manquée. | Moyen |
| Coût d'inference d'un Twin profond | Un tour riche = 20-40 k tokens de contexte. Ordre de grandeur : 0,05 à 0,30 € par tour riche ; 15 à 60 €/mois pour un utilisateur quotidien non bridé `[EST.]`. Disposition à payer grand public : 15-25 €/mois `[EST.]`. **L'économie unitaire peut s'inverser.** À traiter dès la conception, pas après. | Structurel |

---

## 6. Ce qui doit être repoussé

| Élément | Repoussé à | Motif |
|---|---|---|
| Agents, intégrations externes, n8n | V2 | Aucune valeur tant que le Twin n'est pas prouvé. §34 dit lui-même qu'ils sont de l'infrastructure. |
| Actions autonomes niveaux 1 et 2 (§36) | V2 | En V1 : préparation + confirmation uniquement. Zéro action irréversible. |
| Board of Directors visible | V2 | Cosmétique tant qu'il n'est pas adossé à des données distinctes (cf. §2). |
| Couche Sims / gamification (§43-46) | V3 | Voir la contradiction en §8. Risque de dénaturer le produit avant qu'il soit prouvé. |
| Détection de patterns psychologiques (§22-23) | V2 | Exige plusieurs mois de données. C'est aussi le point de risque juridique et éthique maximal. |
| Multilingue, devises, international (§65-66) | V2+ | Coût réel, valeur nulle sur 10 bêta-testeurs francophones. |
| Apprentissage inter-utilisateurs | V3 | Exige ~1 000 utilisateurs × 6 mois `[EST.]`. C'est le moat, il n'est pas atteignable tôt. |
| Voix, avatar, application mobile | V3 | Aucun rapport avec la vérité à prouver (§106). |
| Multi-modèles à l'exécution | V2 | **Je contredis §88 sur le calendrier** : l'abstraction dans le code, oui, dès le début. La bascule réelle entre fournisseurs, non — c'est de l'optimisation prématurée avant l'ajustement produit-marché. |

---

## 7. Risques majeurs

Classés par gravité, la plus grave d'abord.

### R1 — Risque de plateforme (existentiel)

`[FAIT]` Les fournisseurs de modèles proposent déjà mémoire persistante, connecteurs,
agents et tâches planifiées. `[EST.]` Ce qui relève de « meilleure mémoire + meilleur prompt »
sera absorbé sous 12-24 mois.

Ce qu'ils ne construisent pas, et probablement pas bientôt : **la capture longitudinale
des résultats réels**, parce qu'elle exige un rituel produit, pas une capacité de modèle.
C'est le seul terrain défendable. Toute heure investie ailleurs est une heure investie
sur un terrain qui sera rasé.

### R2 — Démarrage à froid inversé

Le produit demande beaucoup d'informations avant de donner de la valeur, et sa valeur
maximale arrive après des mois. La courbe de rétention est exactement l'inverse de ce
dont une jeune entreprise a besoin. `[HYP.]` Le WOW 1 (§21) est le seul contrepoids ;
s'il n'arrive pas dans les 15 premières minutes, il n'y aura pas de mois 3.

### R3 — Absence de signal de résultat

Sans données de résultat, la boucle §81 ne tourne pas, le Reality Engine est vide,
la calibration est impossible, et le produit redevient un chatbot avec de la mémoire.
**Le document ne dit nulle part comment les résultats entrent dans le système.**
Ma réponse est en §9 (le rituel hebdomadaire).

### R4 — Juridique et réglementaire

`[FAIT]` Le RGPD s'applique intégralement : base légale, minimisation, droit d'accès,
de rectification, d'effacement, de portabilité.
`[EST. / à faire valider par un juriste]` Points sensibles spécifiques à ce produit :
- Des données de catégorie particulière (santé, convictions, orientation) peuvent
  **surgir spontanément** dans une conversation de vie. Il faut une politique de refus
  d'enregistrement, pas seulement une politique de consentement.
- Le règlement européen sur l'IA impose des obligations de transparence, et encadre
  strictement l'inférence d'états émotionnels dans certains contextes. Un produit qui
  infère des traits psychologiques et conseille sur la carrière se situe dans une zone
  à faire qualifier par un juriste **avant** la mise en ligne, pas après.
- L'article 22 du RGPD (décision entièrement automatisée) est probablement évité tant que
  l'humain décide (§10) — mais cela doit rester vrai dans le code, pas seulement dans le discours.

### R5 — Sécurité de l'utilisateur (lacune du cahier des charges)

Un produit qui explore les peurs, les échecs, la démotivation et les blocages **rencontrera
des utilisateurs en détresse psychologique**. Le document ne contient aucun protocole de crise.
C'est une lacune sérieuse et non négociable : détection, arrêt du mode dur, orientation
vers des ressources humaines, journalisation. À concevoir avant la première bêta, pas après.

### R6 — Effet « intrusif »

§24 (« tu dis vouloir X mais tu fais Y ») est la fonctionnalité la plus impressionnante
et la plus susceptible de faire fuir un utilisateur. `[HYP.]` Elle n'est acceptable
qu'après un capital de confiance, jamais dans les premières semaines, et toujours
formulée comme question, jamais comme constat.

### R7 — Économie unitaire

Voir §5. Un produit à forte profondeur de contexte et à abonnement grand public
peut avoir une marge brute négative sur ses utilisateurs les plus engagés — c'est-à-dire
sur ses meilleurs utilisateurs.

### R8 — Risque fondateur

Traité en §16. C'est en réalité le risque le plus élevé du projet.

---

## 8. Incohérences et faiblesses du cahier des charges

1. **§45 vs §43-46.** « La bonne métrique n'est pas le temps passé » puis une couche
   inspirée des Sims, qui est précisément un mécanisme de temps passé.
   *Résolution proposée :* afficher la progression (compétences, objectifs, obstacles franchis),
   interdire les mécaniques de rappel — pas de séries quotidiennes, pas de badges,
   pas de notification dont le but est le retour dans l'application.

2. **§90 vs §77.** Un produit qui dit non a une rétention plus faible qu'un produit qui flatte.
   Le document exige les deux : franchise totale et « est-ce que ça te manquerait ».
   Ce n'est pas insoluble, mais cela signifie que **le jeu de métriques de §76 est mal calibré** :
   la rétention à 7 jours n'est pas la bonne mesure pour ce produit. La bonne mesure est
   le taux de retour après un désaccord.

3. **Le Reality Engine n'a pas d'entrée.** §37-41 décrivent minutieusement le traitement
   des résultats et jamais leur acquisition. C'est le trou central du document.

4. **§73 (carrière) contre §8 (apprendre de la réalité).** Le premier cas d'usage choisi
   a des cycles de résultat de 3 à 6 mois. La boucle d'apprentissage a besoin de cycles courts.
   **Le domaine choisi est le bon, mais la granularité de mesure est mauvaise.**
   *Résolution :* mesurer les micro-résultats hebdomadaires (candidatures envoyées, réponses
   obtenues, entretiens, heures de formation tenues) et non le résultat terminal.

5. **§22 vs §67.** « Psychologie comportementale » et « pas de psychologue improvisé »
   sont posés côte à côte sans mécanisme de séparation. Il faut une liste fermée
   de ce qui peut être inféré, et une liste fermée de ce qui ne peut jamais l'être
   (diagnostic, pathologie, santé mentale, traits cliniques).

6. **§88 vs §21.** L'indépendance fournisseur et la qualité maximale du moment WOW
   tirent en sens opposés. L'indépendance est un objectif d'architecture, pas d'exécution.

7. **Absences totales.** Le document ne dit rien sur : le prix, le modèle économique,
   le coût d'exploitation, la concurrence, l'équipe, le financement, le délai.
   Pour un document dit « fondateur », c'est une omission majeure — ce sont ces quatre
   variables qui tuent les projets, pas la vision.

8. **Ratio manifeste/spécification.** 108 sections de principes, 1 section de MVP,
   aucune affirmation falsifiable hormis §106. Un cahier des charges qui ne peut pas
   être contredit par un test ne guide pas la construction — il la légitime.
   C'est le signal de risque le plus important du document lui-même.

---

## 9. Architecture produit recommandée

**Un objet, trois surfaces, un rituel.**

```
                        ┌──────────────────┐
                        │   LE TWIN        │  assertions typées, datées,
                        │   (l'objet)      │  contestables, versionnées
                        └────────┬─────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐     ┌─────────▼────────┐     ┌─────────▼────────┐
│ CONVERSATION   │     │  MIROIR          │     │  LEDGER          │
│ le capteur     │     │  « ce que je     │     │  décisions,      │
│ et l'interface │     │  sais de toi »   │     │  prédictions,    │
│                │     │  éditable        │     │  résultats       │
└───────┬────────┘     └─────────┬────────┘     └─────────┬────────┘
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │   LE POINT       │  rituel hebdomadaire, 5 min :
                        │   (le rituel)    │  ce qui s'est passé, prédictions
                        └──────────────────┘  résolues, Twin mis à jour
```

### Les trois surfaces

- **Conversation.** Elle n'est jamais une fin. Chaque échange significatif se termine
  par une écriture visible : « j'ai noté ceci », « j'ai corrigé cela », « je note ma prédiction ».
- **Miroir.** L'écran qui rend le produit non-copiable perceptuellement. Faits, observations,
  hypothèses, avec pour chaque ligne : la source, la date, un bouton *corriger*,
  un bouton *supprimer*, un bouton *pourquoi tu penses ça ?*.
- **Ledger.** L'historique stratégique. C'est l'écran qui, au mois 6, produit le WOW 6 et 7.

### Le rituel — ma réponse au trou central du document

**Le Point** : une fois par semaine, 5 minutes, toujours au même moment, initié par JARVIS.
Trois questions seulement :
1. Qu'est-ce que tu as fait de ce qu'on avait prévu ?
2. Qu'est-ce qui s'est passé que je ne sais pas ?
3. Une prédiction arrivée à échéance : elle s'est vérifiée ou non ?

C'est le **seul** point d'entrée des résultats réels en V1. Sans intégration, sans agent,
sans capteur. Si les utilisateurs ne tiennent pas ce rituel, le produit n'a pas de boucle
d'apprentissage — et il faut le savoir au mois 2, pas au mois 20.

**Le taux de complétion du Point est la métrique principale de la bêta.** Pas la rétention,
pas le nombre de messages.

---

## 10. Architecture technique recommandée

### Principe directeur

> Soigner obsessionnellement le modèle de données. Être décontracté sur tout le reste.
> Le modèle de données est irréversible ; le framework, l'hébergeur, le modèle IA
> et l'interface sont remplaçables en quelques jours.

### Modèle de données (le cœur)

Base relationnelle unique (PostgreSQL). Sept tables portent tout le produit :

| Table | Rôle | Champs critiques |
|---|---|---|
| `assertions` | Le Twin | `sujet`, `predicat`, `valeur`, `nature` (fait/observation/hypothèse), `confiance`, `source_message_id`, `valide_de`, `valide_jusqu_a`, `remplace_id` |
| `goals` | Objectifs | déclaré, profond hypothétique, priorité, échéance, statut |
| `decisions` | Ledger | contexte, options envisagées, recommandation, décision réelle, date |
| `predictions` | Falsifiabilité | `decision_id`, énoncé, `echeance`, confiance, `resultat` (null → vrai/faux/partiel), date de résolution |
| `actions` | Action Engine | statut, résultat attendu, résultat réel, preuve d'exécution |
| `events` | Journal brut | tout ce qui s'est passé, append-only |
| `messages` | Transcriptions | source de provenance de toute assertion |

**Trois règles absolues :**
1. **Aucune mise à jour destructive d'une assertion.** On clôt la validité et on en crée
   une nouvelle avec `remplace_id`. C'est ce qui donne §16 et §98 gratuitement,
   et l'auditabilité RGPD par-dessus.
2. **Aucune assertion sans provenance.** Une assertion sans `source_message_id`
   est un bug, pas une donnée. Impossible à rattraper rétroactivement.
3. **Le modèle IA n'écrit jamais en base directement.** Il produit un JSON validé
   contre un schéma strict ; un code déterministe écrit.

### Récupération de contexte

**Contradiction assumée avec le réflexe habituel : ne commence pas par une base vectorielle.**

Un être humain se décrit en quelques centaines d'assertions. Cela tient intégralement
dans le contexte d'un modèle moderne. Le Twin *est* la compression ; la recherche
sémantique est une béquille pour mémoire non structurée. Ajouter `pgvector` plus tard,
uniquement pour retrouver des passages de transcription brute.

Gain : moins de pièces mobiles, comportement déterministe, débogage possible par un novice.

### Utilisation des modèles — deux voies

| Voie | Usage | Part des appels `[EST.]` |
|---|---|---|
| Économique / rapide | extraction, classification, détection des trous, routage, résumés | 70-85 % |
| Puissante | synthèse personnalisée, analyse de décision, trajectoires, Board | 15-30 % |

Toute écriture dans le Twin passe par la voie économique avec sortie structurée.
La voie puissante ne sert qu'aux moments où l'utilisateur perçoit l'intelligence.

### Indépendance fournisseur — la version honnête

Une interface interne unique `appel_modele(tache, schema, budget)`.
Chaque prompt est un fichier versionné avec un jeu de tests attendu.
**L'indépendance ne vient pas de la couche d'abstraction, elle vient de la suite de tests.**
Sans elle, changer de modèle est un saut dans le vide et tu resteras chez ton fournisseur
par peur — c'est-à-dire la dépendance que §88 veut éviter.

### Pile technique recommandée pour un fondateur non-développeur

- **Un seul langage : TypeScript.** Next.js pour l'application (interface + serveur ensemble).
  Motif : un seul langage à déboguer au lieu de deux, et c'est la pile la mieux couverte
  par les IA de développement `[EST.]` — ce qui compte énormément quand l'IA écrit le code.
- **PostgreSQL géré** (Supabase ou Neon). Pas d'administration de base.
- **Hébergement géré** (Vercel). Pas de serveur.
- **Travaux de fond** : une file de tâches simple. Les écritures dans le Twin se font
  *après* la réponse, jamais dans le chemin de réponse.
- **Ce qu'il ne faut pas faire :** microservices, Kubernetes, Python + API séparée,
  n8n dans le cœur du produit, framework d'agents pour l'orchestration.

### Chiffrement — la version honnête

Chiffrement au repos, chiffrement de champ pour les assertions sensibles, clé par utilisateur.
**Le chiffrement de bout en bout est incompatible avec des appels de modèle côté serveur.**
Ne le promets jamais dans la communication : ce serait un mensonge, et §61 l'interdit
par analogie.

---

## 11. Le MVP que je construirais réellement

**Durée :** 4 à 6 semaines pour un développeur expérimenté `[EST.]`.
**Affirmation falsifiable qu'il doit tester :** §106.

| # | Fonctionnalité | Pourquoi elle est dedans |
|---|---|---|
| 1 | Compte + entrée (lien magique par email) | Minimum vital |
| 2 | Onboarding adaptatif sur ~25 créneaux d'information, avec arrêt automatique à « assez pour agir » | Loi 1, §18, §20 |
| 3 | Twin typé : faits / observations / hypothèses, confiance, provenance | §13, cœur du produit |
| 4 | Miroir éditable + « pourquoi tu penses ça ? » | §15, §63 — c'est l'écran qui prouve que ce n'est pas un chatbot |
| 5 | Synthèse personnalisée avec demande de confirmation | §21, WOW 1 |
| 6 | Objectifs : déclaré + objectif profond hypothétique + conflits | §25-27 |
| 7 | 2 à 3 trajectoires qualitatives, hypothèses explicites, « ce qui les ferait changer » | §28-29 |
| 8 | Ledger : contexte, options, recommandation, décision, **prédiction datée** | §40 — la brique qui n'existe nulle part ailleurs |
| 9 | **Le Point** hebdomadaire, 5 min, résolution des prédictions | §37 — le trou du document, comblé |
| 10 | Mode dur / mode normal, choix explicite | §49-50, faible coût, fort effet perçu |
| 11 | Protocole de crise | Non négociable |
| 12 | Export intégral + suppression du compte | §62, RGPD |

**Rien d'autre. Douze éléments.**

Le test de la bêta n'est pas §77. C'est plus dur et plus mesurable :

> À la semaine 4, la synthèse produite par JARVIS est jugée **meilleure** que celle
> de la semaine 1 par au moins 7 utilisateurs sur 10, en comparaison aveugle,
> **et** au moins 6 utilisateurs sur 10 ont tenu 3 « Points » hebdomadaires.

Si ce test échoue, la thèse centrale du produit est fausse et aucune fonctionnalité
supplémentaire ne la sauvera.

---

## 12. Ce que je ne construirais surtout pas dans le MVP

| À ne pas construire | Motif |
|---|---|
| Agents, orchestration, n8n | §34 les dit invisibles : invisibles signifie aussi qu'ils peuvent être absents sans que l'utilisateur le sache |
| Intégrations externes (email, agenda, banque) | Coût, permissions, RGPD, casse. Le Point les remplace en V1 |
| Actions à effet réel | Responsabilité juridique + §61 exige une couche d'exécution vérifiée |
| Gamification, Sims, badges, séries | Contredit §45. Et si le produit a besoin de badges pour retenir, c'est qu'il ne marche pas |
| Board of Directors visible | Cosmétique tant qu'il n'est pas adossé à des données distinctes |
| Détection de patterns psychologiques | Pas assez de données, risque maximal |
| Base vectorielle | Complexité sans valeur à cette échelle |
| Application mobile, voix, avatar | Zéro rapport avec la vérité à prouver |
| Multilingue, devises, fuseaux | Dix testeurs francophones |
| Bascule multi-fournisseurs à l'exécution | Optimisation prématurée. **Je contredis §88 sur ce point de calendrier** |
| Paiement, facturation | Aucun revenu attendu en bêta |
| Notifications proactives | §48 : mal fait, c'est destructeur. Le Point suffit |

---

## 13. Du MVP au produit complet

Progression **par preuve**, jamais par calendrier. Chaque porte a un critère chiffré
qui autorise — ou interdit — la suivante.

| Porte | Condition d'ouverture | Ce qu'on ajoute ensuite |
|---|---|---|
| **G0 → G1** | Test §11 réussi sur 10 utilisateurs | Actions en mode *préparation seule* (CV, message, candidature préparés mais envoyés par l'utilisateur) |
| **G1 → G2** | Taux « préparé → réellement envoyé » supérieur au taux « conseillé → envoyé » | Première intégration en **lecture seule** (agenda ou email), pour remplacer une partie du déclaratif |
| **G2 → G3** | Décroissance prouvée du déclaratif + 50 utilisateurs actifs | Calibration visible : « mes estimations de délai ont été trop optimistes de 40 % » — c'est le WOW 6 |
| **G3 → G4** | ~30 prédictions résolues par utilisateur, sur ~200 utilisateurs | Apprentissage inter-utilisateurs, anonymisé, sur consentement explicite. **C'est ici que naît l'avantage défendable** |
| **G4 → G5** | Avantage mesurable des recommandations informées par l'agrégat | Deuxième domaine de vie |
| **G5** | **Test de plateforme** : ajouter un domaine ne doit exiger *aucune* modification du schéma du Twin | Si le schéma doit changer, il était faux — corriger avant d'élargir |

Gamification : jamais avant G3, et uniquement en affichage de progression réelle.
Board visible : G2. Autonomie niveau 1 : G3, et uniquement sur des actions réversibles.

**Règle transversale :** à chaque porte, si l'ajout ne peut pas être justifié par
« cela améliore la compréhension, la décision, l'action ou l'apprentissage » (§102),
il ne passe pas.

---

## 14. Décisions techniques qui nous enfermeraient

Séparation nette entre l'irréversible et le réversible. Presque tout le monde
se trompe d'endroit où être prudent.

### Irréversible — à ne jamais rater

| Erreur | Conséquence |
|---|---|
| **Stocker le Twin en texte libre ou en vecteurs uniquement** | Ni audit, ni correction fine, ni versionnement, ni raisonnement. **La pire erreur disponible.** Elle transforme définitivement le projet en chatbot avec mémoire |
| **Mettre à jour les croyances en place, sans historique** | Détruit §16, §92, §98. Irrattrapable pour toutes les données passées |
| **Assertions sans provenance** | Détruit §15 et §63. Impossible de répondre « pourquoi tu penses ça ? » rétroactivement |
| **Schéma du Twin spécifique à la carrière** | Bloque §97. Le Twin doit être générique ; le domaine est une étiquette, pas une structure |
| **Confier la mémoire à l'abstraction d'un framework ou d'un fournisseur** | Dépendance exactement à la couche que §88 exige de posséder |
| **n8n comme cœur d'orchestration** | Non versionnable, non testable, non migrable |
| **Absence d'isolation des données par utilisateur dès le départ** | Migration ultérieure très douloureuse sous contrainte RGPD |
| **Prompts en dur, sans version ni tests** | Impossible de savoir si un changement de modèle améliore ou dégrade. C'est le mécanisme réel de la dépendance fournisseur |

### Réversible — ne pas y perdre de temps

Framework d'interface, hébergeur, fournisseur de modèle, design, nom, structure des fichiers,
choix entre Supabase et Neon. Tout cela se change en quelques jours.

---

## 15. Est-ce que la vision peut devenir un produit nouveau et mondialement scalable ?

Réponse en quatre parties, parce qu'une seule serait malhonnête.

**a) La catégorie est-elle réelle ?** Oui `[EST., confiance élevée]`.
Un modèle personnel persistant est la couche manquante entre l'humain et ses outils.
Ce n'est pas une intuition isolée : les grands fournisseurs vont dans cette direction.

**b) La différenciation est-elle défendable par un tiers ?** Partiellement, et étroitement.
Tout ce qui relève de « mémoire + prompt + agents » sera absorbé `[EST.]`.
Ce qui ne le sera pas : **des prédictions enregistrées, confrontées à des résultats réels,
et l'apprentissage agrégé de ce qui fonctionne réellement pour quel type de personne.**
Les laboratoires ne construisent pas cela, parce que cela exige un rituel produit et une
relation longue, pas une capacité de modèle. C'est la seule fenêtre, et elle est réelle.

**c) Est-ce mondialement scalable ?** Structurellement oui, pratiquement plus lentement
qu'un chatbot. La valeur dépend de la capture des résultats, qui dépend d'intégrations,
qui sont spécifiques à chaque pays (marché du travail, banque, administration).
Le produit passe donc à l'échelle par **domaine × pays**, pas par simple traduction.
`[EST.]` C'est une entreprise à 5-7 ans, pas à 18 mois.

**d) Alors, oui ou non ?**

**Oui pour la vision. Non pour ce document tel qu'il est, exécuté par toi tel que tu es aujourd'hui.**

Le problème n'est pas l'idée. Le problème est que **l'avantage se forme après 18 à 36 mois
d'utilisateurs retenus**, et que rien dans ta situation actuelle ne permet de financer
ni de survivre à cette période. Une bonne idée dont la fenêtre de valeur s'ouvre après
ta réserve de trésorerie n'est pas une bonne idée pour toi ; c'en est une pour quelqu'un
d'autre, ou pour toi plus tard.

---

## 16. Ce que ton propre dossier oblige à dire

C'est la partie que tu n'as pas demandée et qui compte le plus.

### Les faits, tirés de tes propres documents

`[FAIT]` `PROFIL.md` : novice, aucune compétence technique constituée, 2 000 € nets/mois,
3 000 € d'épargne, ~20 h/semaine, objectif 2 500 €/mois en 6-12 mois, **rien n'a encore
été tenté**, blocage déclaré : *peur de se tromper et de perdre du temps*.

`[FAIT]` `FEUILLE-DE-ROUTE.md`, écrite **hier** : « Priorité 8 — Opportuniste : agents IA.
À ajouter si le marché existe encore sous cette forme. **Aucune décision de démission
ne doit en dépendre.** »

`[FAIT]` `PLAN-MOIS-1.md`, écrit hier : première semaine = vérifier la clause d'exclusivité,
ouvrir un compte Klaviyo. Aucune de ces deux actions n'apparaît comme faite.

### Ce que cela signifie

Vingt-quatre heures après avoir classé l'IA en priorité 8, tu proposes la version
maximale de la priorité 8 : une entreprise mondiale de Personal AI.

Ce n'est pas de l'ambition mal placée. C'est **le mécanisme exact que ton profil décrit** :
la peur de se tromper trouve toujours un projet plus grand à préparer, parce que préparer
un projet immense est infiniment plus confortable que d'envoyer le premier message
à une boutique en ligne. Un cahier des charges de 108 sections est une manière très
convaincante de ne pas commencer.

**Tu as tort sur le calendrier, pas sur l'idée.** Je le dis explicitement, comme convenu.

### Les chiffres qui tranchent

| Question | Réponse `[EST.]` |
|---|---|
| Effort pour le MVP §11, par un développeur expérimenté | 4-6 semaines |
| Effort pour toi, novice, assisté par IA, à 20 h/semaine | 6-9 mois, avec un risque d'abandon élevé au premier obstacle d'infrastructure |
| Revenu produit par ce MVP à 12 mois | 0 € |
| Revenu produit par `FEUILLE-DE-ROUTE.md` à 12 mois | 2 000-3 000 €/mois récurrents |
| Financement nécessaire pour en faire une entreprise | 300 k€ - 1 M€ en amorçage européen |
| Probabilité qu'un fonds européen finance un fondateur solo non technique sur de l'IA grand public | Très faible `[EST.]` — un cofondateur technique est en pratique obligatoire |
| Coût d'inference pendant une bêta de 50 utilisateurs actifs | 400-1 500 €/mois, sur une épargne de 3 000 € |

Cette dernière ligne suffit à conclure : **ta bêta consommerait ton épargne de départ
en 2 à 6 mois, sans produire un euro.**

### Ce que je recommande — une seule option

**Ne l'abandonne pas. Ne le lance pas. Vis-le.**

Tu as déjà commencé sans le voir. Ce dépôt — `PROFIL.md`, `STRATEGIE.md`,
`FEUILLE-DE-ROUTE.md`, les décisions consignées — **est une version primitive du Digital Twin.**
Des faits, des hypothèses, des contraintes, une stratégie, un historique versionné.
Il lui manque exactement trois choses : les prédictions datées, les résultats,
et le rituel qui les capture.

Donc :

1. **Tu exécutes `FEUILLE-DE-ROUTE.md` sans modification.** Semaine 1 : clause d'exclusivité,
   compte Klaviyo. C'est ce qui produit du revenu et te sort du logement de fonction.
2. **Tu construis JARVIS pour toi seul, 2 h par semaine, dans ce dépôt**, sans code au début :
   le Twin, le Ledger, les prédictions datées, le Point hebdomadaire. En markdown, en git.
3. **Tu deviens ton propre utilisateur pendant 12 mois.** Au mois 12 tu possèdes
   ce qu'aucun concurrent ne peut fabriquer : un registre de décisions réelles avec
   prédictions résolues sur une transition de vie réussie ou ratée. C'est à la fois
   la preuve du concept, la démonstration commerciale, et le seul contenu qui rende
   l'histoire crédible devant un cofondateur ou un investisseur.
4. **Tu codes le produit à partir du mois 12**, financé par la prestation, avec les
   compétences d'automatisation acquises en priorité 4 — qui sont exactement les
   compétences requises — et avec un cofondateur technique.

Cette option domine strictement l'alternative : elle ne sacrifie rien de la vision,
ne consomme pas l'épargne, produit du revenu, et améliore la qualité du produit
en le fondant sur une expérience vécue plutôt que sur un document.

L'alternative — tout arrêter et construire JARVIS maintenant — exige un cofondateur
technique, 12-18 mois sans revenu et 15-20 k€ que tu n'as pas. Je la déconseille,
et la raison n'est pas l'idée : c'est l'ordre.

**Rappel de ta propre règle, écrite hier :** *« Tout ce que tu veux vraiment faire reste
au programme. La seule question était l'ordre. »* Elle s'applique intégralement ici.

---

## 17. Ce que je ferais dans les 7 prochains jours

| # | Action | Durée |
|---|---|---|
| 1 | Relire le contrat de travail : clause d'exclusivité | 30 min |
| 2 | Ouvrir le compte Klaviyo, démarrer la certification | 3 h |
| 3 | Écrire dans ce dépôt tes 5 premières **prédictions datées** sur les 3 prochains mois (première vente, épargne, heures réellement tenues) | 45 min |
| 4 | Fixer le jour et l'heure du **Point** hebdomadaire, et le tenir une première fois | 5 min |
| 5 | Ne rien coder | — |

Le point 3 est le début réel de JARVIS. Il coûte 45 minutes et il teste la seule
hypothèse qui compte : le système peut-il enregistrer ce qu'il croit, puis découvrir
qu'il s'est trompé ?

Si tu ne tiens pas ce rituel pour toi-même pendant 8 semaines, aucun utilisateur ne le tiendra,
et le produit décrit dans le cahier des charges n'a pas de boucle d'apprentissage.
**C'est le test le moins cher et le plus décisif du projet entier.**
