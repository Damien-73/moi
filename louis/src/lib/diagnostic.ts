// Le diagnostic de fin d'entrée.
//
// Il n'est JAMAIS présenté comme un verdict. Toujours comme un brouillon :
// « voilà ce que je crois avoir compris, dis-moi ce que j'ai faux ».
// La correction que la personne apporte vaut dix réponses à des questions —
// c'est la meilleure donnée que le produit obtiendra jamais.

import type { Reponse, Creneau } from "./entree";

export type Diagnostic = {
  comprehension: string[];
  obstacle: string | null;
  action: { libelle: string; niveau: "annulable" } | null;
  incertitudes: string[];
};

function reponse(reponses: Reponse[], creneau: Creneau): string | null {
  const r = reponses.find((x) => x.creneau === creneau);
  const t = r?.texte.trim();
  return t ? t : null;
}

function extrait(texte: string, max = 120): string {
  const t = texte.replace(/\s+/g, " ").trim();
  return t.length <= max ? t : t.slice(0, max - 1).trimEnd() + "…";
}

/**
 * Construit le diagnostic à partir des seules réponses données.
 *
 * ---------------------------------------------------------------------------
 * ICI SE BRANCHE LE MODÈLE.
 * Cette version compose le diagnostic par règles, sans appel externe, pour que
 * l'écran tourne et soit testable dès aujourd'hui. Quand la clé d'API sera en
 * place, cette fonction devient un appel au modèle avec sortie contrainte par
 * schéma — le reste de l'application ne bouge pas d'une ligne.
 *
 * Deux règles à ne pas perdre au passage :
 *   - le modèle n'écrit jamais en base : il renvoie ce JSON, du code écrit
 *   - ce qui n'est pas su est dit, jamais comblé
 * ---------------------------------------------------------------------------
 */
export function construireDiagnostic(reponses: Reponse[]): Diagnostic {
  const comprehension: string[] = [];
  const incertitudes: string[] = [];

  const resultat = reponse(reponses, "resultat_vise");
  const temps = reponse(reponses, "temps_disponible");
  const bloque = reponse(reponses, "ce_qui_bloque");
  const contrainte = reponse(reponses, "contrainte_principale");
  const tentatives = reponse(reponses, "tentatives_passees");
  const rythme = reponse(reponses, "rythme_soutenable");
  const energie = reponse(reponses, "energie");

  if (resultat) comprehension.push(`Ce que tu veux régler : ${extrait(resultat)}`);
  if (contrainte)
    comprehension.push(`Ce qui n'est pas négociable : ${extrait(contrainte)}`);
  if (temps) comprehension.push(`Le temps que tu as vraiment : ${extrait(temps)}`);
  if (tentatives)
    comprehension.push(`Ce que tu as déjà tenté : ${extrait(tentatives)}`);
  if (rythme) comprehension.push(`Le rythme qui tient chez toi : ${extrait(rythme)}`);

  const obstacle = bloque ? extrait(bloque, 160) : null;

  if (!temps) incertitudes.push("combien de temps tu as réellement par semaine");
  if (!contrainte) incertitudes.push("ce qui n'est pas négociable dans ta vie");
  if (!tentatives) incertitudes.push("ce que tu as déjà essayé, et ce que ça a donné");
  if (!energie) incertitudes.push("à quel moment de la journée tu es disponible");

  // La première action est toujours de niveau « annulable ». Rien
  // d'irréversible, rien qui sorte vers l'extérieur, rien qui engage.
  const action = resultat
    ? {
        libelle: energie
          ? `Bloquer un créneau de 30 minutes (${extrait(energie, 40)}) pour la première étape`
          : "Bloquer un créneau de 30 minutes cette semaine pour la première étape",
        niveau: "annulable" as const,
      }
    : null;

  return { comprehension, obstacle, action, incertitudes };
}
