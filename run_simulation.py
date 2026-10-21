"""Lance une simulation de crise multi-agents.

Exemples :
    python run_simulation.py --essai --etapes 1
    python run_simulation.py                      # simulation complete, grand modele

Options :
    --scenario CHEMIN   fichier de scenario (defaut : agent/scenarios/operation_miroir.json)
    --etapes 1,2        ne joue que ces etapes
    --essai             tout sur le petit modele (quota separe), pour les tests
    --max-demandes N    demandes transmises entre acteurs par etape (defaut : 6)

Resultats dans runs/<date>_<scenario>/ : journal.jsonl (journal d'audit
complet) et resume.json.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

from agent.agent3_coordination.orchestrator import Orchestrator, load_scenario, new_run_dir
from agent.agent3_coordination.report import build as build_report

ROOT = Path(__file__).resolve().parent

STATUS_ICON = {"etayee": "OK ", "citation_douteuse": "~~ ", "non_etayee": "?? ", "citation_invalide": "XX "}


def show(entry: dict) -> None:
    ev = entry["evenement"]
    if ev == "simulation_debut":
        print(f"\n=== {entry['titre']} — mode {entry['mode']} ===")
    elif ev == "etape_revelee":
        print(f"\n--- Etape {entry['etape']} ({entry['moment']}) : {entry['titre']}")
        print(f"    informes : {', '.join(entry['destinataires'])}")
    elif ev.startswith("intervention_"):
        rep = entry.get("reponse") or {}
        kind = ev.replace("intervention_", "")
        head = f"    [{entry['agent']}] {kind} — {entry['jetons']} jetons, {entry['duree_s']} s"
        if entry.get("erreur"):
            head += f"  ! {entry['erreur']}"
        print(head)
        for c in entry.get("verification", [])[:6]:
            src = "; ".join(c["sources"]) or "aucune source"
            extra = f"  (mention non verifiee : {', '.join(c['mentions_non_verifiees'])})" if c["mentions_non_verifiees"] else ""
            print(f"       {STATUS_ICON.get(c['statut'], '   ')}{c['action'][:90]}  <- {src[:80]}{extra}")
        if kind == "analyse" and rep.get("synthese"):
            print(f"       synthese : {rep['synthese'][:300]}")
    elif ev == "demande_transmise":
        print(f"    -> {entry['de']} demande a {entry['a']} : {entry['objet'][:100]}")
    elif ev == "simulation_fin":
        r = entry["resume"]
        print(f"\n=== Fin : {r['interventions']} interventions, {r['jetons_total']} jetons")
        print(f"    verifications : {r['verifications']}  |  taux d'actions etayees : {r['taux_etayees']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", type=Path, default=ROOT / "agent" / "scenarios" / "operation_miroir.json")
    ap.add_argument("--etapes", default="")
    ap.add_argument("--essai", action="store_true")
    ap.add_argument("--max-demandes", type=int, default=6)
    args = ap.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    scenario = load_scenario(args.scenario)
    steps = [int(s) for s in args.etapes.split(",") if s.strip()] or None
    run_dir = new_run_dir(ROOT / "runs", scenario["id"])

    start = time.time()
    orch = Orchestrator(scenario, run_dir, essai=args.essai, max_demandes=args.max_demandes, on_event=show)
    orch.run(steps)
    report = build_report(run_dir)
    print(f"\nDuree : {round(time.time() - start)} s")
    print(f"Journal d'audit : {run_dir / 'journal.jsonl'}")
    print(f"Rapport lisible : {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
