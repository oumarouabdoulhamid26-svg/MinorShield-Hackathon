# MinorShield Policy Lab — Technical report, version 2 (draft)

> Draft written on 24/10/2026, to be poured into the official template
> (5 pages maximum). Figures marked `{{…}}` come from the reference run
> (planned for 24/10 evening) and are filled in afterwards. Section order
> follows the FAQ of the hackathon page (a to h).

AI for Good Sandbox Hackathon – {{Team name}} – MinorShield Policy Lab
Team leader: Abdoul-Hamid Oumarou — Team members: {{to complete}} — Contact: oumarouabdoulhamid26@gmail.com
GitHub: https://github.com/oumarouabdoulhamid26-svg/MinorShield-Hackathon

## 1. Introduction

MinorShield is a parental-control application already deployed in Cameroon (2nd prize, national ICT project competition 2026). It captures what is displayed on a child's phone, analyses it with AI models (nudity, violence, toxic text) and blocks dangerous content while alerting the parent. Protecting a child this way raises questions the law has not settled: may a private tool watch a child's screen, send the captures to a foreign AI service, keep them for the police, or alert the authorities about an emerging campaign? And when such a tool reveals a real crisis, can the institutions concerned act together?

MinorShield Policy Lab answers these questions in a sandbox. Six AI agents, each representing a group of real institutions sharing one objective (regulators, data protection authority, criminal justice chain, social and educational protection, digital companies, and MinorShield as the innovative AI solution), handle a sextortion crisis revealed in six stages. Each agent knows only what has been disclosed to it, acts within the mandate the law gives it and must justify every action with an article it actually retrieved; a legal-advisor agent judges each action, identifies the gaps of the law and compares them with the EU, the UK, the US, Australia, the UAE and the UN. Every citation is checked automatically and every exchange is written to an audit log. The domain is child online protection; Cameroon is the field of illustration, and every gap is stated for the domain with verified global examples.

## 2. Description of the use case

**The AI solution and its real architecture.** On the child's phone, MinorShield captures the screen and sends it to its server, which returns a decision (`DetectionResponse`: label, category, scores). Nudity is detected on the server (NudeNet); violence and text are also sent to OpenAI's moderation service in the United States; a local lexicon covers Cameroonian slang. If the content is judged inappropriate, the screen is masked and the parent alerted. This architecture is effective, but it is also exactly where the law is silent or demanding: consent for a minor, transfer of a child's data abroad, retention, liability for errors.

**Gaps in existing approaches.** (1) Crisis exercises between institutions are rare, costly and leave no trace of why a decision was taken. (2) General-purpose chatbots answer legal questions from memory and invent plausible articles. (3) Comparisons with foreign law are done by hand. (4) Nobody sees in advance where mandates overlap or where no institution is competent.

**How the solution answers them.** A citable knowledge base (official texts split article by article); agents whose mandates come from the law; information revealed progressively and unequally; coordination through requests between agents; automatic verification of every citation; a full audit log; an orchestrator driven by a declarative ML Intent that reconfigures itself when quality drops.

## 3. Use case requirements

