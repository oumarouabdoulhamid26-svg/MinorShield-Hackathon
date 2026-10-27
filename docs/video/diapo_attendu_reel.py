"""Diapositive de la scene 9 de la video : resultat attendu et resultat reel, etape par etape.

    python docs/video/diapo_attendu_reel.py   ->  docs/video/attendu_reel.png

Sources : lacunes attendues du scenario et relecture humaine de la simulation de
reference du 24/10/2026 (docs/LACUNES.md, section C).
"""

from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).with_name("attendu_reel.png")
INK, OK, PART, MISS = "#2f3e4e", "#2e7d4f", "#b26a00", "#b3261e"

ROWS = [
    ("1", "Rise in blocked content",
     "No channel or threshold for a private tool\nto alert the authorities",
     [("Found", OK)]),
    ("2", "Block on a 14-year-old's phone,\ncapture sent abroad",
     "Screen monitoring and consent · transfer to a\nforeign AI service · liability for a false positive ·\ndetector standards · definition of harmful content",
     [("Transfer, liability: partly", PART), ("Monitoring, standards, definition: missed", MISS)]),
    ("3", "Two victims (15 and 19),\nschool exclusion",
     "Overlap of two ministries · no school directive ·\n19-year-old outside the Charter (under 18)",
     [("Overlap, school: found", OK), ("Age threshold: missed", MISS)]),
    ("4", "Images on a foreign platform",
     "No reach on foreign platforms ·\n15-day notice too slow for viral content",
     [("Reach: found", OK), ("Notice: partly (48 h proposed)", PART)]),
    ("5", "Leak from a school app",
     "Breach notice \"without delay\" with no deadline ·\ndata protection authority only since June 2026",
     [("Deadline: found (72 h)", OK), ("New authority: missed", MISS)]),
    ("6", "Block the platform nationwide?",
     "Child protection vs freedom of expression ·\nno crisis coordination body",
     [("Both found", OK)]),
]

fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
ax.set_xlim(0, 160)
ax.set_ylim(-3, 90)
ax.axis("off")
fig.patch.set_facecolor("white")

ax.text(80, 85, "Expected gaps vs. what the agents actually found", ha="center", fontsize=24,
        fontweight="bold", color=INK)
ax.text(80, 80.2, "Reference run, 24 Oct 2026 · gpt-oss-120b · expected gaps written into the scenario "
                  "before the run · human review", ha="center", fontsize=12.5, color="#5b6b7c")

for x, title in [(0.5, "Stage"), (11, "Event"), (47, "Expected (written beforehand)"), (111, "Actual result")]:
    ax.text(x, 74, title, fontsize=14, fontweight="bold", color=INK, va="center")
ax.plot([1, 159], [71.5, 71.5], color=INK, lw=1.2)

y = 66
for stage, event, expected, results in ROWS:
    ax.text(4.5, y, stage, fontsize=18, fontweight="bold", color=INK, va="center", ha="center")
    ax.text(11, y, event, fontsize=12.5, color=INK, va="center", linespacing=1.3)
    ax.text(47, y, expected, fontsize=11.5, color=INK, va="center", linespacing=1.3)
    top = y + 2.1 * (len(results) - 1)
    for k, (label, color) in enumerate(results):
        bullet = "" if k and color == results[k - 1][1] and label[0].islower() else "● "
        ax.text(111, top - 4.2 * k, (bullet or "   ") + label, fontsize=12.5, color=color,
                va="center", fontweight="bold")
    ax.plot([1, 159], [y - 5.4, y - 5.4], color="#d9dee5", lw=0.8)
    y -= 10.8

ax.text(80, 3.5, "Total: 7 found · 3 partly · 5 missed (out of 15 expected) · plus 4 gaps not anticipated:",
        ha="center", fontsize=13, fontweight="bold", color=INK)
ax.text(80, -0.5, "police access to mobile-money records · anonymisation before transmission · "
                  "data authority / ICT regulator overlap · missing implementing text",
        ha="center", fontsize=11.5, color=INK)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(OUT)
