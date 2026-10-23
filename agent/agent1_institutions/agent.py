"""Agent institutionnel de la simulation de crise.

Chaque agent :
  1. ne connait que les etapes qui lui ont ete revelees et les messages qui
     lui sont adresses (asymetrie d'information exigee par l'enonce) ;
  2. cherche dans la base de connaissances les articles pertinents, en
     privilegiant ses textes prioritaires ;
  3. presente ces extraits au modele sous des identifiants [E1], [E2]... ;
  4. exige une reponse JSON structuree dont chaque action juridique cite ces
     identifiants. Les citations sont ensuite verifiees par le journal
     d'audit (server/crisis/audit.py).
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from agent.commun import llm
from agent.agent1_institutions.roles import ROLES, Role
from bd.knowledge.ingest import embed_texts
from bd.knowledge.kb import KnowledgeBase

logger = logging.getLogger(__name__)

LEGAL_CATEGORY = "Child_Online_Protection"
# Budget : une simulation complete doit tenir dans le quota journalier gratuit
# (200 000 jetons). Une premiere simulation complete en consommait 174 000 ;
# ces reglages en economisent environ 20 %.
# Valeurs par defaut ; le ML Intent (agent/intent.json) les remplace au demarrage.
EXTRACT_CHARS = 600          # longueur maximale d'un extrait presente au modele
DEFAULT_EXTRACTS = 4
ANSWER_EXTRACTS = 3          # extraits pour repondre a une demande
OLD_STEP_CHARS = 0           # 0 = etapes anciennes en entier ; sinon tronquees a N caracteres
INBOX_KEEP = 0               # 0 = tous les messages ; sinon les N derniers
MESSAGE_CHARS = 0            # 0 = messages en entier ; sinon tronques a N caracteres
PRIO_MARGIN = 0.15           # ecart de similarite toleree pour un extrait prioritaire
MAX_PER_FILE = 2             # extraits au plus par texte, pour garder des sources variees

_LEGAL_FILES: dict[str, str] = {}


def _legal_files(kb: KnowledgeBase) -> dict[str, str]:
    """Fichiers du corpus juridique et leur pays (lus une fois, puis gardes)."""
    if not _LEGAL_FILES:
        res = kb.main.get(where={"document_category": LEGAL_CATEGORY}, include=["metadatas"])
        for m in res["metadatas"]:
            _LEGAL_FILES.setdefault(m.get("source_file", ""), m.get("country", ""))
    return _LEGAL_FILES


@dataclass
class Extract:
    """Un extrait de la base presente a l'agent, citable par son identifiant."""
    id: str
    source_file: str
    article: str
    page: str
    country: str
    similarity: float
    text: str

    def label(self) -> str:
        first = self.text.splitlines()[0] if self.text else self.source_file
        title = first.strip("[]").split("] —")[0] if first.startswith("[") else self.source_file
        art = f", article {self.article}" if self.article and self.article.isdigit() else ""
        page = f", p. {self.page}" if self.page else ""
        return f"{title}{art}{page}"

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "source_file": self.source_file, "article": self.article,
                "page": self.page, "country": self.country,
                "similarity": round(self.similarity, 3), "label": self.label(),
                # Le texte exact presente a l'agent : le lecteur du journal peut
                # ainsi verifier lui-meme ce que dit l'article cite.
                "texte": self.text}


@dataclass
class Turn:
    """Trace complete d'une intervention d'agent (pour le journal d'audit)."""
    agent: str
    kind: str                         # "reaction", "reponse" ou "analyse"
    step: int
    visible_info: list[str]
    messages_in: list[dict[str, str]]
    query: str
    extracts: list[Extract]
    output: dict[str, Any]
    raw: str
    model: str
    tokens: int
    seconds: float
    parse_error: Optional[str] = None


