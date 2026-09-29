"""Lance un setup sur une ou plusieurs paires et écrit le rapport.

In-sample (étapes 4 et 5) :
    python -m src.backtest.runner --setup zone_a_zone --pairs EURUSD
    python -m src.backtest.runner --setup zone_a_zone            # 7 paires

Out-of-sample (étape 6, UNE SEULE FOIS, après accord) :
    OOS_ACCORD=zone_a_zone python -m src.backtest.runner --setup zone_a_zone --oos
"""
from __future__ import annotations

import argparse
import importlib
from datetime import datetime, timezone

import pandas as pd

from src.backtest.engine import Market, run_backtest
from src.backtest.metrics import per_pair, summarize
from src.config import PAIRS, RESULTS_DIR
from src.data.quality import clean
from src.data.resample import mid, resample
from src.data.store import load_m1
from src.validation.criteria import evaluate, suspicious
from src.validation.oos_lock import unlock_oos
from src.validation.random_baseline import permutation_test
from src.validation.trials import count_trials, log_trial

EXIT_MODES = ("simple", "partial")
LIMITS = [
    "Filtre annonces non appliqué : aucun historique fiable du calendrier économique disponible.",
    "Swap : valeurs estimées (config), pas des relevés de courtier.",
    "Capital : intérêts composés dans l'ordre de clôture des trades ; les positions simultanées "
    "sur plusieurs paires sont approximées.",
    "Bougies M1 sans cotation (minutes « plates ») absentes des données Dukascopy : les trous courts sont normaux.",
]


def prepare(pair: str, period: str, token=None, timeframe: str = "H1") -> tuple[Market, pd.DataFrame]:
    m1, _ = clean(load_m1(pair, period, token))
    return Market.from_df(pair, m1), mid(resample(m1, timeframe))


def run(setup, pairs: list[str], period: str, token=None) -> tuple[dict, dict[str, pd.DataFrame]]:
    markets, trades = {}, {m: [] for m in EXIT_MODES}
    for pair in pairs:
        mk, bars = prepare(pair, period, token)
        markets[pair] = mk
        sig = setup.detect(bars, **setup.PARAMS)
        for mode in EXIT_MODES:
            trades[mode].append(run_backtest(mk, sig, exit_mode=mode))
        print(f"{pair}: {len(sig)} signaux", flush=True)
    return markets, {m: pd.concat(v, ignore_index=True) for m, v in trades.items()}


def _fmt(x) -> str:
    if isinstance(x, float):
        return f"{x:.3f}"
    return str(x)


def _summary_lines(title: str, s: dict) -> list[str]:
    return [
        f"### {title}", "",
        "| indicateur | valeur |", "|---|---|",
        f"| trades | {s['trades']} |",
        f"| win rate | {s['win_rate']:.1%} |",
        f"| espérance par trade | {s['expectancy_R']:+.3f} R |",
        f"| profit factor | {s['profit_factor']:.2f} |",
        f"| plus longue série de pertes | {s['longest_losing_streak']} |",
        f"| rendement total, risque 1 % | {s['return_1pct']:+.1%} |",
        f"| drawdown max, risque 1 % | {s['max_dd_1pct']:.1%} |",
        f"| drawdown Monte Carlo 95e pct, risque 1 % | {s['mc_dd95_1pct']:.1%} |",
        f"| rendement total, risque 2 % | {s['return_2pct']:+.1%} |",
        f"| drawdown max, risque 2 % | {s['max_dd_2pct']:.1%} |",
        f"| drawdown Monte Carlo 95e pct, risque 2 % | {s['mc_dd95_2pct']:.1%} |",
        "",
    ]


