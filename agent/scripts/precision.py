"""Precision des affirmations « etayees » : relecture humaine d'un echantillon.

Le taux d'actions etayees (84,0 % dans la simulation de reference du 27/10) dit qu'une
affirmation cite un extrait reellement fourni, du bon texte et du bon pays.
Il ne dit pas que l'extrait FONDE l'affirmation telle qu'elle est formulee.
Seule une relecture le peut : ce script tire un echantillon, le fait relire
et calcule la precision avec un intervalle de confiance de Wilson a 95 %.

    python agent/scripts/precision.py echantillon [--journal J] [--taille 30] [--graine 2026]
    python agent/scripts/precision.py relire --relecteur NOM
    python agent/scripts/precision.py score

Etiquettes (une par affirmation) :
    fondee      l'extrait cite fonde l'affirmation telle qu'elle est ecrite
    partielle   l'extrait est pertinent mais ne couvre qu'une partie de
                l'affirmation, ou l'affirmation va plus loin que le texte
    non_fondee  l'extrait ne fonde pas l'affirmation
    incertain   les textes ne permettent pas de trancher

« incertain » est compte a part et exclu du denominateur (le nombre est
indique) : le ranger d'un cote ou de l'autre fausserait le resultat.
Deux precisions sont donnees : stricte (fondee seulement) et large
(fondee + partielle). Avec deux relecteurs, l'accord est mesure par le kappa
de Cohen et le score retenu est celui des cas ou ils sont d'accord.

L'echantillon est stratifie par type d'intervention (reaction des agents,
reponse a une demande, analyse du conseiller), en proportion de leur poids,
avec une graine fixe : un second relecteur relit exactement les memes cas.
Aucun appel au modele de langage.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "docs" / "precision" / "reference_20261027"
ECHANTILLON = DOSSIER / "echantillon.jsonl"
RESULTATS = DOSSIER / "resultats.md"
JOURNAL = ROOT / "docs" / "exemple_simulation" / "journal.jsonl"

ETIQUETTES = ("fondee", "partielle", "non_fondee", "incertain")
RACCOURCIS = {"f": "fondee", "p": "partielle", "n": "non_fondee", "i": "incertain"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Proportion k/n et son intervalle de Wilson (95 % par defaut)."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    marge = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, centre - marge), min(1.0, centre + marge)


def kappa(a: list[str], b: list[str]) -> float:
    """Kappa de Cohen entre deux suites d'etiquettes."""
    n = len(a)
    if n == 0:
        return 0.0
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[e] * cb[e] for e in set(a) | set(b)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def elements(kind: str, rep: dict) -> list[dict]:
    """Elements verifies d'une intervention, dans l'ordre de ``verify_turn``
    (une entree de « verification » par element)."""
    if kind == "reaction":
        return [a for a in rep.get("actions") or [] if isinstance(a, dict)]
    if kind == "reponse":
        return [rep]
    out = [v for v in rep.get("verifications") or [] if isinstance(v, dict)]
    for g in rep.get("lacunes") or []:
        if isinstance(g, dict):
            out.append(g)
            out += [c for c in g.get("comparaison") or [] if isinstance(c, dict)]
    return out


def population(journal: Path) -> list[dict]:
    """Toutes les affirmations au statut « etayee », avec leurs extraits cites
    et, pour les simulations recentes, la citation recopiee par l'agent."""
    out = []
    for l in journal.read_text(encoding="utf-8").splitlines():
        e = json.loads(l)
        if not e["evenement"].startswith("intervention_") or e.get("erreur"):
            continue
        extraits = {x["id"]: x for x in e.get("extraits", [])}
        kind = e["evenement"].replace("intervention_", "")
        items = elements(kind, e.get("reponse") or {})
        for i, v in enumerate(e.get("verification", [])):
            if v["statut"] != "etayee":
                continue
            item = items[i] if i < len(items) else {}
            justification = item.get("justification") or item.get("commentaire") or ""
            if kind == "reponse":
                justification = item.get("reponse", "")
            out.append({
                "type": kind,
                "etape": e["etape"], "agent": e["agent"], "institution": v.get("institution", ""),
                "affirmation": v["action"], "justification": justification,
                "citation": item.get("citation", ""),
                "extraits": [{"id": c, "source": extraits[c]["label"], "source_file": extraits[c]["source_file"],
                              "article": extraits[c].get("article", ""), "texte": extraits[c]["texte"]}
                             for c in v["citations_valides"] if c in extraits],
            })
    return out