# Les lois camerounaises designent les institutions par leur fonction, rarement
# par leur nom. Sans ce lexique, les agents confondaient les acteurs (ex. :
# « l'organe charge de la regulation des TIC (MINESEC) » au lieu de l'ANTIC).
LEXIQUE = """AGENTS (identifiant a mettre dans "destinataire") ET TERMES DES LOIS QUI LES DESIGNENT :
- regulateurs : ANTIC = « organe charge de la regulation des TIC » ; ART = « organe charge de la regulation des telecommunications » ; MINPOSTEL = « Ministere en charge des telecommunications »
- apdp : APDP = « Autorite de protection des donnees a caractere personnel »
- penal : Police judiciaire = « officiers de police judiciaire » ; Parquet = « Procureur de la Republique »
- social : MINAS = « Ministere en charge des affaires sociales » ; MINPROFF = « Ministere en charge de la femme et de la famille » ; MINESEC (« Ministeres en charge de l'education »)
- entreprises : Operateurs = « fournisseurs d'acces a Internet », « operateurs des reseaux de communications electroniques » ; Tchatlink = « promoteur de reseau social » ; ScolaPlus = « responsable du traitement des donnees »
- minorshield : MinorShield
"destinataire" est TOUJOURS l'un de ces identifiants, jamais le nom d'une institution."""

SCHEMA_REACTION = """{
  "evaluation": "ta lecture de la situation, a partir de ce que tu sais",
  "inconnues": ["ce que tu ignores et qui compte pour decider"],
  "actions": [
    {"institution": "l'institution qui agit, choisie dans ta liste",
     "action": "ce qu'elle fait, dans les limites de sa mission",
     "base_legale": ["E1"],
     "justification": "pourquoi cet extrait fonde l'action"}
  ],
  "demandes": [{"destinataire": "identifiant d'un autre acteur", "objet": "ce que tu lui demandes",
                "raison": "pourquoi ton action depend de lui"}],
  "lacunes": ["ce que la loi ne te permet pas de faire, ou ne prevoit pas"],
  "confiance": 0.0,
  "raisonnement": ["etape 1 de ton raisonnement", "etape 2", "..."]
}"""

SCHEMA_REPONSE = """{
  "institution": "l'institution qui repond, choisie dans ta liste",
  "reponse": "ta reponse a la demande",
  "base_legale": ["E1"],
  "peut_agir": true,
  "raisonnement": ["etape 1", "etape 2"]
}"""


