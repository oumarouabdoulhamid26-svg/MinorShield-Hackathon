# MinorShield Policy Lab

**Agents IA pour la protection des mineurs en ligne : une simulation de crise
multi-agents fondée sur le droit camerounais et comparée aux pratiques
mondiales, adossée à une application réelle de protection des enfants.**

Projet soumis au hackathon *ITU AI for Good Lab — United Arab Emirates*.

---

## Organisation du dépôt

```
MinorShield-Hackathon/
├── agent/                       Les agents IA (Policy Lab)
│   ├── agent1_institutions/     6 agents acteurs : régulateurs (ANTIC, ART, MINPOSTEL), APDP,
│   │                            chaîne pénale, protection sociale et éducative, entreprises, MinorShield
│   ├── agent2_conseiller/       conseiller juridique : verdicts, lacunes, comparaisons mondiales
│   ├── agent3_coordination/     animateur neutre, journal d'audit, vérification des citations, rapport
│   ├── commun/                  configuration, lecture du ML Intent, accès unique au modèle de langage
│   ├── intent.json              ML Intent (Y.3172) : sources, agents, modèles, contraintes, seuil de qualité
│   ├── scenarios/               le scénario « Opération Miroir » (6 étapes)
│   ├── scripts/                 page de démonstration, re-vérification d'une simulation
│   └── tests/                   tests de l'orchestrateur (faux modèle : aucun jeton consommé)
├── application/                 L'application MinorShield (la « solution d'IA innovante »)
│   ├── frontend/                applications Android : parent (app/) et enfant (app-enfant/)
│   └── backend/                 API FastAPI : détection d'images et de textes, comptes, alertes
├── bd/                          La base de connaissances
│   ├── InputDocs/               textes de loi (Cameroun + UE, R.-U., É.-U., Australie) et documents UIT
│   ├── knowledge/               ingestion et recherche (code de référence UIT, amélioré)
│   ├── scripts/                 préparation des textes (découpage, OCR, ajout incrémental)
│   └── SOURCES.md               provenance de chaque texte
├── docs/                        conception, rapport technique, simulation de référence, vidéo
└── run_simulation.py            lancement d'une simulation
```

## En une phrase

Six agents IA, représentant chacun un groupe d'institutions ou d'acteurs réels
qui partagent le même objectif, gèrent ensemble une crise de chantage sexuel
visant des élèves. Chacun ne sait que ce qu'on lui a révélé, agit dans les
limites de son mandat et **justifie chaque décision par l'article de loi qu'il
a réellement retrouvé** ; un conseiller juridique relève les lacunes du droit
et les compare aux pratiques de l'Union européenne, du Royaume-Uni, des
États-Unis, de l'Australie, des Émirats arabes unis et de l'ONU. Un animateur
programmé, sans modèle de langage, révèle les étapes et transmet les demandes.

| Agent | Institutions représentées |
|---|---|
| Régulateurs du numérique | ANTIC (dont le CIRT national), ART, MINPOSTEL |
| Protection des données | APDP |
| Chaîne pénale | Police judiciaire, Parquet |
| Protection sociale et éducative | MINAS, MINPROFF, MINESEC |
| Entreprises du numérique | Opérateurs télécoms, Tchatlink et ScolaPlus (entreprises fictives) |
| Agent innovant | MinorShield |

Les institutions sont regroupées par objectif, mais les acteurs dont les
intérêts s'opposent (régulateur et entreprise régulée, protection de l'enfant
et protection de ses données) restent des agents distincts : leurs désaccords
font apparaître les lacunes du droit.

## Correspondance avec les exigences du hackathon

| Exigence | Où la trouver |
|---|---|
| Base de connaissances de lois et politiques | `bd/` — textes découpés **article par article** et citables |
| Agent « solution d'IA innovante » | `agent/agent1_institutions/` (rôle MinorShield) et `application/` |
| Agent « conseiller juridique et politique » | `agent/agent2_conseiller/` |
| Agents « participants institutionnels » | `agent/agent1_institutions/` |
| Coordination multi-agents | `agent/agent3_coordination/orchestrator.py` |
| Scénario séquencé, information inégale | `agent/scenarios/operation_miroir.json` |
| Journal d'audit et traçabilité | `agent/agent3_coordination/audit.py`, `docs/exemple_simulation/` |
| Alignement UIT-T Y.3172 | [docs/Y3172.md](docs/Y3172.md) : les 20 exigences, état et preuve de chacune ; `agent/intent.json` (ML Intent) |
| Lacunes de politiques et de normes | [docs/LACUNES.md](docs/LACUNES.md) : 10 lacunes du domaine et 5 lacunes de normes, avec exemples internationaux vérifiés, et relecture humaine de la simulation de référence |
| Ce qui est prouvé, et ses limites | [docs/PREUVES.md](docs/PREUVES.md) : chaque affirmation, sa preuve, sa limite |

### La vérification des citations

