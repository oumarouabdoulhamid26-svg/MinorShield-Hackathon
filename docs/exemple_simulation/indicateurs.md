# Indicateurs — 20261024-214752_operation_miroir

**Lacunes attendues retrouvées (automatique) : 1/15** — à confirmer par relecture humaine.

## Citations

- Modèle(s) : openai/gpt-oss-120b (53)
- Interventions : 53 (dont 0 en erreur)
- Affirmations vérifiées : 110 — etayee 95, non_etayee 10, citation_douteuse 4, citation_invalide 1
- **Taux d'actions étayées : 86.4%**

| Agent | Étayées | Douteuses | Non étayées | Invalides | Taux |
|---|---|---|---|---|---|
| apdp | 8 | 0 | 0 | 0 | 100% |
| conseiller | 39 | 0 | 1 | 1 | 95% |
| entreprises | 10 | 0 | 1 | 0 | 91% |
| minorshield | 6 | 2 | 2 | 0 | 60% |
| penal | 15 | 2 | 2 | 0 | 79% |
| regulateurs | 12 | 0 | 4 | 0 | 75% |
| social | 5 | 0 | 0 | 0 | 100% |

## Coordination

- Demandes transmises entre agents : 25 (répétitions évitées : 0, coordinations internes : 13, non transmises : 0, écartées par la limite : 10)
- Actions avec institution nommée : 69 sur 69
- Reconfigurations automatiques : 2 (nouvelle_tentative 2)
- Interruption / reprise : 0 / 0

## Consommation

| Type | Nombre | Jetons moyens | Total |
|---|---|---|---|
| reaction | 22 | 3211 | 70654 |
| reponse | 25 | 2443 | 61093 |
| analyse | 6 | 4555 | 27330 |
| **total** | 53 | | **159077** |

## Lacunes attendues (rapprochement automatique, seuil 0.65)

| Étape | Lacune attendue | Lacune relevée la plus proche | Par | Similarité | Statut |
|---|---|---|---|---|---|
| 1 | La loi n° 2023/009 (art. 33) oblige les fournisseurs d'accès à signaler les contenus portant atteinte aux enfants, mais ne prévoit ni canal ni seuil d'alerte pour un outil tiers de protection de l'enfance ou pour des signaux agrégés | La loi ne précise pas les modalités de partage de statistiques agrégées par un tiers privé comme MinorShield. | regulateurs | 0.54 | à vérifier |
| 2 | Surveillance et vie privée : au-delà du consentement parental exigé pour un mineur (loi n° 2024/017, art. 9(3)), aucun texte ne dit quand la surveillance de l'écran d'un enfant par un outil privé est licite, ni quelle place donner à l'avis de l'enfant | La loi ne précise pas de procédure exacte pour le partage de captures d’écran à des autorités étrangères, limitant notre capacité à le faire sans consentement explicite. | minorshield | 0.62 | à vérifier |
| 2 | Transfert transfrontalier : la loi n° 2024/017 (art. 32) soumet tout transfert vers un État étranger à l'autorisation préalable de l'APDP, mais rien n'encadre les services d'IA étrangers appelés en temps réel | La loi ne précise pas la procédure exacte pour solliciter la remise de données hébergées à l'étranger (serveur OpenAI aux États-Unis). | penal | 0.60 | à vérifier |
| 2 | Responsabilité : aucun texte ne désigne qui répond d'un blocage injustifié ou d'une détection manquée (développeur, parent, école) | Nous ne disposons pas d’un cadre légal autorisant la sanction directe des auteurs du contenu. | minorshield | 0.58 | à vérifier |
| 2 | Normes : aucune norme pour mesurer et publier les performances d'un détecteur de contenus, ni pour expliquer un blocage à l'enfant | Nous ne disposons pas d’un cadre légal autorisant la sanction directe des auteurs du contenu. | minorshield | 0.59 | à vérifier |
| 2 | Définition : le « contenu inapproprié » de la loi n° 2023/009 (art. 3) ne correspond pas aux catégories du détecteur (nudité, violence, texte) | Nous ne disposons pas d’un cadre légal autorisant la sanction directe des auteurs du contenu. | minorshield | 0.53 | à vérifier |
| 3 | La victime de 19 ans n'est pas un « enfant » au sens de la loi n° 2023/009 (moins de 18 ans), alors que la majorité civile est à 21 ans | Le texte de loi ne précise pas les modalités de coordination entre MINAS et MINPROFF. | social | 0.39 | à vérifier |
| 3 | Chevauchement des missions MINAS et MINPROFF | Le texte de loi ne précise pas les modalités de coordination entre MINAS et MINPROFF. | social | 0.60 | à vérifier |
| 3 | Absence de directive scolaire sur la protection des élèves victimes en ligne | Le MINESEC ne dispose d'aucune disposition légale pour intervenir directement dans la protection des élèves victimes d'extorsion en ligne. | social | 0.69 | retrouvée (auto) |
| 4 | Portée extraterritoriale limitée face aux plateformes sans établissement au Cameroun | La loi ne précise pas les procédures exactes pour contraindre une plateforme étrangère sans présence locale. | regulateurs | 0.61 | à vérifier |
| 4 | Délai de mise en demeure de 15 jours (loi n° 2023/009, art. 28), inadapté à une diffusion virale | La loi ne précise pas les procédures exactes pour contraindre une plateforme étrangère sans présence locale. | regulateurs | 0.46 | à vérifier |
| 5 | Autorité de protection des données en place depuis juin 2026 seulement : procédures en construction | Pas de disposition explicite imposant l'anonymisation des données avant transmission aux autorités compétentes. | conseiller | 0.58 | à vérifier |
| 5 | La loi n° 2024/017 (art. 22) impose d'informer « sans délai » l'APDP et les personnes concernées, mais sans délai chiffré (72 heures dans le RGPD, art. 33) ni règle propre aux enfants | Absence de texte précisant le délai de notification des violations de données à caractère personnel aux personnes concernées. | conseiller | 0.55 | à vérifier |
| 6 | Conflit d'objectifs : protection de l'enfance contre liberté d'expression et impact économique | Absence de texte prévoyant le blocage total et temporaire d'une plateforme en ligne à l'échelle nationale pour des raisons de protection des enfants. | conseiller | 0.49 | à vérifier |
| 6 | Absence de mécanisme formel de coordination interinstitutionnelle de crise | Aucun extrait fourni ne décrit la procédure de notification publique d’une violation (art. 22) pour que je puisse l’appliquer | apdp | 0.52 | à vérifier |