class CrisisAgent:
    def __init__(self, role: Role, kb: KnowledgeBase, essai: bool = False):
        self.role = role
        self.kb = kb
        # Mode essai : tout passe par le petit modele (quota separe), pour
        # garder le quota du grand modele aux simulations de reference.
        self.essai = essai
        self.known_steps: list[str] = []
        self.inbox: list[dict[str, str]] = []

    # ------------------------------------------------------------------ memoire
    def receive_step(self, step: dict[str, Any]) -> None:
        self.known_steps.append(f"Etape {step['numero']} ({step['moment']}) — {step['titre']} : {step['information']}")

    def receive_message(self, sender: str, content: str) -> None:
        self.inbox.append({"de": sender, "contenu": content})

    # ---------------------------------------------------------------- recherche
    def retrieve(self, query: str, n: Optional[int] = None,
                 country: Optional[str] = None) -> list[Extract]:
        """Cherche les extraits juridiques les plus pertinents.

        Deux recherches : une dans tout le corpus juridique, une limitee aux
        textes prioritaires de l'agent. Les gros textes etrangers (RGPD, DSA,
        Online Safety Act) dominent sinon la premiere recherche et evincent le
        texte national qui fonde le mandat de l'agent. La moitie des extraits
        est donc reservee aux textes prioritaires, s'ils sont assez pertinents
        (au plus PRIO_MARGIN de similarite sous le meilleur resultat general) ;
        le reste suit la pertinence, avec un leger bonus aux textes prioritaires.
        """
        n = n or DEFAULT_EXTRACTS
        where: dict[str, Any] = {"document_category": LEGAL_CATEGORY}
        if country:
            where = {"$and": [where, {"country": country}]}
        emb = embed_texts([query])[0]
        res = self.kb.search(emb, n_results=max(n * 4, 16), where=where)
        general = list(zip(res["documents"][0], res["metadatas"][0], res["distances"][0]))

        prio_files = self._priority_files(country)
        prio_hits: list[tuple[str, dict[str, Any], float]] = []
        if prio_files:
            res_p = self.kb.search(emb, n_results=n * 2,
                                   where={"$and": [where, {"source_file": {"$in": prio_files}}]})
            prio_hits = list(zip(res_p["documents"][0], res_p["metadatas"][0], res_p["distances"][0]))

        out: list[Extract] = []
        seen: set[tuple[str, str]] = set()
        per_file: dict[str, int] = {}

        def add(doc: str, meta: dict[str, Any], sim: float) -> None:
            key = (meta.get("source_file", ""), meta.get("article", "") or meta.get("chunk_index", ""))
            # Au plus MAX_PER_FILE extraits d'un meme texte : un long document
            # (Observation generale, RGPD) ne doit pas occuper toutes les places.
            if key in seen or len(out) >= n or per_file.get(key[0], 0) >= MAX_PER_FILE:
                return
            seen.add(key)
            per_file[key[0]] = per_file.get(key[0], 0) + 1
            out.append(Extract(
                id="", source_file=meta.get("source_file", ""), article=meta.get("article", ""),
                page=meta.get("page", ""), country=meta.get("country", ""),
                similarity=sim, text=doc[:EXTRACT_CHARS],
            ))

        best = max((1 - d for _, _, d in general), default=0.0)
        # Le premier texte prioritaire fonde le mandat de l'agent : il a
        # toujours au moins un extrait, s'il est assez pertinent.
        main_files = [f for f in prio_files if f.startswith(self.role.sources_prioritaires[0])]
        if main_files:
            res_m = self.kb.search(emb, n_results=1,
                                   where={"$and": [where, {"source_file": {"$in": main_files}}]})
            for doc, meta, dist in zip(res_m["documents"][0], res_m["metadatas"][0], res_m["distances"][0]):
                if 1 - dist >= best - PRIO_MARGIN:
                    add(doc, meta, 1 - dist)
        for doc, meta, dist in prio_hits[: (n + 1) // 2]:
            if 1 - dist >= best - PRIO_MARGIN:
                add(doc, meta, 1 - dist)

        scored = []
        for doc, meta, dist in general + prio_hits:
            sim = 1 - dist
            bonus = 0.05 if meta.get("source_file", "") in prio_files else 0.0
            scored.append((sim + bonus, sim, doc, meta))
        scored.sort(key=lambda x: x[0], reverse=True)
        for _, sim, doc, meta in scored:
            add(doc, meta, sim)
        return out

    def _priority_files(self, country: Optional[str]) -> list[str]:
        """Fichiers de la base dont le nom commence par un prefixe prioritaire."""
        prio = self.role.sources_prioritaires
        return [f for f, c in _legal_files(self.kb).items()
                if any(f.startswith(p) for p in prio) and (not country or c == country)]

    @staticmethod
    def number(extracts: list[Extract], start: int = 1) -> list[Extract]:
        for i, e in enumerate(extracts, start=start):
            e.id = f"E{i}"
        return extracts

    @staticmethod
    def format_extracts(extracts: list[Extract]) -> str:
        if not extracts:
            return "(aucun extrait pertinent trouve dans la base)"
        return "\n\n".join(f"[{e.id}] {e.label()} — pays : {e.country}\n{e.text}" for e in extracts)

    # ------------------------------------------------------------------ prompts
    def system_prompt(self) -> str:
        r = self.role
        institutions = ", ".join(r.institutions) or r.nom
        return f"""Tu joues le role de : {r.nom}, dans une simulation de crise au Cameroun.

TA MISSION : {r.mission}

INSTITUTIONS QUE TU REPRESENTES : {institutions}

FONDEMENTS DE TES POUVOIRS :
{chr(10).join('- ' + f for f in r.fondements) or '- aucun'}

LIMITES DE TON MANDAT :
{chr(10).join('- ' + l for l in r.limites) or '- aucune precisee'}

REGLES IMPERATIVES :
1. Tu ne connais QUE les informations qui te sont transmises. N'invente aucun fait et ne suppose rien sur ce que savent les autres acteurs.
2. Tu n'agis que dans les limites de ta mission. Chaque action indique dans "institution" UNE seule institution, recopiee exactement de cette liste : {institutions}.
3. Coordination : pour chaque mesure, information ou decision qui releve d'un AUTRE agent de la liste ci-dessous (un pouvoir que tu n'as pas, une donnee qu'il detient, une decision qu'il doit prendre), adresse-lui une demande dans "demandes", avec la raison. Dans une crise, presque toute action depend d'un autre agent : si tu n'adresses aucune demande, explique pourquoi dans "raisonnement".
4. Toute action fondee sur le droit cite au moins un extrait fourni. "base_legale" contient UNIQUEMENT des identifiants d'extraits (exemple : ["E2", "E4"]), JAMAIS un numero d'article ecrit de memoire. Ne mentionne aucun article absent des extraits. Si aucun extrait ne fonde une action, laisse "base_legale" vide et explique-le dans "lacunes".
5. Dis clairement ce que tu ignores.
6. Sois concis : au plus 3 actions et 3 demandes, une evaluation de 2 phrases, un raisonnement de 4 etapes courtes au plus.
7. Reponds uniquement en francais, uniquement en JSON valide.

{LEXIQUE}"""

    def situation(self) -> str:
        """Ce que l'agent sait. Pour limiter les jetons (ML Intent, « historique »),
        les etapes anciennes et les messages peuvent etre abreges : l'etape en
        cours reste toujours en entier."""
        def cut(s: str, limit: int) -> str:
            return s if not limit or len(s) <= limit else s[:limit].rstrip() + " [...]"
        steps = [cut(s, OLD_STEP_CHARS) for s in self.known_steps[:-1]] + self.known_steps[-1:]
        inbox = self.inbox[-INBOX_KEEP:] if INBOX_KEEP else self.inbox
        known = "\n".join(f"- {s}" for s in steps) or "- (aucune)"
        msgs = "\n".join(f"- De {m['de']} : {cut(m['contenu'], MESSAGE_CHARS)}" for m in inbox) or "- (aucun)"
        older = len(self.inbox) - len(inbox)
        if older > 0:
            msgs = f"- ({older} messages plus anciens non repetes)\n" + msgs
        return f"CE QUE TU SAIS :\n{known}\n\nMESSAGES RECUS :\n{msgs}"

    # ------------------------------------------------------------------- actes
    def react(self, step_no: int, n_extracts: Optional[int] = None) -> Turn:
        """Reaction a la derniere etape revelee (``n_extracts`` : plus d'extraits
        lors d'une nouvelle tentative decidee par l'orchestrateur)."""
        query = f"{self.role.mission}\n{self.known_steps[-1] if self.known_steps else ''}"
        extracts = self.number(self.retrieve(query, n=n_extracts))
        user = (f"{self.situation()}\n\nEXTRAITS DE LA BASE DE CONNAISSANCES :\n{self.format_extracts(extracts)}"
                f"\n\nQue fais-tu maintenant ? Reponds avec exactement cette structure JSON :\n{SCHEMA_REACTION}")
        return self._call("reaction", step_no, query, extracts, user, fast=self.essai)

    def answer(self, step_no: int, sender: str, request: str) -> Turn:
        """Reponse courte a une demande d'un autre acteur.

        Meme modele que les reactions : en mode reference, toute la simulation
        doit tourner sur le grand modele (et ne pas dependre du quota du petit).
        """
        query = f"{self.role.mission}\n{request}"
        extracts = self.number(self.retrieve(query, n=ANSWER_EXTRACTS))
        user = (f"{self.situation()}\n\nDEMANDE DE {sender} : {request}\n\n"
                f"EXTRAITS DE LA BASE DE CONNAISSANCES :\n{self.format_extracts(extracts)}"
                f"\n\nReponds a cette demande avec exactement cette structure JSON :\n{SCHEMA_REPONSE}")
        return self._call("reponse", step_no, query, extracts, user, fast=self.essai)

    # ----------------------------------------------------------------- interne
    def _call(self, kind: str, step_no: int, query: str, extracts: list[Extract],
              user: str, fast: bool) -> Turn:
        visible = list(self.known_steps)
        inbox = list(self.inbox)
        try:
            res = llm.chat(self.system_prompt(), user, fast=fast, max_tokens=2500)
        except Exception as e:  # noqa: BLE001
            logger.error("Agent %s : appel LLM impossible (%s)", self.role.id, e)
            return Turn(self.role.id, kind, step_no, visible, inbox, query, extracts,
                        {}, "", llm.model_name(fast), 0, 0.0, parse_error=f"appel LLM : {e}")
        output, err = parse_json(res.text)
        if res.finish_reason == "length":
            err = "reponse tronquee (limite de longueur atteinte)" + (f" ; {err}" if err else "")
        return Turn(self.role.id, kind, step_no, visible, inbox, query, extracts,
                    output, res.text, res.model, res.total_tokens, res.seconds, parse_error=err)


def parse_json(raw: str) -> tuple[dict[str, Any], Optional[str]]:
    """Lit la reponse JSON du modele, en tolerant un enrobage ```json ... ```."""
    text = raw.strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}, "aucun objet JSON dans la reponse"
    try:
        data = json.loads(m.group(0))
        return (data, None) if isinstance(data, dict) else ({}, "JSON non objet")
    except json.JSONDecodeError as e:
        return {}, f"JSON invalide : {e}"
