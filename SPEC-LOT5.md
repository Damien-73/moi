# Spécification technique — Lot 5 : journal utilisateur et écart comportemental

Document d'implémentation. Complète le cahier des charges §5 module E et §25.2.

> **C'est la fonction qui fait payer.** Elle ne dépend pas de l'existence d'un avantage de
> marché : dire à quelqu'un qu'il entre deux bougies trop tôt garde toute sa valeur même si
> aucune figure n'est rentable. C'est la seule fonction robuste au risque principal du projet.

---

## 1. Import

### 1.1 Formats acceptés

| Format | Origine | Priorité |
|---|---|---|
| Rapport HTML « Statement » | MetaTrader 4 | v1 |
| Rapport HTML ou XLSX | MetaTrader 5 | v1 |
| CSV générique | Modèle publié par nos soins | v1 |
| CSV cTrader, TradingView | Autres plateformes | v2 |

**Aucune connexion au compte de courtage.** Ni identifiants, ni jeton, ni lecture d'API :
l'utilisateur téléverse un fichier qu'il a exporté lui-même. Cela supprime toute question de
détention d'accès à un compte financier, et la charge réglementaire qui l'accompagne.

### 1.2 Champs requis et champs optionnels

| Champ | Statut | Défaut si absent |
|---|---|---|
| Symbole | **Requis** | Ligne rejetée |
| Sens (achat / vente) | **Requis** | Ligne rejetée |
| Horodatage d'entrée, prix d'entrée | **Requis** | Ligne rejetée |
| Horodatage de sortie, prix de sortie | **Requis** | Position encore ouverte : exclue des statistiques, conservée |
| Volume | Requis | Ligne rejetée |
| Stop, objectif | Optionnel | Voir §3.1 — le risque est alors reconstruit |
| Commission, swap | Optionnel | 0, et l'utilisateur est averti que ses résultats sont surestimés |

### 1.3 Normalisation des symboles

Les courtiers ajoutent des suffixes : `EURUSD.pro`, `EURUSDm`, `EURUSD_raw`, `EUR/USD`, `EURUSD#`.

Règle : mise en majuscules, suppression des séparateurs non alphabétiques, puis suppression de
tout suffixe après les six premières lettres si les six premières correspondent à une paire
connue. Les symboles non résolus sont **présentés à l'utilisateur pour association manuelle**,
et l'association est mémorisée.

### 1.4 Le piège de l'heure du serveur de courtage

*C'est l'erreur qui fausse silencieusement toute l'analyse horaire — la partie la plus utile
du produit.*

Les rapports MetaTrader sont horodatés en **heure du serveur du courtier**, presque jamais en
UTC : le plus souvent UTC+2 ou UTC+3, avec un changement d'heure qui suit parfois le calendrier
américain et non européen. Sans correction, une analyse « vos pertes se concentrent à 9 h »
désigne la mauvaise séance de deux à trois heures.

**Détection automatique du décalage :**

```
1. Extraire l'ensemble des horodatages du fichier.
2. Le marché du change est fermé du vendredi 17:00 au dimanche 17:00 New York.
   Le trou hebdomadaire dans les horodatages révèle le décalage du serveur.
3. Estimer le décalage qui aligne ce trou sur la fermeture réelle.
4. Vérifier la cohérence sur au moins 8 semaines distinctes.
5. Si l'estimation est ambiguë (moins de 8 semaines, ou trous incohérents),
   DEMANDER le décalage à l'utilisateur. Ne jamais deviner en silence.
```

Le décalage retenu et sa méthode d'obtention sont affichés à l'utilisateur, modifiables, et
enregistrés avec l'import.

### 1.5 Contrôles de cohérence au chargement

Sortie antérieure à l'entrée · prix hors de l'amplitude réelle du marché à cet instant,
vérifié contre nos propres bougies · volume nul ou négatif · doublons exacts.
Toute ligne suspecte est **signalée à l'utilisateur, pas supprimée en silence**.

