"""Construit le rapport technique Word a partir du brouillon Markdown, dans le modele officiel.

    python docs/rapport_technique/construire_rapport.py [--corps 10.5] [--tableaux 8.5]

Le modele est le rapport Word existant (styles, en-tete, titres numerotes,
figure) ; son corps est remplace par le contenu de brouillon_v2_EN.md :
« ## N. Titre » -> titre numerote, paragraphes, listes « - », tableaux « | »,
**gras**. La figure 1 est remplacee par figure_architecture.png et inseree
apres la section 2.
"""

from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt

HERE = Path(__file__).resolve().parent
MODELE = HERE / "MinorShield_Policy_Lab_Technical_Report.docx"
BROUILLON = HERE / "brouillon_v2_EN.md"
FIGURE = HERE / "figure_architecture.png"
SORTIE = HERE / "MinorShield_Policy_Lab_Technical_Report.docx"


def typographie(text: str) -> str:
    """Apostrophes et guillemets typographiques (’ et “ ”), hors adresses web."""
    if "http" in text:
        return text
    text = re.sub(r'"([^"]+)"', "“\\1”", text)
    return text.replace("'", "’")


def runs_from_markdown(par, text: str, size: float) -> None:
    """Ajoute le texte au paragraphe en gerant **gras** ; les `code` deviennent du texte simple."""
    text = typographie(text.replace("`", ""))
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part:
            r = par.add_run(part)
            r.bold = i % 2 == 1
            r.font.size = Pt(size)


def set_font(rpr_parent, name: str) -> None:
    """Impose la police ``name`` a un element w:rPr (toutes les ecritures)."""
    rfonts = rpr_parent.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr_parent.makeelement(qn("w:rFonts"), {})
        rpr_parent.insert(0, rfonts)
    for k in list(rfonts.attrib):
        if k.endswith("Theme"):
            del rfonts.attrib[k]
    for att in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(att), name)


def uniform_font(d, name: str) -> None:
    """Une seule police dans tout le document : styles, puis chaque passage de texte."""
    for st in d.styles.element.iter(qn("w:style")):
        rpr = st.find(qn("w:rPr"))
        if rpr is None:
            rpr = st.makeelement(qn("w:rPr"), {})
            st.append(rpr)
        set_font(rpr, name)
    defaults = d.styles.element.find(qn("w:docDefaults"))
    if defaults is not None:
        for rpr in defaults.iter(qn("w:rPr")):
            set_font(rpr, name)
    # Numeros des titres (« 1. », « 2. ») : police propre a la numerotation.
    numbering = d.part.numbering_part.element
    for lvl in numbering.iter(qn("w:lvl")):
        rpr = lvl.find(qn("w:rPr"))
        if rpr is None:
            rpr = lvl.makeelement(qn("w:rPr"), {})
            lvl.append(rpr)
        set_font(rpr, name)
    for r in d.element.body.iter(qn("w:r")):
        rpr = r.find(qn("w:rPr"))
        if rpr is None:
            rpr = r.makeelement(qn("w:rPr"), {})
            r.insert(0, rpr)
        set_font(rpr, name)


