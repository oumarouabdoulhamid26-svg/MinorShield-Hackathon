# Indicateurs — simulation du 2026-10-27 21:05 (UTC)

**Lacunes attendues retrouvées (automatique) : 3/15** — à confirmer par relecture humaine.

## Citations

- Modèle(s) : openai/gpt-oss-120b (47)
- Interventions : 47 (dont 0 en erreur)
- Affirmations vérifiées : 94 — etayee 79, non_etayee 8, citation_douteuse 6, citation_invalide 1
- **Taux d'actions étayées : 84.0%**
- Citations retrouvées mot pour mot dans l'extrait cité : 74 sur 80

| Agent | Étayées | Douteuses | Non étayées | Invalides | Taux |
|---|---|---|---|---|---|
| apdp | 11 | 2 | 2 | 0 | 73% |
| conseiller | 29 | 2 | 1 | 1 | 88% |
| entreprises | 4 | 0 | 1 | 0 | 80% |
| minorshield | 8 | 0 | 1 | 0 | 89% |
| penal | 11 | 2 | 0 | 0 | 85% |
| regulateurs | 11 | 0 | 1 | 0 | 92% |
| social | 5 | 0 | 2 | 0 | 71% |

## Coordination

- Demandes transmises entre agents : 19 (répétitions évitées : 1, coordinations internes : 13, non transmises : 1, écartées par la limite : 5)
- Actions avec institution nommée : 61 sur 61
- Reconfigurations automatiques : 3 (nouvelle_tentative 3)
- Interruption / reprise : 0 / 0

## Consommation

| Type | Nombre | Jetons moyens | Total |
|---|---|---|---|
| reaction | 22 | 3746 | 82426 |
| reponse | 19 | 2742 | 52116 |
| analyse | 6 | 5294 | 31768 |
| **total** | 47 | | **166310** |

## Lacunes attendues (rapprochement automatique, seuil 0.65)

| Étape | Lacune attendue | Lacune relevée la plus proche | Par | Similarité | Statut |
|---|---|---|---|---|---|
| 1 | La loi n° 2023/009 (art. 33) oblige les fournisseurs d'accès à signaler les contenus portant atteinte aux enfants, mais ne prévoit ni canal ni seuil d'alerte pour un outil tiers de protection de l'enfance ou pour des signaux agrégés | La loi ne précise pas les modalités exactes de la campagne d'alerte ni les obligations de partage de données avec MinorShield. | regulateurs | 0.57 | à vérifier |
| 2 | Surveillance et vie privée : au-delà du consentement parental exigé pour un mineur (loi n° 2024/017, art. 9(3)), aucun texte ne dit quand la surveillance de l'écran d'un enfant par un outil privé est licite, ni quelle place donner à l'avis de l'enfant | La loi ne précise pas la procédure exacte pour solliciter directement les données de MinorShield, d'où la demande à l'APDP. | penal | 0.52 | à vérifier |
| 2 | Transfert transfrontalier : la loi n° 2024/017 (art. 32) soumet tout transfert vers un État étranger à l'autorisation préalable de l'APDP, mais rien n'encadre les services d'IA étrangers appelés en temps réel | La loi ne précise pas la procédure exacte pour obtenir rapidement une autorisation de transfert en situation d'urgence | apdp | 0.61 | à vérifier |
| 2 | Responsabilité : aucun texte ne désigne qui répond d'un blocage injustifié ou d'une détection manquée (développeur, parent, école) | Aucun texte fourni ne détaille les modalités de communication du blocage au parent | apdp | 0.75 | retrouvée (auto) |
| 2 | Normes : aucune norme pour mesurer et publier les performances d'un détecteur de contenus, ni pour expliquer un blocage à l'enfant | Aucun texte fourni ne détaille les modalités de communication du blocage au parent | apdp | 0.68 | retrouvée (auto) |
| 2 | Définition : le « contenu inapproprié » de la loi n° 2023/009 (art. 3) ne correspond pas aux catégories du détecteur (nudité, violence, texte) | Absence de cadre précis sur la durée légale de conservation des données de contenus bloqués et sur les conditions de transmission aux autorités. | conseiller | 0.53 | à vérifier |
| 3 | La victime de 19 ans n'est pas un « enfant » au sens de la loi n° 2023/009 (art. 3 : moins de 18 ans), alors que le Code pénal (art. 347) protège spécialement les mineurs de 16 à 21 ans | La loi ne prévoit pas explicitement la procédure de demande directe de logs à un prestataire privé comme MinorShield sans passer par l'APDP | penal | 0.42 | à vérifier |
| 3 | Chevauchement des missions MINAS et MINPROFF | Le partage de compétences entre MINAS et MINPROFF n’est pas clairement défini dans la loi | social | 0.64 | à vérifier |
| 3 | Absence de directive scolaire sur la protection des élèves victimes en ligne | Aucune disposition légale ne prévoit de mesures spécifiques du MINESEC pour la protection des élèves victimes en ligne | social | 0.79 | retrouvée (auto) |
| 4 | Portée extraterritoriale limitée face aux plateformes sans établissement au Cameroun | Absence de délai précis imposé aux plateformes étrangères pour répondre à une demande de retrait de contenus illicites | conseiller | 0.56 | à vérifier |
| 4 | Délai de mise en demeure de 15 jours (loi n° 2023/009, art. 28), inadapté à une diffusion virale | Absence de délai précis imposé aux plateformes étrangères pour répondre à une demande de retrait de contenus illicites | conseiller | 0.52 | à vérifier |
| 5 | Autorité de protection des données en place depuis juin 2026 seulement : procédures en construction | La loi ne prévoit pas de procédure obligatoire de notification de fuite de données aux établissements et aux familles | social | 0.53 | à vérifier |
| 5 | La loi n° 2024/017 (art. 22) impose d'informer « sans délai » l'APDP et les personnes concernées, mais sans délai chiffré (72 heures dans le RGPD, art. 33) ni règle propre aux enfants | Absence d'obligation légale précise de notification rapide des violations de données aux personnes concernées et aux autorités compétentes. | conseiller | 0.58 | à vérifier |
| 6 | Conflit d'objectifs : protection de l'enfance contre liberté d'expression et impact économique | Pas de disposition détaillant la procédure de transmission de données personnelles d'enfants vers des autorités étrangères au-delà du consentement | minorshield | 0.43 | à vérifier |
| 6 | Absence de mécanisme formel de coordination interinstitutionnelle de crise | Absence de texte légal précisant les conditions de partage de statistiques agrégées avec les autorités nationales | minorshield | 0.61 | à vérifier |
