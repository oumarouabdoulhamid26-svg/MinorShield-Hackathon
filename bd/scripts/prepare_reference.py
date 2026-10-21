"""Convertit un texte de reference etranger (PDF ou HTML) en fichier texte propre.

Le fichier produit commence par le titre officiel puis la source, comme les
textes camerounais (scripts/split_recueil.py), afin que chaque extrait de la
base reste identifiable lorsqu'un agent le cite.

Usage :
    python scripts/prepare_reference.py <entree.pdf|html> <sortie.txt> --titre "..." --source "..."
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import pymupdf


def pdf_text(path: Path) -> str:
    doc = pymupdf.open(path)
    return "\n".join(f"[PAGE {i}]\n{p.get_text()}" for i, p in enumerate(doc, start=1))


def html_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", raw)
    # Les fins de blocs deviennent des retours a la ligne, pour garder
    # « Article 28 » en debut de ligne (decoupage article par article).
    raw = re.sub(r"(?i)</(p|div|tr|li|h[1-6]|table)>|<br\s*/?>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"[ \t ]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entree", type=Path)
    ap.add_argument("sortie", type=Path)
    ap.add_argument("--titre", required=True)
    ap.add_argument("--source", required=True)
    args = ap.parse_args()

    body = pdf_text(args.entree) if args.entree.suffix.lower() == ".pdf" else html_text(args.entree)
    body = re.sub(r"(?m)^[ \t]+", "", body).strip()
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(f"{args.titre}\n\nSource : {args.source}\n\n{body}\n", encoding="utf-8")
    print(f"{args.sortie.name} : {len(body)} caracteres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
