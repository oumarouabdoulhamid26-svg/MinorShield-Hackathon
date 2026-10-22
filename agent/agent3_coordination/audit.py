"""Journal d'audit et verification des citations.

Chaque intervention d'agent est enregistree (fichier JSONL, une ligne par
evenement) avec : ce que l'agent savait, les extraits retrouves, sa reponse,
son raisonnement explicite, le modele et les jetons consommes.

Chaque action est en outre VERIFIEE :
  - « etayee »            : cite au moins un extrait reellement fourni ;
  - « non_etayee »        : ne cite aucun extrait ;
  - « citation_invalide » : cite un identifiant qui n'a pas ete fourni
                            (signe d'une invention du modele).
Les articles mentionnes dans le texte libre mais absents des extraits cites
sont signales (« mention non verifiee »).
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from agent.agent1_institutions.agent import Turn
from agent.agent1_institutions.roles import ROLES

_ARTICLE_MENTION = re.compile(r"\bart(?:icle|\.)?\s*(\d{1,3})\b", re.I)
# Textes nommes par leur numero : « Directive 2018/1725 », « Règlement (UE) 2016/679 »,
# « loi n° 2023/009 », « décret 2015/3759/PM »...
_INSTRUMENT_MENTION = re.compile(
    r"\b(?:directive|r[èe]glement|regulation|loi|law|d[ée]cret|decree)\s*(?:\(UE\)|\(EU\))?\s*(?:n[°o]\s*)?"
    r"(\d{2,4}\s*/\s*\d{1,5})", re.I)
# Textes nommes par leur sigle ou leur nom usuel. Valeur : fragment du nom de
# fichier qui doit figurer parmi les extraits cites ; None = texte absent de la
# base (toute mention est donc invérifiable).
_NAMED_INSTRUMENTS = {
    r"\bCOPPA\b|Children'?s Online Privacy": "COPPA",
    r"\bDSA\b|Digital Services Act": "EU_DSA",
    r"\bRGPD\b|\bGDPR\b|protection des donn[ée]es \(UE\)": "EU_RGPD",
    r"Online Safety Act 2023": "UK_Online_Safety",
    r"Online Safety Act 2021": "Australia_Online_Safety",
    r"\bCCPA\b|\bCPRA\b|California Consumer Privacy": None,
    r"\bKOSA\b|Kids Online Safety": None,
    r"\bDMA\b|Digital Markets Act": None,
    r"\bAI Act\b|r[èe]glement sur l'intelligence artificielle": None,
    r"Age Appropriate Design|Children'?s Code": None,
    r"\bLCEN\b|Informatique et libert[ée]s": None,
}
_JURIDICTIONS = {
    "European Union": ("ue", "union europ", "europe", "eu "),
    "United Kingdom": ("royaume-uni", "royaume uni", "uk", "britann"),
    "United States": ("etats-unis", "états-unis", "usa", "us ", "amérique", "amerique"),
    "Australia": ("australie", "australia"),
    "Cameroon": ("cameroun", "cameroon"),
}

# Statuts, du plus sur au moins sur.
STATUTS = ("etayee", "citation_douteuse", "non_etayee", "citation_invalide")


def _ids(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    out = []
    for v in value:
        out += re.findall(r"\bE\d+\b", str(v))
    return out


def _country_of(juridiction: str) -> Optional[str]:
    j = f" {juridiction.lower()} "
    for country, keys in _JURIDICTIONS.items():
        if any(k in j for k in keys):
            return country
    return None


def check_citations(cited: list[str], text: str, extracts_by_id: dict[str, Any],
                    juridiction: Optional[str] = None) -> dict[str, Any]:
    """Verifie qu'une affirmation s'appuie reellement sur les extraits fournis.

    Au-dela de l'existence des identifiants cites, on controle :
      - les articles mentionnes dans le texte : doivent appartenir aux extraits cites ;
      - les textes nommes par leur numero (« Directive 2018/1725 ») : doivent
        figurer dans le titre d'un extrait cite ;
      - la juridiction annoncee (« UE : ... ») : doit correspondre au pays de
        l'extrait cite.
    Toute anomalie fait passer le statut a « citation_douteuse ».
    """
    valid = [c for c in cited if c in extracts_by_id]
    invalid = sorted(set(c for c in cited if c not in extracts_by_id))
    cited_articles = {str(extracts_by_id[c].article) for c in valid}
    cited_titles = " ".join(extracts_by_id[c].label() for c in valid)
    titles_norm = re.sub(r"\s", "", cited_titles)

    unverified_articles = sorted({a for a in _ARTICLE_MENTION.findall(text or "") if a not in cited_articles})
    unverified_instruments = sorted({re.sub(r"\s", "", n) for n in _INSTRUMENT_MENTION.findall(text or "")
                                     if re.sub(r"\s", "", n) not in titles_norm})
    cited_files = " ".join(extracts_by_id[c].source_file for c in valid)
    for pattern, file_part in _NAMED_INSTRUMENTS.items():
        m = re.search(pattern, text or "", re.I)
        if m and (file_part is None or file_part not in cited_files):
            unverified_instruments.append(m.group(0))
    incoherence = []
    if juridiction and valid:
        expected = _country_of(juridiction)
        got = {extracts_by_id[c].country for c in valid}
        if expected and expected not in got:
            incoherence.append(f"« {juridiction} » annonce, mais la source citee concerne : {', '.join(sorted(got))}")

    if invalid:
        status = "citation_invalide"
    elif not valid:
        status = "non_etayee"
    elif unverified_articles or unverified_instruments or incoherence:
        status = "citation_douteuse"
    else:
        status = "etayee"
    return {
        "statut": status,
        "citations_valides": valid,
        "citations_invalides": invalid,
        "sources": [extracts_by_id[c].label() for c in valid],
        "mentions_non_verifiees": [f"article {a}" for a in unverified_articles],
        "textes_non_verifies": unverified_instruments,
        "incoherences": incoherence,
    }


def _institution(agent_id: str, value: Any) -> dict[str, Any]:
    """L'institution nommee pour une action appartient-elle a l'agent ?

    Un agent qui regroupe plusieurs institutions doit dire laquelle agit ;
    une institution absente ou etrangere a l'agent est signalee.
    """
    role = ROLES.get(agent_id)
    allowed = role.institutions if role else []
    name = str(value or "").strip()

    def norm(s: str) -> str:
        return "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")

    match = next((i for i in allowed if name and (norm(name) in norm(i) or norm(i) in norm(name))), "")
    return {"institution": match or name, "institution_valide": bool(match) or not allowed}


def verify_turn(turn: Turn) -> list[dict[str, Any]]:
    """Verifie chaque action (ou la reponse) d'une intervention."""
    by_id = {e.id: e for e in turn.extracts}
    out = turn.output or {}
    checks: list[dict[str, Any]] = []
    if not out:
        # Appel au modele echoue (quota, reseau) ou reponse illisible : rien a
        # verifier. L'erreur reste visible dans le journal, mais n'est pas
        # comptee comme une action « non etayee ».
        return checks
    if turn.kind == "reaction":
        for a in out.get("actions", []) or []:
            if not isinstance(a, dict):
                continue
            text = f"{a.get('action', '')} {a.get('justification', '')}"
            c = check_citations(_ids(a.get("base_legale")), text, by_id)
            c["action"] = a.get("action", "")
            c.update(_institution(turn.agent, a.get("institution")))
            checks.append(c)
    elif turn.kind == "reponse":
        c = check_citations(_ids(out.get("base_legale")), out.get("reponse", ""), by_id)
        c["action"] = out.get("reponse", "")
        c.update(_institution(turn.agent, out.get("institution")))
        checks.append(c)
    elif turn.kind == "analyse":
        # 1. Verdicts du conseiller sur les actions des acteurs
        for v in out.get("verifications", []) or []:
            if isinstance(v, dict):
                text = f"{v.get('commentaire', '')}"
                c = check_citations(_ids(text), text, by_id)
                c["action"] = f"Verdict « {v.get('verdict', '')} » sur {v.get('acteur', '')} : {v.get('action', '')}"
                checks.append(c)
        # 2. Lacunes : constat sur le droit camerounais...
        for item in out.get("lacunes", []) or []:
            if not isinstance(item, dict):
                continue
            c = check_citations(_ids(item.get("texte_camerounais")), item.get("lacune", ""), by_id,
                                juridiction="Cameroun")
            c["action"] = f"Lacune : {item.get('lacune', '')}"
            checks.append(c)
            # ... et chaque comparaison avec une juridiction etrangere
            for comp in item.get("comparaison", []) or []:
                if not isinstance(comp, dict):
                    continue
                text = f"{comp.get('pratique', '')}"
                c = check_citations(_ids(comp.get("reference")), text, by_id,
                                    juridiction=str(comp.get("juridiction", "")))
                c["action"] = f"Comparaison {comp.get('juridiction', '')} : {comp.get('pratique', '')}"
                checks.append(c)
    return checks


