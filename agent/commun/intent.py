"""Lecture du ML Intent (agent/intent.json) et traduction en configuration.

UIT-T Y.3172 demande une maniere declarative de decrire une application ML
(REQ-ML-SPEC-001 a 004) : sources de donnees, modeles, contraintes de temps et
de ressources, sorties. Ce module lit cette specification, la valide, puis
configure les modules concernes (modele de langage, recherche, historique).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "agent" / "intent.json"

REQUIRED = ("id", "sources", "agents", "modeles", "contraintes", "qualite", "sorties")


def load(path: Path = DEFAULT_PATH) -> dict[str, Any]:
    raw = path.read_bytes()
    intent = json.loads(raw.decode("utf-8"))
    missing = [k for k in REQUIRED if k not in intent]
    if missing:
        raise ValueError(f"ML Intent incomplet ({path.name}) : champs manquants {missing}")
    intent["_fichier"] = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
    intent["_empreinte"] = hashlib.sha256(raw).hexdigest()[:12]
    return intent


def apply(intent: dict[str, Any], essai: bool) -> dict[str, Any]:
    """Configure les modules a partir de l'intent ; renvoie ce qui a ete applique."""
    from agent.agent1_institutions import agent as agent_mod
    from agent.commun import llm

    c = intent["contraintes"]
    agent_mod.DEFAULT_EXTRACTS = int(c.get("extraits_par_agent", agent_mod.DEFAULT_EXTRACTS))
    agent_mod.ANSWER_EXTRACTS = int(c.get("extraits_par_reponse", agent_mod.ANSWER_EXTRACTS))
    agent_mod.EXTRACT_CHARS = int(c.get("longueur_extrait", agent_mod.EXTRACT_CHARS))
    h = c.get("historique", {})
    agent_mod.OLD_STEP_CHARS = int(h.get("etapes_anciennes_caracteres", agent_mod.OLD_STEP_CHARS))
    agent_mod.INBOX_KEEP = int(h.get("messages_gardes", agent_mod.INBOX_KEEP))
    agent_mod.MESSAGE_CHARS = int(h.get("message_caracteres", agent_mod.MESSAGE_CHARS))
    llm.REQUEST_TOKEN_BUDGET = int(c.get("jetons_max_par_requete", llm.REQUEST_TOKEN_BUDGET))

    mode = "essai" if essai else "reference"
    modeles = intent["modeles"][mode]
    llm.use_model(modeles["principal"])
    return {
        "fichier": intent["_fichier"],
        "empreinte": intent["_empreinte"],
        "mode": mode,
        "modele_principal": modeles["principal"],
        "modele_secours": modeles.get("secours"),
        "agents": intent["agents"],
        "contraintes": c,
        "qualite": intent["qualite"],
    }
