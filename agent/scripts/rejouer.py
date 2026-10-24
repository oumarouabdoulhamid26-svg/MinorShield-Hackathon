"""Rejoue une simulation a partir de son journal d'audit, sans appel au modele.

Demonstration de secours (finale, connexion instable, quota epuise) : on
montre exactement ce qui s'est passe, evenement par evenement. Ce n'est pas une
nouvelle simulation et l'ecran l'indique.

    python agent/scripts/rejouer.py runs/<date>_<scenario>                 # defilement continu
    python agent/scripts/rejouer.py runs/<date>_<scenario> --pas-a-pas     # Entree entre les etapes
    python agent/scripts/rejouer.py runs/<date>_<scenario> --etapes 2,5 --details
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from run_simulation import show  # noqa: E402


def details(entry: dict) -> None:
    """Complements utiles en presentation : texte de l'etape, lacunes, conflits."""
    ev = entry["evenement"]
    if ev == "etape_revelee":
        print(f"    {entry['information'][:600]}")
        if entry.get("entree_simulee"):
            print(f"    [entree SIMULEE] {json.dumps(entry['entree_simulee'].get('sortie'), ensure_ascii=False)[:300]}")
    elif ev == "intervention_analyse":
        rep = entry.get("reponse") or {}
        for g in (rep.get("lacunes") or [])[:4]:
            txt = g.get("lacune", "") if isinstance(g, dict) else str(g)
            comp = ", ".join(c.get("juridiction", "") for c in (g.get("comparaison") or []) if isinstance(c, dict)) \
                if isinstance(g, dict) else ""
            print(f"       LACUNE : {txt[:200]}" + (f"  [comparaison : {comp}]" if comp else ""))
        for c in (rep.get("conflits") or [])[:2]:
            print(f"       CONFLIT : {str(c)[:200]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", type=Path)
    ap.add_argument("--pause", type=float, default=0.4, help="secondes entre deux evenements")
    ap.add_argument("--pas-a-pas", action="store_true", help="attendre Entree avant chaque etape")
    ap.add_argument("--etapes", default="", help="ne rejouer que ces etapes (ex. 2,5)")
    ap.add_argument("--details", action="store_true", help="afficher le texte des etapes, les lacunes et les conflits")
    args = ap.parse_args()

    journal = [json.loads(l) for l in (args.run / "journal.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    etapes = {int(s) for s in args.etapes.split(",") if s.strip()}
    print(f"### REJEU du journal {args.run.name} — aucun appel au modele, evenements enregistres le "
          f"{journal[0]['horodatage'][:16].replace('T', ' ')} (UTC) ###")
    for entry in journal:
        if etapes and "etape" in entry and entry["etape"] not in etapes:
            continue
        if entry["evenement"] == "etape_revelee" and args.pas_a_pas:
            input("\n[Entree] pour l'etape suivante...")
        show(entry)
        if args.details:
            details(entry)
        time.sleep(args.pause)
    return 0


if __name__ == "__main__":
    sys.exit(main())
