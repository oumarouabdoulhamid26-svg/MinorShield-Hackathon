"""Decoupe le recueil officiel de l'ART en un fichier texte par loi ou decret.

Source : « Recueil des textes du secteur des Postes, Telecommunications et
TIC - Edition 2023 », publie par l'Agence de Regulation des
Telecommunications (art.cm).

Pourquoi decouper : ingere en un seul bloc, chaque extrait serait attribue au
« recueil » ; decoupe, chaque extrait porte le nom exact du texte (ex.
« Loi n° 2023/009 »), ce que les agents citent dans leurs justifications.

Usage :
    python scripts/split_recueil.py <recueil.pdf> --list
    python scripts/split_recueil.py <recueil.pdf> --extract <dossier_sortie>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pymupdf

SOURCE = (
    "Recueil des textes du secteur des Postes, Telecommunications et TIC - "
    "Edition 2023 (Agence de Regulation des Telecommunications, art.cm)"
)

TITLE_RX = re.compile(
    r"^\s*(LOI|D[ÉE]CRET)\s*N\s*[°o0]?\s*([0-9]{2,4}\s*/\s*[0-9lI]{2,5}(?:\s*/\s*PM)?)"
    r"[^\n]{0,40}\n?[^\n]{0,10}?((?:PORTANT|RELATIVE|R[ÉE]GISSANT|FIXANT|MODIFIANT|INSTITUANT)[^\n]{0,90})?",
    re.I | re.M,
)

# Textes retenus pour la base : (fichier de sortie, page PDF de debut, page de fin, titre officiel)
# Pages determinees avec --list puis verifiees a la lecture (voir docs/SOURCES.md).
SELECTION: list[tuple[str, int, int, str]] = [
    ("Loi_2023-009_Charte_protection_enfants_en_ligne_Cameroun.txt", 224, 230,
     "Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun"),
    ("Loi_2010-012_Cybersecurite_cybercriminalite_Cameroun.txt", 200, 218,
     "Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun"),
    ("Loi_2010-013_Communications_electroniques_Cameroun.txt", 177, 199,
     "Loi n° 2010/013 du 21 decembre 2010 regissant les communications electroniques au Cameroun"),
    ("Loi_2015-006_Modification_communications_electroniques_Cameroun.txt", 219, 223,
     "Loi n° 2015/006 du 20 avril 2015 modifiant et completant certaines dispositions de la loi n° 2010/013"),
    ("Loi_2010-021_Commerce_electronique_Cameroun.txt", 85, 98,
     "Loi n° 2010/021 du 21 decembre 2010 regissant le commerce electronique au Cameroun"),
    ("Decret_2012-512_Organisation_MINPOSTEL_Cameroun.txt", 10, 40,
     "Decret n° 2012/512 du 12 novembre 2012 portant organisation du Ministere des Postes et Telecommunications"),
    ("Decret_2019-150_Organisation_ANTIC_Cameroun.txt", 51, 61,
     "Decret n° 2019/150 du 22 mars 2019 portant organisation et fonctionnement de l'ANTIC"),
    ("Decret_2020-727_Organisation_ART_Cameroun.txt", 66, 76,
     "Decret n° 2020/727 du 03 decembre 2020 portant reorganisation et fonctionnement de l'ART"),
    ("Decret_2015-3759-PM_Identification_abonnes_Cameroun.txt", 325, 329,
     "Decret n° 2015/3759/PM du 03 septembre 2015 fixant les modalites d'identification des abonnes et des equipements terminaux"),
    ("Decret_2012-1643-PM_Audit_securite_obligatoire_Cameroun.txt", 274, 277,
     "Decret n° 2012/1643/PM du 14 juin 2012 fixant les conditions et modalites d'audit de securite obligatoire"),
    ("Decret_2013-0399-PM_Protection_consommateurs_communications_electroniques_Cameroun.txt", 303, 307,
     "Decret n° 2013/0399/PM du 27 fevrier 2013 fixant les modalites de protection des consommateurs des services de communications electroniques"),
]


def page_texts(pdf: Path) -> list[str]:
    return [p.get_text() for p in pymupdf.open(pdf)]


def list_titles(pages: list[str]) -> None:
    for i, text in enumerate(pages, start=1):
        if i <= 7:  # sommaire
            continue
        for m in TITLE_RX.finditer(text):
            kind = m.group(1).upper().replace("É", "E")
            num = re.sub(r"\s", "", m.group(2))
            obj = (m.group(3) or "").strip()
            if obj:
                print(f"p.{i:<4} {kind:7} {num:<14} {obj[:80]}")


def clean(text: str) -> str:
    # Retire les en-tetes et pieds de page repetes du recueil.
    text = re.sub(r"Recueil des textes du secteur des Postes, T[ée]l[ée]communications et TIC - Edition 2023", "", text)
    text = re.sub(r"Minist[èe]re des Postes et T[ée]l[ée]communications", "", text)
    text = re.sub(r"Le secteur des t[ée]l[ée]communications et TIC", "", text)
    text = text.replace("­", "-").replace("ﬁ", "fi").replace("ﬀ", "ff")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def extract(pages: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, start, end, title in SELECTION:
        body = []
        for p in range(start, end + 1):
            body.append(f"\n[PAGE {p} du recueil PDF]\n{clean(pages[p - 1])}\n")
        content = f"{title}\n\nSource : {SOURCE}, pages PDF {start} a {end}.\n" + "".join(body)
        (out_dir / filename).write_text(content, encoding="utf-8")
        print(f"{filename} : pages {start}-{end}, {len(content)} caracteres")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true")
    g.add_argument("--extract", type=Path, metavar="DOSSIER")
    args = ap.parse_args()

    pages = page_texts(args.pdf)
    if args.list:
        list_titles(pages)
    else:
        extract(pages, args.extract)
    return 0


if __name__ == "__main__":
    sys.exit(main())
