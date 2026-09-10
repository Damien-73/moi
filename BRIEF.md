# Brief — à lire avant tout le reste

Ce document s'adresse à la personne, ou à l'assistant, qui va construire.
**Dix minutes de lecture. Ne commencez pas sans l'avoir lu.**

---

## 1. Ce qu'on construit, en trois phrases

Une application qui détecte automatiquement des configurations chartistes sur le marché des
changes, **publie chaque détection avant d'en connaître l'issue** dans un registre que
n'importe qui peut vérifier, puis mesure le résultat frais déduits — y compris pour les
configurations qu'elle a écartées.

Le produit n'est pas le moteur de détection : il existe déjà ailleurs et se copie en trois mois.
**Le produit est un historique de résultats que personne ne peut fabriquer après coup**, et ce
qu'il permet de dire à un utilisateur sur son propre comportement.

## 2. La phrase qui doit guider chaque arbitrage

> **Le produit *est* ses chiffres.**
> Tout ce qui rend un chiffre invérifiable détruit le produit, quelle que soit la fonctionnalité
> gagnée en échange.

Quand une décision technique est difficile, c'est cette phrase qui tranche. Toujours.

## 3. Les six choses à ne jamais faire

*Elles ne sont pas négociables et aucune circonstance ne les justifie.*

| # | Interdit | Pourquoi |
|---|---|---|
| 1 | Utiliser une information postérieure à l'instant simulé | Rend tout résultat faussement excellent. C'est **la** faute mortelle du domaine |
| 2 | Supprimer ou modifier une détection publiée | Le registre est un livre comptable. On corrige par un ajout, jamais par une suppression |
| 3 | Modifier une règle sans créer une nouvelle version de stratégie | L'historique se réécrirait silencieusement |
| 4 | Recalculer une détection en cours de bougie | Résultat différent à chaque tick, donc non reproductible, donc invérifiable |
| 5 | Utiliser une donnée non reproductible par un tiers — volume de ticks, VWAP forex | Un vérificateur externe n'obtiendrait pas le même résultat |
| 6 | Introduire de l'apprentissage automatique, ou empiler des indicateurs | Surapprentissage garanti, et redondance : la même information comptée plusieurs fois |

## 4. Ce qui existe déjà

| Élément | État |
|---|---|
| `app/` — lot 1 | **Écrit, testé, fonctionnel.** 25 tests verts, aucune dépendance externe |
| `CAHIER-DES-CHARGES.md` | Le quoi et le pourquoi, 33 sections |
| `SPEC-LOT2.md` | Le range et le score, formule par formule |
| `SPEC-LOT3.md` | Registre, arbre de Merkle, ancrage externe, vérificateur |
| `SPEC-LOT5.md` | Import du journal utilisateur, écart comportemental |
| `SPEC-LOT11.md` | Mode contrainte |
| `SPEC-DESIGN.md` | Interface, ergonomie, temps réel |

**Le code du lot 1 fixe le niveau d'exigence attendu.** Lisez-le avant d'écrire une ligne :
il montre comment les pivots portent leur bougie de confirmation, comment le harnais
point-in-time attaque le système avec des données aberrantes, et comment un test qui ne peut
pas échouer est complété par une contre-épreuve.

## 5. Par où commencer, et dans quel ordre

| Ordre | Lot | Pourquoi à cette place |
|---|---|---|
| 1 | **Lot 0** — compte Stripe validé | Un refus bloquerait la monétisation après des mois de travail. **Avant le code** |
| 2 | **Lot 2** — le range de bout en bout | Voir §7. C'est aussi un point de décision produit |
| 3 | **Lot 3** — registre et ancrage | **L'actif prend de la valeur avec le temps : il doit démarrer le plus tôt possible**, même moche |
| 4 | Lots 4 à 15 | Voir `CAHIER-DES-CHARGES.md` §28 |

Le lot 3 avant l'interface, avant les figures supplémentaires, avant le paiement. Chaque
semaine de retard sur le lot 3 est une semaine d'historique perdue à jamais.

## 6. Ce que « terminé » veut dire

> **Un lot n'est pas terminé quand le code fonctionne.
> Il est terminé quand le résultat est reproductible par un tiers.**