def completer(tirage: list[dict]) -> int:
    """Ajoute a chaque extrait le texte complet de l'article (ou du bloc) dans
    la base : l'agent n'a vu que les 500 premiers caracteres, le relecteur
    juge sur le texte entier."""
    sys.path.insert(0, str(ROOT))
    from bd.knowledge.kb import KnowledgeBase  # noqa: E402

    main = KnowledgeBase().main
    cache: dict[str, list[tuple[dict, str]]] = {}
    n = 0
    for a in tirage:
        for x in a["extraits"]:
            fichier = x["source_file"]
            if fichier not in cache:
                r = main.get(where={"source_file": fichier}, include=["metadatas", "documents"])
                cache[fichier] = sorted(zip(r["metadatas"], r["documents"]), key=lambda md: int(md[0].get("chunk_index", 0)))
            morceaux = cache[fichier]
            if x.get("article"):
                docs = [d for m, d in morceaux if m.get("article") == x["article"]]
            else:
                docs = [d for m, d in morceaux if d.startswith(x["texte"][:200])]
            if docs:
                x["texte_complet"] = "\n".join(docs)
                n += 1
    return n


def cmd_echantillon(args) -> int:
    pop = population(args.journal)
    par_type = defaultdict(list)
    for a in pop:
        par_type[a["type"]].append(a)
    rng = random.Random(args.graine)
    # Repartition proportionnelle (plus forts restes), au moins un cas par type.
    parts = {t: args.taille * len(v) / len(pop) for t, v in par_type.items()}
    quotas = {t: max(1, int(p)) for t, p in parts.items()}
    for t in sorted(parts, key=lambda t: parts[t] - int(parts[t]), reverse=True):
        if sum(quotas.values()) >= args.taille:
            break
        quotas[t] += 1
    tirage = []
    for t in sorted(par_type):
        tirage += rng.sample(par_type[t], min(quotas[t], len(par_type[t])))
    rng.shuffle(tirage)
    complets = completer(tirage)
    DOSSIER.mkdir(parents=True, exist_ok=True)
    with ECHANTILLON.open("w", encoding="utf-8") as f:
        for i, a in enumerate(tirage, 1):
            f.write(json.dumps({"cas": i, **a}, ensure_ascii=False) + "\n")
    print(f"Population : {len(pop)} affirmations etayees ({', '.join(f'{t} {len(v)}' for t, v in sorted(par_type.items()))})")
    print(f"Echantillon : {len(tirage)} cas ({', '.join(f'{t} {q}' for t, q in sorted(quotas.items()))}), graine {args.graine}")
    print(f"Texte complet retrouve dans la base pour {complets}/{sum(len(a['extraits']) for a in tirage)} extraits")
    print(f"Ecrit : {ECHANTILLON.relative_to(ROOT).as_posix()}")
    return 0


def lire_echantillon() -> list[dict]:
    return [json.loads(l) for l in ECHANTILLON.read_text(encoding="utf-8").splitlines() if l.strip()]


def fichier_relecture(nom: str) -> Path:
    return DOSSIER / f"relecture_{nom}.jsonl"