def write_report(setup, pairs, period, trades, perm, n_trials, is_trades=None, path=None) -> str:
    name = setup.NAME
    lines = [f"# Rapport — {name} — {'OUT-OF-SAMPLE' if period == 'oos' else 'in-sample 2014–2022'}", "",
             f"Généré le {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC. Paires : {', '.join(pairs)}.",
             f"Paramètres : `{setup.PARAMS}`. Essais journalisés pour ce setup : **{n_trials}**.", ""]
    for mode in EXIT_MODES:
        tr = trades[mode]
        if suspicious(tr):
            lines += [f"> ATTENTION ({mode}) : profit factor > 2 ou win rate > 65 %. Règle 8 : "
                      "résultat à traiter comme un bug possible avant toute conclusion.", ""]
        lines += _summary_lines(f"Sortie {mode}", summarize(tr))
        pp = per_pair(tr)
        lines += ["| paire | trades | win rate | espérance R | PF | total R |", "|---|---|---|---|---|---|"]
        for p, r in pp.iterrows():
            lines.append(f"| {p} | {int(r['trades'])} | {r['win_rate']:.1%} | {r['expectancy_R']:+.3f} | "
                         f"{r['profit_factor']:.2f} | {r['total_R']:+.1f} |")
        lines.append("")
    p = perm["simple"]
    lines += ["## Référence entrées aléatoires (sortie simple)", "",
              f"Espérance setup {p['observed_expectancy_R']:+.3f} R ; hasard : moyenne "
              f"{p['random_mean_expectancy_R']:+.3f} R, 95e percentile {p['random_p95_expectancy_R']:+.3f} R ; "
              f"p = {p['p_value']:.4f} ({p['n_sims']} simulations).", ""]
    base = is_trades["simple"] if is_trades is not None else trades["simple"]
    oos = trades["simple"] if period == "oos" else None
    crit = evaluate(base, p["p_value"] if period != "oos" else perm["is_p_value"], oos)
    lines += ["## Critères de validation (sortie simple, après coûts)", "",
              "| critère | valeur | seuil | OK |", "|---|---|---|---|"]
    lines += [f"| {c['critere']} | {_fmt(c['valeur'])} | {c['seuil']} | {'oui' if c['ok'] else 'NON'} |" for c in crit]
    if period == "oos":
        verdict = "VALIDÉ" if all(c["ok"] for c in crit) else "REJETÉ"
        lines += ["", f"## Verdict : **{verdict}**"]
    lines += ["", "## Limites", ""] + [f"- {x}" for x in LIMITS]
    text = "\n".join(lines) + "\n"
    if path is None:
        suffix = "" if period == "oos" else ("_is" if len(pairs) > 1 else f"_is_{pairs[0]}")
        path = RESULTS_DIR / f"report_{name}{suffix}.md"
    path.write_text(text, encoding="utf-8")
    return str(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", required=True)
    ap.add_argument("--pairs", nargs="+", default=PAIRS)
    ap.add_argument("--sims", type=int, default=1000)
    ap.add_argument("--oos", action="store_true")
    args = ap.parse_args()
    setup = importlib.import_module(f"src.setups.{args.setup}")

    if not args.oos:
        markets, trades = run(setup, args.pairs, "is")
        for mode in EXIT_MODES:
            log_trial(setup.NAME, "is", args.pairs, mode, setup.PARAMS, summarize(trades[mode], mc_sims=10))
        perm = {"simple": permutation_test(markets, trades["simple"], n_sims=args.sims)}
        print(write_report(setup, args.pairs, "is", trades, perm, count_trials(setup.NAME)))
        return

    token = unlock_oos(setup.NAME, setup.PARAMS)  # refuse si non figé, sans accord, ou déjà utilisé
    is_markets, is_trades = run(setup, args.pairs, "is")
    is_p = permutation_test(is_markets, is_trades["simple"], n_sims=args.sims)["p_value"]
    del is_markets
    markets, trades = run(setup, args.pairs, "oos", token)
    perm = {"simple": permutation_test(markets, trades["simple"], n_sims=args.sims) | {"is_p_value": is_p}}
    print(write_report(setup, args.pairs, "oos", trades, perm, count_trials(setup.NAME), is_trades))


if __name__ == "__main__":
    main()
