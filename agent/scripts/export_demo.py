"""Produit la page de demonstration (HTML autonome) d'une simulation.

Usage :
    python scripts/export_demo.py runs/<date>_<scenario>

Ecrit runs/<...>/demo.html : un fichier unique (donnees incluses, aucun
serveur ni connexion requis) qui presente la crise etape par etape, les
decisions des assistants avec leur statut de verification et les articles
cites, les echanges entre assistants et l'analyse du conseiller juridique.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from agent.agent1_institutions.roles import ROLES  # noqa: E402

TEMPLATE = r"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MinorShield Policy Lab — __TITRE__</title>
<style>
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#15181d; --muted:#5d6672; --line:#e3e6eb;
  --accent:#1f5fbf; --accent-soft:#e8f0fc;
  --ok:#1b7f4b; --ok-bg:#e6f4ec; --warn:#a35d00; --warn-bg:#fdf1e0;
  --doubt:#9a5b00; --doubt-bg:#fff4d6; --bad:#b42318; --bad-bg:#fdecea;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0f1216; --panel:#171b21; --ink:#e7eaee; --muted:#9aa4b1; --line:#2a3039;
  --accent:#7aa8f0; --accent-soft:#1b2738;
  --ok:#5cc58c; --ok-bg:#15291f; --warn:#f0b35c; --warn-bg:#2d2211;
  --doubt:#f2c35b; --doubt-bg:#2d2610; --bad:#f08a80; --bad-bg:#2e1715; color-scheme:dark;}}
:root[data-theme="dark"]{
  --bg:#0f1216; --panel:#171b21; --ink:#e7eaee; --muted:#9aa4b1; --line:#2a3039;
  --accent:#7aa8f0; --accent-soft:#1b2738;
  --ok:#5cc58c; --ok-bg:#15291f; --warn:#f0b35c; --warn-bg:#2d2211;
  --doubt:#f2c35b; --doubt-bg:#2d2610; --bad:#f08a80; --bad-bg:#2e1715; color-scheme:dark;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:28px 18px 60px}
h1{font-size:1.75rem;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:1.25rem;margin:0}
h3{font-size:1.02rem;margin:0}
.muted{color:var(--muted)}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;font-weight:700;color:var(--accent)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:22px 0 8px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.kpi b{display:block;font-size:1.5rem;font-variant-numeric:tabular-nums}
.kpi span{font-size:.82rem;color:var(--muted)}
.timeline{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;display:flex;gap:8px;flex-wrap:wrap;border-bottom:1px solid var(--line);margin-bottom:18px}
.timeline a{text-decoration:none;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:.85rem}
.timeline a:hover{border-color:var(--accent)}
section.step{margin:30px 0}
.stephead{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px}
.num{background:var(--accent);color:#fff;border-radius:8px;padding:2px 9px;font-weight:700}
blockquote{margin:10px 0 12px;padding:12px 14px;background:var(--accent-soft);border-left:3px solid var(--accent);border-radius:0 10px 10px 0}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{font-size:.78rem;border:1px solid var(--line);border-radius:999px;padding:2px 9px;background:var(--panel)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}
.card.advisor{border-color:var(--accent)}
.badge{display:inline-block;font-size:.74rem;font-weight:700;border-radius:6px;padding:2px 7px;white-space:nowrap}
.s-etayee{color:var(--ok);background:var(--ok-bg)}
.s-citation_douteuse{color:var(--doubt);background:var(--doubt-bg)}
.s-non_etayee{color:var(--warn);background:var(--warn-bg)}
.s-citation_invalide{color:var(--bad);background:var(--bad-bg)}
.act{border-top:1px solid var(--line);padding:9px 0}
.act:first-of-type{border-top:0}
.flags{font-size:.82rem;color:var(--bad);margin-top:3px}
details{margin-top:6px}
summary{cursor:pointer;color:var(--accent);font-size:.86rem}
.extract{white-space:pre-wrap;font-size:.84rem;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:9px 10px;margin-top:6px;max-height:260px;overflow:auto}
.msg{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px dashed var(--line)}
.msg .arrow{color:var(--accent);font-weight:700;white-space:nowrap}
ul.tight{margin:6px 0 0;padding-left:20px}
.table{width:100%;border-collapse:collapse;font-size:.88rem}
.table th,.table td{border-bottom:1px solid var(--line);padding:7px 6px;text-align:left;vertical-align:top}
.tablewrap{overflow-x:auto}
.legend{display:flex;gap:10px;flex-wrap:wrap;font-size:.84rem;margin-top:10px}
footer{margin-top:40px;font-size:.84rem;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
const DATA = __DATA__;
const NOMS = __NOMS__;
const STATUT = {etayee:"✅ étayée",citation_douteuse:"🔶 douteuse",non_etayee:"⚠️ non étayée",citation_invalide:"❌ invalide"};
const VERDICT = {fondee:"✅ fondée",a_verifier:"⚠️ à vérifier",non_fondee:"❌ non fondée"};
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const nom = id => NOMS[id] || id;
const list = v => Array.isArray(v) ? v.filter(x => String(x).trim()) : (v ? [v] : []);

function extractBox(ex){
  if(!ex) return "";
  return `<details><summary>${esc(ex.label)}</summary><div class="extract">${esc(ex.texte || "(texte non enregistré dans ce journal)")}</div></details>`;
}
function checks(entry){
  const byId = Object.fromEntries((entry.extraits||[]).map(x => [x.id, x]));
  return (entry.verification||[]).map(c => {
    const flags = [...(c.citations_invalides||[]).map(i => "identifiant inexistant : "+i),
                   ...(c.mentions_non_verifiees||[]), ...(c.textes_non_verifies||[]).map(t => "texte absent de la base : "+t),
                   ...(c.incoherences||[])];
    return `<div class="act"><span class="badge s-${c.statut}">${STATUT[c.statut]||c.statut}</span> ${c.institution ? "<b>"+esc(c.institution)+"</b> — " : ""}${esc(c.action)}
      ${flags.length ? `<div class="flags">${flags.map(esc).join(" · ")}</div>` : ""}
      ${(c.citations_valides||[]).map(i => extractBox(byId[i])).join("")}</div>`;
  }).join("");
}
function reaction(e){
  const r = e.reponse || {};
  if(e.erreur) return `<div class="card"><h3>${esc(nom(e.agent))}</h3><p class="flags">${esc(e.erreur)}</p></div>`;
  return `<div class="card"><h3>${esc(nom(e.agent))}</h3>
    <p>${esc(r.evaluation)}</p>
    ${list(r.inconnues).length ? `<p class="muted"><b>Ce qu'il ignore :</b> ${list(r.inconnues).map(esc).join(" ; ")}</p>` : ""}
    ${checks(e)}
    ${list(r.lacunes).length ? `<p><b>Lacunes signalées</b></p><ul class="tight">${list(r.lacunes).map(x=>`<li>${esc(x)}</li>`).join("")}</ul>` : ""}
    ${list(e.raisonnement).length ? `<details><summary>Raisonnement explicite</summary><ol class="tight">${list(e.raisonnement).map(x=>`<li>${esc(x)}</li>`).join("")}</ol></details>` : ""}
    <p class="muted" style="font-size:.78rem;margin:8px 0 0">${esc(e.modele)} · ${e.jetons} jetons · ${e.duree_s} s</p></div>`;
}
function advisor(e){
  const r = e.reponse || {};
  const byId = Object.fromEntries((e.extraits||[]).map(x => [x.id, x]));
  const ver = (r.verifications||[]).filter(v => v && typeof v === "object");
  const gaps = (r.lacunes||[]).filter(g => g && typeof g === "object");
  return `<div class="card advisor"><div class="eyebrow">Conseiller juridique et politique</div>
    <p>${esc(r.synthese)}</p>
    ${ver.length ? `<div class="tablewrap"><table class="table"><tr><th>Acteur</th><th>Action</th><th>Verdict</th><th>Commentaire</th></tr>
      ${ver.map(v=>`<tr><td>${esc(nom(v.acteur))}</td><td>${esc(v.action)}</td><td>${VERDICT[v.verdict]||esc(v.verdict)}</td><td>${esc(v.commentaire)}</td></tr>`).join("")}</table></div>` : ""}
    ${gaps.map(g => `<div class="act"><b>Lacune :</b> ${esc(g.lacune)}
      ${list(g.texte_camerounais).map(i => extractBox(byId[i])).join("")}
      ${(g.comparaison||[]).filter(c=>c&&typeof c==="object").map(c => `<div style="margin-top:6px"><span class="chip">${esc(c.juridiction)}</span> ${esc(c.pratique)} ${extractBox(byId[String(c.reference||"").trim()])}</div>`).join("")}
      ${g.recommandation ? `<p><b>Recommandation :</b> ${esc(g.recommandation)}</p>` : ""}</div>`).join("")}
    ${list(r.conflits).length ? `<p><b>Conflits</b></p><ul class="tight">${list(r.conflits).map(x=>`<li>${esc(x)}</li>`).join("")}</ul>` : ""}
    ${list(r.coordination).length ? `<p><b>Problèmes de coordination</b></p><ul class="tight">${list(r.coordination).map(x=>`<li>${esc(x)}</li>`).join("")}</ul>` : ""}
    <h3 style="margin-top:12px">Vérification des citations du conseiller</h3>${checks(e)}</div>`;
}

const ev = DATA.journal;
const debut = ev.find(e => e.evenement === "simulation_debut") || {};
const fin = ev.find(e => e.evenement === "simulation_fin");
const steps = ev.filter(e => e.evenement === "etape_revelee");
let html = `<div class="eyebrow">MinorShield Policy Lab · simulation de crise multi-agents</div>
  <h1>${esc(debut.titre)}</h1><p class="muted">${esc(DATA.scenario.resume || "")}<br>Mode : ${esc(debut.mode)} · ${esc(debut.horodatage)}</p>`;
if(fin){
  const r = fin.resume, v = r.verifications || {};
  const pct = r.taux_etayees == null ? "—" : Math.round(r.taux_etayees*100) + " %";
  html += `<div class="kpis">
    <div class="kpi"><b>${r.interventions}</b><span>interventions d'assistants</span></div>
    <div class="kpi"><b>${pct}</b><span>affirmations étayées par un extrait</span></div>
    <div class="kpi"><b>${v.citation_douteuse||0}</b><span>citations douteuses</span></div>
    <div class="kpi"><b>${v.citation_invalide||0}</b><span>citations invalides détectées</span></div>
    <div class="kpi"><b>${r.jetons_total.toLocaleString("fr-FR")}</b><span>jetons consommés</span></div></div>`;
}
html += `<nav class="timeline">${steps.map(s => `<a href="#etape-${s.etape}">${s.etape}. ${esc(s.titre)}</a>`).join("")}</nav>`;
for(const s of steps){
  const evs = ev.filter(e => e.etape === s.etape && e.evenement !== "etape_revelee");
  html += `<section class="step" id="etape-${s.etape}"><div class="stephead"><span class="num">Étape ${s.etape}</span><h2>${esc(s.titre)}</h2><span class="muted">${esc(s.moment)}</span></div>
    <blockquote>${esc(s.information)}</blockquote>
    <div class="chips"><span class="muted" style="font-size:.82rem">Informés :</span>${s.destinataires.map(d=>`<span class="chip">${esc(nom(d))}</span>`).join("")}</div>`;
  for(const e of evs){
    if(e.evenement === "intervention_reaction") html += reaction(e);
    else if(e.evenement === "demande_transmise") html += `<div class="msg"><span class="arrow">${esc(nom(e.de))} → ${esc(nom(e.a))}</span><span>${esc(e.objet)}</span></div>`;
    else if(e.evenement === "intervention_reponse"){
      const c = (e.verification||[])[0] || {};
      html += `<div class="msg"><span class="arrow">↳ ${esc(nom(e.agent))}</span><span><span class="badge s-${c.statut}">${STATUT[c.statut]||""}</span> ${esc((e.reponse||{}).reponse)}</span></div>`;
    }
    else if(e.evenement === "intervention_analyse") html += advisor(e);
    else if(e.evenement === "demandes_ecartees") html += `<p class="muted">${e.nombre} demande(s) non transmise(s) : ${esc(e.raison)}</p>`;
  }
  html += `</section>`;
}
html += `<footer><b>Comment lire les statuts.</b><div class="legend">
  <span class="badge s-etayee">✅ étayée</span> s'appuie sur un extrait réellement fourni à l'assistant
  <span class="badge s-citation_douteuse">🔶 douteuse</span> cite un extrait réel, mais mentionne un article ou un texte absent de cet extrait, ou annonce une autre juridiction
  <span class="badge s-non_etayee">⚠️ non étayée</span> aucune source citée
  <span class="badge s-citation_invalide">❌ invalide</span> cite un identifiant qui n'a jamais été fourni (invention)</div>
  <p>Chaque assistant ne connaît que les étapes qui lui ont été révélées. Les extraits sont tirés de la base de connaissances (lois camerounaises et références internationales) ; cliquer sur une source affiche le texte exact présenté à l'assistant.</p>
  <p>${esc(DATA.scenario.avertissement || "")}</p></footer>`;
document.getElementById("app").innerHTML = html;
</script>
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    run = Path(sys.argv[1])
    journal = [json.loads(l) for l in (run / "journal.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    scenario = {}
    resume = run / "resume.json"
    if resume.exists():
        scenario = json.loads(resume.read_text(encoding="utf-8")).get("scenario", {})
    titre = next((e.get("titre", "") for e in journal if e["evenement"] == "simulation_debut"), "")
    noms = {r.id: r.nom.split(" —")[0] for r in ROLES.values()}

    def js(obj) -> str:
        # Empeche une chaine « </script> » de fermer prematurement la balise.
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    page = (TEMPLATE.replace("__TITRE__", titre)
            .replace("__DATA__", js({"journal": journal, "scenario": scenario}))
            .replace("__NOMS__", js(noms)))
    out = run / "demo.html"
    out.write_text(page, encoding="utf-8")
    print(f"Page de demonstration : {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
