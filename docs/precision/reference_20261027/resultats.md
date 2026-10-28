# Précision des affirmations « étayées » — relecture humaine

Échantillon : 30 affirmations tirées parmi celles que la vérification automatique classe « étayées » (`docs/precision/reference_20261027/echantillon.jsonl`, tirage stratifié par type, graine fixe). Question posée au relecteur : l'extrait cité fonde-t-il l'affirmation telle qu'elle est écrite ? Intervalle de confiance de Wilson à 95 %. Méthode : `agent/scripts/precision.py`.

### Relecteur « claude »

- Cas relus : 30 — fondée 15, partielle 8, non fondée 7, incertain 0 (exclus du dénominateur)
- **Précision stricte (fondée) : 50% — IC 95 % [33% ; 67%]** (n = 30)
- Précision large (fondée + partielle) : 77% — IC 95 % [59% ; 88%]

| Type | Cas | Fondée | Partielle | Non fondée | Incertain |
|---|---|---|---|---|---|
| analyse | 11 | 8 | 2 | 1 | 0 |
| reaction | 14 | 7 | 5 | 2 | 0 |
| reponse | 5 | 0 | 1 | 4 | 0 |

## Cas non fondés ou partiels (relecteur « claude »)

| Cas | Étape | Agent | Affirmation | Extrait(s) | Étiquette | Commentaire |
|---|---|---|---|---|---|---|
| 2 | 2 | conseiller | Comparaison Australie : Le Online Safety Act prévoit des ordonnances de retrait et de conservation limitées, a | Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 64/157) | non_fondee | la citation (decoupee par des points de suspension) porte sur des declarations publiques apres des infractions repetees ; rien sur des ordonnances de conservation ni des delais de transmission aux autorites |
| 4 | 5 | minorshield | Conformément à l'article 23(2) de la loi n° 2023/009, nous avons mis en place un système de paramétrage qui re | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23,  | non_fondee | l'art. 23(2) impose un parametrage protecteur de la vie privee ; consentement parental ecrit, conservation de 30 jours et transmission « aux autorites americaines » n'y sont pas (et ces faits sont inventes) |
| 5 | 6 | regulateurs | Déployer des moyens préventifs de blocage des contenus illicites sur les réseaux nationaux en ordonnant aux op | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10,  | partielle | art. 10(1) : mandat general de moyens preventifs ; le pouvoir d'ordonner un filtrage aux operateurs n'y est pas (l'art. 10(2) renvoie a un autre texte) |
| 7 | 6 | apdp | Demander à MinorShield de fournir les consentements parentaux associés aux captures d'écran avant tout transfe | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17,  | partielle | art. 17 : renvoi general a la reglementation ; l'exigence des consentements parentaux avant transfert a l'etranger releve de la loi 2024/017, non citee |
| 8 | 6 | conseiller | Comparaison Australie : Le bloqueur peut imposer un blocage limité dans le temps (max 3 mois) sur du matériel  | Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 78/157) | partielle | duree maximale de 3 mois exacte (s. 96) ; mais les blocking requests visent les contenus de violence odieuse (Part 8), pas tout « materiel juge prejudiciable » |
| 12 | 5 | regulateurs | L'ANTIC peut ordonner à l'opérateur mobile de suspendre les services de paiement utilisés pour le chantage, d' | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10,  | non_fondee | l'art. 10 ne donne aucun pouvoir de suspendre des services de paiement, ni de mise en demeure a 15 jours sous peine de sanctions |
| 13 | 2 | minorshield | Conserver la capture d'écran concernée pendant 30 jours, conformément aux exigences de mise en place de mécani | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23,  | non_fondee | l'art. 23(3) vise le retrait et le blocage, pas la conservation de captures pendant 30 jours |
| 15 | 4 | conseiller | Comparaison Australie : Obligation de délivrer un avis de retrait dans un délai déterminé | Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157) | partielle | la citation dit qu'un avis de retrait PEUT etre donne ; ni obligation ni delai determine |
| 18 | 5 | apdp | Publier un avis public rappelant l'obligation de notification des violations de données aux personnes concerné | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, ar | non_fondee | l'art. 53 (traitement des plaintes) ne porte pas sur la notification des violations aux personnes concernees (art. 22, non fourni) |
| 23 | 1 | minorshield | Continuer de bloquer les contenus identifiés comme atteignant la dignité ou l'intégrité des enfants et alerter | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23,  | partielle | le blocage est fonde (art. 23(3)), l'alerte aux parents ne l'est pas par cette citation |
| 24 | 4 | regulateurs | Émettre une alerte de sécurité et recommander aux opérateurs de télécommunications de mettre en place un filtr | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27,  | partielle | l'art. 27 vise les atteintes qui ne sont PAS des infractions penales ; or la sextorsion en est une ; la collaboration avec l'ART est fondee |
| 25 | 4 | regulateurs | Nous prenons acte de votre demande et, conformément à nos prérogatives, nous émettons une décision officielle  | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10,  | partielle | art. 10(1) : mandat general ; une decision formelle de suspension d'acces n'y est pas prevue |
| 26 | 6 | regulateurs | Conformément à l'article 10, l'ANTIC peut déployer des moyens préventifs et répressifs pour protéger les enfan | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10,  | non_fondee | ni l'art. 10 ni l'art. 27 ne prevoient le blocage d'une plateforme entiere (le conseiller le releve lui-meme dans sa synthese) |
| 27 | 6 | entreprises | Nous procédons immédiatement au retrait des images de la victime de la plateforme et fournirons les preuves de | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14,  | non_fondee | l'art. 14 impose de suspendre l'acces du consommateur auteur de la publication, pas de retirer les images |
| 28 | 6 | entreprises | Suspendre l'accès au contenu incriminé publié sur Tchatlink, conformément à la demande des autorités compétent | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14,  | partielle | l'art. 14 vise la suspension de l'acces de l'auteur de la publication, a la demande des autorites ; bloquer un contenu precis sur une plateforme etrangere n'est pas la meme mesure |
