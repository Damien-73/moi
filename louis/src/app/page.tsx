"use client";

import { useMemo, useState } from "react";
import {
  prochaineQuestion,
  progression,
  assezPourAgir,
  type Reponse,
} from "@/lib/entree";
import { construireDiagnostic } from "@/lib/diagnostic";

type Etape = "accueil" | "questions" | "diagnostic" | "suite";

export default function Entree() {
  const [etape, setEtape] = useState<Etape>("accueil");
  const [nom, setNom] = useState("Louis");
  const [renommer, setRenommer] = useState(false);
  const [reponses, setReponses] = useState<Reponse[]>([]);
  const [brouillon, setBrouillon] = useState("");
  const [correction, setCorrection] = useState("");
  const [corrige, setCorrige] = useState(false);

  const question = useMemo(() => prochaineQuestion(reponses), [reponses]);
  const diagnostic = useMemo(() => construireDiagnostic(reponses), [reponses]);

  function repondre() {
    const texte = brouillon.trim();
    if (!texte || !question) return;
    setReponses((r) => [
      ...r,
      { questionId: question.id, creneau: question.creneau, texte },
    ]);
    setBrouillon("");
  }

  // On s'arrête dès qu'il n'y a plus de question utile, ou dès qu'on en sait
  // assez pour agir. Deux erreurs interdites : trop peu, et l'interrogatoire.
  const fini = question === null || (assezPourAgir(reponses) && reponses.length >= 5);

  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-xl flex-col px-5 pb-10 pt-8">
      <header className="mb-8 flex items-baseline justify-between">
        <span className="text-lg font-semibold tracking-tight">{nom}</span>
        {etape === "questions" && (
          <span className="text-xs text-encre-faible tabular-nums">
            {reponses.length}/8
          </span>
        )}
      </header>

      {etape === "questions" && (
        <div
          className="mb-8 h-px w-full bg-trait"
          role="progressbar"
          aria-valuenow={Math.round(progression(reponses) * 100)}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="h-px bg-accent transition-all duration-500"
            style={{ width: `${progression(reponses) * 100}%` }}
          />
        </div>
      )}

      {/* ---------------------------------------------------------- accueil */}
      {etape === "accueil" && (
        <section className="apparait flex flex-1 flex-col justify-center gap-6">
          <h1 className="text-3xl leading-tight font-semibold tracking-tight">
            Je m'appelle Louis.
          </h1>

          <p className="text-encre-douce leading-relaxed">
            Mais c'est le tien. Tu peux m'appeler comme tu veux — maintenant ou
            plus tard.
          </p>

          {renommer ? (
            <input
              id="nom-assistant"
              autoFocus
              value={nom}
              onChange={(e) => setNom(e.target.value)}
              onBlur={() => !nom.trim() && setNom("Louis")}
              className="w-full rounded-lg border border-trait bg-surface px-4 py-3 text-lg outline-none focus:border-accent"
              aria-label="Le nom de ton assistant"
            />
          ) : (
            <button
              onClick={() => setRenommer(true)}
              className="self-start text-sm text-accent underline underline-offset-4"
            >
              Lui donner un autre nom
            </button>
          )}

          <p className="text-encre-douce leading-relaxed">
            Je ne te connais pas encore, donc ce que je vais te dire aujourd'hui
            vaut ce que ça vaut. Réponds à quelques questions et je serai
            nettement plus utile.
          </p>

          <button
            onClick={() => setEtape("questions")}
            className="mt-2 rounded-xl bg-accent px-6 py-4 text-base font-medium text-fond"
          >
            On règle quoi aujourd'hui ?
          </button>

          <p className="text-xs leading-relaxed text-encre-faible">
            Pas de compte à créer pour l'instant. Rien n'est envoyé nulle part.
          </p>
        </section>
      )}

      {/* -------------------------------------------------------- questions */}
      {etape === "questions" && !fini && question && (
        <section key={question.id} className="apparait flex flex-1 flex-col gap-5">
          <h2 className="text-2xl leading-snug font-medium tracking-tight text-balance">
            {question.texte}
          </h2>
          {question.aide && (
            <p className="text-sm text-encre-faible">{question.aide}</p>
          )}

          <textarea
            id={`reponse-${question.id}`}
            autoFocus
            rows={5}
            value={brouillon}
            onChange={(e) => setBrouillon(e.target.value)}
            placeholder="Écris comme ça vient."
            className="w-full resize-none rounded-xl border border-trait bg-surface px-4 py-3 leading-relaxed outline-none placeholder:text-encre-faible focus:border-accent"
          />

          <div className="mt-auto flex items-center gap-3 pt-4">
            <button
              onClick={repondre}
              disabled={!brouillon.trim()}
              className="flex-1 rounded-xl bg-accent px-6 py-4 font-medium text-fond disabled:opacity-30"
            >
              Continuer
            </button>
            <button
              onClick={() =>
                setReponses((r) => [
                  ...r,
                  { questionId: question.id, creneau: question.creneau, texte: "" },
                ])
              }
              className="px-3 py-4 text-sm text-encre-faible"
            >
              Passer
            </button>
          </div>
        </section>
      )}

      {/* ----------------------------------------- fin des questions -> bascule */}
      {etape === "questions" && fini && (
        <section className="apparait flex flex-1 flex-col justify-center gap-6">
          <h2 className="text-2xl font-medium tracking-tight">
            J'en sais assez pour te dire quelque chose d'utile.
          </h2>
          <p className="text-encre-douce leading-relaxed">
            Je pourrais continuer à te poser des questions. Je préfère te montrer
            ce que j'ai compris et me faire corriger.
          </p>
          <button
            onClick={() => setEtape("diagnostic")}
            className="rounded-xl bg-accent px-6 py-4 font-medium text-fond"
          >
            Montre-moi
          </button>
        </section>
      )}

      {/* ------------------------------------------------------- diagnostic */}
      {etape === "diagnostic" && (
        <section className="apparait flex flex-1 flex-col gap-7">
          <div>
            <p className="mb-2 text-xs uppercase tracking-widest text-accent">
              Brouillon
            </p>
            <h2 className="text-2xl leading-snug font-medium tracking-tight text-balance">
              Voilà ce que je crois avoir compris. Dis-moi ce que j'ai faux.
            </h2>
          </div>

          <ul className="flex flex-col gap-3">
            {diagnostic.comprehension.map((ligne, i) => (
              <li
                key={i}
                className="rounded-xl border border-trait bg-surface px-4 py-3 leading-relaxed"
              >
                {ligne}
              </li>
            ))}
          </ul>

          {diagnostic.obstacle && (
            <div className="border-l-2 border-accent pl-4">
              <p className="mb-1 text-xs uppercase tracking-widest text-encre-faible">
                Ce qui me semble te bloquer
              </p>
              <p className="leading-relaxed">{diagnostic.obstacle}</p>
            </div>
          )}

          {diagnostic.incertitudes.length > 0 && (
            <div>
              <p className="mb-2 text-xs uppercase tracking-widest text-encre-faible">
                Ce que je ne sais pas encore
              </p>
              <p className="text-sm leading-relaxed text-encre-douce">
                {diagnostic.incertitudes.join(" · ")}
              </p>
            </div>
          )}

          <div className="flex flex-col gap-3">
            <textarea
              id="correction"
              rows={3}
              value={correction}
              onChange={(e) => setCorrection(e.target.value)}
              placeholder="Qu'est-ce que j'ai faux ?"
              className="w-full resize-none rounded-xl border border-trait bg-surface px-4 py-3 leading-relaxed outline-none placeholder:text-encre-faible focus:border-accent"
            />
            {corrige && (
              <p className="text-sm text-accent">
                Noté. Je corrige ce que je croyais savoir — l'ancienne version
                reste dans ton historique.
              </p>
            )}
            <div className="flex gap-3">
              <button
                onClick={() => {
                  if (correction.trim()) setCorrige(true);
                  setEtape("suite");
                }}
                className="flex-1 rounded-xl bg-accent px-6 py-4 font-medium text-fond"
              >
                {correction.trim() ? "Corrige et continue" : "C'est juste"}
              </button>
            </div>
          </div>
        </section>
      )}

      {/* ------------------------------------------------------------ suite */}
      {etape === "suite" && (
        <section className="apparait flex flex-1 flex-col gap-7">
          <h2 className="text-2xl leading-snug font-medium tracking-tight">
            La première chose à faire
          </h2>

          {diagnostic.action && (
            <div className="rounded-xl border border-trait bg-surface px-4 py-4">
              <p className="leading-relaxed">{diagnostic.action.libelle}</p>
              <p className="mt-3 text-sm text-encre-faible">
                Action annulable — tu pourras la défaire d'un geste.
              </p>
            </div>
          )}

          {/* Règle absolue : ne jamais prétendre avoir agi. Sans agenda
              connecté, l'action est PRÊTE, pas FAITE. On le dit. */}
          <div className="border-l-2 border-encre-faible pl-4">
            <p className="text-sm leading-relaxed text-encre-douce">
              Je ne l'ai pas encore fait : je n'ai pas accès à ton agenda.
              Connecte-le et je le bloque moi-même — c'est le moment où je
              commence à travailler au lieu de te conseiller.
            </p>
          </div>

          <button
            className="rounded-xl bg-accent px-6 py-4 font-medium text-fond"
            onClick={() => alert("Connexion de l'agenda : prochaine étape à construire.")}
          >
            Connecter mon agenda
          </button>

          <p className="text-sm leading-relaxed text-encre-faible">
            Demain à la même heure, je t'ouvrirai avec ce que j'aurai remarqué.
            Pas une notification pour te faire revenir : quelque chose à te dire.
          </p>
        </section>
      )}
    </main>
  );
}