- **Data (SRC, C, PP).** Official legal texts only, with source, date and page recorded (`bd/SOURCES.md`): 13 Cameroonian texts, including the Child Online Protection Charter (Law 2023/009), the data protection law (2024/017, obtained from the Presidency's certified copy by OCR) and the Penal Code; 7 international references (EU DSA and GDPR, UK and Australian Online Safety Acts, US COPPA Rule, UAE Federal Decree-Law 26/2025 on Child Digital Safety, UN General Comment No. 25); the ITU strategy corpus. Article-level chunks, local multilingual embeddings (bge-m3): {{8,344}} chunks. No real child data: the detector output of stage 2 is simulated in the real API format and labelled as such.
- **Retrieval quality.** 15 control queries with a hand-verified expected article: the agents' retrieval finds it in 14/15 cases (MRR 0.82), against 7/15 for a plain search, thanks to two rules: the key articles of each agent's mandate are always offered, and at most two extracts per text.
- **Model (M).** Open-weight gpt-oss-120b (Groq), structured JSON output with explicit reasoning; fallback model declared in the ML Intent. Each request fits the free-tier limit (8,000 tokens per minute); a full run uses {{tokens}} tokens.
- **Policy (P).** An agent acts only on information revealed to it; it cites only extract IDs it received; every action names the institution acting; it states what the law does not allow.
- **Sink and human oversight.** Outputs (audit log, report, demonstration page, indicators) are deliberation material for human decision-makers, not legal advice.

## 4. Mapping with ITU-T Y.3172

| Node | Implementation |
|---|---|
| SRC | Legal texts of 7 jurisdictions, scenario, simulated MinorShield detector output |
| C / PP | Ingestion, OCR, article-level chunking with metadata, bge-m3 embeddings |
| M | Six actor agents and one advisor on gpt-oss-120b, retrieval-augmented |
| P | Mandate limits, institution named per action, citation verification, advisor verdicts |
| D | Orchestrator: stages revealed to their recipients only, requests routed between agents |
| SINK | Audit log, readable report, demonstration page, indicators |
| MLFO / ML Intent | Orchestrator configured by `agent/intent.json` (sources, agents, models, constraints, quality threshold, outputs) |

Of the 20 requirements of Y.3172 (detail and evidence in `docs/Y3172.md`), **15 are implemented, 4 partially and 2 not**. Highlights: declarative ML Intent translated into configuration (SPEC-001/002, time and token constraints logged when exceeded); automatic reconfiguration when the share of supported actions falls below the threshold, and fallback model when a quota is exhausted (MNG-001/004: {{n}} reconfigurations in the reference run); monitoring through citation checks and indicators (MNG-003); chaining retrieve → reason → verify → coordinate → advise → report (MNG-005). Not claimed: transfer of trained models and training data (INT-001/002), since no model is fine-tuned and no real child data may be used.

## 5. Mapping with the ITU AI Readiness Report 2.0

| Dimension | Contribution of the project |
|---|---|
| D10 AI & Policies | Core of the project: testing a legal framework before a crisis; gaps identified with global examples |
| D7 Strategy Alignment | Six agents grouping 13 institutions act on one shared legal base; coordination problems become visible |
| D8 Collaboration with AI | Agents state their confidence, unknowns and gaps; humans decide |
| D6 Human Interface | Demonstration page and replay: every decision opens the article it relies on |
| D4 Contextualisation | Cameroonian law and slang lexicon; comparison with five other jurisdictions and the UN |
| D11 AI for Inclusion | Free open-weight models, French-language corpus, runs on a laptop without GPU |
| D1 Data/Model Marketplace | Provenance of every text, open repository, corrections to the ITU reference corpus |

## 6. Requirements mapped to local policies

| Requirement of the use case | Cameroonian text | What it requires |
|---|---|---|
| Analysing a minor's screen | Law 2024/017, art. 9(3) | Consent of the parents or legal representative |
| Sending captures to a foreign AI service | Law 2024/017, art. 32 | Prior authorisation of the data protection authority |
| Retaining captures | Law 2024/017, art. 13 | Retention limited to what the processing needs, period set in the authorisation |
| Data breach | Law 2024/017, art. 22 | Inform the authority and the persons concerned "without delay" |
| Reporting harmful content | Law 2023/009, art. 16 and 33 | Providers must report child sexual abuse material (fine of 25 to 250 million FCFA) |
| Removing content | Law 2023/009, art. 14, 27–29 | Suspension of a user on request; 15-day formal notice before sanctions |
| Qualifying the offence | Penal Code, art. 303 and 347; Law 2010/012, art. 80–82 | Blackmail; offences against minors aged 16 to 21; child sexual abuse material online |

## 7. Evaluation scenario: technical solution and policy

"Operation Mirror", six stages over three days, each revealed only to the agents concerned:

| Stage | Event | Expected tension |
|---|---|---|
| 1 | MinorShield detects a 400% rise in blocked content | Can a private tool alert the authorities, with which data? |
| 2 | A message is blocked on a 14-year-old's phone (simulated detector output, score 0.62); the capture went to a foreign AI service; MinorShield offers to keep captures 30 days for the police | Consent, transfer abroad, retention, liability for a false positive |
| 3 | Two victims (15 and 19); the school considers excluding the younger | Penal qualification, age thresholds, protection of the pupil |
| 4 | Images spread on a foreign platform | Reach of national law, removal deadline |
| 5 | The source is a leak from a school app, unreported for three weeks | Breach notification, liability |
| 6 | Media pressure: block the platform nationwide? | Proportionality, freedom of expression (controversy) |

**Results of the reference run** ({{date}}, gpt-oss-120b): {{interventions}} interventions, {{requests}} requests routed between agents, {{rate}} of legal claims supported by an extract provided, institution named in {{x}}/{{y}} actions, {{n}} automatic reconfigurations, {{tokens}} tokens. Of the {{k}} gaps written into the scenario beforehand, {{found}} were identified (automatic matching confirmed by human review). {{Two or three illustrations: what worked, what was missed, AI errors caught and not caught.}}

**Handling the controversy.** The system never decides: it produces the material for a human deliberation. On stage 6 the advisor {{…}}; our answer favours targeted, motivated measures under judicial control before any general block.

**Limits.** The verifier cannot detect a correct citation used for a wrong claim; the detector input is simulated; results come from one model and one scenario. A human legal review remains mandatory.

## 8. Policy gaps and standards gaps

Detail, sources and global examples: `docs/LACUNES.md`. Summary:

| Gap (domain: child online protection) | Cameroonian source | Global example |
|---|---|---|
| No channel or threshold for third-party child-safety tools to report | Law 2023/009, art. 33 | UK OSA 2023 s. 66; UAE DL 26/2025 art. 10–11; DSA art. 18 |
| 15-day notice for content that spreads in hours | Law 2023/009, art. 28 | Australia OSA 2021 s. 77 (24 hours) |
| No reach on foreign platforms, no local representative | Law 2023/009, art. 2, 14–16 | DSA art. 2 and 13; UAE DL art. 3 |
| Breach notification "without delay", no deadline, nothing specific to minors | Law 2024/017, art. 22 | GDPR art. 33 (72 hours) and 34 |
| Inconsistent age thresholds (under 18 vs 16–21) | Law 2023/009, art. 3; Penal Code art. 347 | UAE DL art. 1; UN GC 25 |
| No rules on monitoring a child's screen beyond parental consent | Law 2024/017, art. 9(3) | UN GC 25 para. 75; GDPR art. 8; UAE DL art. 13 and 7 |
| Real-time foreign AI services not addressed by transfer rules | Law 2024/017, art. 32 | GDPR art. 44–45 |
| No liability or appeal for errors of protection tools | No provision | DSA art. 17 and 20 |
| No coordination body; overlapping ministries | Law 2023/009, art. 4–8 | UAE DL art. 4–5; UN GC 25 para. 27 |
| No framework or proportionality for blocking a platform | Law 2023/009, art. 14 | UAE DL art. 10(3); DSA art. 17, 20 |

**Standards gaps.** (N1) Y.3172 has no node to verify that a language-model output is grounded in its sources: we propose one between M and SINK, with two metrics (share of supported claims, recall of expected gaps). (N2) The AI Readiness Report 2.0 does not cover agentic AI (delegation, multi-agent coordination, autonomy): indicators should cover traceability of exchanges, respect of mandates and grounding. (N3) No standard to measure and publish the performance of on-device content detectors or to explain a block to a child. (N4) Laws published only as (often scanned) PDF, without a machine-readable, article-level format. (N5) Integrity issues in the ITU reference corpus (two truncated files, 20 of 67 documents with a wrong country), corrected in our repository.