---

## 2. Rapprochement avec les détections

Un trade de l'utilisateur est rapproché d'une détection publiée si **toutes** ces conditions
sont vraies :

| Condition | Tolérance |
|---|---|
| Même instrument | Exacte |
| Même sens | Exacte |
| Entrée dans la fenêtre de la détection | `[entree_ts − 2 bougies, entree_ts + 5 bougies]` de l'unité de temps de la détection |
| Prix d'entrée proche | `|prix_utilisateur − prix_detection| ≤ 0,5 × ATR` de la détection |

En cas de candidats multiples : le plus proche en temps, puis en prix. Un trade ne peut être
rapproché que d'une détection, et réciproquement.

**Les trades non rapprochés — la majorité — sont analysés quand même** : les mesures
comportementales du §3 ne dépendent pas du rapprochement. Seule la comparaison directe à la
base (§4) le requiert.

---

## 3. Mesures

### 3.1 Reconstruction du risque quand le stop est absent

La plupart des traders ne placent pas de stop enregistré. Sans risque, pas de R, donc pas
d'espérance — et l'indicateur principal du produit devient inutilisable.

**Trois niveaux, dans cet ordre, la méthode retenue étant toujours affichée :**

| Niveau | Condition | Risque retenu |
|---|---|---|
| 1 | Stop présent dans le fichier | `|entrée − stop|` |
| 2 | Absent, mais l'utilisateur déclare un risque habituel en % | Converti en distance de prix depuis le volume |
| 3 | Aucune information | **Excursion défavorable maximale médiane** de ses propres trades perdants, calculée sur ses données. Résultats marqués « risque estimé » partout où ils apparaissent |

Le niveau 3 est explicitement moins fiable. Il est **affiché comme tel**, jamais dissimulé.

### 3.2 Les huit mesures comportementales

Toutes calculées à partir des trades de l'utilisateur et de **nos** données de marché, ce qui
permet de mesurer ce que son relevé ne contient pas.

| # | Mesure | Calcul | Ce qu'elle révèle |
|---|---|---|---|
| 1 | **Espérance nette en R** | Moyenne des R nets | Le seul chiffre qui dit s'il gagne |
| 2 | **Asymétrie gain/perte** | `|perte moyenne en R| / gain moyen en R` | > 1 : il coupe ses gains et laisse courir ses pertes — la cause de perte la plus répandue |
| 3 | **Capture du mouvement favorable** | Sur les gagnants : `(sortie − entrée) / excursion favorable maximale` | Sortie prématurée. Une capture à 40 % signifie qu'il laisse 60 % du mouvement disponible |
| 4 | **Dimensionnement de revanche** | Corrélation entre le risque du trade `n` et le résultat du trade `n−1` | Corrélation négative : il augmente sa mise après une perte. Marqueur comportemental le plus destructeur |
| 5 | **Délai après perte** | Délai médian avant le trade suivant, après un gain contre après une perte | Un délai plus court après une perte signale la précipitation |
| 6 | **Espérance par séance et par jour** | R net moyen groupé par séance et par jour de semaine | Les créneaux qui coûtent de l'argent |
| 7 | **Concentration corrélée** | Positions simultanées sur des paires de corrélation > 0,7 | Le risque réellement pris dépasse le risque cru |
| 8 | **Série de pertes observée contre attendue** | Plus longue série réelle, comparée à celle attendue pour son taux de réussite | Distingue une malchance normale d'une dégradation réelle |

### 3.3 Chiffrer chaque constat en R

Toute mesure est convertie en **coût estimé, exprimé en R par trade** : c'est ce qui permet de
les classer et de ne montrer que ce qui compte.

Exemple pour la mesure 3 :

```
coût = (1 − taux_de_capture) × excursion_favorable_moyenne_des_gagnants × part_de_gagnants
```

---

## 4. L'écart comportemental

