# Contrôle de la recherche dans la base de connaissances

Mesure du 23/10/2026 21:00 — 15 requêtes (`bd/controle/requetes_controle.json`), embeddings `bge-m3`, aucun appel au modèle de langage.

| Mode | Article attendu en 1re position | Article attendu trouvé | MRR |
|---|---|---|---|
| Recherche brute (5 premiers résultats) | 7/15 | 7/15 | 0.47 |
| Recherche de l'agent (extraits reçus) | 11/15 | 14/15 | 0.82 |

MRR : moyenne de 1/rang de l'article attendu (1 = toujours premier, 0 = jamais trouvé).

| Id | Agent | Question | Attendu | Rang (brute) | Rang (agent) | 1er résultat brut |
|---|---|---|---|---|---|---|
| Q01 | conseiller | Jusqu'à quel âge une personne est-elle considérée comme un enfant pour la protection en ligne ? | Loi_2023-009 art. 3 | — | 1 (sur 4) | US_COPPA_Rule_16CFR312.txt art. — |
| Q02 | regulateurs | Combien de jours un fournisseur défaillant a-t-il pour se conformer après une mise en demeure du régulateur des TIC ? | Loi_2023-009 art. 28 | 1 | 1 (sur 4) | Loi_2023-009_Charte_protecti art. 28 |
| Q03 | entreprises | Quelle sanction risque un fournisseur d'accès qui ne signale pas un contenu portant atteinte à un enfant ? | Loi_2023-009 art. 33 | 1 | 1 (sur 4) | Loi_2023-009_Charte_protecti art. 33 |
| Q04 | entreprises | Un réseau social peut-il être obligé de couper l'accès d'un utilisateur qui publie des contenus nuisibles aux enfants ? | Loi_2023-009 art. 14 | 1 | 1 (sur 4) | Loi_2023-009_Charte_protecti art. 14 |
| Q05 | social | Quel ministère forme le personnel à la détection et à la prise en charge des enfants abusés en ligne ? | Loi_2023-009 art. 8 | 1 | 1 (sur 4) | Loi_2023-009_Charte_protecti art. 8 |
| Q06 | apdp | Un élève de 15 ans peut-il consentir seul à l'utilisation de ses données personnelles ? | Loi_2024-017 art. 9 | — | 1 (sur 4) | EU_RGPD_Reglement_2016-679_F art. 8 |
| Q07 | apdp | Une école a subi une fuite des numéros de téléphone des familles : qui doit être prévenu et quand ? | Loi_2024-017 art. 22 | — | 1 (sur 4) | ONU_CRC_Observation_generale art. — |
| Q08 | apdp | Peut-on envoyer les images signalées d'un enfant vers un serveur situé dans un autre pays ? | Loi_2024-017 art. 32 | — | 1 (sur 4) | ONU_CRC_Observation_generale art. — |
| Q09 | apdp | Quelles sont les missions de l'autorité chargée de contrôler les traitements de données ? | Loi_2024-017 art. 53 | — | 1 (sur 4) | EU_RGPD_Reglement_2016-679_F art. 4 |
| Q10 | penal | Quelle infraction pour quelqu'un qui menace de publier des photos intimes si la victime ne paie pas ? | Loi_2016-007 art. 303 | — | — (sur 4) | Australia_Online_Safety_Act_ art. — |
| Q11 | penal | Les peines sont-elles aggravées lorsque la victime d'une atteinte sexuelle a 19 ans ? | Loi_2016-007 art. 347 | — | 2 (sur 4) | UK_Online_Safety_Act_2023.tx art. — |
| Q12 | penal | Quelles peines pour la diffusion d'images sexuelles de mineurs par Internet ? | Loi_2010-012 art. 81 | 1 | 1 (sur 4) | Loi_2010-012_Cybersecurite_c art. 80 |
| Q13 | conseiller | Existe-t-il ailleurs un organe national chargé de coordonner les autorités sur la sécurité numérique des enfants ? | UAE_Decree art. 4 | — | 4 (sur 4) | ONU_CRC_Observation_generale art. — |
| Q14 | conseiller | Must online platforms immediately report child sexual abuse material to the authorities? | UAE_Decree art. 10 | 1 | 2 (sur 4) | UAE_Decree_Law_26-2025_Child art. 15 |
| Q15 | conseiller | En Europe, dans quel délai faut-il notifier une violation de données à l'autorité de contrôle ? | EU_RGPD art. 33 | 1 | 1 (sur 3) | EU_RGPD_Reglement_2016-679_F art. 33 |