Concrètement, pour chaque lot : les tests passent, **la contre-épreuve échoue bien sur un calcul
volontairement fautif**, deux exécutions complètes produisent des empreintes identiques, et
aucune constante numérique n'est écrite en dur dans le code.

## 7. Un exemple complet, de bout en bout

*Pour fixer les idées. Chiffres illustratifs.*

**Détection.** EUR/USD, H4. Quatre pivots alternés confirmés délimitent un range entre 1,0780 et
1,0865. Hauteur 85 pips = 2,4 ATR — dans les bornes. Durée 41 bougies — dans les bornes.
3 % des clôtures hors bornes — sous le seuil. Pas de dérive. **Range constitué.**

**Méthode R1, retour sur borne basse.** Une bougie touche 1,0784 et clôture à 1,0798.
Entrée 1,0798 · invalidation 1,0776 (borne − 0,5 ATR) · objectif 1,0822 (milieu du range).
Risque = 22 pips.

**Score.** Tendance journalière haussière +2 · zone support *neutralisée, c'est la borne* ·
niveau rond 1,0800 à 0,08 ATR +1 · divergence RSI +1 · faisabilité D = 0,31 +1 ·
chevauchement Londres–New York +1 · aucune annonce macro 0 · extension 0,7 ATR 0 ·
qualité 3 touches et écart 0,11 ATR +2 · régime ADX 17, cohérent avec R1 +1.
**Total 9 sur 10 atteignables = 90 % → annoncée.**

**Publication.** Écrite, empreinte calculée, feuille intégrée à l'arbre de Merkle du cycle,
tête de chaîne ancrée sur trois supports externes. Notification envoyée 31 secondes après la
clôture. **À cet instant, l'issue est inconnue de tout le monde, éditeur compris.**

**Résolution.** 6 bougies plus tard, le parcours en M1 montre 1,0822 touché avant 1,0776.
Objectif atteint. Spread horaire 1,1 pip à l'entrée et à la sortie, portage 0,3 pip sur
26 heures.
**Résultat : +1,09 R brut, +0,98 R net.** Les deux sont affichés côte à côte.

**Ce que l'utilisateur voit alors :** ce résultat, **et** la statistique de la même configuration
sur 1 240 cas, **et** celle du groupe témoin des configurations écartées. Jamais un chiffre seul.

## 8. Contexte de réalisation

| | |
|---|---|
| Équipe | **Une personne**, assistée par IA |
| Budget d'infrastructure | **Moins de 150 €/mois** avant le premier client |
| Conséquence | Peu de pièces, un seul langage, aucune complexité optionnelle. Pas de microservices, pas de Kubernetes, pas de file de messages |

Toute proposition qui augmente le nombre de composants à maintenir doit être refusée par défaut.

## 9. Que faire quand la spécification est muette

Cela arrivera. Dans ce cas, et dans cet ordre :

1. **Choisir l'option la plus reproductible**, même si elle est moins élégante ou moins rapide.
2. **Choisir l'option la plus conservatrice** : celle qui donne le résultat le moins flatteur.
   Si deux interprétations sont défendables, retenir celle qui dégrade le chiffre publié.
3. **Écrire la décision** dans le document d'implémentation concerné, avec son motif.
4. **Ne jamais deviner en silence.**

La règle 2 mérite d'être comprise : sur ce produit, une erreur qui **sous-estime** un résultat
coûte de la performance ; une erreur qui le **surestime** coûte la crédibilité, c'est-à-dire
tout. Les deux ne sont pas symétriques.

## 10. Ce que ce projet n'est pas

Ce n'est pas un vendeur de signaux, ni une promesse de rentabilité, ni un tableau de bord de
trading. Le dossier prévoit explicitement le cas où **les résultats mesurés seraient nuls ou
négatifs**, et impose de les publier tels quels : le produit devient alors *l'outil qui chiffre
ce que l'analyse technique coûte réellement*, ce qui reste une position unique et vendable
(`CAHIER-DES-CHARGES.md` §30).

Si cette perspective vous paraît absurde, ce projet n'est pas pour vous. Si elle vous paraît
être la seule position honnête tenable sur ce marché, vous avez compris l'essentiel.
