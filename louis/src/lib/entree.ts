// L'entrée — les trente premières minutes.
//
// Ce n'est pas un questionnaire : c'est un réservoir de questions et un
// sélecteur. À chaque tour, on pose la question qui remplit le créneau
// d'information manquant le plus utile — jamais une question dont on
// connaît déjà la réponse.
//
// Règles du cahier des charges appliquées ici :
//   - 8 à 10 questions à l'entrée, pas trente
//   - chaque question doit servir à quelque chose que la personne verra
//     dans les vingt minutes
//   - l'agenda ne se demande qu'APRÈS avoir donné quelque chose

export type Creneau =
  | "situation"
  | "resultat_vise"
  | "echeance"
  | "temps_disponible"
  | "contrainte_principale"
  | "tentatives_passees"
  | "ce_qui_bloque"
  | "rythme_soutenable"
  | "energie"
  | "tolerance_risque";

export type Question = {
  id: string;
  creneau: Creneau;
  texte: string;
  aide?: string;
  /** Créneaux qui doivent déjà être remplis pour que la question ait du sens. */
  requiert?: Creneau[];
  /** Poids de base : plus il est haut, plus la question est prioritaire. */
  poids: number;
};

/**
 * Le réservoir. Il est volontairement plus grand que le nombre de questions
 * posées : deux personnes ne doivent pas recevoir le même parcours.
 */
export const RESERVOIR: Question[] = [
  {
    id: "q_situation",
    creneau: "situation",
    texte: "Raconte-moi où tu en es aujourd'hui, en deux ou trois phrases.",
    aide: "Pas besoin d'être organisé. Ce qui te vient.",
    poids: 100,
  },
  {
    id: "q_resultat",
    creneau: "resultat_vise",
    texte: "Si on règle une seule chose ensemble, ce serait laquelle ?",
    aide: "Même si c'est flou. « Je ne sais pas » est une réponse valable.",
    poids: 95,
  },
  {
    id: "q_deja_essaye",
    creneau: "tentatives_passees",
    texte: "Tu as déjà essayé quelque chose là-dessus ? Qu'est-ce qui s'est passé ?",
    requiert: ["resultat_vise"],
    poids: 88,
  },
  {
    id: "q_bloque",
    creneau: "ce_qui_bloque",
    texte: "Qu'est-ce qui t'arrête, concrètement ?",
    aide: "Le vrai frein, pas celui qui fait bonne figure.",
    requiert: ["resultat_vise"],
    poids: 85,
  },
  {
    id: "q_temps",
    creneau: "temps_disponible",
    texte: "Tu as combien de temps par semaine, réellement ?",
    aide: "Le temps que tu as, pas celui que tu voudrais avoir.",
    poids: 82,
  },
  {
    id: "q_contrainte",
    creneau: "contrainte_principale",
    texte: "Qu'est-ce qui n'est pas négociable dans ta vie en ce moment ?",
    aide: "Un travail, quelqu'un, un lieu, de l'argent.",
    poids: 78,
  },
  {
    id: "q_rythme",
    creneau: "rythme_soutenable",
    texte:
      "Quand tu t'es lancé dans quelque chose et que tu as tenu, ça ressemblait à quoi ?",
    aide: "Beaucoup d'un coup, ou un peu tous les jours ?",
    requiert: ["tentatives_passees"],
    poids: 72,
  },
  {
    id: "q_energie",
    creneau: "energie",
    texte: "À quel moment de la journée tu es le plus disponible ?",
    poids: 65,
  },
  {
    id: "q_echeance",
    creneau: "echeance",
    texte: "Tu as une date en tête, ou une échéance qui te pousse ?",
    requiert: ["resultat_vise"],
    poids: 60,
  },
  {
    id: "q_risque",
    creneau: "tolerance_risque",
    texte:
      "Tu préfères avancer lentement en sécurité, ou vite quitte à te tromper ?",
    poids: 55,
  },
];

export type Reponse = { questionId: string; creneau: Creneau; texte: string };

/** Nombre de questions posées à l'entrée. Au-delà, c'est un interrogatoire. */
export const QUESTIONS_MAX = 8;

/**
 * Choisit la prochaine question : celle qui remplit un créneau encore vide,
 * dont les prérequis sont satisfaits, et de poids le plus élevé.
 * Renvoie null quand on en sait assez pour agir.
 */
export function prochaineQuestion(reponses: Reponse[]): Question | null {
  if (reponses.length >= QUESTIONS_MAX) return null;

  const remplis = new Set(reponses.map((r) => r.creneau));
  const posees = new Set(reponses.map((r) => r.questionId));

  const candidates = RESERVOIR.filter((q) => {
    if (posees.has(q.id)) return false;
    if (remplis.has(q.creneau)) return false; // jamais une question dont on a la réponse
    if (q.requiert?.some((c) => !remplis.has(c))) return false;
    return true;
  });

  if (candidates.length === 0) return null;
  return candidates.sort((a, b) => b.poids - a.poids)[0];
}

/** « Assez d'informations pour agir » : les quatre créneaux qui décident d'un plan. */
const CRENEAUX_ESSENTIELS: Creneau[] = [
  "resultat_vise",
  "temps_disponible",
  "ce_qui_bloque",
  "contrainte_principale",
];

export function assezPourAgir(reponses: Reponse[]): boolean {
  const remplis = new Set(reponses.map((r) => r.creneau));
  return CRENEAUX_ESSENTIELS.every((c) => remplis.has(c));
}

export function progression(reponses: Reponse[]): number {
  return Math.min(1, reponses.length / QUESTIONS_MAX);
}
