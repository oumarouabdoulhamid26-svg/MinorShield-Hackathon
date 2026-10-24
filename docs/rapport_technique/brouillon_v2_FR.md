# MinorShield Policy Lab — Rapport technique, version 2 (traduction française)

> Traduction du brouillon anglais `brouillon_v2_EN.md` (version de référence
> soumise au hackathon). Chiffres de la simulation de référence du 24/10/2026
> (`docs/exemple_simulation/`), tous justifiés dans `docs/PREUVES.md`.

AI for Good Sandbox Hackathon – [Nom de l'équipe] – MinorShield Policy Lab
Chef d'équipe : Abdoul-Hamid Oumarou — Membres de l'équipe : [à compléter] — Contact : oumarouabdoulhamid26@gmail.com
Lien GitHub : https://github.com/oumarouabdoulhamid26-svg/MinorShield-Hackathon

## 1. Introduction

MinorShield est une application de contrôle parental déjà déployée au Cameroun (2e prix du Concours national du meilleur projet TIC 2026). Elle capture ce qui s'affiche sur le téléphone d'un enfant, l'analyse avec des modèles d'IA (nudité, violence, texte toxique) et bloque les contenus dangereux en alertant le parent. Protéger un enfant de cette façon soulève des questions que le droit n'a pas tranchées : un outil privé peut-il surveiller l'écran d'un enfant, envoyer ses captures à un service d'IA étranger, les conserver pour la police, ou alerter les autorités d'une campagne naissante ? Et lorsqu'un tel outil révèle une crise réelle, les institutions concernées peuvent-elles agir ensemble ?

MinorShield Policy Lab répond à ces questions dans un bac à sable. Six agents IA, représentant chacun un groupe d'institutions réelles qui partagent le même objectif (régulateurs, autorité de protection des données, chaîne pénale, protection sociale et éducative, entreprises du numérique, et MinorShield comme solution d'IA innovante), gèrent une crise de chantage sexuel révélée en six étapes. Chaque agent ne connaît que ce qui lui a été révélé, agit dans le mandat que la loi lui donne et doit justifier chaque action par un article qu'il a réellement retrouvé ; un agent conseiller juridique juge chaque action, relève les lacunes du droit et les compare à l'Union européenne, au Royaume-Uni, aux États-Unis, à l'Australie, aux Émirats arabes unis et à l'ONU. Chaque citation est vérifiée automatiquement et chaque échange est inscrit dans un journal d'audit. Le domaine est la protection des mineurs en ligne ; le Cameroun sert de terrain d'illustration, et chaque lacune est formulée pour le domaine, avec des exemples mondiaux vérifiés.

## 2. Description du cas d'usage

**La solution d'IA et son architecture réelle.** Sur le téléphone de l'enfant, MinorShield capture l'écran et l'envoie à son serveur, qui renvoie une décision (`DetectionResponse` : étiquette, catégorie, scores). La nudité est détectée sur le serveur (NudeNet) ; la violence et le texte sont aussi envoyés au service de modération d'OpenAI, aux États-Unis ; un lexique local couvre l'argot camerounais. Si le contenu est jugé inapproprié, l'écran est masqué et le parent alerté. Cette architecture est efficace, mais c'est aussi précisément là que le droit est muet ou exigeant : consentement pour un mineur, transfert des données d'un enfant à l'étranger, conservation, responsabilité en cas d'erreur.

**Faiblesses des approches existantes.** (1) Les exercices de crise entre institutions sont rares, coûteux, et ne gardent aucune trace des raisons d'une décision. (2) Les assistants conversationnels généralistes répondent de mémoire et inventent des articles plausibles. (3) Les comparaisons avec le droit étranger se font à la main. (4) Personne ne voit à l'avance où les mandats se chevauchent ni où aucune institution n'est compétente.

**Comment la solution y répond.** Une base de connaissances citable (textes officiels découpés article par article) ; des agents dont les mandats viennent de la loi ; une information révélée progressivement et inégalement ; une coordination par demandes entre agents ; la vérification automatique de chaque citation ; un journal d'audit complet ; un orchestrateur piloté par un ML Intent déclaratif, qui se reconfigure quand la qualité baisse.

## 3. Exigences du cas d'usage

