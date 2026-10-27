"""Tests de l'orchestrateur : ML Intent, reconfiguration automatique, reprise.

Le modele de langage est remplace par un faux modele : les tests ne consomment
aucun jeton et provoquent volontairement les situations a verifier (reponse
mal etayee, quota epuise, simulation interrompue). La recherche dans la base
reste reelle (embeddings locaux via Ollama).

    python -m unittest agent.tests.test_orchestration -v

Les erreurs que les tests provoquent volontairement (quota epuise...) ne sont
pas affichees : seul compte le verdict de chaque test.
"""

from __future__ import annotations

import json
import logging
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

from agent.agent1_institutions import agent as agent_mod
from agent.agent3_coordination.orchestrator import Orchestrator, load_scenario
from agent.commun import intent as intent_mod
from agent.commun import llm

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = load_scenario(ROOT / "agent" / "scenarios" / "operation_miroir.json")


def scenario(steps: list[int]) -> dict:
    s = dict(SCENARIO)
    s["etapes"] = [e for e in SCENARIO["etapes"] if e["numero"] in steps]
    return s


def reaction(supported: bool) -> str:
    return json.dumps({
        "evaluation": "situation lue", "inconnues": [],
        "actions": [{"institution": "MinorShield", "action": "Informer le parent du blocage",
                     "base_legale": ["E1"] if supported else [],
                     "justification": "l'extrait fourni fonde cette information" if supported else ""}],
        "demandes": [], "lacunes": [], "confiance": 0.5, "raisonnement": ["etape 1"]})


ANALYSE = json.dumps({"verifications": [], "lacunes": [], "conflits": [], "coordination": [],
                      "synthese": "analyse factice"})
REPONSE = json.dumps({"institution": "APDP", "reponse": "pris en compte", "base_legale": [],
                      "peut_agir": True, "raisonnement": []})


class FakeLLM:
    """Faux modele : ``plan`` donne, dans l'ordre, la suite des reactions
    (« ok », « non_etayee » ou « quota ») ; ensuite tout est « ok »."""

    def __init__(self, plan: list[str]):
        self.plan = list(plan)
        self.models: list[str] = []

    def __call__(self, system, user, fast=False, **kw):
        self.models.append(llm.model_name(fast))
        if "Analyse cette etape" in user:
            text = ANALYSE
        elif "Reponds a cette demande" in user:
            text = REPONSE
        else:
            kind = self.plan.pop(0) if self.plan else "ok"
            if kind == "quota":
                raise RuntimeError("Error code: 429 - Rate limit reached")
            text = reaction(kind == "ok")
        return llm.LLMResult(text=text, model=llm.model_name(fast), prompt_tokens=100, completion_tokens=50)


class OrchestrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run_dir = Path(self.tmp.name) / "run"
        # Connexions HTTP laissees ouvertes par le client Ollama (sans effet sur
        # les resultats) et erreurs provoquees volontairement : non affichees.
        warnings.simplefilter("ignore", ResourceWarning)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        llm.use_model(None)
        self.tmp.cleanup()

    def journal(self) -> list[dict]:
        return [json.loads(l) for l in (self.run_dir / "journal.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_intent_configure_les_modules(self):
        intent = intent_mod.load()
        cfg = intent_mod.apply(intent, essai=True)
        self.assertEqual(llm.model_name(True), intent["modeles"]["essai"]["principal"])
        self.assertEqual(agent_mod.DEFAULT_EXTRACTS, intent["contraintes"]["extraits_par_agent"])
        self.assertEqual(cfg["agents"], intent["agents"])
        self.assertEqual(len(cfg["empreinte"]), 12)

    def test_reconfiguration_si_taux_sous_le_seuil(self):
        fake = FakeLLM(["non_etayee", "ok"])
        with mock.patch.object(llm, "chat", fake):
            Orchestrator(scenario([1]), self.run_dir, essai=True).run()
        rec = [e for e in self.journal() if e["evenement"] == "reconfiguration"]
        self.assertTrue(rec, "aucune reconfiguration inscrite au journal")
        self.assertEqual(rec[0]["type"], "nouvelle_tentative")
        self.assertEqual(rec[0]["retenue"], "nouvelle")
        self.assertGreater(rec[0]["apres"]["extraits"], rec[0]["avant"]["extraits"])

    def test_bascule_sur_le_modele_de_secours(self):
        intent = intent_mod.load()
        fake = FakeLLM(["quota"])
        with mock.patch.object(llm, "chat", fake):
            Orchestrator(scenario([1]), self.run_dir, essai=True, intent=intent).run()
        rec = [e for e in self.journal() if e["evenement"] == "reconfiguration" and e["type"] == "bascule_modele"]
        self.assertEqual(len(rec), 1)
        self.assertEqual(rec[0]["apres"], intent["modeles"]["essai"]["secours"])
        self.assertEqual(fake.models[-1], intent["modeles"]["essai"]["secours"])

    def test_arret_propre_si_aucun_modele_ne_repond(self):
        # Quota epuise sur le principal puis sur le secours : arret, puis reprise.
        fake = FakeLLM(["quota", "quota"])
        with mock.patch.object(llm, "chat", fake):
            Orchestrator(scenario([1, 2]), self.run_dir, essai=True).run()
        stop = [e for e in self.journal() if e["evenement"] == "simulation_interrompue"]
        self.assertEqual(len(stop), 1)
        self.assertIn("--reprendre", stop[0]["reprise"])
        self.assertFalse([e for e in self.journal() if e["evenement"] == "intervention_analyse"])
        llm.use_model(None)
        with mock.patch.object(llm, "chat", FakeLLM([])):
            Orchestrator(scenario([1, 2]), self.run_dir, essai=True).resume()
        j = self.journal()
        self.assertTrue([e for e in j if e["evenement"] == "etape_abandonnee" and e["etape"] == 1])
        self.assertEqual([e["etape"] for e in j if e["evenement"] == "intervention_analyse"], [1, 2])

    def test_reprise_ne_rejoue_pas_les_etapes_terminees(self):
        with mock.patch.object(llm, "chat", FakeLLM([])):
            Orchestrator(scenario([1, 2]), self.run_dir, essai=True).run(steps=[1])
            orch = Orchestrator(scenario([1, 2]), self.run_dir, essai=True)
            orch.resume()
        j = self.journal()
        reprise = next(e for e in j if e["evenement"] == "simulation_reprise")
        self.assertEqual(reprise["etapes_deja_jouees"], [1])
        analyses = [e["etape"] for e in j if e["evenement"] == "intervention_analyse"]
        self.assertEqual(analyses, [1, 2])
        # La memoire de MinorShield (destinataire des etapes 1 et 2) contient les deux etapes.
        self.assertEqual(len(orch.agents["minorshield"].known_steps), 2)

    def test_destinataire_ecrit_avec_le_nom_de_l_institution(self):
        from agent.agent3_coordination.orchestrator import resolve_agent
        agents = {a: None for a in intent_mod.load()["agents"]}
        for ecrit, attendu in [("antic", "regulateurs"), ("Police judiciaire", "penal"), ("Tchatlink", "entreprises"),
                               ("opérateurs télécoms", "entreprises"), ("MINPROFF", "social"), ("apdp", "apdp")]:
            self.assertEqual(resolve_agent(ecrit, agents), attendu, ecrit)
        self.assertIsNone(resolve_agent("inconnu", agents))

    def test_articles_cles_fournis_a_l_agent(self):
        from bd.knowledge.kb import KnowledgeBase
        intent_mod.apply(intent_mod.load(), essai=True)
        a = agent_mod.CrisisAgent(agent_mod.ROLES["apdp"], KnowledgeBase())
        ex = a.retrieve("transfert des captures d'ecran d'une mineure vers un serveur a l'etranger")
        self.assertIn(("Loi_2024-017_Protection_donnees_personnelles_Cameroun.txt", "32"),
                      [(e.source_file, e.article) for e in ex])

    def test_contrainte_de_temps_controlee(self):
        intent = intent_mod.load()
        intent["contraintes"]["duree_max_par_etape_s"] = 0.001
        with mock.patch.object(llm, "chat", FakeLLM([])):
            Orchestrator(scenario([1]), self.run_dir, essai=True, intent=intent).run()
        dep = [e for e in self.journal() if e["evenement"] == "contrainte_depassee"]
        self.assertEqual(dep[0]["contrainte"], "duree_max_par_etape_s")

    def test_historique_abrege(self):
        a = agent_mod.CrisisAgent(agent_mod.ROLES["apdp"], kb=None)
        with mock.patch.multiple(agent_mod, OLD_STEP_CHARS=50, INBOX_KEEP=2, MESSAGE_CHARS=30):
            a.known_steps = ["ancienne " * 40, "etape en cours " * 20]
            a.inbox = [{"de": "penal", "contenu": f"message {i} " * 10} for i in range(5)]
            s = a.situation()
        self.assertIn("etape en cours " * 20, s)          # l'etape en cours reste entiere
        self.assertIn("[...]", s)
        self.assertIn("3 messages plus anciens", s)


if __name__ == "__main__":
    unittest.main()