| Statut | Signification |
|---|---|
| ✅ étayée | s'appuie sur un extrait réellement fourni à l'assistant |
| 🔶 douteuse | cite un vrai extrait, mais mentionne un article ou un texte absent de cet extrait |
| ⚠️ non étayée | aucune source citée |
| ❌ invalide | cite un extrait qui n'a jamais été fourni (invention) |

## Démarrage rapide (agents)

Prérequis : Python 3.11, [Ollama](https://ollama.com) (embeddings), une clé
d'API [Groq](https://console.groq.com) (gratuite).

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt
ollama pull bge-m3
copy .env.example .env      # puis renseigner AIREADY_GROQ_API_KEY
```

Construire la base de connaissances (dans `bd/chromadb/`) :

```bash
python -m bd.knowledge.ingest --dir bd/InputDocs --reset
```

Lancer une simulation :

```bash
python run_simulation.py --essai --etapes 1     # essai rapide (petit modèle, étape 1)
python run_simulation.py                        # simulation complète de référence
python run_simulation.py --reprendre runs/<date>_<scénario>   # reprise après un quota épuisé
```

La simulation est pilotée par le **ML Intent** `agent/intent.json` (UIT-T
Y.3172, REQ-ML-SPEC-001 à 004) : agents actifs, modèles principal et de
secours, contraintes (jetons, extraits, historique), seuil de qualité et
sorties. L'orchestrateur se **reconfigure seul** et l'inscrit au journal
(REQ-ML-MNG-001 et MNG-004) :

- si le taux d'actions étayées d'un agent passe sous le seuil, nouvelle
  tentative avec plus d'extraits ; la meilleure est gardée ;
- si le quota du modèle principal est épuisé, bascule sur le modèle de secours.

Tests de l'orchestrateur (faux modèle de langage, aucun jeton consommé) :

```bash
python -m unittest agent.tests.test_orchestration -v
```

Chaque simulation produit dans `runs/<date>_<scénario>/` un journal d'audit
complet (`journal.jsonl`), un rapport lisible (`rapport.md`) et un bilan
chiffré (`resume.json`). Page de démonstration autonome :

```bash
python agent/scripts/export_demo.py runs/<date>_<scénario>
```

Réappliquer les contrôles de citation à une simulation déjà jouée, sans appel
au modèle : `python agent/scripts/reverify.py runs/<date>_<scénario>`.

Indicateurs d'une simulation (citations, coordination, jetons, lacunes
attendues retrouvées) : `python agent/scripts/indicateurs.py runs/<date>_<scénario>`.

Démonstration de secours, sans connexion ni quota : rejouer une simulation à
partir de son journal, étape par étape.

```bash
python agent/scripts/rejouer.py docs/exemple_simulation --pas-a-pas --details
```

Modèles : `gpt-oss-120b` (raisonnement, via Groq, poids ouverts),
`gpt-oss-20b` (essais), `bge-m3` (embeddings multilingues, local via Ollama).

## L'application MinorShield

Application Android qui analyse en temps quasi réel le contenu affiché sur le
téléphone d'un enfant et bloque les contenus inappropriés, en alertant le
parent. 2ᵉ prix du Concours national du meilleur projet TIC (Cameroun, 2026).
Voir [application/frontend/README_FRONTEND.md](application/frontend/README_FRONTEND.md)
et [application/backend/README_DEPLOIEMENT.md](application/backend/README_DEPLOIEMENT.md).

Pour compiler l'application, il faut fournir vos propres paramètres, absents du
dépôt public :

- `application/frontend/app/google-services.json` (projet Firebase) ;
- la clé `API_KEY` dans `application/frontend/app-enfant/.../network/ChildApiClient.kt`,
  identique à `API_KEY` dans `application/backend/.env` (voir `.env.example`).

## Code de référence de l'UIT

La base de connaissances s'appuie sur le code de référence
[CrashingGuru/ITUAIReadiness](https://github.com/CrashingGuru/ITUAIReadiness)
(licence MIT, voir [LICENSE](LICENSE) et
[docs/README_reference_UIT.md](docs/README_reference_UIT.md)). Améliorations
mesurées :

| Amélioration | Constat et mesure |
|---|---|
| Embeddings multilingues `bge-m3` au lieu de `nomic-embed-text` | Sur des textes juridiques français : 3/3 questions réussies au lieu de 2/3, marge de séparation ×10 |
| Détection du pays d'un document | 20 documents sur 67 étaient mal étiquetés (dont 3 attribués à tort à l'Inde) |
| Découpage des textes juridiques article par article | Chaque morceau correspond à un article citable, avec sa page |
| Fichiers de référence défectueux | 2 PDF du dépôt d'origine sont tronqués et illisibles (signalés, exclus) |
| Outil d'ajout incrémental | La commande d'origine recrée des doublons à chaque lancement |

## Avertissement

Le scénario est fictif. Les entreprises « Tchatlink » et « ScolaPlus » sont
inventées. Les assistants simulent des institutions ; leurs réponses ne
constituent ni un avis juridique ni la position de ces institutions.