def lire_relecture(path: Path) -> dict[int, dict]:
    if not path.exists():
        return {}
    return {r["cas"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r}


def cmd_relire(args) -> int:
    cas = lire_echantillon()
    path = fichier_relecture(args.relecteur)
    faits = lire_relecture(path)
    restants = [c for c in cas if c["cas"] not in faits]
    print(f"{len(faits)} cas deja relus, {len(restants)} restants. Reponses : "
          "f = fondee, p = partielle, n = non fondee, i = incertain, q = quitter (la suite est conservee).")
    for c in restants:
        print("\n" + "=" * 78)
        print(f"Cas {c['cas']}/{len(cas)} — etape {c['etape']}, {c['type']} de l'agent {c['agent']}"
              + (f" ({c['institution']})" if c["institution"] else ""))
        print(f"\nAFFIRMATION : {c['affirmation']}")
        if c["justification"]:
            print(f"JUSTIFICATION DONNEE : {c['justification']}")
        if c.get("citation"):
            print(f"CITATION RECOPIEE PAR L'AGENT : « {c['citation']} »")
        for x in c["extraits"]:
            complet = x.get("texte_complet", x["texte"]).strip()
            suite = "" if len(complet) <= len(x["texte"].strip()) + 5 else \
                f"   [l'agent n'a recu que les {len(x['texte'])} premiers caracteres]"
            print(f"\n--- {x['id']} : {x['source']}{suite}\n{complet}")
        while True:
            rep = input("\nL'extrait fonde-t-il l'affirmation ? [f/p/n/i/q] ").strip().lower()
            if rep == "q":
                return 0
            if rep in RACCOURCIS:
                break
        note = input("Commentaire (facultatif) : ").strip()
        faits[c["cas"]] = {"cas": c["cas"], "etiquette": RACCOURCIS[rep], "commentaire": note}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(faits[c["cas"]], ensure_ascii=False) + "\n")
    print(f"\nRelecture terminee : {path.relative_to(ROOT).as_posix()}")
    return 0


def bloc_score(titre: str, etiquettes: list[str], par_type: dict[str, list[str]]) -> list[str]:
    c = Counter(etiquettes)
    n = c["fondee"] + c["partielle"] + c["non_fondee"]
    ps, ls, hs = wilson(c["fondee"], n)
    pl, ll, hl = wilson(c["fondee"] + c["partielle"], n)
    out = [f"### {titre}", "",
           f"- Cas relus : {len(etiquettes)} — fondée {c['fondee']}, partielle {c['partielle']}, "
           f"non fondée {c['non_fondee']}, incertain {c['incertain']} (exclus du dénominateur)",
           f"- **Précision stricte (fondée) : {ps:.0%} — IC 95 % [{ls:.0%} ; {hs:.0%}]** (n = {n})",
           f"- Précision large (fondée + partielle) : {pl:.0%} — IC 95 % [{ll:.0%} ; {hl:.0%}]", "",
           "| Type | Cas | Fondée | Partielle | Non fondée | Incertain |", "|---|---|---|---|---|---|"]
    for t, et in sorted(par_type.items()):
        ct = Counter(et)
        out.append(f"| {t} | {len(et)} | {ct['fondee']} | {ct['partielle']} | {ct['non_fondee']} | {ct['incertain']} |")
    return out + [""]


