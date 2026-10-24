"""Figure 1 du rapport technique : architecture du Policy Lab sur le pipeline UIT-T Y.3172.

    python docs/rapport_technique/figure_architecture.py          ->  figure_architecture.png
    python docs/rapport_technique/figure_architecture.py --fr     ->  figure_architecture_fr.png
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

FR = "--fr" in sys.argv
OUT = Path(__file__).with_name("figure_architecture_fr.png" if FR else "figure_architecture.png")
INK = "#2f3e4e"

BOXES_EN = [
    ("SRC", "13 Cameroonian laws\nand decrees\n7 international references\nITU documents\nMinorShield detector\noutput (simulated)", "#dce8f5", False),
    ("COLLECTOR /\nPREPROCESSOR", "Text extraction, OCR\nArticle-level chunks\n+ page, country\nbge-m3 embeddings\n(local)", "#dce8f5", False),
    ("ML FUNCTION", "6 actor agents\n+ legal advisor\nKey mandate articles\nretrieved first\ngpt-oss-120b\n(open weights)", "#d6ede1", False),
    ("VERIFICATION\n(proposed node)", "Each citation checked:\nsupported / doubtful /\nunsupported / invalid\nInstitution named\nper action", "#fbe5c6", True),
    ("SINK", "Audit log (JSONL)\nReport, indicators\nGap table\nDemo page, replay\n→ human decision", "#e4dff0", False),
]
BOXES_FR = [
    ("SRC", "13 lois et décrets\ncamerounais\n7 références\ninternationales\nDocuments de l'UIT\nDétecteur MinorShield\n(sortie simulée)", "#dce8f5", False),
    ("COLLECTEUR /\nPRÉTRAITEMENT", "Extraction du texte, OCR\nDécoupage par article\n+ page, pays\nEmbeddings bge-m3\n(locaux)", "#dce8f5", False),
    ("FONCTION ML", "6 agents acteurs\n+ conseiller juridique\nArticles clés du mandat\nfournis en priorité\ngpt-oss-120b\n(poids ouverts)", "#d6ede1", False),
    ("VÉRIFICATION\n(nœud proposé)", "Citation contrôlée :\nétayée / douteuse /\nnon étayée / invalide\nInstitution nommée\npour chaque action", "#fbe5c6", True),
    ("SINK", "Journal d'audit (JSONL)\nRapport, indicateurs\nTableau des lacunes\nDémo, rejeu\n→ décision humaine", "#e4dff0", False),
]
TITLE_EN = "SANDBOX — crisis scenario “Operation Mirror” (6 stages revealed to different agents)"
TITLE_FR = "BAC À SABLE — scénario de crise « Opération Miroir » (6 étapes révélées à des agents différents)"
MLFO_EN = ("Orchestrator (MLFO), driven by the ML Intent (agent/intent.json): reveals stages, routes requests\n"
           "between agents, reconfigures itself below the quality threshold, switches model if a quota runs out")
MLFO_FR = ("Orchestrateur (MLFO), piloté par le ML Intent (agent/intent.json) : révèle les étapes, transmet les demandes\n"
           "entre agents, se reconfigure sous le seuil de qualité, change de modèle si un quota est épuisé")

boxes = BOXES_FR if FR else BOXES_EN

fig, ax = plt.subplots(figsize=(15.6, 5.6), dpi=150)
ax.set_xlim(0, 156)
ax.set_ylim(0, 56)
ax.axis("off")

ax.add_patch(FancyBboxPatch((1, 1), 154, 54, boxstyle="round,pad=0,rounding_size=1.5",
                            fc="#f3f6fb", ec="#7a8aa5", lw=1.6, ls=(0, (4, 3))))
ax.text(78, 51.2, TITLE_FR if FR else TITLE_EN,
        ha="center", va="center", fontsize=14 if FR else 15, fontweight="bold", color=INK)

w, gap, x0, y0, h = 26.6, 4.2, 3.5, 17.5, 29
for i, (title, body, color, dashed) in enumerate(boxes):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=color, ec=INK, lw=1.6, ls=(0, (4, 2)) if dashed else "-"))
    ax.text(x + w / 2, y0 + h - 4.2, title, ha="center", va="center", fontsize=12.5, fontweight="bold", color=INK)
    ax.text(x + w / 2, y0 + h / 2 - 3, body, ha="center", va="center", fontsize=10.6, color=INK, linespacing=1.35)
    if i < len(boxes) - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.6, y0 + h / 2), (x + w + gap - 0.6, y0 + h / 2),
                                     arrowstyle="-|>", mutation_scale=14, color=INK, lw=2))

# Orchestrateur (MLFO) pilote par le ML Intent
ax.add_patch(FancyBboxPatch((x0, 3.2), 5 * w + 4 * gap, 9.5, boxstyle="round,pad=0,rounding_size=1.2",
                            fc="white", ec=INK, lw=1.6))
ax.text(x0 + (5 * w + 4 * gap) / 2, 7.95, MLFO_FR if FR else MLFO_EN,
        ha="center", va="center", fontsize=10.4, color=INK, linespacing=1.35)
mx = x0 + 2 * (w + gap) + w / 2
ax.add_patch(FancyArrowPatch((mx, 13.0), (mx, 17.2), arrowstyle="<|-|>", mutation_scale=12, color=INK, lw=1.8))

fig.savefig(OUT, bbox_inches="tight", pad_inches=0.05)
print(OUT)