- **Données (SRC, C, PP).** Uniquement des textes juridiques officiels, avec source, date et page enregistrées (`bd/SOURCES.md`) : 13 textes camerounais, dont la Charte de protection des enfants en ligne (loi 2023/009), la loi sur les données personnelles (2024/017, obtenue par OCR de la copie certifiée de la Présidence) et le Code pénal ; 7 références internationales (DSA et RGPD européens, Online Safety Acts britannique et australien, règle COPPA américaine, décret-loi fédéral émirien 26/2025 sur la sécurité numérique des enfants, Observation générale n° 25 de l'ONU) ; le corpus stratégique de l'UIT. Découpage par article, embeddings multilingues locaux (bge-m3) : 8 344 passages. Aucune donnée réelle d'enfant : la sortie du détecteur de l'étape 2 est simulée au format réel de l'API, et signalée comme telle.
- **Qualité de la recherche.** 15 requêtes de contrôle dont l'article attendu est vérifié à la main : la recherche des agents le retrouve dans 14 cas sur 15 (MRR 0,82), contre 7 sur 15 pour une recherche brute, grâce à deux règles : les articles clés du mandat de chaque agent lui sont toujours proposés, et au plus deux extraits par texte.
- **Modèle (M).** gpt-oss-120b à poids ouverts (Groq), réponse JSON structurée avec raisonnement explicite ; modèle de secours déclaré dans le ML Intent. Chaque requête respecte la limite de l'offre gratuite (8 000 jetons par minute) ; une simulation complète consomme 165 279 jetons (21 minutes sur un ordinateur portable sans carte graphique).
- **Politique (P).** Un agent n'agit que sur les informations qui lui ont été révélées ; il ne cite que les identifiants d'extraits reçus ; chaque action nomme l'institution qui agit ; il dit ce que la loi ne lui permet pas.
- **Sortie et contrôle humain.** Les sorties (journal d'audit, rapport, page de démonstration, indicateurs) sont des éléments de délibération pour des décideurs humains, pas un avis juridique.

## 4. Correspondance avec UIT-T Y.3172

| Nœud | Mise en œuvre |
|---|---|
| SRC | Textes de loi de 7 juridictions, scénario, sortie simulée du détecteur MinorShield |
| C / PP | Ingestion, OCR, découpage par article avec métadonnées, embeddings bge-m3 |
| M | Six agents acteurs et un conseiller sur gpt-oss-120b, avec recherche augmentée |
| P | Limites de mandat, institution nommée pour chaque action, vérification des citations, verdicts du conseiller |
| D | Orchestrateur : étapes révélées à leurs seuls destinataires, demandes transmises entre agents |
| SINK | Journal d'audit, rapport lisible, page de démonstration, indicateurs |
| MLFO / ML Intent | Orchestrateur configuré par `agent/intent.json` (sources, agents, modèles, contraintes, seuil de qualité, sorties) |

Sur les 20 exigences de Y.3172 (détail et preuves dans `docs/Y3172.md`), **15 sont mises en œuvre, 4 partiellement et 2 non**. Points forts : ML Intent déclaratif traduit en configuration (SPEC-001/002, dépassements de temps et de jetons journalisés) ; reconfiguration automatique quand la part d'actions étayées passe sous le seuil, et modèle de secours quand un quota est épuisé (MNG-001/004 : 2 reconfigurations dans la simulation de référence, toutes deux bénéfiques) ; surveillance par la vérification des citations et les indicateurs (MNG-003) ; enchaînement rechercher → raisonner → vérifier → coordonner → conseiller → rapporter (MNG-005). Non revendiqué : transfert de modèles entraînés et de données d'entraînement (INT-001/002), puisqu'aucun modèle n'est ajusté et qu'aucune donnée réelle d'enfant ne peut être utilisée.

## 5. Correspondance avec le rapport AI Readiness 2.0 de l'UIT

| Dimension | Apport du projet |
|---|---|
| D10 IA et politiques | Cœur du projet : éprouver un cadre juridique avant une crise ; lacunes identifiées avec des exemples mondiaux |
| D7 Alignement stratégique | Six agents regroupant 13 institutions agissent sur une base juridique commune ; les problèmes de coordination deviennent visibles |
| D8 Collaboration avec l'IA | Les agents indiquent leur confiance, ce qu'ils ignorent et les lacunes ; les humains décident |
| D6 Interface humaine | Page de démonstration et rejeu : chaque décision ouvre l'article sur lequel elle s'appuie |
| D4 Contextualisation | Droit camerounais et lexique d'argot local ; comparaison avec cinq autres juridictions et l'ONU |
| D11 IA pour l'inclusion | Modèles gratuits à poids ouverts, corpus en français, fonctionne sur un portable sans carte graphique |
| D1 Place de marché données/modèles | Provenance de chaque texte, dépôt ouvert, corrections du corpus de référence de l'UIT |

## 6. Exigences rapportées aux politiques locales

| Exigence du cas d'usage | Texte camerounais | Ce qu'il impose |
|---|---|---|
| Analyser l'écran d'un mineur | Loi 2024/017, art. 9(3) | Consentement des parents ou du représentant légal |
| Envoyer les captures à un service d'IA étranger | Loi 2024/017, art. 32 | Autorisation préalable de l'autorité de protection des données |
| Conserver les captures | Loi 2024/017, art. 13 | Conservation limitée au besoin du traitement, durée fixée dans l'autorisation |
| Violation de données | Loi 2024/017, art. 22 | Informer l'autorité et les personnes concernées « sans délai » |
| Signaler les contenus nuisibles | Loi 2023/009, art. 16 et 33 | Les fournisseurs doivent signaler la pédopornographie (amende de 25 à 250 millions FCFA) |
| Retirer les contenus | Loi 2023/009, art. 14, 27 à 29 | Suspension d'un utilisateur sur demande ; mise en demeure de 15 jours avant sanction |
| Qualifier l'infraction | Code pénal, art. 303 et 347 ; loi 2010/012, art. 80 à 82 | Chantage ; infractions sur mineurs de 16 à 21 ans ; pédopornographie en ligne |

## 7. Scénario d'évaluation : solution technique et politiques

« Opération Miroir », six étapes sur trois jours, chacune révélée aux seuls agents concernés :

| Étape | Événement | Tension attendue |
|---|---|---|
| 1 | MinorShield détecte une hausse de 400 % des contenus bloqués | Un outil privé peut-il alerter les autorités, avec quelles données ? |
| 2 | Un message est bloqué sur le téléphone d'une collégienne de 14 ans (sortie simulée du détecteur, score 0,62) ; la capture est partie vers un service d'IA étranger ; MinorShield propose de conserver les captures 30 jours pour la police | Consentement, transfert à l'étranger, conservation, responsabilité d'un faux positif |
| 3 | Deux victimes (15 et 19 ans) ; l'école envisage d'exclure la plus jeune | Qualification pénale, seuils d'âge, protection de l'élève |
| 4 | Les images circulent sur une plateforme étrangère | Portée du droit national, délai de retrait |
| 5 | La source est une fuite d'une application scolaire, non signalée depuis trois semaines | Notification de la violation, responsabilité |
| 6 | Pression médiatique : bloquer la plateforme dans tout le pays ? | Proportionnalité, liberté d'expression (controverse) |

**Résultats de la simulation de référence** (24 octobre 2026, gpt-oss-120b, journal complet dans `docs/exemple_simulation/`) : 53 interventions ; 25 demandes transmises entre agents, aucune perdue (29 demandes adressées au nom d'une institution ont été redirigées vers le bon agent) ; **86,4 % des 110 affirmations juridiques étayées par un extrait réellement fourni** (autorité de protection des données 100 %, conseiller 95 %) ; institution nommée dans 69 actions sur 69 ; 2 reconfigurations automatiques ; 165 279 jetons. Sur les 15 lacunes inscrites à l'avance dans le scénario, la relecture humaine en compte **7 identifiées, 3 partiellement, 5 manquées**, plus 4 lacunes que nous n'avions pas prévues (accès de la police aux relevés Mobile Money, anonymisation avant transmission, chevauchement entre l'autorité de protection des données et le régulateur des TIC, texte d'application manquant).

**Ce qui a fonctionné.** Étape 2 : l'autorité de protection des données a exigé l'anonymisation avant toute transmission à la police, la police a constaté qu'aucune procédure ne permet d'obtenir des données hébergées sur les serveurs d'un fournisseur d'IA étranger, et MinorShield a expliqué au parent le risque de faux positif sans trouver de base légale pour un droit de recours. Étape 5 : le conseiller a relevé que « sans délai » ne fixe aucune échéance et a recommandé 72 heures. **Ce qui a été manqué.** Pour la troisième simulation consécutive, aucun agent n'a remarqué que la victime de 19 ans échappe à la Charte (moins de 18 ans) alors que le Code pénal protège les mineurs de 16 à 21 ans ; personne n'a interrogé la légalité de la surveillance de l'écran de l'enfant elle-même. Ces lacunes proviennent de notre analyse humaine et sont présentées comme telles.

**Erreurs de l'IA détectées, et non détectées.** Le vérificateur a signalé 1 identifiant d'extrait inventé, 4 citations douteuses et 10 actions non étayées. Il ne voit pas un extrait réel utilisé pour une affirmation fausse : la relecture humaine en a trouvé 4 (l'art. 25 du DSA présenté comme une obligation de retrait, une obligation de notification des violations attribuée à la COPPA, des pouvoirs de blocage australiens surestimés, une règle de conservation déclarée absente alors que l'art. 13 de la loi 2024/017 la prévoit).

**Traitement de la controverse.** Le système ne décide jamais : il produit la matière d'une délibération humaine. À l'étape 6, le conseiller n'a trouvé aucune base légale pour bloquer une plateforme entière, a consigné le conflit entre protection de l'enfance et liberté d'expression, et a recommandé un blocage temporaire sous contrôle judiciaire, réexaminé après 15 jours ; notre réponse privilégie des mesures ciblées et motivées, sous contrôle judiciaire, avant tout blocage général.

**Limites.** Le vérificateur ne détecte pas une citation correcte utilisée pour une affirmation fausse ; l'entrée du détecteur est simulée ; les résultats viennent d'un seul modèle et d'un seul scénario. Une relecture juridique humaine reste obligatoire.

## 8. Lacunes de politiques et de normes

Détail, sources et exemples mondiaux : `docs/LACUNES.md`. Synthèse :

| Lacune (domaine : protection des mineurs en ligne) | Source camerounaise | Exemple mondial |
|---|---|---|
| Ni canal ni seuil pour qu'un outil tiers de protection signale | Loi 2023/009, art. 33 | R.-U., OSA 2023 s. 66 ; Émirats, DL 26/2025 art. 10 et 11 ; DSA art. 18 |
| Mise en demeure de 15 jours pour des contenus qui circulent en quelques heures | Loi 2023/009, art. 28 | Australie, OSA 2021 s. 77 (24 heures) |
| Aucune prise sur les plateformes étrangères, pas de représentant local | Loi 2023/009, art. 2, 14 à 16 | DSA art. 2 et 13 ; Émirats, DL art. 3 |
| Notification d'une violation « sans délai », sans échéance ni règle propre aux mineurs | Loi 2024/017, art. 22 | RGPD art. 33 (72 heures) et 34 |
| Seuils d'âge incohérents (moins de 18 ans contre 16 à 21 ans) | Loi 2023/009, art. 3 ; Code pénal, art. 347 | Émirats, DL art. 1 ; ONU, OG 25 |
| Aucune règle sur la surveillance de l'écran d'un enfant au-delà du consentement parental | Loi 2024/017, art. 9(3) | ONU, OG 25 par. 75 ; RGPD art. 8 ; Émirats, DL art. 13 et 7 |
| Services d'IA étrangers appelés en temps réel non visés par les règles de transfert | Loi 2024/017, art. 32 | RGPD art. 44 et 45 |
| Ni responsabilité ni recours en cas d'erreur d'un outil de protection | Aucune disposition | DSA art. 17 et 20 |
| Aucun organe de coordination ; ministères aux missions qui se chevauchent | Loi 2023/009, art. 4 à 8 | Émirats, DL art. 4 et 5 ; ONU, OG 25 par. 27 |
| Ni cadre ni proportionnalité pour bloquer une plateforme | Loi 2023/009, art. 14 | Émirats, DL art. 10(3) ; DSA art. 17 et 20 |

**Lacunes de normes.** (N1) Y.3172 ne prévoit aucune étape pour vérifier qu'une sortie de modèle de langage est fondée sur ses sources : nous en proposons une entre M et SINK, avec deux indicateurs (part des affirmations étayées, rappel des lacunes attendues). (N2) Le rapport AI Readiness 2.0 ne couvre pas l'IA agentique (délégation, coordination multi-agents, autonomie) : des indicateurs devraient mesurer la traçabilité des échanges, le respect des mandats et l'ancrage dans les sources. (N3) Aucune norme pour mesurer et publier les performances des détecteurs de contenus, ni pour expliquer un blocage à un enfant. (N4) Lois publiées seulement en PDF (souvent scannés), sans format ouvert lisible par machine, article par article. (N5) Défauts d'intégrité dans le corpus de référence de l'UIT (deux fichiers tronqués, 20 documents sur 67 avec un pays erroné), corrigés dans notre dépôt.
