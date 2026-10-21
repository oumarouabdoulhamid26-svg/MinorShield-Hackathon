"""Animateur de la simulation : protocole de coordination multi-agents.

Pour chaque etape du scenario :
  1. l'etape est revelee UNIQUEMENT a ses destinataires ;
  2. chaque destinataire reagit (recherche + raisonnement + actions) ;
  3. les demandes d'un acteur a un autre sont transmises ; le destinataire
     repond (meme s'il n'a pas recu l'etape : l'information circule alors par
     la demande, comme dans la realite) ;
  4. le conseiller juridique analyse l'etape ;
  5. tout est consigne dans le journal d'audit.

L'animateur ne joue aucune institution et ne prend aucune decision.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from agent.agent2_conseiller.advisor import Advisor
from agent.agent1_institutions.agent import CrisisAgent, Turn
from agent.agent3_coordination.audit import AuditLog
from agent.agent1_institutions.roles import ACTEURS, ROLES
from bd.knowledge.kb import KnowledgeBase

logger = logging.getLogger(__name__)


def load_scenario(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class Orchestrator:
    def __init__(self, scenario: dict[str, Any], run_dir: Path, essai: bool = False,
                 max_demandes: int = 6, on_event: Optional[Callable[[dict[str, Any]], None]] = None):
        self.scenario = scenario
        self.kb = KnowledgeBase()
        self.essai = essai
        self.max_demandes = max_demandes
        self.agents = {r.id: CrisisAgent(r, self.kb, essai=essai) for r in ACTEURS}
        self.advisor = Advisor(self.kb, essai=essai)
        self.audit = AuditLog(run_dir, scenario["id"])
        self.on_event = on_event or (lambda e: None)
        self.steps_out: list[dict[str, Any]] = []

    def _emit(self, entry: dict[str, Any]) -> None:
        self.on_event(entry)

    def run(self, steps: Optional[list[int]] = None) -> dict[str, Any]:
        self._emit(self.audit.event(
            "simulation_debut", scenario=self.scenario["id"], titre=self.scenario["titre"],
            mode="essai (petit modele)" if self.essai else "reference (grand modele)",
            acteurs=[a.id for a in ACTEURS]))

        for step in self.scenario["etapes"]:
            if steps and step["numero"] not in steps:
                continue
            self.steps_out.append(self.run_step(step))

        summary = self.audit.summary()
        self._emit(self.audit.event("simulation_fin", resume=summary))
        self.audit.save({"scenario": self.scenario, "etapes": self.steps_out})
        return summary

    def run_step(self, step: dict[str, Any]) -> dict[str, Any]:
        n = step["numero"]
        dests = [d for d in step["destinataires"] if d in self.agents]
        self._emit(self.audit.event("etape_revelee", etape=n, moment=step["moment"], titre=step["titre"],
                                    information=step["information"], destinataires=dests))

        # 1-2. Revelation et reactions
        turns: list[Turn] = []
        for d in dests:
            self.agents[d].receive_step(step)
        for d in dests:
            t = self.agents[d].react(n)
            turns.append(t)
            self._emit(self.audit.turn(t))

        # 3. Transmission des demandes entre acteurs
        demandes = []
        for t in list(turns):
            for dem in (t.output or {}).get("demandes", []) or []:
                if not isinstance(dem, dict):
                    continue
                to = str(dem.get("destinataire", "")).strip().lower()
                if to in self.agents and to != t.agent:
                    demandes.append((t.agent, to, str(dem.get("objet", ""))))
        if len(demandes) > self.max_demandes:
            self._emit(self.audit.event("demandes_ecartees", etape=n,
                                        nombre=len(demandes) - self.max_demandes,
                                        raison="limite de demandes par etape (quota du modele)"))
        for sender, to, objet in demandes[: self.max_demandes]:
            self.agents[to].receive_message(sender, objet)
            self._emit(self.audit.event("demande_transmise", etape=n, de=sender, a=to, objet=objet))
            rep = self.agents[to].answer(n, sender, objet)
            turns.append(rep)
            self._emit(self.audit.turn(rep, demande={"de": sender, "objet": objet}))
            answer = (rep.output or {}).get("reponse") or "(pas de reponse exploitable)"
            self.agents[sender].receive_message(to, f"Reponse a ta demande « {objet} » : {answer}")

        # 4. Analyse du conseiller juridique
        analyse = self.advisor.analyse(step, turns)
        self._emit(self.audit.turn(analyse))

        return {"etape": n, "destinataires": dests, "demandes": len(demandes),
                "interventions": len(turns), "analyse": analyse.output}


def new_run_dir(base: Path, scenario_id: str) -> Path:
    return base / f"{datetime.now():%Y%m%d-%H%M%S}_{scenario_id}"
