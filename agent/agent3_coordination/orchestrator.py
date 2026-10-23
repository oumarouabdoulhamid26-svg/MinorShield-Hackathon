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

Role d'orchestrateur ML au sens de UIT-T Y.3172 (MLFO) :
  - il est configure par le ML Intent (agent/intent.json, REQ-ML-SPEC-001 a 004) ;
  - il surveille la qualite de chaque reaction et se reconfigure si elle passe
    sous le seuil de l'intent : nouvelle tentative avec plus d'extraits ;
  - il bascule sur le modele de secours si le quota du modele principal est
    epuise (REQ-ML-MNG-001 et MNG-004) ;
  - il peut reprendre une simulation interrompue a partir de son journal.
Chaque reconfiguration est inscrite au journal d'audit.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from agent.agent2_conseiller.advisor import Advisor
from agent.agent1_institutions.agent import CrisisAgent, Turn
from agent.agent3_coordination.audit import AuditLog, verify_turn
from agent.agent1_institutions.roles import ROLES
from agent.commun import intent as intent_mod
from agent.commun import llm
from bd.knowledge.kb import KnowledgeBase

logger = logging.getLogger(__name__)


def load_scenario(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class SimulationInterrompue(Exception):
    """Le modele ne repond plus (quota epuise y compris pour le modele de
    secours, modele inexistant) : on arrete proprement, pour reprendre plus tard."""


def _fatal(error: Optional[str]) -> bool:
    low = (error or "").lower()
    return llm.is_quota_error(low) or "404" in low or "does not exist" in low or "model_not_found" in low


def _support_rate(turn: Turn) -> Optional[float]:
    """Part des actions d'une intervention etayees par un extrait (None : rien a verifier)."""
    checks = verify_turn(turn)
    if not checks:
        return None
    return sum(1 for c in checks if c["statut"] == "etayee") / len(checks)


class Orchestrator:
    def __init__(self, scenario: dict[str, Any], run_dir: Path, essai: bool = False,
                 max_demandes: Optional[int] = None,
                 on_event: Optional[Callable[[dict[str, Any]], None]] = None,
                 intent: Optional[dict[str, Any]] = None):
        self.scenario = scenario
        self.intent = intent or intent_mod.load()
        self.config = intent_mod.apply(self.intent, essai)
        self.kb = KnowledgeBase()
        self.essai = essai
        self.max_demandes = max_demandes or int(self.config["contraintes"].get("demandes_max_par_etape", 6))
        self.qualite = self.config["qualite"]
        self.secours = self.config.get("modele_secours")
        self.agents = {aid: CrisisAgent(ROLES[aid], self.kb, essai=essai)
                       for aid in self.config["agents"] if aid in ROLES}
        self.advisor = Advisor(self.kb, essai=essai)
        self.audit = AuditLog(run_dir, scenario["id"])
        self.on_event = on_event or (lambda e: None)
        self.steps_out: list[dict[str, Any]] = []
        self.deja_demande: set[tuple[str, str, str]] = set()

    def _emit(self, entry: dict[str, Any]) -> None:
        self.on_event(entry)

    # --------------------------------------------------------------- deroule
    def run(self, steps: Optional[list[int]] = None) -> dict[str, Any]:
        self._emit(self.audit.event(
            "simulation_debut", scenario=self.scenario["id"], titre=self.scenario["titre"],
            mode="essai (petit modele)" if self.essai else "reference (grand modele)",
            acteurs=list(self.agents), intent=self._intent_trace()))
        return self._run_steps(steps)

    def resume(self, steps: Optional[list[int]] = None) -> dict[str, Any]:
        """Reprend une simulation interrompue (quota epuise, coupure) dans le meme dossier.

        La memoire des agents (etapes vues, messages recus) est reconstruite a
        partir du journal ; les etapes deja analysees par le conseiller ne sont
        pas rejouees.
        """
        done = self._restore()
        self._emit(self.audit.event("simulation_reprise", etapes_deja_jouees=sorted(done),
                                    intent=self._intent_trace()))
        todo = [s["numero"] for s in self.scenario["etapes"]
                if s["numero"] not in done and (not steps or s["numero"] in steps)]
        return self._run_steps(todo)

    def _run_steps(self, steps: Optional[list[int]]) -> dict[str, Any]:
        for step in self.scenario["etapes"]:
            if steps is not None and step["numero"] not in steps:
                continue
            try:
                self.steps_out.append(self.run_step(step))
            except SimulationInterrompue as e:
                self._emit(self.audit.event(
                    "simulation_interrompue", etape=step["numero"], raison=str(e),
                    reprise=f"python run_simulation.py --reprendre {self.audit.run_dir.as_posix()}"))
                break
        summary = self.audit.summary()
        self._emit(self.audit.event("simulation_fin", resume=summary))
        self.audit.save({"scenario": self.scenario, "intent": self._intent_trace(), "etapes": self.steps_out})
        return summary

    def _intent_trace(self) -> dict[str, Any]:
        return {k: self.config[k] for k in ("fichier", "empreinte", "mode", "modele_principal", "modele_secours")}

    def run_step(self, step: dict[str, Any]) -> dict[str, Any]:
        n = step["numero"]
        dests = [d for d in step["destinataires"] if d in self.agents]
        self._emit(self.audit.event("etape_revelee", etape=n, moment=step["moment"], titre=step["titre"],
                                    information=step["information"], destinataires=dests,
                                    # Entree d'un systeme externe (ex. sortie du detecteur de
                                    # MinorShield), marquee simulee : Y.3172 REQ-ML-COR-002b.
                                    entree_simulee=step.get("entree_simulee")))

        # 1-2. Revelation et reactions (avec controle de qualite)
        turns: list[Turn] = []
        for d in dests:
            self.agents[d].receive_step(step)
        for d in dests:
            t = self._react(d, n)
            turns.append(t)
            self._emit(self.audit.turn(t))

        # 3. Transmission des demandes entre acteurs
        demandes = []
        for t in list(turns):
            for dem in (t.output or {}).get("demandes", []) or []:
                if not isinstance(dem, dict):
                    continue
                to = str(dem.get("destinataire", "")).strip().lower()
                objet = str(dem.get("objet", ""))
                cle = (t.agent, to, " ".join(objet.lower().split()))
                if to in self.agents and to != t.agent and cle in self.deja_demande:
                    # Meme demande deja transmise a une etape precedente : la
                    # reponse est deja dans la memoire de l'agent.
                    self._emit(self.audit.event("demande_repetee", etape=n, de=t.agent, a=to, objet=objet))
                elif to in self.agents and to != t.agent:
                    demandes.append((t.agent, to, objet))
                elif to == t.agent or any(to in i.lower() for i in ROLES[t.agent].institutions):
                    # Passation entre institutions d'un meme agent (police -> parquet).
                    self._emit(self.audit.event("coordination_interne", etape=n, agent=t.agent,
                                                destinataire=to, objet=objet))
                else:
                    # Destinataire inconnu (nom d'institution au lieu d'un agent) :
                    # trace dans le journal, pas d'oubli silencieux.
                    self._emit(self.audit.event("demande_non_transmise", etape=n, de=t.agent,
                                                destinataire=to, objet=objet))
        if len(demandes) > self.max_demandes:
            self._emit(self.audit.event("demandes_ecartees", etape=n,
                                        nombre=len(demandes) - self.max_demandes,
                                        raison="limite de demandes par etape (ML Intent)"))
        for sender, to, objet in demandes[: self.max_demandes]:
            self.deja_demande.add((sender, to, " ".join(objet.lower().split())))
            self.agents[to].receive_message(sender, objet)
            self._emit(self.audit.event("demande_transmise", etape=n, de=sender, a=to, objet=objet))
            rep = self._call_with_fallback(to, n, lambda: self.agents[to].answer(n, sender, objet))
            turns.append(rep)
            self._emit(self.audit.turn(rep, demande={"de": sender, "objet": objet}))
            answer = (rep.output or {}).get("reponse") or "(pas de reponse exploitable)"
            self.agents[sender].receive_message(to, f"Reponse a ta demande « {objet} » : {answer}")

        # 4. Analyse du conseiller juridique
        analyse = self._call_with_fallback("conseiller", n, lambda: self.advisor.analyse(step, turns))
        self._emit(self.audit.turn(analyse))

        return {"etape": n, "destinataires": dests, "demandes": len(demandes),
                "interventions": len(turns), "analyse": analyse.output}

    # -------------------------------------------------------- reconfiguration
    def _call_with_fallback(self, agent_id: str, n: int, call: Callable[[], Turn]) -> Turn:
        """Appel d'un agent ; si le quota du modele courant est epuise, bascule
        une fois sur le modele de secours de l'intent et recommence."""
        turn = call()
        if not _fatal(turn.parse_error):
            return turn
        if (llm.is_quota_error(turn.parse_error or "") and self.secours
                and llm.model_name(self.essai) != self.secours):
            avant = llm.model_name(self.essai)
            llm.use_model(self.secours)
            self._emit(self.audit.event(
                "reconfiguration", etape=n, agent=agent_id, type="bascule_modele",
                raison=f"quota epuise sur {avant}", avant=avant, apres=self.secours,
                regle="ML Intent : modeles.secours (Y.3172 REQ-ML-MNG-001, MNG-004)"))
            turn = call()
            if not _fatal(turn.parse_error):
                return turn
        # Plus aucun modele disponible : inutile de continuer a vide.
        raise SimulationInterrompue(f"{agent_id} : {turn.parse_error}")

    def _react(self, agent_id: str, n: int) -> Turn:
        """Reaction d'un agent, controlee : si son taux d'actions etayees passe
        sous le seuil de l'intent, nouvelle tentative avec plus d'extraits.
        La meilleure des deux tentatives est gardee ; l'autre reste tracee."""
        agent = self.agents[agent_id]
        turn = self._call_with_fallback(agent_id, n, lambda: agent.react(n))
        seuil = float(self.qualite.get("seuil_taux_etayees_agent", 0))
        tentatives = int(self.qualite.get("nouvelles_tentatives", 0))
        extra = int(self.qualite.get("extraits_supplementaires", 2))
        n_extraits = len(turn.extracts)
        for essai_no in range(1, tentatives + 1):
            taux = _support_rate(turn)
            if taux is None or taux >= seuil or turn.parse_error:
                break
            n_extraits += extra
            nouveau = self._call_with_fallback(agent_id, n, lambda: agent.react(n, n_extracts=n_extraits))
            nouveau_taux = _support_rate(nouveau)
            garde = nouveau if (nouveau_taux or 0) > taux else turn
            self.audit.tokens += (turn if garde is nouveau else nouveau).tokens
            self._emit(self.audit.event(
                "reconfiguration", etape=n, agent=agent_id, type="nouvelle_tentative",
                raison=f"taux d'actions etayees {taux:.0%} sous le seuil de {seuil:.0%}",
                avant={"extraits": len(turn.extracts), "taux": round(taux, 3), "jetons": turn.tokens},
                apres={"extraits": len(nouveau.extracts), "taux": round(nouveau_taux or 0, 3),
                       "jetons": nouveau.tokens},
                tentative=essai_no, retenue="nouvelle" if garde is nouveau else "initiale",
                regle="ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)"))
            turn = garde
        return turn

    # ------------------------------------------------------------------ reprise
    def _restore(self) -> set[int]:
        """Recharge le journal existant et reconstruit la memoire des agents.

        Une etape est terminee quand le conseiller l'a analysee. Une etape
        interrompue en cours de route est rejouee entierement : sa trace
        partielle reste dans le journal (marquee abandonnee) mais n'entre ni
        dans la memoire des agents ni dans le bilan.
        """
        entries = self.audit.read_existing()
        done = {e["etape"] for e in entries
                if e["evenement"] == "intervention_analyse" and not e.get("erreur")}
        partial = {e["etape"] for e in entries if "etape" in e} - done
        self.audit.load_existing(entries, keep_steps=done)
        for n in sorted(partial):
            self._emit(self.audit.event("etape_abandonnee", etape=n,
                                        raison="etape interrompue, rejouee entierement a la reprise"))
        steps = {s["numero"]: s for s in self.scenario["etapes"]}
        for e in entries:
            if "etape" in e and e["etape"] not in done:
                continue
            ev = e["evenement"]
            if ev == "etape_revelee" and e["etape"] in steps:
                for d in e.get("destinataires", []):
                    if d in self.agents:
                        self.agents[d].receive_step(steps[e["etape"]])
            elif ev == "demande_transmise" and e["a"] in self.agents:
                self.agents[e["a"]].receive_message(e["de"], e["objet"])
                self.deja_demande.add((e["de"], e["a"], " ".join(e["objet"].lower().split())))
            elif ev == "intervention_reponse" and e.get("demande"):
                dem = e["demande"]
                answer = (e.get("reponse") or {}).get("reponse") or "(pas de reponse exploitable)"
                if dem.get("de") in self.agents:
                    self.agents[dem["de"]].receive_message(
                        e["agent"], f"Reponse a ta demande « {dem.get('objet', '')} » : {answer}")
            elif ev == "intervention_analyse" and not e.get("erreur"):
                self.steps_out.append({"etape": e["etape"], "analyse": e.get("reponse")})
            elif ev == "reconfiguration" and e.get("type") == "bascule_modele":
                llm.use_model(e["apres"])
        return done


def new_run_dir(base: Path, scenario_id: str) -> Path:
    return base / f"{datetime.now():%Y%m%d-%H%M%S}_{scenario_id}"
