# Louis — V1

Assistant personnel. Première brique : **l'écran d'entrée**.

---

## Faire tourner l'application sur ton ordinateur

Il te faut **Node.js version 20 ou plus** — à installer une fois depuis nodejs.org.

Ensuite, dans un terminal, depuis ce dossier :

```bash
npm install     # une seule fois, installe les dépendances
npm run dev     # lance l'application
```

Puis ouvre **http://localhost:3000** dans ton navigateur.

Pour arrêter : `Ctrl + C` dans le terminal.

> **Regarde-la sur ton téléphone.** C'est un produit mobile avant tout.
> Dans les outils de développement du navigateur (`F12`), active l'affichage
> mobile. C'est le seul format qui compte pour juger cet écran.

### Vérifier que rien n'est cassé

```bash
npm run typecheck   # vérifie qu'il n'y a pas d'erreur de code
npm run build       # vérifie que l'application se construit
```

Ces deux commandes doivent passer **avant** chaque envoi de code. Toujours.

---

## Ce qui est construit

| Fichier | Ce que c'est |
|---|---|
| `db/schema.sql` | **Le modèle de données.** La seule partie irréversible du produit. |
| `src/lib/entree.ts` | Le réservoir de questions et le sélecteur adaptatif |
| `src/lib/diagnostic.ts` | La construction du brouillon de fin d'entrée |
| `src/app/page.tsx` | L'écran d'entrée, de l'accueil à la première action |

### Le parcours, tel qu'il tourne aujourd'hui

1. **L'accueil** — Louis se présente, propose d'être renommé, et dit franchement
   qu'il ne sait encore rien.
2. **Les questions** — huit au maximum, choisies une par une selon ce qui manque.
   Jamais une question dont la réponse est déjà connue.
3. **Le brouillon** — « voilà ce que je crois avoir compris, dis-moi ce que j'ai
   faux », plus la liste de ce qu'il ne sait pas encore.
4. **La première action** — proposée, et **annoncée comme non faite**, parce
   qu'aucun agenda n'est connecté.

Ce dernier point n'est pas un manque : c'est la règle la plus importante du
produit qui s'applique. **Ne jamais prétendre avoir agi.** Le jour où l'agenda
sera branché, la phrase changera parce que l'action sera réellement exécutée.

---

## Ce qui n'est pas encore là

- Aucune base de données branchée : les réponses vivent dans la page et
  disparaissent au rechargement
- Aucun appel à un modèle d'IA — le diagnostic est composé par règles
- Pas de compte, pas d'agenda, pas de rendez-vous quotidien

**Où se branche le modèle :** dans `src/lib/diagnostic.ts`, fonction
`construireDiagnostic`. Elle est isolée exprès. Quand la clé d'API sera là,
cette fonction devient un appel au modèle avec sortie contrainte par schéma,
et **rien d'autre ne bouge dans l'application**.

---

## Les trois règles encodées dans le modèle de données

Elles sont dans `db/schema.sql` et ne doivent jamais être assouplies :

1. **Aucune affirmation sans provenance.** `source_message_id` est obligatoire.
   Sans ça, impossible de répondre à « pourquoi tu penses ça ? ».
2. **Jamais d'écrasement.** Une croyance qui change n'est pas modifiée : on clôt
   sa validité et on en crée une nouvelle. C'est ce qui permet de raconter
   comment quelqu'un est devenu ce qu'il est.
3. **Toutes les sources n'ont pas le même poids.** L'agenda ne ment pas, un pari
   résolu ne ment pas, une déclaration si.

Une quatrième est encodée dans `messages.exclu_du_modele` : un échange de
détresse est **conservé mais exclu du modèle**. Quelqu'un qui s'effondre un soir
ne doit pas être défini par ce soir-là pendant des années.

---

## Note technique

`npm run dev` et `npm run build` utilisent l'option `--webpack`. C'est
volontaire : la version actuelle de Turbopack est en conflit avec Tailwind 4
(erreur `Missing field negated on ScannerOptions.sources`). Quand les versions
seront réconciliées, retirer `--webpack` des deux scripts dans `package.json`
et revérifier avec `npm run build`.