def cmd_score(args) -> int:
    cas = {c["cas"]: c for c in lire_echantillon()}
    relectures = {p.stem.replace("relecture_", ""): lire_relecture(p) for p in sorted(DOSSIER.glob("relecture_*.jsonl"))}
    relectures = {k: v for k, v in relectures.items() if v}
    if not relectures:
        print("Aucune relecture : lancer d'abord « relire --relecteur NOM ».")
        return 1
    out = ["# Précision des affirmations « étayées » — relecture humaine", "",
           f"Échantillon : {len(cas)} affirmations tirées parmi celles que la vérification automatique "
           f"classe « étayées » (`{ECHANTILLON.relative_to(ROOT).as_posix()}`, tirage stratifié par type, graine fixe). "
           "Question posée au relecteur : l'extrait cité fonde-t-il l'affirmation telle qu'elle est écrite ? "
           "Intervalle de confiance de Wilson à 95 %. Méthode : `agent/scripts/precision.py`.", ""]
    for nom, rel in relectures.items():
        ids = [i for i in cas if i in rel]
        par_type = defaultdict(list)
        for i in ids:
            par_type[cas[i]["type"]].append(rel[i]["etiquette"])
        complet = "" if len(ids) == len(cas) else f" (incomplète : {len(ids)}/{len(cas)})"
        out += bloc_score(f"Relecteur « {nom} »{complet}", [rel[i]["etiquette"] for i in ids], par_type)

    noms = list(relectures)
    if len(noms) >= 2:
        a, b = relectures[noms[0]], relectures[noms[1]]
        communs = sorted(set(a) & set(b))
        la, lb = [a[i]["etiquette"] for i in communs], [b[i]["etiquette"] for i in communs]
        accord = sum(x == y for x, y in zip(la, lb))
        out += [f"### Accord entre « {noms[0]} » et « {noms[1]} »", "",
                f"- Cas relus par les deux : {len(communs)} ; même étiquette : {accord} "
                f"({accord / len(communs):.0%}) ; kappa de Cohen : {kappa(la, lb):.2f}", ""]
        desaccords = [i for i in communs if a[i]["etiquette"] != b[i]["etiquette"]]
        if desaccords:
            out += ["| Cas | Affirmation | " + noms[0] + " | " + noms[1] + " |", "|---|---|---|---|"]
            for i in desaccords:
                out.append(f"| {i} | {cas[i]['affirmation'][:90]} | {a[i]['etiquette']} | {b[i]['etiquette']} |")
            out.append("")
        par_type = defaultdict(list)
        for i in communs:
            if a[i]["etiquette"] == b[i]["etiquette"]:
                par_type[cas[i]["type"]].append(a[i]["etiquette"])
        out += bloc_score("Cas où les deux relecteurs sont d'accord",
                          [e for v in par_type.values() for e in v], par_type)

    premier = relectures[noms[0]]
    erreurs = [i for i in sorted(premier) if premier[i]["etiquette"] in ("non_fondee", "partielle")]
    if erreurs:
        out += [f"## Cas non fondés ou partiels (relecteur « {noms[0]} »)", "",
                "| Cas | Étape | Agent | Affirmation | Extrait(s) | Étiquette | Commentaire |", "|---|---|---|---|---|---|---|"]
        for i in erreurs:
            c, r = cas[i], premier[i]
            src = " ; ".join(x["source"] for x in c["extraits"])
            out.append(f"| {i} | {c['etape']} | {c['agent']} | {c['affirmation'][:110]} | {src[:110]} | "
                       f"{r['etiquette']} | {r.get('commentaire', '')} |")
    RESULTATS.write_text("\n".join(out) + "\n", encoding="utf-8")
    for l in out:
        if l.startswith(("### ", "- **", "- Préc", "- Cas relus par")):
            print(l.replace("**", ""))
    print(f"Detail : {RESULTATS.relative_to(ROOT).as_posix()}")
    return 0


def main() -> int:
    global DOSSIER, ECHANTILLON, RESULTATS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dossier", type=Path, default=DOSSIER,
                    help="dossier de l'echantillon et des relectures (un par simulation relue)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("echantillon")
    e.add_argument("--journal", type=Path, default=JOURNAL)
    e.add_argument("--taille", type=int, default=30)
    e.add_argument("--graine", type=int, default=2026)
    r = sub.add_parser("relire")
    r.add_argument("--relecteur", required=True)
    sub.add_parser("score")
    args = ap.parse_args()
    DOSSIER = args.dossier if args.dossier.is_absolute() else ROOT / args.dossier
    ECHANTILLON, RESULTATS = DOSSIER / "echantillon.jsonl", DOSSIER / "resultats.md"
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    return {"echantillon": cmd_echantillon, "relire": cmd_relire, "score": cmd_score}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
