"""Ajoute des documents a la base de connaissances, sans tout reconstruire.

Pourquoi ce script : la commande d'ingestion de reference
(``python -m bd.knowledge.ingest``) recharge systematiquement les
definitions du cadre UIT, ce qui cree des doublons a chaque lancement. Ce
script n'ajoute QUE les fichiers demandes et saute ceux deja presents.

Usage :
    python scripts/add_documents.py <fichier ou dossier> [...] [--remplacer]

--remplacer : supprime d'abord les morceaux deja presents pour ces fichiers,
              puis les reingere (utile apres un changement de decoupage).

La categorie d'un document est le nom de son dossier parent dans InputDocs/
(ex. ``Child_Online_Protection``), comme dans l'ingestion de reference.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bd.knowledge.ingest import ingest_file  # noqa: E402
from bd.knowledge.kb import KnowledgeBase  # noqa: E402

SUPPORTED = {".pdf", ".txt", ".md", ".csv", ".html"}


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix.lower() in SUPPORTED)
        elif p.suffix.lower() in SUPPORTED:
            files.append(p)
    return [f for f in files if f.name.lower() != "inputs.md"]


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s")
    args = sys.argv[1:]
    replace = "--remplacer" in args
    files = collect([a for a in args if a != "--remplacer"])
    if not files:
        print(__doc__)
        return 1

    kb = KnowledgeBase()
    if replace:
        # Supprime les anciens morceaux de ces fichiers avant de les reingerer
        # (ex. apres un changement de methode de decoupage).
        for f in files:
            old = kb.main.get(where={"source_file": f.name})["ids"]
            if old:
                kb.main.delete(ids=old)
                logging.info("Remplacement : %d anciens morceaux supprimes pour %s", len(old), f.name)
    present = {m["source_file"] for m in kb.main.get(include=["metadatas"])["metadatas"]}

    total, skipped, failed = 0, [], []
    for f in files:
        if f.name in present:
            skipped.append(f.name)
            continue
        try:
            n = ingest_file(f, kb, extra_metadata={"document_category": f.parent.name})
        except Exception as e:  # noqa: BLE001
            logging.error("Echec sur %s : %s", f.name, e)
            n = 0
        if n == 0:
            failed.append(f.name)
        total += n

    print(f"\nAjoutes : {total} morceaux depuis {len(files) - len(skipped) - len(failed)} fichier(s)")
    if skipped:
        print(f"Deja presents (ignores) : {len(skipped)}")
    if failed:
        print("Illisibles ou vides :")
        for name in failed:
            print("  -", name)
    print("Base :", kb.stats())
    return 0


if __name__ == "__main__":
    sys.exit(main())