class AuditLog:
    """Journal d'une simulation : un fichier JSONL + un resume final."""

    def __init__(self, run_dir: Path, scenario_id: str):
        self.run_dir = run_dir
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.path = run_dir / "journal.jsonl"
        self.scenario_id = scenario_id
        self.entries: list[dict[str, Any]] = []
        self.status_counter: Counter = Counter()
        self.tokens = 0
        self.institutions = Counter()   # actions avec / sans institution valide

    def event(self, kind: str, **data: Any) -> dict[str, Any]:
        entry = {"horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "evenement": kind, **data}
        self.entries.append(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
        return entry

    def turn(self, turn: Turn, demande: Optional[dict[str, str]] = None) -> dict[str, Any]:
        checks = verify_turn(turn)
        for c in checks:
            self.status_counter[c["statut"]] += 1
            if "institution_valide" in c:
                self.institutions["valide" if c["institution_valide"] else "manquante"] += 1
        self.tokens += turn.tokens
        return self.event(
            f"intervention_{turn.kind}",
            etape=turn.step,
            agent=turn.agent,
            demande=demande,
            informations_visibles=turn.visible_info,
            messages_recus=turn.messages_in,
            requete_recherche=turn.query,
            extraits=[e.to_dict() for e in turn.extracts],
            reponse=turn.output,
            raisonnement=(turn.output or {}).get("raisonnement", []),
            verification=checks,
            modele=turn.model,
            jetons=turn.tokens,
            duree_s=turn.seconds,
            erreur=turn.parse_error,
        )

    def summary(self) -> dict[str, Any]:
        total = sum(self.status_counter.values())
        return {
            "scenario": self.scenario_id,
            "evenements": len(self.entries),
            "interventions": sum(1 for e in self.entries if e["evenement"].startswith("intervention")),
            "verifications": dict(self.status_counter),
            "taux_etayees": round(self.status_counter["etayee"] / total, 3) if total else None,
            "jetons_total": self.tokens,
            "institution_nommee": dict(self.institutions),
            "demandes_transmises": sum(1 for e in self.entries if e["evenement"] == "demande_transmise"),
            "demandes_non_transmises": sum(1 for e in self.entries if e["evenement"] == "demande_non_transmise"),
        }

    def save(self, extra: Optional[dict[str, Any]] = None) -> Path:
        out = {"resume": self.summary(), **(extra or {})}
        p = self.run_dir / "resume.json"
        p.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return p


def turn_as_dict(turn: Turn) -> dict[str, Any]:
    d = asdict(turn)
    d["extracts"] = [e.to_dict() for e in turn.extracts]
    return d
