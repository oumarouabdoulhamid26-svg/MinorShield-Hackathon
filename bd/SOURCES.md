# Sources de la base de connaissances

Chaque document de la base est listé ici avec sa provenance exacte et la façon
dont il a été traité. Les textes sont dans
`bd/InputDocs/<catégorie>/`.

---

## 1. Textes juridiques camerounais — `Child_Online_Protection/`

**Source unique :** *Recueil des textes du secteur des Postes,
Télécommunications et TIC — Édition 2023*, publié par l'Agence de Régulation
des Télécommunications (ART) et le Ministère des Postes et Télécommunications.

- Adresse : <https://art.cm/sites/default/files/documents/Recueil%20des%20textes%20du%20secteur%20des%20Postes%2C%20T%C3%A9l%C3%A9communications%20et%20TIC%20-%20Edition%202023.pdf>
- Fichier : 464 pages, 14 419 598 octets (taille conforme à celle annoncée par le serveur).
- Traitement : texte natif du PDF (pas d'OCR) ; découpage en un fichier par
  texte avec `bd/scripts/split_recueil.py` ; en-têtes et pieds de page répétés
  retirés ; marqueurs `[PAGE n]` conservés pour la citation.

| Fichier | Texte officiel | Pages du recueil |
|---|---|---|
| `Loi_2023-009_…` | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun | 224–230 |
| `Loi_2010-012_…` | Loi n° 2010/012 du 21 décembre 2010 relative à la cybersécurité et à la cybercriminalité | 200–218 |
| `Loi_2010-013_…` | Loi n° 2010/013 du 21 décembre 2010 régissant les communications électroniques | 177–199 |
| `Loi_2015-006_…` | Loi n° 2015/006 du 20 avril 2015 modifiant la loi n° 2010/013 | 219–223 |
| `Loi_2010-021_…` | Loi n° 2010/021 du 21 décembre 2010 régissant le commerce électronique | 85–98 |
| `Decret_2012-512_…` | Décret n° 2012/512 du 12 novembre 2012 portant organisation du MINPOSTEL | 10–40 |
| `Decret_2019-150_…` | Décret n° 2019/150 du 22 mars 2019 portant organisation et fonctionnement de l'ANTIC | 51–61 |
| `Decret_2020-727_…` | Décret n° 2020/727 du 3 décembre 2020 portant réorganisation et fonctionnement de l'ART | 66–76 |
| `Decret_2015-3759-PM_…` | Décret n° 2015/3759/PM du 3 septembre 2015 — identification des abonnés et des terminaux | 325–329 |
| `Decret_2012-1643-PM_…` | Décret n° 2012/1643/PM du 14 juin 2012 — audit de sécurité obligatoire | 274–277 |
| `Decret_2013-0399-PM_…` | Décret n° 2013/0399/PM du 27 février 2013 — protection des consommateurs des communications électroniques | 303–307 |

### Contrôles effectués

- **Loi 2023/009 :** les 49 articles sont présents ; le texte se termine par
  l'article 49 et la formule de promulgation « Yaoundé, le 25 juillet 2023 —
  Paul Biya ». Cela tranche la divergence de date relevée dans la presse
  (certaines sources indiquaient le 28 juillet 2023).
- **Recoupement :** une copie scannée de la loi 2023/009 portant la mention
  « www.prc.cm » (site de la Présidence de la République) a aussi été obtenue
  via Digital Business Africa ; elle sert de contrôle croisé par OCR.

### Textes recherchés mais non obtenus

| Texte | Situation |
|---|---|
| Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel | Existence et principales dispositions confirmées par plusieurs sources secondaires (création de l'APDP, art. 53 ; entrée en vigueur le 23 juin 2026). **Texte intégral officiel introuvable en ligne à ce jour.** |
| Décret portant organisation du Gouvernement (attributions MINAS / MINPROFF / MINESEC) | Non inclus dans le recueil de l'ART. |

---

## 2. Références mondiales — `Child_Online_Protection/`

Traitement : conversion en texte avec `bd/scripts/prepare_reference.py` (titre
officiel et source en tête de fichier), puis découpage article par article
lorsque le texte est organisé en articles (DSA : 93 articles, RGPD : 99) ;
les textes organisés en « sections » (Royaume-Uni, Australie, États-Unis)
sont découpés en blocs de taille fixe, chacun précédé du titre.

| Texte | Source officielle | Langue | Statut |
|---|---|---|---|
| Règlement (UE) 2022/2065 — Digital Services Act | EUR-Lex (CELEX 32022R2065), version HTML | Français | Obtenu — 93 articles |
| Règlement (UE) 2016/679 — RGPD | EUR-Lex (CELEX 32016R0679) | Français | Obtenu — 99 articles |
| Online Safety Act 2023 (Royaume-Uni) | legislation.gov.uk (ukpga/2023/50) | Anglais | Obtenu |
| COPPA Rule, 16 CFR Part 312 (États-Unis) | eCFR — version incluant la modification du 22 avril 2025 | Anglais | Obtenu |
| Online Safety Act 2021 (Australie) | Federal Register of Legislation (C2021A00076), **version d'origine du 23 juillet 2021** | Anglais | Obtenu |
| Online Safety Act 2021 consolidé au 11 décembre 2024 (Australie), incluant la réforme sur l'âge minimum des réseaux sociaux | Federal Register of Legislation (C2024C00852) | Anglais | **Non obtenu** — le serveur renvoie une page d'erreur au téléchargement automatisé |
| Observation générale n° 25 (2021), Comité des droits de l'enfant de l'ONU | Bibliothèque numérique de l'ONU (CRC/C/GC/25, fiche 3906061) | Français | **Non obtenu** — protection anti-robots du serveur ; à télécharger manuellement. Une copie disponible sur le site du BICE a été écartée : il s'agit d'un résumé illustré de 5 pages, pas du texte officiel. |

> **Conséquence pour la simulation :** la version australienne utilisée
> précède la réforme de 2024. Les comparaisons avec l'Australie portent donc
> sur le régime de 2021.

---

## 3. Documents fournis par l'UIT — `AI_Strategies/` et `AI_Use_Cases/`

Repris du dépôt de référence
[CrashingGuru/ITUAIReadiness](https://github.com/CrashingGuru/ITUAIReadiness)
(licence MIT). Liste détaillée : `bd/InputDocs/Inputs.md`.

**Anomalie constatée dans le dépôt de référence :** deux PDF sont tronqués et
illisibles — `Kenya_AI_Strategy_2025-2030.pdf` (6,9 Mo stockés pour
23,9 Mo annoncés dans son propre en-tête) et
`China_AI_Security_Governance_Framework_2025.pdf` (marqueur de fin de
fichier absent). Ils ne sont pas dans la base ; un résumé de la stratégie
kényane (`Kenya_AI_Strategy_2025_2030_summary.txt`) y figure.