def add_page_numbers(d, size: float = 10) -> None:
    """Numero de page centre en pied de page (champ PAGE, mis a jour par Word)."""
    for sec in d.sections:
        footer = sec.footer
        footer.is_linked_to_previous = False
        par = footer.paragraphs[0]
        for r in list(par.runs):
            r._r.getparent().remove(r._r)
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for kind, text in (("begin", None), ("instr", " PAGE "), ("separate", None), ("text", "1"), ("end", None)):
            run = par.add_run()
            run.font.size = Pt(size)
            if kind == "instr":
                el = run._r.makeelement(qn("w:instrText"), {qn("xml:space"): "preserve"})
                el.text = text
                run._r.append(el)
            elif kind == "text":
                run.text = text
            else:
                run._r.append(run._r.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): kind}))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corps", type=float, default=10.5)
    ap.add_argument("--tableaux", type=float, default=8.5)
    ap.add_argument("--police", default="Times New Roman")
    ap.add_argument("--equipe", default="", help="remplace le nom d'equipe entre crochets de l'en-tete")
    ap.add_argument("--membres", default="", help="remplace les membres entre crochets de l'en-tete")
    ap.add_argument("--mentor", default="", help="ajoute une ligne « Mentor » sous les membres de l'equipe")
    ap.add_argument("--modele", type=Path, default=MODELE)
    ap.add_argument("--sortie", type=Path, default=SORTIE)
    ap.add_argument("--brouillon", type=Path, default=BROUILLON)
    ap.add_argument("--figure", type=Path, default=FIGURE)
    ap.add_argument("--legende", default="Figure 1 – Architecture of MinorShield Policy Lab mapped onto the ITU-T "
                                         "Y.3172 pipeline, with the proposed verification node")
    args = ap.parse_args()

    d = docx.Document(str(args.modele))
    body = d.element.body
    kids = list(body.iterchildren())
    sect = kids[-1]
    heading_tpl = next(k for k in kids if k.find(f".//{qn('w:numPr')}") is not None)
    para_tpl = next(k for k in kids[4:] if k.tag == qn("w:p") and k.find(f".//{qn('w:numPr')}") is None
                    and k.find(f".//{qn('a:blip')}") is None and "".join(k.itertext()).strip())
    fig_tpl = next(k for k in kids if k.find(f".//{qn('a:blip')}") is not None)
    cap_tpl = kids[kids.index(fig_tpl) + 1]
    tbl_style = next((docx.table.Table(k, d).style for k in kids if k.tag == qn("w:tbl")), None)

    # Image : nouveau contenu, proportions recalculees.
    blip = fig_tpl.find(f".//{qn('a:blip')}")
    img_part = d.part.related_parts[blip.get(qn("r:embed"))]
    png = args.figure.read_bytes()
    img_part._blob = png
    from PIL import Image
    with Image.open(args.figure) as im:
        w, h = im.size
    for ext in fig_tpl.iter():
        if ext.tag in (qn("wp:extent"), qn("a:ext")) and ext.get("cx"):
            ext.set("cy", str(int(int(ext.get("cx")) * h / w)))

    # On garde l'en-tete (4 premiers paragraphes), on vide le reste.
    for k in kids[4:-1]:
        body.remove(k)

    def new_par(text: str, size: float):
        p_el = copy.deepcopy(para_tpl)
        for r in p_el.findall(qn("w:r")):
            p_el.remove(r)
        sect.addprevious(p_el)
        par = docx.text.paragraph.Paragraph(p_el, d)
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        runs_from_markdown(par, text, size)
        return par

    def new_heading(text: str):
        h_el = copy.deepcopy(heading_tpl)
        for r in h_el.findall(qn("w:r"))[1:]:
            h_el.remove(r)
        h_el.findall(f".//{qn('w:t')}")[0].text = typographie(text)
        sect.addprevious(h_el)

    def new_table(rows: list[list[str]]):
        prev = sect.getprevious()   # la phrase qui introduit le tableau (avant add_table)
        t = d.add_table(rows=len(rows), cols=len(rows[0]))
        if tbl_style is not None:
            t.style = tbl_style
        # Largeur des colonnes proportionnelle a la longueur moyenne du texte.
        sec = d.sections[0]
        usable = sec.page_width - sec.left_margin - sec.right_margin
        # Une colonne est au moins assez large pour son mot le plus long : pas de
        # mot coupe en son milieu (« Nœ/ud »).
        weights = [max(sum(len(r[j]) for r in rows) / len(rows),
                       2.4 * max(len(w) for r in rows for w in r[j].replace("**", "").split() or [""]), 10)
                   for j in range(len(rows[0]))]
        widths = [int(usable * wgt / sum(weights)) for wgt in weights]
        t.autofit = False
        for tr in t.rows:   # une ligne de tableau n'est jamais coupee entre deux pages
            trpr = tr._tr.get_or_add_trPr()
            trpr.append(trpr.makeelement(qn("w:cantSplit"), {}))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.cell(i, j)
                cell.width = widths[j]
                cell.text = ""
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(0)
                runs_from_markdown(par, f"**{val}**" if i == 0 and "**" not in val else val, args.tableaux)
        # Jamais d'en-tete de tableau seul en bas de page : la phrase qui
        # introduit le tableau, l'en-tete et la premiere ligne restent ensemble ;
        # un long tableau peut continuer page suivante, avec l'en-tete repete.
        for row in t.rows[:2]:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.keep_with_next = True
        hdr = t.rows[0]._tr.get_or_add_trPr()
        hdr.append(hdr.makeelement(qn("w:tblHeader"), {}))
        if prev is not None and prev.tag == qn("w:p"):
            docx.text.paragraph.Paragraph(prev, d).paragraph_format.keep_with_next = True
        sect.addprevious(t._tbl)
        sp = new_par("", 4)   # petit espace apres le tableau
        sp.paragraph_format.space_after = Pt(2)
        sp.paragraph_format.space_before = Pt(0)

    lines = args.brouillon.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## 1."))
    table: list[list[str]] = []
    section = 0
    for line in lines[start:] + [""]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                table.append(cells)
            continue
        if table:
            new_table(table)
            table = []
        if line.startswith("## "):
            if section == 2:   # figure apres la section 2 (cas d'usage)
                sect.addprevious(copy.deepcopy(fig_tpl))
                cap = copy.deepcopy(cap_tpl)
                sect.addprevious(cap)
            section += 1
            new_heading(re.sub(r"^##\s+\d+\.\s*", "", line))
        elif line.startswith("- "):
            new_par("• " + line[2:], args.corps)
        elif line.strip():
            new_par(line, args.corps)

    # Legende de la figure, a jour.
    for p in d.paragraphs:
        if p.text.startswith("Figure 1"):
            for r in p.runs[1:]:
                r.text = ""
            p.runs[0].text = args.legende
    # En-tete : nom d'equipe et membres a la place des crochets du modele.
    for p in d.paragraphs[:4]:
        for r in p.runs:
            if args.equipe:
                r.text = re.sub(r"\[(Team Name|Nom de l'équipe)\]", args.equipe, r.text)
            if args.membres:
                r.text = re.sub(r"\[(to be completed|à compléter)\]", args.membres, r.text)
            # Titre sur deux lignes nettes : evenement et equipe, puis nom de la solution.
            if args.equipe and r.text.endswith(" – MinorShield Policy Lab"):
                r.text = r.text[: -len(" – MinorShield Policy Lab")] + " –\nMinorShield Policy Lab"
            if "'" in r.text and "http" not in r.text:
                r.text = r.text.replace("'", "’")
            if args.mentor and ("Team members" in r.text or "Membres de l" in r.text):
                label = "Mentor : " if "Membres" in r.text else "Mentor: "
                fin = "\n" if r.text.endswith("\n") else ""
                r.text = r.text.rstrip("\n") + "\n" + label + args.mentor + fin
    add_page_numbers(d)
    uniform_font(d, args.police)
    d.save(str(args.sortie))
    print(args.sortie)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