*La fonction qui distingue le produit de tous les journaux de trading existants : eux n'ont
aucune base de référence à laquelle comparer.*

Pour les trades rapprochés d'une détection :

| Comparaison | Formule |
|---|---|
| Écart de résultat | `R net utilisateur − R net de la détection` |
| Écart d'entrée | Nombre de bougies entre son entrée et celle de la détection |
| Écart de sortie | Sa sortie en R, comparée à l'objectif de la détection |
| Écart de sélection | Score moyen des configurations qu'il a prises, comparé au score moyen des annoncées |

L'écart de sélection est souvent le plus révélateur : il montre si le problème est **ce qu'il
choisit** ou **comment il l'exécute**. Ce sont deux corrections opposées.

### Règle d'affichage — au plus trois constats

> **On affiche au maximum trois constats, classés par coût estimé en R décroissant.**

Un tableau de bord de quarante indicateurs ne change aucun comportement : il donne
l'impression d'un diagnostic sans en produire. Trois constats chiffrés, hiérarchisés, avec le
coût de chacun.

```
1.  Vous sortez trop tôt de vos gagnants.
    Capture moyenne du mouvement favorable : 41 %.
    Coût estimé : 0,34 R par trade  ·  sur 128 trades

2.  Vous augmentez votre mise après une perte.
    Corrélation risque / résultat précédent : −0,38.
    Coût estimé : 0,19 R par trade  ·  sur 128 trades

3.  Vos trades du vendredi après-midi perdent.
    Espérance : −0,44 R contre +0,02 R le reste de la semaine.
    Coût estimé : 0,08 R par trade  ·  sur 21 trades
```

Chaque constat est **cliquable** vers la liste exacte des trades concernés. Sans cette liste,
le constat reste une affirmation ; avec elle, il devient vérifiable — la même exigence que
pour le journal public.

### Seuil de fiabilité

Aucun constat n'est affiché sous **30 trades** pour une mesure globale, ni sous **15 trades**
pour une mesure segmentée (par séance, par jour). En dessous : « pas encore assez de trades
pour conclure — 12 sur 30 ». Application au journal personnel de la même règle que pour les
statistiques publiques (cahier des charges §7).

---

## 5. Données personnelles

| Règle | Application |
|---|---|
| Chiffrement au repos | Toutes les tables de trades utilisateur |
| Suppression | Effective en moins de 30 jours, sauvegardes comprises, sur simple demande |
| Export | Format ouvert, à tout moment, sans condition |
| **Usage agrégé** | **Consentement explicite, séparé et révocable, refusé par défaut** |
| Cloisonnement | Les données d'un utilisateur ne servent jamais à produire un affichage vu par un autre, hors agrégat consenti et anonymisé |

**Point stratégique :** la base comportementale agrégée est le second avantage concurrentiel du
produit (cahier des charges §2), et elle grandit avec le nombre d'utilisateurs, pas avec le
temps. Elle ne peut se constituer **que** sur consentement explicite. Le demander clairement,
en expliquant ce qu'il apporte à l'utilisateur, produit un taux d'acceptation bien supérieur à
une case précochée dans des conditions générales — et c'est la seule pratique défendable.

---

## 6. Critères d'acceptation

| # | Critère |
|---|---|
| 1 | Un rapport MT4 et un rapport MT5 réels s'importent sans intervention manuelle |
| 2 | Le décalage horaire du serveur est détecté automatiquement, affiché, et modifiable |
| 3 | Un fichier sans stop produit quand même une espérance, marquée « risque estimé » |
| 4 | Les huit mesures sont calculées et chacune est convertie en coût en R |
| 5 | L'écran final n'affiche jamais plus de trois constats |
| 6 | Chaque constat renvoie à la liste exacte des trades concernés |
| 7 | Sous les seuils, l'écran affiche le nombre de trades manquants, jamais un chiffre |
| 8 | Le consentement à l'usage agrégé est refusé par défaut et révocable en un clic |
