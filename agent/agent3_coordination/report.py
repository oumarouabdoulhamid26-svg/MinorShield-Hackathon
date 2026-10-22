"""Rapport lisible (Markdown) d'une simulation, construit depuis le journal d'audit."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from agent.agent1_institutions.roles import ROLES

STATUT = {"etayee": "✅ étayée", "citation_douteuse": "🔶 citation douteuse", "non_etayee": "⚠️ non étayée", "citation_invalide": "❌ citation invalide"}
VERDICT = {"fondee": "✅ fondée", "a_verifier": "⚠️ à vérifier", "non_fondee": "❌ non fondée"}


def _name(agent_id: str) -> str:
    r = ROLES.get(agent_id)
    return r.nom.split(" —")[0] if r else agent_id


def _warnings(c: dict) -> str:
    parts = []
    if c.get("mentions_non_verifiees"):
        parts.append("mention non vérifiée : " + ", ".join(c["mentions_non_verifiees"]))
    if c.get("textes_non_verifies"):
        parts.append("texte absent de la base : " + ", ".join(c["textes_non_verifies"]))
    if c.get("incoherences"):
        parts.append("; ".join(c["incoherences"]))
    return (" · " + " · ".join(parts)) if parts else ""


def _list(items: Any) -> list[str]:
    if isinstance(items, list):
        return [str(i) for i in items if str(i).strip()]
    return [str(items)] if items else []


def _steps(items: Any) -> list[str]:
    """Etapes de raisonnement ; un bloc unique « 1. ... 2. ... » est redecoupe."""
    steps = _list(items)
    if len(steps) == 1 and re.search(r"\b2\.\s", steps[0]):
        steps = [s.strip() for s in re.split(r"(?:^|\s)\d+\.\s", steps[0]) if s.strip()]
    return [re.sub(r"^\d+\.\s*", "", s) for s in steps]


def build(run_dir: Path) -> Path:
    entries = [json.loads(line) for line in (run_dir / "journal.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    out: list[str] = []
    debut = next((e for e in entries if e["evenement"] == "simulation_debut"), {})
    fin = next((e for e in entries if e["evenement"] == "simulation_fin"), {})
    out.append(f"# Rapport de simulation — {debut.get('titre', '')}\n")
    out.append(f"*Mode : {debut.get('mode', '')} · {debut.get('horodatage', '')}*\n")

    if fin:
        r = fin["resume"]
        v = r.get("verifications", {})
        out.append("## Bilan\n")
        out.append("| Indicateur | Valeur |\n|---|---|")
        out.append(f"| Interventions d'agents | {r.get('interventions')} |")
        out.append(f"| Actions étayées par un extrait | {v.get('etayee', 0)} |")
        out.append(f"| Actions non étayées | {v.get('non_etayee', 0)} |")
        out.append(f"| Citations invalides | {v.get('citation_invalide', 0)} |")
        taux = r.get("taux_etayees")
        out.append(f"| Taux d'actions étayées | {f'{taux:.0%}' if taux is not None else '—'} |")
        inst = r.get("institution_nommee") or {}
        if inst:
            out.append(f"| Actions avec institution nommée | {inst.get('valide', 0)} sur "
                       f"{inst.get('valide', 0) + inst.get('manquante', 0)} |")
        if "demandes_transmises" in r:
            out.append(f"| Demandes entre agents | {r['demandes_transmises']} transmises, "
                       f"{r.get('demandes_non_transmises', 0)} non transmises |")
        out.append(f"| Jetons consommés | {r.get('jetons_total')} |\n")

    for e in entries:
        ev = e["evenement"]
        if ev == "etape_revelee":
            out.append(f"\n---\n\n## Étape {e['etape']} — {e['titre']}\n")
            out.append(f"**{e['moment']}** · Informés : {', '.join(_name(d) for d in e['destinataires'])}\n")
            out.append(f"> {e['information']}\n")
        elif ev == "demande_transmise":
            out.append(f"\n**Demande** — {_name(e['de'])} → {_name(e['a'])} : {e['objet']}\n")
        elif ev == "demande_non_transmise":
            out.append(f"\n*Demande non transmise (destinataire inconnu « {e['destinataire']} »)* — "
                       f"{_name(e['de'])} : {e['objet']}\n")
        elif ev.startswith("intervention_"):
            rep = e.get("reponse") or {}
            kind = ev.replace("intervention_", "")
            if e.get("erreur"):
                out.append(f"\n### {_name(e['agent'])}\n\n*Erreur : {e['erreur']}*\n")
                continue
            if kind == "reaction":
                out.append(f"\n### {_name(e['agent'])}\n")
                if rep.get("evaluation"):
                    out.append(f"**Évaluation.** {rep['evaluation']}\n")
                inc = _list(rep.get("inconnues"))
                if inc:
                    out.append("**Ce qu'il ignore :** " + " ; ".join(inc) + "\n")
                checks = e.get("verification", [])
                if checks:
                    out.append("| Action | Vérification | Sources |\n|---|---|---|")
                    for c in checks:
                        src = "<br>".join(c["sources"]) or "—"
                        warn = _warnings(c)
                        qui = f"**{c['institution']}** — " if c.get("institution") else ""
                        if c.get("institution_valide") is False:
                            warn += " ⚠️ institution non précisée"
                        out.append(f"| {qui}{c['action']} | {STATUT.get(c['statut'], c['statut'])}{warn} | {src} |")
                    out.append("")
                lac = _list(rep.get("lacunes"))
                if lac:
                    out.append("**Lacunes signalées :**\n" + "\n".join(f"- {x}" for x in lac) + "\n")
                rais = _steps(rep.get("raisonnement"))
                if rais:
                    out.append("<details><summary>Raisonnement explicite</summary>\n\n"
                               + "\n".join(f"{i}. {x}" for i, x in enumerate(rais, 1)) + "\n\n</details>\n")
            elif kind == "reponse":
                checks = e.get("verification", [{}])
                c = checks[0] if checks else {}
                out.append(f"**Réponse de {_name(e['agent'])}** ({STATUT.get(c.get('statut'), '')}) : {rep.get('reponse', '')}\n")
            elif kind == "analyse":
                out.append("\n### ⚖️ Analyse du conseiller juridique\n")
                if rep.get("synthese"):
                    out.append(f"{rep['synthese']}\n")
                ver = [v for v in rep.get("verifications", []) or [] if isinstance(v, dict)]
                if ver:
                    out.append("| Acteur | Action | Verdict | Commentaire |\n|---|---|---|---|")
                    for v in ver:
                        out.append(f"| {_name(str(v.get('acteur', '')))} | {v.get('action', '')} | "
                                   f"{VERDICT.get(v.get('verdict'), v.get('verdict', ''))} | {v.get('commentaire', '')} |")
                    out.append("")
                extracts = {x["id"]: x["label"] for x in e.get("extraits", [])}
                for g in rep.get("lacunes", []) or []:
                    if not isinstance(g, dict):
                        continue
                    out.append(f"**Lacune : {g.get('lacune', '')}**\n")
                    refs = [extracts.get(i, i) for i in _list(g.get("texte_camerounais"))]
                    if refs:
                        out.append("- Droit camerounais : " + " ; ".join(refs))
                    for comp in g.get("comparaison", []) or []:
                        if isinstance(comp, dict):
                            ref = extracts.get(str(comp.get("reference", "")), comp.get("reference", ""))
                            out.append(f"- {comp.get('juridiction', '')} : {comp.get('pratique', '')}"
                                       + (f" *({ref})*" if ref else ""))
                    if g.get("recommandation"):
                        out.append(f"- **Recommandation :** {g['recommandation']}")
                    out.append("")
                for title, key in (("Conflits", "conflits"), ("Problèmes de coordination", "coordination")):
                    items = _list(rep.get(key))
                    if items:
                        out.append(f"**{title} :**\n" + "\n".join(f"- {x}" for x in items) + "\n")

    path = run_dir / "rapport.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path
