"""Conseiller juridique et politique.

A la fin de chaque etape, il examine les interventions des acteurs et :
  1. juge la base legale de chaque action (fondee / a verifier / non fondee) ;
  2. identifie les lacunes, flous et conflits du droit camerounais ;
  3. les compare aux pratiques mondiales, en citant les extraits retrouves.

Il cherche dans deux corpus distincts : le droit camerounais et les
references etrangeres, afin que la comparaison s'appuie sur des textes reels.
"""

from __future__ import annotations

import json
import re
from typing import Any

from agent.commun import llm
from agent.agent1_institutions.agent import CrisisAgent, Extract, Turn, parse_json
from agent.agent1_institutions.roles import ROLES
from bd.knowledge.kb import KnowledgeBase

SCHEMA_ANALYSE = """{
  "verifications": [
    {"acteur": "identifiant", "action": "action examinee",
     "verdict": "fondee | a_verifier | non_fondee", "commentaire": "pourquoi"}
  ],
  "lacunes": [
    {"lacune": "ce que le droit camerounais ne prevoit pas, ou prevoit mal",
     "texte_camerounais": ["E1"],
     "comparaison": [{"juridiction": "UE, Royaume-Uni, Etats-Unis, Australie, Emirats arabes unis ou ONU",
                      "pratique": "ce qui y est prevu", "reference": "E6"}],
     "references": ["E1", "E6"],
     "recommandation": "proposition concrete pour combler la lacune"}
  ],
  "conflits": ["conflit entre objectifs ou entre acteurs"],
  "coordination": ["probleme de coordination observe entre institutions"],
  "synthese": "resume en 3 phrases"
}"""


