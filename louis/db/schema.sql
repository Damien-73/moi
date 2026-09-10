-- Louis — modèle de données
--
-- C'est la seule partie irréversible du produit. L'hébergeur, le framework,
-- le modèle d'IA et l'interface se remplacent en quelques jours. Ceci, non.
--
-- Trois règles absolues, encodées ici et pas seulement écrites dans le cahier :
--   1. Aucune affirmation sans provenance      -> assertions.source_message_id NOT NULL
--   2. Jamais d'écrasement d'une croyance      -> valide_jusqu_a + remplace_id
--   3. Toutes les sources n'ont pas le même poids -> assertions.source_type

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------- personnes

create table utilisateurs (
  id              uuid primary key default gen_random_uuid(),
  email           text unique not null,
  prenom          text,
  -- Le nom que CETTE personne donne à son assistant. « Louis » par défaut.
  -- C'est la réponse au problème du genre : la marque est Louis, l'instance
  -- porte le nom que chacun lui donne.
  nom_assistant   text not null default 'Louis',
  mode            text not null default 'normal'
                    check (mode in ('normal', 'dur')),
  -- L'heure du rendez-vous quotidien, choisie par la personne.
  heure_rdv       time,
  fuseau          text not null default 'Europe/Paris',
  majeur_confirme boolean not null default false,
  cree_le         timestamptz not null default now()
);

-- ------------------------------------------------------------- transcriptions

-- Source de provenance de toute assertion. Rien n'entre dans le modèle
-- sans pouvoir désigner le message qui l'a produit.
create table messages (
  id              uuid primary key default gen_random_uuid(),
  utilisateur_id  uuid not null references utilisateurs(id) on delete cascade,
  role            text not null check (role in ('personne', 'assistant')),
  contenu         text not null,
  -- Un échange de détresse est CONSERVÉ mais EXCLU du modèle : quelqu'un qui
  -- s'effondre un soir ne doit pas être défini par ce soir-là pendant des années.
  exclu_du_modele boolean not null default false,
  cree_le         timestamptz not null default now()
);

create index on messages (utilisateur_id, cree_le desc);

-- -------------------------------------------------------------------- le twin

-- Une assertion n'est jamais modifiée. Quand la croyance change, on clôt
-- la validité de l'ancienne et on en crée une nouvelle qui la remplace.
-- C'est ce qui permet de raconter comment quelqu'un est devenu ce qu'il est.
create table assertions (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,

  sujet             text not null,   -- 'contraintes', 'objectifs', 'rythme'...
  predicat          text not null,   -- 'temps_disponible', 'tolerance_risque'...
  valeur            text not null,

  nature            text not null
                      check (nature in ('fait', 'observation', 'hypothese')),
  confiance         real not null default 0.5
                      check (confiance >= 0 and confiance <= 1),

  -- Le poids de la source. L'agenda ne ment pas, un pari résolu ne ment pas,
  -- une déclaration, si. L'écart entre les deux est lui-même une donnée.
  source_type       text not null
                      check (source_type in ('declaration','agenda','pari_resolu','action_observee')),
  source_message_id uuid not null references messages(id),

  valide_de         timestamptz not null default now(),
  valide_jusqu_a    timestamptz,               -- null = croyance actuelle
  remplace_id       uuid references assertions(id),
  -- Pourquoi la croyance a changé. C'est ce qui alimente « j'ai changé d'avis sur toi ».
  motif_revision    text
);

create index on assertions (utilisateur_id, sujet, predicat);
-- L'état courant du twin : les assertions encore valides.
create index on assertions (utilisateur_id) where valide_jusqu_a is null;

-- ----------------------------------------------------------------- objectifs

create table objectifs (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,
  formulation       text not null,             -- ce que la personne a dit vouloir
  objectif_profond  text,                      -- hypothèse, jamais un verdict
  profond_confirme  boolean not null default false,
  priorite          int  not null default 3,
  echeance          date,
  statut            text not null default 'actif'
                      check (statut in ('actif','atteint','abandonne','suspendu')),
  cree_le           timestamptz not null default now()
);

-- ---------------------------------------------------------- carnet de décisions

create table decisions (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,
  objectif_id       uuid references objectifs(id) on delete set null,
  contexte          text not null,
  options           jsonb not null default '[]'::jsonb,
  recommandation    text,
  -- Les deux arguments réels entre lesquels l'assistant a hésité.
  argument_pour     text,
  argument_contre   text,
  decision_prise    text,
  cree_le           timestamptz not null default now()
);

-- La brique qui n'existe nulle part ailleurs : ce que l'assistant croit
-- qu'il va se passer, écrit à l'avance, avec une date, et vérifié après.
create table predictions (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,
  decision_id       uuid references decisions(id) on delete set null,
  enonce            text not null,
  echeance          date not null,
  confiance         real not null default 0.5
                      check (confiance >= 0 and confiance <= 1),
  -- Le duel : la personne se prédit elle-même avant de voir l'avis de l'assistant.
  pari_personne     boolean,
  resultat          text check (resultat in ('juste','faux','partiel')),
  resolue_le        timestamptz,
  cree_le           timestamptz not null default now()
);

create index on predictions (utilisateur_id, echeance) where resultat is null;

-- -------------------------------------------------------------------- actions

create table actions (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,
  libelle           text not null,
  -- Les trois niveaux. Rien d'irréversible n'est jamais automatique.
  niveau            text not null
                      check (niveau in ('annulable','sortante','engageante')),
  statut            text not null default 'prevue'
                      check (statut in ('prevue','faite','echouee','annulee')),
  -- Règle absolue : ne jamais prétendre avoir agi. Une action 'faite' sans
  -- preuve est un bug, pas une donnée.
  preuve            text,
  message_echec     text,
  cree_le           timestamptz not null default now(),
  faite_le          timestamptz
);

-- --------------------------------------------------------------------- journal

create table evenements (
  id                uuid primary key default gen_random_uuid(),
  utilisateur_id    uuid not null references utilisateurs(id) on delete cascade,
  type              text not null,
  charge            jsonb not null default '{}'::jsonb,
  cree_le           timestamptz not null default now()
);

create index on evenements (utilisateur_id, cree_le desc);

-- ---------------------------------------------------------------- vue du twin

-- Ce que l'assistant croit aujourd'hui. C'est cette vue qui alimente
-- l'écran « ce que je sais de toi ».
create view twin_actuel as
  select a.*
    from assertions a
    join messages m on m.id = a.source_message_id
   where a.valide_jusqu_a is null
     and m.exclu_du_modele = false;
