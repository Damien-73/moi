# Louis — à régler avant la première ligne de code

Mise à jour : 2026-09-10. Nom du produit retenu : **Louis**.

---

## 1. La clause d'exclusivité — comment la trouver en cinq minutes

> Information générale, pas un conseil juridique. En cas de doute sur ton contrat précis,
> l'inspection du travail répond gratuitement.

### À quoi elle ressemble

Cherche dans ton contrat les titres **Exclusivité**, **Obligations du salarié**,
**Loyauté**, ou parcours simplement les clauses générales — elle n'est pas toujours titrée.
La formulation standard ressemble à ceci :

> « Le salarié s'engage à consacrer l'exclusivité de son activité professionnelle à la Société
> et s'interdit d'exercer, directement ou indirectement, toute autre activité professionnelle,
> rémunérée ou non, pendant la durée du présent contrat, sauf autorisation écrite préalable
> de l'employeur. »

Les mots à repérer : **exclusivité**, **toute autre activité**, **rémunérée ou non**,
**autorisation écrite préalable**.

### Ce que ça change, concrètement

| Situation | Tu peux | Tu ne peux pas |
|---|---|---|
| **La clause existe** | Apprendre, construire, coder, tester avec des proches | **Facturer** un client sans autorisation écrite |
| **Pas de clause** | Exercer une autre activité | Concurrencer ton employeur, utiliser son temps ou son matériel |

**Dans les deux cas, l'obligation de loyauté s'applique** — elle vaut pour tout salarié,
même sans clause écrite. Concrètement : jamais depuis le matériel ou les heures de l'employeur,
et aucun client dans le secteur de ton employeur.

### Point important pour toi

Une clause d'exclusivité **ne bloque pas le développement de Louis**. Elle bloque
l'encaissement. Ton calendrier de construction est donc inchangé ; seule la date
de la première facture dépend de cette lecture.

### Si la clause existe

Deux options :
1. **Demander une autorisation écrite.** Beaucoup d'employeurs l'accordent pour une activité
   sans rapport avec la leur. Une demande écrite, une réponse écrite, c'est réglé.
2. **Attendre la démission pour facturer.** La bêta gratuite avec des proches ne pose
   aucun problème entre-temps.

La micro-entreprise se crée **au moment de la première facture**, pas avant.

---

## 2. Les décisions techniques — tranchées

### Agenda : Google Calendar, seul, en V1

**Pourquoi :** part de marché la plus large chez tes premiers utilisateurs, interface de
programmation la mieux documentée, authentification standard, fonctionne sur tous les appareils.

**Pourquoi pas Apple :** pas d'accès serveur correct. Le protocole disponible est pénible
et fragile — des semaines de travail pour un résultat médiocre.

**Outlook :** en V2, quand les clients entreprise arriveront.

**À vérifier auprès de tes dix premiers testeurs** avant de coder : s'ils sont tous sur
Apple, la décision change.

### Hébergement : Europe, base PostgreSQL gérée

**Décision : Supabase en région européenne (Francfort ou Paris) + hébergement applicatif
en région européenne.**

**Pourquoi :** vitesse de développement, aucune administration de serveur, et les données
restent physiquement en Europe.

**La réserve honnête :** ces sociétés sont américaines. Même avec des serveurs européens,
elles restent théoriquement soumises au droit américain. Pour une bêta de dix personnes,
c'est acceptable avec les contrats standards de sous-traitance. **Avant de dépasser
quelques centaines de clients avec des données d'humeur, il faudra réévaluer** et
éventuellement basculer sur un hébergeur français.

**Pourquoi ce n'est pas grave :** PostgreSQL est portable. Migrer d'hébergeur est une
opération de quelques jours. C'est exactement pour ça que le modèle de données compte
et que l'hébergeur, non.

### Technologie : un seul langage

**TypeScript, application Next.js, base PostgreSQL.**

Un seul langage à déboguer au lieu de deux, et c'est la pile la mieux couverte par les
IA de développement — ce qui compte énormément quand l'IA écrit une partie du code.

Pas de microservices. Pas de Python en parallèle. Pas de n8n dans le cœur du produit.

---

## 3. Le périmètre V1 — validé

