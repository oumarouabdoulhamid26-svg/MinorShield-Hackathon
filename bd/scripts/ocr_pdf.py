"""Transforme un PDF scanne en texte (OCR Tesseract, francais par defaut).

Beaucoup de textes officiels camerounais ne sont publies qu'en scan : leur
PDF ne contient que des images, illisibles pour l'ingestion. Ce script :

  1. rend chaque page en image a 300 ppp (PyMuPDF) ;
  2. la fait lire par Tesseract ;
  3. ecrit un fichier .txt avec des marqueurs ``[PAGE n]`` pour que les
     agents puissent citer la page d'origine.

Usage :
    python scripts/ocr_pdf.py <entree.pdf> <sortie.txt> [--lang fra] [--title "..."]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

TESSERACT = "tesseract"


def ocr_page(png: Path, lang: str) -> str:
    out = subprocess.run(
        [TESSERACT, str(png), "stdout", "-l", lang, "--psm", "4"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True,
    )
    return out.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("txt", type=Path)
    ap.add_argument("--lang", default="fra")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--title", default="", help="Ligne d'en-tete ajoutee en tete du fichier")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    parts: list[str] = []
    if args.title:
        parts.append(args.title.strip() + "\n")
    parts.append(f"(Texte obtenu par OCR Tesseract depuis : {args.pdf.name}, {doc.page_count} pages)\n")

    with tempfile.TemporaryDirectory() as tmp:
        for i, page in enumerate(doc, start=1):
            png = Path(tmp) / f"p{i}.png"
            page.get_pixmap(dpi=args.dpi).save(png)
            text = ocr_page(png, args.lang).strip()
            parts.append(f"\n[PAGE {i}]\n{text}\n")
            print(f"page {i}/{doc.page_count} : {len(text)} caracteres", flush=True)

    args.txt.parent.mkdir(parents=True, exist_ok=True)
    args.txt.write_text("".join(parts), encoding="utf-8")
    print(f"\nEcrit : {args.txt} ({args.txt.stat().st_size} octets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