class Advisor(CrisisAgent):
    def __init__(self, kb: KnowledgeBase, essai: bool = False):
        super().__init__(ROLES["conseiller"], kb, essai=essai)

    def retrieve_both(self, query: str) -> list[Extract]:
        local = self.retrieve(query, n=4, country="Cameroon")
        foreign = self._retrieve_foreign(query, n=4)
        return self.number(local + foreign)

    # Juridictions de comparaison presentes dans la base.
    FOREIGN = ("European Union", "United Kingdom", "United States", "Australia",
               "United Arab Emirates", "global")   # « global » : Observation generale n° 25 (ONU)

    def _retrieve_foreign(self, query: str, n: int) -> list[Extract]:
        """Meilleur extrait de CHAQUE juridiction etrangere, pour une comparaison equilibree.

        Une recherche globale ramenait surtout le texte australien (blocs longs
        et generalistes) au detriment du DSA, du RGPD ou de la loi britannique.
        """
        from agent.agent1_institutions.agent import EXTRACT_CHARS
        from bd.knowledge.ingest import embed_texts
        vec = embed_texts([query])[0]
        found: list[Extract] = []
        for country in self.FOREIGN:
            where = {"$and": [{"document_category": "Child_Online_Protection"}, {"country": country}]}
            try:
                res = self.kb.search(vec, n_results=1, where=where)
            except Exception:  # noqa: BLE001 - juridiction absente de la base
                continue
            for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
                found.append(Extract("", meta.get("source_file", ""), meta.get("article", ""),
                                     meta.get("page", ""), meta.get("country", ""), 1 - dist,
                                     doc[:EXTRACT_CHARS]))
        found.sort(key=lambda e: e.similarity, reverse=True)
        return found[:n]

    @staticmethod
    def _key(e: Extract) -> tuple[str, str, str]:
        return (e.source_file, e.article, e.text[:80])

    def gather(self, turns: list[Turn], query: str, max_cited: int = 8,
               n_foreign: int = 4, n_local: int = 3,
               checks: tuple[str, ...] = ()) -> tuple[list[Extract], dict, int]:
        """Construit UNE liste d'extraits numerotee pour toute l'etape.

        Chaque agent numerote ses extraits a partir de E1 : sans renumerotation,
        « E1 » designerait des articles differents selon l'agent, et le
        conseiller confondrait les sources. On reunit donc d'abord les extraits
        reellement cites par les acteurs (pour juger chaque action sur le texte
        meme qu'elle invoque), puis ses propres recherches (droit camerounais et
        references etrangeres), dans une seule liste.
        Ordre de la liste (qui sert aussi d'ordre de priorite face au budget de
        jetons) : extraits cites par les acteurs (les plus invoques d'abord,
        au plus ``max_cited``), puis references etrangeres (jamais sacrifiees :
        la comparaison internationale est au coeur de l'evaluation), puis
        recherches complementaires en droit camerounais (sacrifiees en premier).
        Retourne les extraits, la correspondance (agent, ancien id) -> nouvel id,
        et le nombre d'extraits a ne jamais retirer.
        """
        from collections import Counter
        counts: Counter = Counter()
        index: dict[tuple, Extract] = {}
        first_seen: dict[tuple, Extract] = {}
        owners: list[tuple[tuple[str, str], tuple]] = []
        for t in turns:
            by_id = {e.id: e for e in t.extracts}
            o = t.output or {}
            cited = []
            for a in (o.get("actions") or []):
                if isinstance(a, dict):
                    cited += a.get("base_legale") or []
            if t.kind == "reponse":
                bl = o.get("base_legale") or []
                cited += bl if isinstance(bl, list) else [bl]
            for cid in cited:
                e = by_id.get(str(cid).strip())
                if not e:
                    continue
                k = self._key(e)
                counts[k] += 1
                first_seen.setdefault(k, e)
                owners.append(((t.agent, e.id), k))

        # 1. Extraits cites par les acteurs : les plus invoques d'abord.
        cited_pool: list[Extract] = []
        for k, _ in counts.most_common(max_cited):
            e = first_seen[k]
            index[k] = Extract("", e.source_file, e.article, e.page, e.country, e.similarity, e.text)
            cited_pool.append(index[k])
        # 2. Textes de controle (definitions, delais) : jamais sacrifies, car
        # ils servent a verifier le champ des textes et le realisme des delais.
        control: list[Extract] = []
        for q in checks:
            for e in self.retrieve(q, n=1, country="Cameroon"):
                if self._key(e) not in index:
                    index[self._key(e)] = e
                    control.append(e)
        # 3. References etrangeres, puis 4. droit camerounais complementaire.
        foreign = [e for e in self._retrieve_foreign(query, n=n_foreign) if self._key(e) not in index]
        for e in foreign:
            index[self._key(e)] = e
        local = [e for e in self.retrieve(query, n=n_local, country="Cameroon") if self._key(e) not in index]
        pool = self.number(cited_pool + control + foreign + local)
        # Correspondance ; un extrait cite mais ecarte (au-dela de max_cited)
        # apparaitra comme « non fourni » dans le resume.
        remap = {owner: index[k].id for owner, k in owners if k in index}
        return pool, remap, len(cited_pool) + len(control) + len(foreign)

    @staticmethod
    def digest(turns: list[Turn], remap: dict, eval_chars: int = 400, max_chars: int = 0) -> str:
        """Resume compact des interventions, avec les identifiants de la liste commune.

        ``eval_chars`` tronque chaque evaluation ; ``max_chars`` plafonne le total
        (pour tenir dans le budget de jetons d'une requete).
        """
        def ids(agent: str, values: Any) -> list[str]:
            vals = values if isinstance(values, list) else [values]
            return [remap.get((agent, str(v).strip()), f"{v} (non fourni)") for v in vals if v]

        lines = []
        for t in turns:
            o = t.output or {}
            if t.kind == "reaction":
                lines.append(f"## {t.agent}\nEvaluation : {str(o.get('evaluation', ''))[:eval_chars]}")
                for a in (o.get("actions") or [])[:4]:
                    if isinstance(a, dict):
                        qui = f" ({a.get('institution')})" if a.get("institution") else ""
                        lines.append(f"- Action{qui} : {a.get('action', '')} | extraits invoques : "
                                     f"{ids(t.agent, a.get('base_legale') or []) or 'aucun'}")
                for g in (o.get("lacunes") or [])[:3]:
                    lines.append(f"- Lacune signalee : {str(g)[:eval_chars]}")
            elif t.kind == "reponse":
                lines.append(f"## {t.agent} (reponse a une demande)\n{str(o.get('reponse', ''))[:eval_chars]} "
                             f"| extraits invoques : {ids(t.agent, o.get('base_legale') or []) or 'aucun'}")
        text = "\n".join(lines)
        if max_chars and len(text) > max_chars:
            text = text[:max_chars] + "\n[... resume tronque pour respecter la taille maximale de la requete]"
        return text

    def build_prompt(self, step: dict[str, Any], extracts: list[Extract], digest: str) -> str:
        return (f"ETAPE {step['numero']} — {step['titre']}\n{step['information']}\n\n"
                f"INTERVENTIONS DES ACTEURS :\n{digest}\n\n"
                f"EXTRAITS (droit camerounais puis references etrangeres) :\n{self.format_extracts(extracts)}\n\n"
                "Analyse cette etape. Juge chaque action en lisant l'extrait qu'elle invoque, identifie les "
                "lacunes du droit camerounais et compare-les aux pratiques etrangeres.\n"
                f"REGLES DE CITATION : les SEULS identifiants valides sont {', '.join(e.id for e in extracts) or 'aucun'}. "
                "Dans chaque commentaire, cite l'identifiant de l'extrait sur lequel tu t'appuies. "
                "Ne nomme AUCUN texte (directive, reglement, loi) qui ne figure pas dans ces extraits. "
                "Avant d'ecrire qu'un texte camerounais « ne prevoit pas » quelque chose, verifie les extraits "
                "camerounais : s'il le prevoit, ce n'est pas une lacune (au plus une imprecision, a qualifier ainsi). "
                "Pour chaque personne concernee (victime, auteur), verifie avec les definitions fournies qu'elle entre "
                "bien dans le champ du texte invoque (age, qualite) ; signale tout ecart entre les seuils d'age des "
                "textes. Quand un texte fixe un delai, juge s'il est adapte au rythme de la crise (contenus viraux, "
                "donnees exposees). "
                "Une comparaison avec un pays doit citer un extrait de CE pays ; s'il n'y en a pas, ecris "
                "« aucun extrait disponible pour cette juridiction » au lieu d'inventer.\n"
                f"Reponds avec exactement cette structure JSON :\n{SCHEMA_ANALYSE}")

    def fit_budget(self, step: dict[str, Any], turns: list[Turn], extracts: list[Extract],
                   remap: dict, n_keep: int, max_tokens: int) -> tuple[list[Extract], str, str]:
        """Reduit la requete jusqu'a ce qu'elle tienne dans le budget de jetons.

        Ordre des sacrifices : 1) les extraits camerounais complementaires
        (fin de liste) ; 2) la longueur des resumes. Les ``n_keep`` premiers
        extraits (cites par les acteurs + references etrangeres) sont conserves.
        """
        system = self.system_prompt()
        eval_chars, max_chars = 400, 0
        for _ in range(25):
            digest = self.digest(turns, remap, eval_chars=eval_chars, max_chars=max_chars)
            user = self.build_prompt(step, extracts, digest)
            if llm.estimate_tokens(system + user) + max_tokens <= llm.REQUEST_TOKEN_BUDGET:
                break
            if len(extracts) > n_keep:
                extracts = extracts[:-1]
            elif eval_chars > 150:
                eval_chars -= 100
            else:
                max_chars = int((max_chars or len(digest)) * 0.8)
        return extracts, digest, user

    def analyse(self, step: dict[str, Any], turns: list[Turn]) -> Turn:
        query = f"{step['titre']}. {step['information']}\n" + " ".join(step.get("questions_attendues", []))
        checks = []
        if re.search(r"\d+\s*ans", step["information"]):
            checks.append("definition de l'enfant : age en dessous duquel une personne est un enfant ou un mineur")
        if re.search(r"(?i)d[ée]lai|mise en demeure|notifi|retrait|suppression|bloqu", step["information"]):
            checks.append("delai impose pour se conformer, retirer un contenu ou notifier")
        extracts, remap, n_keep = self.gather(turns, query, checks=tuple(checks))
        max_tokens = 3000
        extracts, digest, user = self.fit_budget(step, turns, extracts, remap, n_keep, max_tokens)
        visible = [f"Etape {step['numero']} : {step['information']}"]
        try:
            res = llm.chat(self.system_prompt(), user, fast=self.essai, max_tokens=max_tokens)
        except Exception as e:  # noqa: BLE001
            return Turn("conseiller", "analyse", step["numero"], visible, [], query, extracts,
                        {}, "", llm.model_name(), 0, 0.0, parse_error=f"appel LLM : {e}")
        output, err = parse_json(res.text)
        if res.finish_reason == "length":
            err = "reponse tronquee (limite de longueur atteinte)" + (f" ; {err}" if err else "")
        return Turn("conseiller", "analyse", step["numero"], visible, [], query, extracts,
                    output, res.text, res.model, res.total_tokens, res.seconds, parse_error=err)
