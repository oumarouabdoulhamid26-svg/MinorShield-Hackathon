"""Indicateurs d'une simulation, a partir de son journal d'audit (aucun appel au modele).

    python agent/scripts/indicateurs.py runs/<date>_<scenario> [--seuil 0.65]

Ecrit runs/<...>/indicateurs.md :
- citations : taux d'actions etayees, global et par agent ;
- coordination : demandes, institution nommee, reconfigurations ;
- consommation : jetons par type d'intervention ;
- lacunes attendues : pour chaque lacune prevue dans le scenario, la lacune
  relevee a la meme etape (conseiller ou agents) la plus proche par le sens
  (similarite cosinus des embeddings bge-m3). Au-dessus du seuil, la lacune est
  « retrouvee (automatique) » ; ce rapprochement doit etre confirme par une
  relecture humaine.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from agent.agent1_institutions.roles import ROLES  # noqa: E402
from bd.knowledge.ingest import embed_texts  # noqa: E402


def cos(a: list[float], b: list[float]) -> float:
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else 0.0


def gap_text(item) -> str:
    return str(item.get("lacune", "")) if isinstance(item, dict) else str(item)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=Path)
    ap.add_argument("--seuil", type=float, default=0.65)
    args = ap.parse_args()

    journal = [json.loads(l) for l in (args.run / "journal.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    resume = json.loads((args.run / "resume.json").read_text(encoding="utf-8"))
    scenario = resume.get("scenario", {})
    abandoned = {e["etape"] for e in journal if e["evenement"] == "etape_abandonnee"}
    done = {e["etape"] for e in journal if e["evenement"] == "intervention_analyse" and not e.get("erreur")}

    def counted(e: dict) -> bool:
        return not ("etape" in e and e["etape"] in abandoned and e["etape"] not in done) or \
            e["horodatage"] > max((x["horodatage"] for x in journal if x["evenement"] == "simulation_reprise"), default="")

    inter = [e for e in journal if e["evenement"].startswith("intervention_") and counted(e)]
    statuts, par_agent = Counter(), defaultdict(Counter)
    jetons = defaultdict(list)
    inst = Counter()
    for e in inter:
        if e.get("erreur"):
            continue
        jetons[e["evenement"][13:]].append(e.get("jetons", 0))
        for c in e.get("verification", []):
            statuts[c["statut"]] += 1
            par_agent[e["agent"]][c["statut"]] += 1
            if "institution_valide" in c:
                inst["valide" if c["institution_valide"] else "manquante"] += 1
    total = sum(statuts.values())
    ev = Counter(e["evenement"] for e in journal)
    reconf = [e for e in journal if e["evenement"] == "reconfiguration"]

    out = [f"# Indicateurs — {args.run.name}", ""]
    modeles = Counter(e.get("modele") for e in inter if not e.get("erreur"))
    out += ["## Citations", "",
            f"- Modèle(s) : {', '.join(f'{m} ({n})' for m, n in modeles.items())}",
            f"- Interventions : {len(inter)} (dont {sum(1 for e in inter if e.get('erreur'))} en erreur)",
            f"- Affirmations vérifiées : {total} — " + ", ".join(f"{k} {v}" for k, v in statuts.most_common()),
            f"- **Taux d'actions étayées : {statuts['etayee'] / total:.1%}**" if total else "- Taux : —", "",
            "| Agent | Étayées | Douteuses | Non étayées | Invalides | Taux |", "|---|---|---|---|---|---|"]
    for a, c in sorted(par_agent.items()):
        n = sum(c.values())
        out.append(f"| {a} | {c['etayee']} | {c['citation_douteuse']} | {c['non_etayee']} | "
                   f"{c['citation_invalide']} | {c['etayee'] / n:.0%} |")
    out += ["", "## Coordination", "",
            f"- Demandes transmises entre agents : {ev['demande_transmise']} "
            f"(répétitions évitées : {ev['demande_repetee']}, coordinations internes : {ev['coordination_interne']}, "
            f"non transmises : {ev['demande_non_transmise']}, écartées par la limite : "
            f"{sum(e.get('nombre', 0) for e in journal if e['evenement'] == 'demandes_ecartees')})",
            f"- Actions avec institution nommée : {inst['valide']} sur {inst['valide'] + inst['manquante']}",
            f"- Reconfigurations automatiques : {len(reconf)} "
            f"({', '.join(f'{k} {v}' for k, v in Counter(e['type'] for e in reconf).items()) or 'aucune'})",
            f"- Interruption / reprise : {ev['simulation_interrompue']} / {ev['simulation_reprise']}", "",
            "## Consommation", "", "| Type | Nombre | Jetons moyens | Total |", "|---|---|---|---|"]
    for k, v in jetons.items():
        out.append(f"| {k} | {len(v)} | {sum(v) // len(v)} | {sum(v)} |")
    out.append(f"| **total** | {sum(len(v) for v in jetons.values())} | | **{sum(sum(v) for v in jetons.values())}** |")

    # Lacunes attendues contre lacunes relevees, etape par etape.
    found_by_step: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for e in inter:
        rep = e.get("reponse") or {}
        for g in rep.get("lacunes", []) or []:
            if gap_text(g):
                found_by_step[e["etape"]].append((e["agent"], gap_text(g)))
    out += ["", f"## Lacunes attendues (rapprochement automatique, seuil {args.seuil})", "",
            "| Étape | Lacune attendue | Lacune relevée la plus proche | Par | Similarité | Statut |",
            "|---|---|---|---|---|---|"]
    retrouvees = attendues = 0
    for step in scenario.get("etapes", []):
        n = step["numero"]
        expected = step.get("lacunes_attendues", [])
        found = found_by_step.get(n, [])
        if not expected:
            continue
        ve = embed_texts(expected)
        vf = embed_texts([t for _, t in found]) if found else []
        for txt, v in zip(expected, ve):
            attendues += 1
            best, who, sim = "—", "—", 0.0
            for (agent, ftxt), w in zip(found, vf):
                s = cos(v, w)
                if s > sim:
                    best, who, sim = ftxt, agent, s
            ok = sim >= args.seuil
            retrouvees += ok
            out.append(f"| {n} | {txt} | {best} | {who} | {sim:.2f} | {'retrouvée (auto)' if ok else 'à vérifier'} |")
    out.insert(2, f"**Lacunes attendues retrouvées (automatique) : {retrouvees}/{attendues}** — "
                  "à confirmer par relecture humaine.\n")
    (args.run / "indicateurs.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"taux etayees {statuts['etayee'] / total:.1%} | lacunes {retrouvees}/{attendues} | "
          f"jetons {sum(sum(v) for v in jetons.values())} -> {args.run / 'indicateurs.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
