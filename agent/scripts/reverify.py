"""Relance la verification des citations sur une simulation deja jouee.

Aucun appel au modele de langage : on relit le journal d'audit, on applique
la version actuelle des controles (server/crisis/audit.py) et on regenere le
bilan et le rapport. Le journal d'origine est conserve a cote
(journal_avant_reverification.jsonl) pour la tracabilite.

Usage : python scripts/reverify.py runs/<date>_<scenario>
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from agent.agent1_institutions.agent import Extract, Turn  # noqa: E402
from agent.agent3_coordination.audit import verify_turn  # noqa: E402
from agent.agent3_coordination.report import build as build_report  # noqa: E402


def main() -> int:
    run_dir = Path(sys.argv[1])
    journal = run_dir / "journal.jsonl"
    backup = run_dir / "journal_avant_reverification.jsonl"
    if not backup.exists():
        backup.write_text(journal.read_text(encoding="utf-8"), encoding="utf-8")
    entries = [json.loads(l) for l in backup.read_text(encoding="utf-8").splitlines() if l.strip()]

    counter: Counter = Counter()
    changes = []
    for e in entries:
        if not e["evenement"].startswith("intervention_"):
            continue
        extracts = [Extract(x["id"], x["source_file"], x["article"], x["page"], x["country"],
                            x["similarity"], x.get("texte", "")) for x in e.get("extraits", [])]
        turn = Turn(e["agent"], e["evenement"].removeprefix("intervention_"), e["etape"], [], [], "",
                    extracts, e.get("reponse") or {}, "", e.get("modele", ""), e.get("jetons", 0), 0.0)
        checks = verify_turn(turn)
        for old, new in zip(e["verification"], checks):
            if old["statut"] != new["statut"]:
                changes.append((e["etape"], e["agent"], old["statut"], new["statut"], new["action"][:90],
                                new["textes_non_verifies"] + new["mentions_non_verifiees"] + new["incoherences"]))
        e["verification"] = checks
        counter.update(c["statut"] for c in checks)

    total = sum(counter.values())
    for e in entries:
        if e["evenement"] == "simulation_fin":
            e["resume"]["verifications"] = dict(counter)
            e["resume"]["taux_etayees"] = round(counter["etayee"] / total, 3) if total else None
            e["reverification"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            resume = run_dir / "resume.json"
            data = json.loads(resume.read_text(encoding="utf-8")) if resume.exists() else {}
            data["resume"] = e["resume"]
            resume.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    journal.write_text("".join(json.dumps(e, ensure_ascii=False, default=str) + "\n" for e in entries),
                       encoding="utf-8")
    build_report(run_dir)

    print(f"Verifications : {dict(counter)} | taux etayees : {round(counter['etayee'] / total, 3)}")
    print(f"Statuts modifies : {len(changes)}")
    for c in changes:
        print(f"  etape {c[0]} {c[1]} : {c[2]} -> {c[3]} | {c[4]} | {c[5]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
