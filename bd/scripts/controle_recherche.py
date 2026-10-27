"""Mesure la qualite de la recherche avec les requetes de controle.

Deux modes sont mesures pour chaque question :
- « base »  : recherche brute dans tout le corpus juridique (5 premiers resultats) ;
- « agent » : recherche telle que l'agent la fait reellement (extraits recus,
              avec la priorite donnee a ses textes nationaux).

Une question est reussie si l'article attendu (ou un article accepte) figure
dans les resultats. Aucun appel au modele de langage : seuls les embeddings
locaux (Ollama) sont utilises.

Usage :
    python bd/scripts/controle_recherche.py [--sortie bd/controle/resultats.md]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agent.agent1_institutions.agent import LEGAL_CATEGORY, CrisisAgent  # noqa: E402
from agent.agent1_institutions.roles import ROLES  # noqa: E402
from bd.knowledge.ingest import embed_texts  # noqa: E402
from bd.knowledge.kb import KnowledgeBase  # noqa: E402

TOP_K = 5


def rank(results: list[tuple[str, str]], cibles: list[dict[str, str]]) -> int | None:
    """Rang (1 = premier) du premier resultat correspondant a une cible."""
    for i, (fichier, article) in enumerate(results, start=1):
        if any(fichier.startswith(c["fichier"]) and str(article) == c["article"] for c in cibles):
            return i
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--requetes", type=Path, default=ROOT / "bd" / "controle" / "requetes_controle.json")
    ap.add_argument("--sortie", type=Path, default=ROOT / "bd" / "controle" / "resultats_controle.md")
    args = ap.parse_args()

    requetes = json.loads(args.requetes.read_text(encoding="utf-8"))["requetes"]
    kb = KnowledgeBase()
    lignes = []
    stats = {"base": [], "agent": []}

    for q in requetes:
        cibles = [q["attendu"]] + q.get("accepte", [])
        emb = embed_texts([q["question"]])[0]
        res = kb.search(emb, n_results=TOP_K, where={"document_category": LEGAL_CATEGORY})
        base = [(m.get("source_file", ""), m.get("article", "")) for m in res["metadatas"][0]]
        ag = CrisisAgent(ROLES[q["agent"]], kb, essai=True).retrieve(q["question"])
        agent = [(e.source_file, e.article) for e in ag]
        r_base, r_agent = rank(base, cibles), rank(agent, cibles)
        stats["base"].append(r_base)
        stats["agent"].append(r_agent)
        premier = base[0] if base else ("", "")
        lignes.append((q, r_base, r_agent, premier, len(agent)))

    def resume(rangs: list[int | None]) -> tuple[int, int, float]:
        top1 = sum(1 for r in rangs if r == 1)
        trouves = sum(1 for r in rangs if r is not None)
        mrr = sum(1 / r for r in rangs if r) / len(rangs)
        return top1, trouves, mrr

    n = len(requetes)
    b1, bk, bmrr = resume(stats["base"])
    a1, ak, amrr = resume(stats["agent"])
    out = [
        "# Contrôle de la recherche dans la base de connaissances",
        "",
        f"Mesure du {datetime.now():%d/%m/%Y %H:%M} — {n} requêtes "
        f"(`{args.requetes.relative_to(ROOT).as_posix()}`), embeddings `bge-m3`, aucun appel au modèle de langage.",
        "",
        "| Mode | Article attendu en 1re position | Article attendu trouvé | MRR |",
        "|---|---|---|---|",
        f"| Recherche brute (5 premiers résultats) | {b1}/{n} | {bk}/{n} | {bmrr:.2f} |",
        f"| Recherche de l'agent (extraits reçus) | {a1}/{n} | {ak}/{n} | {amrr:.2f} |",
        "",
        "MRR : moyenne de 1/rang de l'article attendu (1 = toujours premier, 0 = jamais trouvé).",
        "",
        "| Id | Agent | Question | Attendu | Rang (brute) | Rang (agent) | 1er résultat brut |",
        "|---|---|---|---|---|---|---|",
    ]
    for q, rb, ra, premier, nag in lignes:
        att = f"{q['attendu']['fichier']} art. {q['attendu']['article']}"
        out.append(f"| {q['id']} | {q['agent']} | {q['question']} | {att} | {rb or '—'} | "
                   f"{ra or '—'} (sur {nag}) | {premier[0][:28]} art. {premier[1] or '—'} |")
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Brute : 1re position {b1}/{n}, trouvé {bk}/{n}, MRR {bmrr:.2f}")
    print(f"Agent : 1re position {a1}/{n}, trouvé {ak}/{n}, MRR {amrr:.2f}")
    echecs = [(q, rb) for q, rb, ra, _, _ in lignes if ra is None]
    if echecs:
        print("Questions ou l'article attendu n'est pas fourni a l'agent (analyse : bd/controle/README.md) :")
        for q, rb in echecs:
            print(f"  {q['id']} — {q['question'][:90]}")
    print("(La recherche brute sert de point de comparaison : ses echecs sont normaux et ne sont pas listes.)")
    print(f"Detail : {args.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