| # | Élément |
|---|---|
| 1 | Web mobile installable |
| 2 | L'entrée : les 30 premières minutes (diagnostic, obstacle nommé, une action exécutée) |
| 3 | Connexion Google Calendar |
| 4 | **Un seul agent** : réorganiser l'agenda |
| 5 | Le miroir éditable, avec « pourquoi tu penses ça ? » |
| 6 | Le carnet de décisions, avec paris courts et duel de prédictions |
| 7 | La ligne de vie |
| 8 | Le quiz éclair (7 minutes) |
| 9 | **Le rendez-vous quotidien** : l'app ouvre en disant quelque chose |
| 10 | Le protocole de détresse |
| 11 | Export intégral et suppression du compte |

**Ajout par rapport à la section 15 du cahier des charges :** le point 9. Sans lui,
la semaine 1 n'a aucun rythme et l'app redevient une page blanche qu'on doit solliciter.

**Condition pour passer en V2 :** au moins 4 personnes sur 10 s'abonneraient si on
leur demandait de payer.

---

## 4. Le protocole de détresse

À implémenter en V1, sans exception. Ce n'est pas une obligation légale : c'est la
condition pour avoir le droit de poser à des gens les questions que Louis leur pose.

### Ce qui déclenche

- Mentions d'envies suicidaires, de se faire du mal, de disparaître, de « ne plus être là »
- Détresse profonde exprimée de façon répétée sur plusieurs jours
- Mentions de violences subies
- Effondrement soudain et marqué de l'état déclaré

En cas de doute, le protocole se déclenche. **Un faux positif coûte une gêne. Un faux
négatif coûte une vie.**

### Ce que Louis fait immédiatement

1. **Arrête tout** : plus de plan, plus d'objectif, plus de pari, plus de mode dur,
   plus aucune exigence. La conversation en cours s'interrompt.
2. **Reconnaît, sans analyser.** « Ce que tu me dis est grave et je le prends au sérieux. »
   Aucune interprétation, aucune hypothèse, aucun conseil.
3. **Dit ce qu'il est.** « Je suis un programme. Je ne suis pas la bonne aide pour ça,
   et je ne veux pas faire semblant de l'être. »
4. **Oriente vers des humains**, avec les numéros affichés en clair :
   - **3114** — numéro national de prévention du suicide, gratuit, 24h/24, 7j/7
   - **15** — urgences médicales
   - Le médecin traitant
5. **Reste disponible** sans insister. Pas de relance, pas de notification,
   pas de « comment tu vas aujourd'hui ? » automatique le lendemain.

### Ce que Louis ne fait jamais

- Poser un diagnostic, ou nommer une pathologie
- Minimiser, relativiser, ou proposer des « solutions »
- Continuer le programme comme si de rien n'était
- Utiliser ces échanges pour enrichir le modèle de la personne
- Supprimer l'échange : il est conservé, mais **exclu** du modèle

### Après

- L'incident est journalisé pour qu'un humain de l'équipe puisse vérifier que le
  protocole s'est bien déclenché
- Le mode dur reste désactivé jusqu'à ce que la personne le réactive elle-même
- Aucune reprise automatique du programme : c'est elle qui décide quand

---

## 5. Ce qu'il reste à produire avant le premier utilisateur

| Quoi | Comment | Coût |
|---|---|---|
| Conditions générales et politique de confidentialité | Modèles gratuits de la CNIL, adaptés | 0 € |
| Registre des traitements | Un tableur suffit | 0 € |
| Vérification d'âge (18 ans minimum) | Une case à l'inscription, dans les conditions | 0 € |
| Engagement d'arrêt : 90 jours de préavis et export | Une phrase, publiée | 0 € |
| **Le texte de l'application** | Les questions d'entrée, le ton, les formulations | Du temps d'écriture |

Le dernier point est le plus important et le seul qui ne s'achète pas : **c'est dans
les mots que Louis existe**, pas dans le code. Un même produit, écrit deux fois
différemment, donne deux entreprises différentes.

---

## Reste à faire par Damien

1. **TMview** — `Louis`, classes 9 et 42, France et UE. 20 minutes.
2. **Le domaine** — dans la foulée. 15 €.
3. **La clause d'exclusivité** — section 1 ci-dessus. 30 minutes.
4. **Envoyer le périmètre V1 à l'associé** pour confirmation ou correction.
