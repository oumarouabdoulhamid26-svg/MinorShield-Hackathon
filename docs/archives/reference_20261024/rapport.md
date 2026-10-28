# Rapport de simulation — Opération Miroir

*Mode : reference (grand modele) · 2026-10-24T20:47:53+00:00*

## Bilan

| Indicateur | Valeur |
|---|---|
| Interventions d'agents | 53 |
| Actions étayées par un extrait | 95 |
| Actions non étayées | 10 |
| Citations invalides | 1 |
| Taux d'actions étayées | 86% |
| Actions avec institution nommée | 69 sur 69 |
| Demandes entre agents | 25 transmises, 0 non transmises |
| Jetons consommés | 165279 |


---

## Étape 1 — Une hausse anormale de contenus bloqués

**J0, 08h00** · Informés : MinorShield, Regulateurs du numerique

> Le système MinorShield constate depuis 48 heures une hausse de 400 % des contenus bloqués sur les appareils d'enfants protégés à Douala et à Yaoundé. Les messages interceptés partagent le même vocabulaire d'argot local et des formules du type « envoie ta photo sinon… ». Il est encore impossible de dire s'il s'agit d'une campagne organisée ou d'une coïncidence. MinorShield propose de ne partager avec les autorités que des statistiques agrégées et anonymisées.


### MinorShield

**Évaluation.** Une hausse de 400 % des blocages détectés en 48 h, avec un vocabulaire d'argot local, suggère une possible campagne de chantage ou d'exploitation. MinorShield ne dispose d'aucune preuve concrète et ne peut que proposer des mesures de suivi et de partage de données agrégées.

**Ce qu'il ignore :** l'origine exacte des messages (campagne organisée ou phénomène isolé) ; le nombre réel d'enfants affectés ; les éventuels auteurs ou réseaux derrière les messages

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Activer le mode de collecte de statistiques agrégées et anonymisées sur les blocages, puis les transmettre aux autorités compétentes conformément aux obligations de transparence. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |

**Lacunes signalées :**
- La loi ne précise pas les modalités exactes de partage de statistiques agrégées avec les autorités
- Aucun cadre légal n'autorise la transmission de captures d'écran brutes sans consentement explicite.

<details><summary>Raisonnement explicite</summary>

1. Identifier l'anomalie de blocage et son caractère potentiellement dangereux.
2. Vérifier les obligations légales de protection et de respect de la vie privée (E1, E2).
3. Décider de collecter uniquement des données agrégées pour limiter les risques de violation de la vie privée.
4. Solliciter l'APDP afin de garantir la conformité du processus avant tout partage.

</details>


### Regulateurs du numerique

**Évaluation.** Une hausse soudaine de contenus bloqués signale une possible campagne de chantage ciblant des enfants, mais aucune preuve concrète n'est encore disponible.

**Ce qu'il ignore :** identité des auteurs des messages ; si les contenus proviennent d'opérateurs locaux ou de plateformes étrangères

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre un avis de vigilance aux opérateurs d'accès Internet et aux fournisseurs de services de messagerie, les invitant à renforcer le filtrage des messages contenant le vocabulaire suspect et à signaler tout incident au CIRT. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| **ART** — Coordonner avec les opérateurs de communications électroniques pour vérifier la conformité des filtres et, le cas échéant, appliquer les mesures correctives prévues à l'article 27. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **MINPOSTEL** — Lancer, dans le cadre du Plan d'Action National de Protection des Enfants en Ligne, une campagne d'information auprès des parents et des établissements scolaires sur les risques de chantage numérique. | ⚠️ non étayée · mention non vérifiée : article 4 | — |

**Lacunes signalées :**
- La loi ne précise pas les modalités de partage de statistiques agrégées par un tiers privé comme MinorShield.
- Aucun texte ne donne à l'ANTIC le droit d'imposer directement des mesures techniques aux plateformes étrangères sans présence locale.

<details><summary>Raisonnement explicite</summary>

1. Identifier le phénomène anormal (hausse de contenus bloqués).
2. Vérifier les prérogatives légales applicables (E1, E2).
3. Déterminer les acteurs capables d'agir (ANTIC, ART, MINPOSTEL).
4. Proposer des actions coordonnées et formuler les demandes nécessaires.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Fournir le statut de conformité des filtres de contenu des opérateurs et signaler tout manquement.


*Coordination interne* — Regulateurs du numerique (regulateurs) : Valider et financer la campagne d'information prévue.


**Demande** — MinorShield → APDP : Validation du protocole d'anonymisation des données de blocage avant transmission aux autorités

**Réponse de APDP** (✅ étayée) : Nous ne pouvons pas valider le protocole d'anonymisation tant que nous n'avons pas reçu la description détaillée des méthodes employées, les garanties techniques et les mesures de contrôle mises en place pour assurer la non‑identifiabilité des données d'enfants. Merci de nous transmettre ces informations afin de vérifier leur conformité aux exigences de protection des données des mineurs.


### ⚖️ Analyse du conseiller juridique

Les actions de l'ANTIC et de l'ART sont solidement fondées sur les articles E3 et E4, tandis que les mesures de MinorShield et de MINPOSTEL nécessitent des précisions légales. Le droit camerounais manque de dispositions détaillées sur le partage de statistiques agrégées et sur l'application de mesures techniques aux acteurs étrangers, contrairement à l'Australie et aux Émirats arabes unis. Il est recommandé d'amender la charte pour combler ces lacunes et d'établir un protocole de coordination inter‑institutionnel.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | Activer le mode de collecte de statistiques agrégées et anonymisées sur les blocages, puis les transmettre aux autorités compétentes | ⚠️ à vérifier | L'extrait E1 impose aux entreprises d'aider les enfants à comprendre les services, mais ne précise pas le partage de statistiques agrégées aux autorités ; l'extrait E2 décrit des obligations de transparence sur la vie privée, sans mentionner de transmission aux pouvoirs publics. La base légale est donc partielle. |
| ANTIC | Émettre un avis de vigilance aux opérateurs d'accès Internet et aux fournisseurs de services de messagerie, les invitant à renforcer le filtrage des messages contenant le vocabulaire suspect et à signaler tout incident au CIRT | ✅ fondée | L'extrait E3 stipule que l'organe chargé de la régulation des TIC déploie des moyens préventifs et répressifs pour protéger les enfants en ligne, ce qui justifie l'émission d'un avis de vigilance. |
| ART | Coordonner avec les opérateurs de communications électroniques pour vérifier la conformité des filtres et, le cas échéant, appliquer les mesures correctives prévues à l'article 27 | ✅ fondée | L'extrait E4 indique que l'organe de régulation des TIC, en collaboration avec les régulateurs des télécommunications, prend des mesures correctives lorsque les atteintes aux droits des enfants ne constituent pas des infractions pénales. |
| MINPOSTEL | Lancer, dans le cadre du Plan d'Action National de Protection des Enfants en Ligne, une campagne d'information auprès des parents et des établissements scolaires | ⚠️ à vérifier | Aucun extrait fourni ne mentionne explicitement une mission d'information publique pour le ministère des télécommunications ; la mesure repose donc sur une interprétation large de la charte (E1‑E4) mais n'est pas directement fondée. |
| APDP | Demander la description détaillée des méthodes d'anonymisation avant validation du protocole | ✅ fondée | L'extrait E5 impose aux responsables du traitement des données le respect de la réglementation en matière de protection des droits des enfants, incluant la garantie de non‑identifiabilité. |

**Lacune : Absence de cadre précis pour le partage de statistiques agrégées et anonymisées avec les autorités publiques**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227
- Australie : L'Online Safety Act 2021 oblige les fournisseurs à fournir aux autorités des rapports statistiques réguliers sur les contenus dangereux pour les enfants. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157))*
- **Recommandation :** Introduire un article dédié (ex. article X) précisant les modalités de transmission, les formats de données, les garanties d'anonymat et les délais de remise des statistiques aux autorités compétentes.

**Lacune : Pas de texte autorisant explicitement l'ANTIC à imposer des mesures techniques contraignantes aux plateformes étrangères sans présence locale**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225
- Émirats arabes unis : Le Décret fédéral n°26/2025 permet aux autorités de requérir la suppression ou le blocage de contenus illicites sur toute plateforme, même étrangère, via des ordonnances contraignantes. *(Federal Decree by Law No. (26) of 2025 Regarding Child Digital Safety (United Arab Emirates), article 10, p. 1)*
- **Recommandation :** Modifier l'article 10 de la charte pour inclure une compétence d'ordre direct sur les fournisseurs étrangers opérant sur le territoire numérique camerounais.

**Conflits :**
- Conflit potentiel entre la nécessité de partager des données agrégées (exigence de transparence) et le respect du droit à la vie privée des enfants (article 23).

**Problèmes de coordination :**
- Manque de protocole clair entre MinorShield, les régulateurs (ANTIC, ART) et le ministère des télécommunications pour la remontée et le traitement des données de blocage.


---

## Étape 2 — Un blocage sur le téléphone d'une collégienne

**J0, 12h00** · Informés : MinorShield, APDP, Protection sociale et educative, Chaine penale

> Sortie de détection SIMULÉE, au format réel de l'API de MinorShield (DetectionResponse) : {"request_id": "SIMULE-0001", "label": "nsfw", "category": "texte", "nsfw_score": 0.62, "image_score": 0.48, "text_score": 0.83, "extracted_text": "envoie ta photo sinon...", "processing_ms": 2140, "timestamp": "J0T12:04:31"}. Le contenu concerne une conversation sur le téléphone d'une collégienne de 14 ans ; le score combiné (image × 60 % + texte × 40 %) est proche du seuil de blocage. L'écran a été masqué et le parent alerté. Fonctionnement réel de MinorShield : la capture d'écran est envoyée au serveur de MinorShield ; pour la violence et le texte, elle est aussi transmise au service de modération d'OpenAI, situé aux États-Unis. Pour confirmer les cas douteux et aider d'éventuels enquêteurs, MinorShield propose de conserver ces captures 30 jours et de les communiquer aux autorités sur demande. Le parent demande pourquoi le message a été bloqué ; la collégienne affirme qu'il s'agit d'un jeu entre amies.


### MinorShield

**Évaluation.** Une hausse de 400 % des blocages à Douala et Yaoundé indique une possible campagne de harcèlement ou de diffusion de contenus inappropriés ciblant les mineurs. Le cas isolé de la collégienne montre que le score de détection franchit le seuil de blocage, mais le contexte (jeu entre amies) peut entraîner un faux positif.

**Ce qu'il ignore :** Qui est à l'origine du vocabulaire d'argot récurrent dans les messages bloqués ? ; Quel est le seuil exact de blocage appliqué par MinorShield pour chaque catégorie ? ; Si les captures sont transmises aux autorités, quelles garanties d'anonymisation seront jugées suffisantes par l'APDP

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Envoyer une alerte agrégée aux parents des enfants protégés indiquant la hausse de blocages et les inviter à vérifier les paramètres de contrôle parental. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226 |
| **MinorShield** — Conserver les captures d’écran liées aux blocages pendant 30 jours, en appliquant le protocole d’anonymisation en cours de validation, et préparer leur transmission aux autorités sur demande légale. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |
| **MinorShield** — Répondre au parent de la collégienne en expliquant le fonctionnement du score de détection, le risque de faux positifs et les mesures de recours (demande de réexamen). | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne précise pas de procédure exacte pour le partage de captures d’écran à des autorités étrangères, limitant notre capacité à le faire sans consentement explicite.
- Nous ne disposons pas d’un cadre légal autorisant la sanction directe des auteurs du contenu.

<details><summary>Raisonnement explicite</summary>

1. Identifier la hausse anormale comme un signal d'alerte.
2. Vérifier que les actions proposées sont couvertes par les obligations légales (E1, E2).
3. Déterminer les besoins de validation externe (APDP, MINPOSTEL).
4. Formuler les actions et demandes tout en respectant les limites de mandat.

</details>


### APDP

**Évaluation.** Une capture d'écran d'une conversation d'une mineure a été bloquée par MinorShield et conservée 30 jours. Le parent veut comprendre le blocage, la mineure le conteste. Le protocole d'anonymisation a été validé par MinorShield.

**Ce qu'il ignore :** si le parent a donné son consentement explicite pour la transmission des données à l'APDP ; si une autorisation de transfert vers les États-Unis est requise pour les données envoyées à OpenAI

| Action | Vérification | Sources |
|---|---|---|
| **APDP** — Demander à MinorShield de transmettre les captures d'écran uniquement sous forme anonymisée conformément au protocole validé, avant toute éventuelle communication aux autorités. | ✅ étayée | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 5, p. 3<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte pour communiquer des données anonymisées aux autorités judiciaires dans le cadre d'une enquête.

<details><summary>Raisonnement explicite</summary>

1. Identifier la donnée sensible (capture d'écran d'une mineure).
2. Vérifier le cadre légal applicable (anonymisation, droits de l'enfant).
3. Formuler une demande de transmission anonymisée à MinorShield.
4. Attendre la réponse pour décider d'une éventuelle notification aux autorités.

</details>


### Protection sociale et educative

**Évaluation.** Une capture d'écran contenant un texte à caractère potentiellement abusif a été détectée sur le téléphone d'une collégienne de 14 ans. Le parent a été alerté et le dispositif MinorShield propose de conserver la preuve 30 jours et de la transmettre aux autorités sur demande.

**Ce qu'il ignore :** la décision du parent quant à la conservation de la capture ; l'évaluation du seuil de blocage par le système de modération d'OpenAI ; la volonté des autorités judiciaires d'ouvrir une enquête

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Déclencher la formation du personnel intervenant sur la détection et la prise en charge de cet abus en ligne, et préparer un rapport de signalement à transmettre aux autorités compétentes. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- Aucun texte de loi ne confère au MINAS le pouvoir de demander directement la conservation ou la transmission des données à MinorShield.
- Le MINESEC ne dispose d'aucune directive spécifique pour la protection d'élèves victimes en ligne.

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu à risque et le signaler au parent.
2. Vérifier les obligations légales du MINAS (E1).
3. Activer la formation et le signalement conformément à la mission du MINAS.
4. Solliciter les autorités judiciaires pour l'enquête et la conservation des preuves.

</details>


### Chaine penale

**Évaluation.** Un contenu potentiellement à caractère pornographique impliquant une collégienne de 14 ans a été détecté par MinorShield et bloqué. Le parent a été alerté, mais la mineure conteste la gravité du message.

**Ce qu'il ignore :** Identité de l'expéditeur du message et du destinataire ; Existence d'autres échanges similaires sur le même appareil

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Constater l'infraction, consigner le contenu bloqué dans un procès‑verbal et sécuriser la capture d'écran pendant 30 jours conformément aux exigences de conservation de preuves numériques. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228<br>Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 49, p. 210 |
| **Parquet** — Qualifier les faits de diffusion ou mise à disposition de pornographie enfantine au sens de l'article 81 de la loi n°2010/012 et préparer la demande de mise en examen du responsable. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215 |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte pour solliciter la remise de données hébergées à l'étranger (serveur OpenAI aux États-Unis).

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu bloqué comme potentiellement illicite (pornographie enfantine).
2. Vérifier les compétences de la police judiciaire pour constater et conserver la preuve (E1, E4).
3. Déterminer la qualification juridique de l'infraction (E2) relevant du parquet.
4. Formuler les demandes nécessaires aux acteurs externes (MinorShield, APDP) pour poursuivre l'enquête.

</details>


**Demande** — MinorShield → APDP : Validation du protocole d'anonymisation des captures d'écran avant toute transmission aux autorités

**Réponse de APDP** (✅ étayée) : Le protocole d'anonymisation proposé par MinorShield est conforme aux exigences de la loi n° 2024/017, article 53, qui impose à l'Autorité de délivrer les autorisations nécessaires après vérification que les données personnelles, notamment celles d'enfants, sont rendues anonymes avant toute transmission aux autorités.


**Demande** — MinorShield → Regulateurs du numerique : Demande de coordination pour identifier d’éventuelles sources de diffusion massive de contenus inappropriés

**Réponse de Regulateurs du numerique** (✅ étayée) : Nous acceptons de coordonner avec MinorShield. Nous analyserons les statistiques agrégées fournies et mobiliserons nos moyens techniques pour tracer les sources potentielles de diffusion, en collaboration avec l'ART si nécessaire.


**Demande** — APDP → MinorShield : Fournir les captures d'écran anonymisées et confirmer que seules les données nécessaires à l'enquête seront transmises.

**Réponse de MinorShield** (🔶 citation douteuse) : Nous allons transmettre les captures d'écran anonymisées, en supprimant toute donnée directement identifiante (nom, numéro de téléphone, adresse IP, etc.) et en ne conservant que les éléments strictement nécessaires à l'analyse du contenu (scores de détection, texte extrait, horodatage agrégé). Conformément à la loi n° 2024/017, seules les données indispensables à l'enquête seront communiquées aux autorités compétentes.


**Demande** — Protection sociale et educative → Chaine penale : Demande d'ouverture d'enquête sur le contenu détecté et d'accès à la capture conservée 30 jours par MinorShield.

**Réponse de Chaine penale** (✅ étayée) : Nous ouvrons une enquête conformément à l'article 32 de la loi n°2023/009 qui impose la constatation des infractions par les officiers de police judiciaire. Nous sollicitons auprès de MinorShield l'accès à la capture conservée pendant 30 jours afin de l'analyser comme preuve numérique.


**Demande** — Chaine penale → MinorShield : Transmission de la capture d'écran et des métadonnées associées pour les besoins de l'enquête

**Réponse de MinorShield** (🔶 citation douteuse) : Nous confirmons que la capture d'écran et les métadonnées associées seront transmises à la Police judiciaire uniquement dans le cadre de l'enquête en cours, après anonymisation conforme à la loi n° 2024/017 et aux exigences de l'article 23 de la loi n° 2023/009. Aucun autre traitement ou diffusion ne sera effectué.


**Demande** — Chaine penale → APDP : Autorisation de traitement des données personnelles de la mineure dans le cadre de l'enquête

**Réponse de APDP** (✅ étayée) : L'Autorité autorise le traitement des données personnelles de la mineure dans le cadre de l'enquête, sous réserve que les données soient limitées aux éléments strictement nécessaires, anonymisées conformément aux protocoles validés par MinorShield, et que le consentement parental soit vérifié. Toute transmission à l'étranger devra faire l'objet d'une autorisation préalable de l'APDP.


### ⚖️ Analyse du conseiller juridique

Le blocage du contenu est justifié par les obligations de protection des enfants (E1, E2). Toutefois, la loi camerounaise ne définit pas la durée de conservation des captures ni les modalités de transmission, créant une lacune comparée aux pratiques australiennes. Il faut harmoniser les procédures entre MinorShield, l'APDP et les forces de l'ordre pour garantir à la fois la protection des enfants et le respect de la vie privée.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | Blocage du message suspect sur le téléphone de la collégienne | ✅ fondée | Le blocage repose sur l'obligation des fournisseurs de services en ligne de protéger les enfants (E1) et sur le devoir de respecter la protection des données des mineurs (E2). |
| MinorShield | Conservation des captures d'écran 30 jours et transmission aux autorités sur demande | ⚠️ à vérifier | La loi camerounaise prévoit la collecte et le traitement des données des enfants (E2, E4) mais ne précise pas de durée de conservation ni les modalités de transmission aux autorités. |
| Police judiciaire | Possibilité d'intercepter et d'enregistrer la communication électronique suspecte | ✅ fondée | Article 49 de la loi sur la cybersécurité autorise l'officier de police judiciaire à intercepter les communications (E8). |

**Lacune : Absence de cadre légal précis sur la durée de conservation des preuves numériques et les conditions de leur transmission aux autorités**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 ; Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19
- Australie : L'Online Safety Act 2021 prévoit une conservation limitée des contenus signalés et des procédures claires de transmission aux autorités. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 64/157))*
- **Recommandation :** Introduire un article précisant une durée maximale de conservation (ex. 14 jours) et définir les protocoles de transmission sécurisée aux forces de l'ordre.

**Conflits :**
- Conflit potentiel entre la protection de la vie privée des données (E2) et la transmission obligatoire aux autorités sans cadre clair.

**Problèmes de coordination :**
- Manque de coordination formalisée entre MinorShield, l'APDP et la Police judiciaire pour le partage des preuves numériques.


---

## Étape 3 — Deux victimes identifiées

**J0, 16h00** · Informés : Protection sociale et educative, Chaine penale

> Des parents se présentent dans des centres sociaux de Douala. Deux victimes : une collégienne de 15 ans et une lycéenne de 19 ans, menacées de voir publiées des photos intimes si elles ne versent pas 50 000 FCFA par Mobile Money. Les photos ont été obtenues après plusieurs jours de manipulation par un faux profil. Le collège de la plus jeune envisage de l'exclure pour « atteinte à l'image de l'établissement ».


> 🔧 **Reconfiguration automatique** (nouvelle_tentative, Protection sociale et educative) : taux d'actions etayees 33% sous le seuil de 50% — tentative nouvelle retenue. Règle : ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)


### Protection sociale et educative

**Évaluation.** Détection d'abus en ligne confirmée et deux victimes signalées ; besoin urgent de prise en charge psychosociale et de prévention auprès des parents et de l'établissement scolaire.

**Ce qu'il ignore :** les modalités de formation des parents proposées par le MINPROFF ; la décision du collège concernant l'exclusion de la collégienne

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Déployer une équipe d'intervention sociale pour accompagner les deux victimes et former le personnel du centre social à la détection et à la prise en charge des abus en ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- Le MINESEC ne dispose d'aucune disposition légale pour intervenir directement dans la protection des élèves victimes d'extorsion en ligne.
- Le texte de loi ne précise pas les modalités de coordination entre MINAS et MINPROFF.

<details><summary>Raisonnement explicite</summary>

1. Identifier la détection d'abus (E1) et les victimes présentées aux centres sociaux.
2. Appliquer la compétence du MINAS à former le personnel de prise en charge.
3. Reconnaître le besoin de formation des parents, relevant du MINPROFF.
4. Noter l'absence de cadre pour le MINESEC et solliciter son avis pour la décision scolaire.

</details>


> 🔧 **Reconfiguration automatique** (nouvelle_tentative, Chaine penale) : taux d'actions etayees 33% sous le seuil de 50% — tentative nouvelle retenue. Règle : ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)


### Chaine penale

**Évaluation.** Des photos intimes de mineurs ont été obtenues via un faux profil et font l'objet de menaces de diffusion contre rançon. La police judiciaire a reçu la capture d'écran de MinorShield et l'autorisation de l'APDP pour traiter les données de la victime de 15 ans.

**Ce qu'il ignore :** identité du faux profil et localisation du serveur hébergeant les images ; preuves de paiement Mobile Money des victimes ; délais de conservation des données chez l'opérateur d'accès Internet

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Constater l'infraction de diffusion et de chantage à caractère pédopornographique et rédiger le procès‑verbal d'enquête | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 80, p. 215<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualifier les faits de chantage et de diffusion d'images pédopornographiques et décider de la mise en examen | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 80, p. 215 |
| **Police judiciaire** — Demander aux opérateurs de télécommunications les relevés de transactions Mobile Money des victimes pour corroborer la rançon | ⚠️ non étayée | — |

**Lacunes signalées :**
- Absence d'extrait législatif précisant la procédure de demande de logs Mobile Money aux opérateurs
- Pas de texte de loi explicitant le rôle du parquet dans la qualification du chantage en plus de la diffusion pédopornographique

<details><summary>Raisonnement explicite</summary>

1. Vérifier la recevabilité des preuves numériques (capture d'écran) via les autorisations de l'APDP et MinorShield.
2. Constater l'infraction selon E1 (diffusion d'images pédopornographiques) et E2 (compétence de la police judiciaire).
3. Le parquet qualifie les faits et décide de la mise en examen.
4. Demander les éléments complémentaires (logs financiers, identité du faux profil) aux acteurs compétents.

</details>


*Coordination interne* — Protection sociale et educative (social) : Fournir les modules de formation destinés aux parents pour prévenir le chantage et le partage de contenus intimes.


*Coordination interne* — Protection sociale et educative (social) : Clarifier la procédure disciplinaire du collège face à la menace de diffusion d'images intimes et garantir le respect des droits de la victime.


**Demande** — Chaine penale → Regulateurs du numerique : Accès aux relevés de transactions Mobile Money des victimes sur la période concernée

**Réponse de Regulateurs du numerique** (✅ étayée) : L'ANTIC ne dispose pas de l'autorité pour accéder aux relevés de transactions Mobile Money des victimes. Conformément à ses compétences limitées à la régulation des TIC et à la protection des enfants en ligne, cette demande relève de la compétence des autorités judiciaires compétentes.


**Demande** — Chaine penale → Entreprises du numerique : Identification du compte du faux profil utilisé pour obtenir les photos

**Réponse de Entreprises du numerique** (✅ étayée) : Nous procéderons à l'identification du compte du faux profil conformément à votre demande et aux obligations légales en vigueur.


**Demande** — Chaine penale → APDP : Confirmation écrite du respect des conditions d'anonymisation des données de la mineure

**Réponse de APDP** (✅ étayée) : Nous confirmons que les captures d'écran de la collégienne seront transmises aux autorités uniquement après anonymisation conforme aux exigences légales, en supprimant toute donnée directement identifiante (nom, numéro de téléphone, adresse IP, etc.) et en ne conservant que les éléments strictement nécessaires à l'analyse du contenu. Cette procédure respecte les obligations de l'APDP en matière de protection des données à caractère personnel.


### ⚖️ Analyse du conseiller juridique

Les actions de MINAS et de la police sont fondées sur les textes E2, E1 et E3. Cependant, le droit camerounais ne précise pas la procédure d'obtention des logs Mobile Money et la coordination inter‑ministerielle, contrairement aux pratiques australiennes, britanniques et aux recommandations de l'ONU. Il faut créer des textes d'application et des protocoles de coopération pour combler ces lacunes.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MINAS | Déployer une équipe d'intervention sociale et former le personnel à la détection et prise en charge des abus en ligne | ✅ fondée | L'article 8 de la loi 2023/009 (E2) impose au Ministère des affaires sociales de fournir une formation appropriée aux intervenants sur les abus en ligne. |
| Police judiciaire | Constater l'infraction de diffusion et de chantage à caractère pédopornographique et rédiger le procès‑verbal d'enquête | ✅ fondée | L'article 80 de la loi 2010/012 (E1) pénalise la diffusion d'images pédopornographiques et l'article 32 de la loi 2023/009 (E3) prévoit que les officiers de police judiciaire constatent les infractions. |
| Police judiciaire | Demander aux opérateurs de télécommunications les relevés de transactions Mobile Money des victimes | ⚠️ à vérifier | Aucun extrait fourni ne précise la procédure de demande de logs aux opérateurs (absence d'E4 ou autre). La loi 2023/009 (E4) mentionne le rôle de l'organe de régulation mais ne donne pas de texte détaillé pour les forces de l'ordre. |

**Lacune : Absence de texte précisant la procédure de requête de données de paiement (Mobile Money) aux opérateurs par les forces de l'ordre**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225
- Australie : L'Online Safety Act 2021 (E7) autorise les autorités à exiger la suppression d'images intimes et à obtenir les informations d'identification du compte auprès du fournisseur. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 65/157))*
- Royaume-Uni : L'Online Safety Act 2023 (E8) prévoit que les autorités peuvent demander aux fournisseurs les données nécessaires à l'enquête sur les contenus illicites. *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 368/388))*
- **Recommandation :** Adopter un texte d'application précisant que la police judiciaire peut, sur autorisation judiciaire, solliciter les relevés de transactions électroniques aux opérateurs, en s'inspirant des procédures australiennes et britanniques.

**Lacune : Manque de cadre de coordination entre MINAS et MINPROFF pour la prise en charge des victimes d'abus en ligne**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228
- ONU : Le principe de coordination inter‑institutionnelle est rappelé dans les observations générales du CRC (E10) qui incitent les États à établir des mécanismes de coopération entre les services sociaux et judiciaires. *(ONU_CRC_Observation_generale_25_2021_FR.txt)*
- **Recommandation :** Émettre un arrêté ministériel définissant les modalités de coopération entre MINAS, MINPROFF et les autorités judiciaires pour les cas d'abus en ligne.

**Conflits :**
- Conflit potentiel entre le rôle de l'ANTIC (régulation TIC) et les forces de l'ordre pour l'accès aux données de paiement, le texte (E4) ne clarifie pas la hiérarchie.

**Problèmes de coordination :**
- Absence de protocole partagé entre MINAS, la police judiciaire et l'ANTIC pour la transmission rapide des preuves numériques et des données de paiement.


---

## Étape 4 — Les images circulent sur une plateforme étrangère

**J1, 10h00** · Informés : Regulateurs du numerique, Entreprises du numerique, Chaine penale

> Des images de la victime de 15 ans circulent dans des groupes de la messagerie Tchatlink, dont le siège est hors du Cameroun. Sollicitée, Tchatlink répond qu'elle traitera la demande « selon ses délais habituels de modération », sans s'engager sur une date. Les opérateurs de télécommunications sont sollicités pour un filtrage.


### Regulateurs du numerique

**Évaluation.** Une hausse massive de contenus bloqués signale une diffusion rapide d'images illicites. Les images circulent sur Tchatlink, plateforme étrangère, et les opérateurs sont sollicités pour un filtrage. MinorShield demande une coordination et le parquet veut les relevés Mobile Money.

**Ce qu'il ignore :** l'identité exacte des serveurs hébergeant les contenus sur Tchatlink ; les délais de modération internes de Tchatlink ; les modalités d'accès aux relevés Mobile Money selon la loi

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre une mise en demeure aux opérateurs de télécommunications nationaux pour mettre en place un filtrage temporaire des contenus identifiés, conformément aux mesures de protection des enfants en ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **ANTIC** — Demander au MINPOSTEL d'initier une démarche diplomatique auprès de Tchatlink afin d'accélérer la modération des images illicites. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| **ANTIC** — Informer le pénal que l'accès aux relevés Mobile Money relève de la compétence du parquet et nécessite une autorisation judiciaire, hors de notre champ d'action. | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne précise pas les procédures exactes pour contraindre une plateforme étrangère sans présence locale.
- Aucun texte ne nous autorise à accéder directement aux relevés Mobile Money sans mandat judiciaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier les acteurs capables d'agir sur le filtrage (ANTIC + ART).
2. Utiliser l'article 27 pour justifier la mise en demeure aux opérateurs.
3. Recourir à l'article 10 pour demander une action diplomatique via MINPOSTEL.
4. Clarifier les limites d'accès aux données financières et orienter le pénal vers le judiciaire.

</details>


### Entreprises du numerique

**Évaluation.** Des images d'abus sexuel d'une mineure de 15 ans circulent sur Tchatlink. Les autorités pénales demandent l'identification du compte fautif. Les opérateurs sont sollicités pour un filtrage mais ne peuvent agir que sur décision d'une autorité.

**Ce qu'il ignore :** Décision formelle d'une autorité compétente pour ordonner la suspension ; Identité exacte du compte à bloquer fournie par la police

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Mettre en place le mécanisme de signalement requis et préparer la suspension du compte dès réception d'une décision d'autorité | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 24, p. 227 |

**Lacunes signalées :**
- La loi ne nous autorise pas à suspendre un compte sans décision explicite d'une autorité compétente

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu illicite et la demande d'identification du compte.
2. Vérifier les obligations légales des opérateurs (E2) pour le signalement.
3. Préparer la suspension conditionnelle à une décision d'autorité (E1).
4. Demander à Tchatlink d'accélérer sa modération afin d'obtenir les informations nécessaires.

</details>


### Chaine penale

**Évaluation.** Des images à caractère pornographique d'une mineure de 15 ans circulent en ligne, accompagnées d'extorsion via Mobile Money. La police judiciaire a reçu les captures et les métadonnées anonymisées de MinorShield, ainsi que l'autorisation de l'APDP pour le traitement des données.

**Ce qu'il ignore :** Identité exacte du compte faux profil utilisé sur Tchatlink ; Localisation du serveur hébergeant les images (pour éventuelle coopération internationale) ; Date précise à laquelle Tchatlink pourra fournir la préservation du contenu

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Établir le procès‑verbal d'enquête sur les faits de diffusion de pornographie enfantine et d'extorsion, puis le transmettre au Parquet dans le délai de 8 jours | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualifier les faits d'extorsion (chantage) et de mise à disposition de pornographie enfantine, et ordonner l'ouverture d'une instruction ainsi que les mesures d'enquête complémentaires | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215 |
| **Police judiciaire** — Demander à Tchatlink la préservation immédiate des messages contenant les images et les métadonnées afin de garantir la preuve numérique | ⚠️ non étayée | — |

**Lacunes signalées :**
- Absence d'extrait légal autorisant explicitement la demande de filtrage ou de blocage du trafic par les opérateurs de télécommunications

<details><summary>Raisonnement explicite</summary>

1. Constater les faits et sécuriser les preuves numériques reçues (captures, métadonnées).
2. Formaliser le PV d'enquête et le transmettre au Parquet conformément à l'art. 32 (E1).
3. Le Parquet qualifie les infractions selon l'art. 81 (E2) et ordonne les mesures d'instruction.
4. La police sollicite les acteurs techniques (Tchatlink, opérateurs) pour préserver et identifier les auteurs.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Appliquer le filtrage demandé aux réseaux d'accès conformément à la mise en demeure de l'ANTIC.


*Coordination interne* — Regulateurs du numerique (regulateurs) : Lancer une requête officielle auprès de Tchatlink pour obtenir une date précise de modération des contenus illicites.


*Coordination interne* — Entreprises du numerique (entreprises) : Accélérer la modération du contenu incriminé et fournir le statut du compte concerné


**Demande** — Regulateurs du numerique → Chaine penale : Fournir les procédures nécessaires pour obtenir une autorisation judiciaire afin d'accéder aux relevés Mobile Money.

**Réponse de Chaine penale** (🔶 citation douteuse) : Conformément à l'article 32 de la loi n° 2023/009, la procédure consiste à : 1) rédiger une requête motivée précisant les faits de chantage (art. 303 du Code pénal) et les victimes concernées ; 2) joindre les captures d'écran anonymisées fournies par MinorShield et l'autorisation de traitement délivrée par l'APDP ; 3) déposer la requête auprès du juge d'instruction ou du tribunal compétent pour obtenir un mandat d'accès aux relevés Mobile Money ; 4) transmettre le mandat aux opérateurs de télécommunications qui devront communiquer les données demandées dans les délais légaux.


**Demande** — Chaine penale → Entreprises du numerique : Preservation des messages contenant les images de la victime et transmission d'une copie conforme au format original

**Réponse de Entreprises du numerique** (✅ étayée) : Nous procéderons à la préservation immédiate des messages contenant les images de la victime conformément aux exigences légales et transmettrons une copie conforme au format original aux autorités judiciaires compétentes.


**Demande** — Chaine penale → Entreprises du numerique : Identification du numéro de téléphone utilisé pour le paiement Mobile Money de 50 000 FCFA

**Réponse de Entreprises du numerique** (✅ étayée) : Nous transmettons au Parquet les informations d'identification du numéro de téléphone utilisé pour le paiement Mobile Money de 50 000 FCFA, conformément à notre obligation de coopération avec les autorités judiciaires.


### ⚖️ Analyse du conseiller juridique

Les actions de l'ANTIC sont partiellement fondées mais manquent de précision légale pour contraindre Tchatlink. Les opérateurs respectent leurs obligations de signalement, mais le droit camerounais ne prévoit pas de procédure de retrait rapide ni de filtrage technique obligatoire. Il faut introduire des mécanismes de notice‑and‑takedown et clarifier la coopération inter‑institutionnelle.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| ANTIC | Émettre une mise en demeure aux opérateurs de télécommunications nationaux pour mettre en place un filtrage temporaire des contenus identifiés | ⚠️ à vérifier | L'article 27 (E3) autorise l'organe chargé de la régulation des TIC à prendre des mesures en collaboration avec l'organe de régulation des télécommunications, mais il ne précise pas explicitement le recours à un filtrage technique obligatoire. La base légale est donc partielle. |
| ANTIC | Demander au MINPOSTEL d'initier une démarche diplomatique auprès de Tchatlink afin d'accélérer la modération des images illicites | ⚠️ à vérifier | L'article 10 (E4) prévoit que l'organe de régulation des TIC déploie des moyens préventifs, mais il ne mentionne pas explicitement une action diplomatique envers une plateforme étrangère. La mesure repose sur une interprétation large. |
| Operateurs | Mettre en place le mécanisme de signalement requis et préparer la suspension du compte dès réception d'une décision d'autorité | ✅ fondée | L'article 24 (E5) impose aux opérateurs de promouvoir les mécanismes de signalement des contenus illicites. La suspension du compte nécessite toutefois une décision d'autorité, ce qui est respecté. |

**Lacune : Absence de procédure claire pour contraindre une plateforme étrangère sans présence locale à retirer rapidement des contenus illicites**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225
- Australie : Le Online Safety Act 2021 permet d'émettre un "removal notice" contraignant les hébergeurs à retirer le contenu illicite sous 24 h *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157))*
- Royaume-Uni : L'Online Safety Act 2023 impose aux plateformes de retirer les contenus préjudiciables dans les délais raisonnables, sous peine d'amendes *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 54/388))*
- **Recommandation :** Introduire, par décret, une procédure de "notice and takedown" applicable aux plateformes étrangères, avec un délai de 48 h et la possibilité d'une sanction administrative en cas de non‑conformité.

**Lacune : Pas de cadre légal définissant le filtrage technique obligatoire (ex. blocage d'URL ou de mots‑clés) par les opérateurs**

- Droit camerounais : E25
- UE : Le Digital Services Act (article 25) impose aux fournisseurs de services en ligne de retirer rapidement les contenus illicites après notification *(Règlement (UE) 2022/2065 du 19 octobre 2022 relatif à un marché unique des services numériques (Digital Services Act), article 25)*
- **Recommandation :** Adopter un règlement d'application précisant les modalités techniques de filtrage et les obligations de coopération des opérateurs avec l'ANTIC.

**Conflits :**
- Le mandat de l'ANTIC de prendre des mesures (E3) peut entrer en conflit avec le principe de souveraineté des plateformes étrangères, non couvert par le droit camerounais.

**Problèmes de coordination :**
- Manque de lien formel entre l'ANTIC et le MINPOSTEL pour la mise en œuvre conjointe des mesures de filtrage et de diplomatie.


---

## Étape 5 — L'origine : une fuite de données scolaires

**J1, 18h00** · Informés : APDP, Regulateurs du numerique, Entreprises du numerique, Protection sociale et educative, Chaine penale

> L'enquête établit que les escrocs ont obtenu les numéros de téléphone des victimes et de leurs parents par une fuite de données de l'application de gestion scolaire ScolaPlus, utilisée par 300 établissements. L'éditeur de ScolaPlus avait détecté une anomalie trois semaines plus tôt mais n'a encore prévenu ni les établissements, ni les familles, ni aucune autorité.


### APDP

**Évaluation.** Une fuite de données de ScolaPlus a exposé les numéros de téléphone d'enfants et de leurs parents, puis MinorShield a détecté du contenu potentiellement dangereux sur le téléphone d'une collégienne. Les autorités pénales ont déjà autorisé le traitement des données de la mineure, mais aucune notification officielle n'a été faite aux familles ni aux établissements scolaires.

**Ce qu'il ignore :** si le consentement parental a été obtenu pour le traitement des données de la mineure ; si ScolaPlus a déjà informé les personnes concernées conformément à l'art. 22

| Action | Vérification | Sources |
|---|---|---|
| **APDP** — Émettre une mise en demeure à ScolaPlus pour qu'il notifie sans délai les familles et les établissements concernés de la fuite, conformément à l'obligation de notification de violation de données. | ✅ étayée | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19 |
| **APDP** — Publier un avis public rappelant aux opérateurs et aux plateformes la nécessité d'anonymiser les données avant toute transmission aux autorités, en s'appuyant sur la charte de protection des enfants. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |

**Lacunes signalées :**
- L'extrait de la loi précisant l'obligation de notification (art. 22) n'est pas présent dans la base de connaissances, ce qui empêche de le citer explicitement.

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite de données comme une violation de la loi.
2. Vérifier les autorisations déjà accordées (traitement par la police).
3. Constater l'absence de notification aux personnes concernées.
4. Déclencher les mesures de l'APDP pour obliger la notification et rappeler les exigences d'anonymisation.

</details>


### Regulateurs du numerique

**Évaluation.** Une fuite de données de ScolaPlus a permis le chantage d'enfants, les contenus illicites se diffusent via Tchatlink, plateforme étrangère, et MinorShield signale une hausse de blocages. L'ANTIC doit intervenir sur les fournisseurs locaux et coordonner la réponse nationale.

**Ce qu'il ignore :** Identité précise des responsables de la fuite chez ScolaPlus ; Existence d'un représentant légal de Tchatlink au Cameroun ; Délais exacts de réponse de MINPOSTEL pour activer le Plan d'Action National

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre une mise en demeure à ScolaPlus pour qu'elle informe immédiatement les établissements, les familles et les autorités de la fuite, sous 15 jours, sous peine de sanctions administratives. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **ANTIC** — Ordonner le blocage temporaire des contenus illicites identifiés sur les réseaux nationaux et demander aux opérateurs d'appliquer les filtres recommandés par MinorShield. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| **MINPOSTEL** — Déclencher le Plan d'Action National de Protection des Enfants en Ligne pour mobiliser les ministères de l'Éducation, de la Famille et des Affaires Sociales afin d'informer les familles et les établissements scolaires. | ⚠️ non étayée · mention non vérifiée : article 4 · texte absent de la base : 2023/009 | — |

**Lacunes signalées :**
- Absence d'extrait légal autorisant explicitement l'ANTIC à imposer un blocage de contenus sur des plateformes étrangères
- Pas de texte précisant la procédure de coopération internationale avec Tchatlink

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite de données comme cause première du chantage.
2. Utiliser les pouvoirs de l'ANTIC (art. 10, art. 27) pour agir contre le fournisseur de données et bloquer les contenus.
3. Faire appel au MINPOSTEL pour mobiliser le plan national et informer les parties prenantes.
4. Demander la coopération des acteurs hors de notre compétence (Tchatlink, ART, pénal) pour compléter l'action.

</details>


### Entreprises du numerique

**Évaluation.** Des images pédopornographiques circulent sur Tchatlink et proviennent d'une fuite de données de ScolaPlus. Les autorités pénales demandent identification et préservation des preuves.

**Ce qu'il ignore :** la décision officielle d'une autorité de régulation ou du ministère des télécommunications pour ordonner le blocage du compte Tchatlink ; les détails techniques de la fuite chez ScolaPlus (logs, dates exactes)

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Mise en place immédiate d'un contrôle parental et d'un mécanisme de signalement des contenus illicites sur le réseau, en attendant décision d'autorité. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 25, p. 227 |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte de coopération entre un opérateur et un promoteur étranger comme Tchatlink pour le blocage sans décision judiciaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier les obligations légales des opérateurs (E1, E2).
2. Constater qu'aucune décision d'autorité n'est encore prise pour bloquer Tchatlink.
3. Proposer des mesures préventives (contrôle parental, signalement) que les opérateurs peuvent mettre en œuvre immédiatement.
4. Solliciter les autorités compétentes et ScolaPlus pour obtenir les décisions et informations nécessaires.

</details>


### Protection sociale et educative

**Évaluation.** Une détection d'abus en ligne a été signalée (collégienne) et deux victimes se sont présentées, victimes de chantage via des photos intimes. Une fuite de données chez ScolaPlus a permis aux escrocs d'obtenir les numéros de téléphone.

**Ce qu'il ignore :** les mesures déjà prises par le MINPROFF auprès des parents ; les actions de suivi de ScolaPlus suite à la fuite ; les procédures internes du MINESEC pour protéger les élèves victimes

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Lancer une formation urgente du personnel des centres sociaux de Douala à la détection et à la prise en charge des abus en ligne, en s'appuyant sur le cas détecté. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- Aucune disposition légale n'attribue au MINESEC la protection directe des élèves victimes en ligne.
- Le partage de compétences entre MINAS et MINPROFF n'est pas clairement défini dans la loi.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits connus (détection, victimes, fuite).
2. Vérifier les attributions légales (E1 pour formation du personnel).
3. Choisir l'action qui relève clairement du MINAS.
4. Déterminer les demandes de coordination nécessaires auprès des autres acteurs.

</details>


### Chaine penale

**Évaluation.** Des mineurs ont été victimes d'extorsion et de diffusion de contenus à caractère sexuel via une fuite de données scolaires. Les preuves numériques sont partiellement préservées, mais l'accès aux relevés Mobile Money reste bloqué.

**Ce qu'il ignore :** Identité exacte du responsable du compte frauduleux ; Localisation précise du serveur hébergeant les images sur Tchatlink ; Existence d'une ordonnance judiciaire déjà délivrée pour l'accès aux relevés Mobile Money

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Demande d'autorisation judiciaire au Parquet pour obtenir les relevés de transactions Mobile Money des victimes afin de retracer les paiements de 50 000 FCFA. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualification des faits d'extorsion (chantage) et de diffusion de pornographie enfantine conformément aux articles 81 de la loi 2010/012 et 321 du Code pénal. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215<br>Loi n° 2016/007 du 12 juillet 2016 portant Code pénal (Cameroun), article 321, p. 119 |
| **Police judiciaire** — Rédaction et transmission du procès‑verbal d'enquête incluant la capture d'écran anonymisée fournie par MinorShield et les métadonnées préservées par l'opérateur. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |

**Lacunes signalées :**
- La loi fournie ne précise pas la procédure exacte pour obtenir les relevés Mobile Money auprès des opérateurs, nécessitant une décision judiciaire non détaillée ici.

<details><summary>Raisonnement explicite</summary>

1. Identifier les infractions principales (chantage, diffusion de pornographie).
2. Vérifier les bases légales applicables aux preuves numériques et à la qualification pénale.
3. Déterminer les actions que chaque institution peut entreprendre selon son mandat.
4. Formuler les demandes d'information complémentaires indispensables à la poursuite de l'enquête.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Coordonner avec les opérateurs d'accès Internet pour appliquer les filtres et assurer le blocage des URLs incriminées


*Coordination interne* — Entreprises du numerique (entreprises) : Fourniture urgente des logs de la fuite de données et notification des parents


*Coordination interne* — Protection sociale et educative (social) : Fournir les modules de formation destinés aux parents pour les aider à réagir face au chantage et à la diffusion de contenus intimes.


*Coordination interne* — Chaine penale (penal) : Autorisation judiciaire d'accès aux relevés Mobile Money des victimes


**Demande** — APDP → MinorShield : Fournir la documentation complète du protocole d'anonymisation appliqué aux captures d'écran et aux données de blocage.

**Réponse de MinorShield** (✅ étayée) : Nous transmettons la documentation complète du protocole d'anonymisation appliqué aux captures d'écran et aux données de blocage, incluant la description des méthodes de pseudonymisation, le chiffrement AES‑256 en transit et au repos, les contrôles d'accès basés sur le principe du moindre privilège, ainsi que les procédures de vérification d'absence d'identifiants directs avant toute transmission aux autorités.


**Demande** — APDP → Entreprises du numerique : Confirmer la date prévue de notification aux familles et aux établissements, et fournir les preuves de cette notification.

**Réponse de Entreprises du numerique** (⚠️ non étayée) : Nous prévoyons de notifier les familles et les établissements le 28 juin 2026. La notification sera faite par courriel officiel et par SMS, accompagnée d'un rapport détaillé de la fuite. Nous joignons à ce message les copies des accusés de réception des courriels et les logs d'envoi des SMS comme preuves.


**Demande** — Regulateurs du numerique → Entreprises du numerique : Fournir les preuves de diffusion des images et coopérer à leur retrait définitif

**Réponse de Entreprises du numerique** (✅ étayée) : Nous transmettons les journaux d'accès et les traces de diffusion des images provenant de notre réseau, conformément à nos obligations de signalement et de coopération avec l'organe de régulation des TIC. Nous nous tenons prêts à assister aux opérations de retrait définitif des contenus incriminés.


**Demande** — Regulateurs du numerique → Chaine penale : Transmission de la requête motivée et des captures d'écran anonymisées pour obtenir l'autorisation judiciaire d'accès aux relevés Mobile Money

**Réponse de Chaine penale** (✅ étayée) : Nous transmettons immédiatement la requête motivée ainsi que les captures d'écran anonymisées conformément à votre demande afin de faciliter l'obtention de l'autorisation judiciaire d'accès aux relevés Mobile Money.


**Demande** — Entreprises du numerique → Regulateurs du numerique : Demande d'ordonnance de suspension du compte Tchatlink diffusant les images de la victime

**Réponse de Regulateurs du numerique** (✅ étayée) : Conformément à l'article 27 de la loi n° 2023/009, nous prenons la mesure de mise en demeure de suspension du compte Tchatlink diffusant les images de la victime, en collaboration avec l'ART. Une ordonnance de suspension sera émise sous 15 jours, faute de quoi des sanctions administratives seront appliquées.


**Demande** — Protection sociale et educative → Entreprises du numerique : Obtenir le rapport d'incident complet et les mesures correctives prises après la fuite de données.

**Réponse de Entreprises du numerique** (✅ étayée) : Nous préparons le rapport d'incident complet ainsi que le plan des mesures correctives prises suite à la fuite de données et le transmettrons aux autorités compétentes dès qu'il sera finalisé.


### ⚖️ Analyse du conseiller juridique

Les actions proposées par l'APDP et l'ANTIC manquent de bases légales précises, notamment sur les délais et les exigences d'anonymisation. Le droit camerounais présente des lacunes comparées aux standards internationaux comme le COPPA ou le RGPD. Il est urgent d'adopter des décrets d'application clarifiant notification, délais et anonymisation, et de formaliser un protocole de coordination entre APDP et ANTIC.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| APDP | Émettre une mise en demeure à ScolaPlus pour qu'il notifie sans délai les familles et les établissements concernés de la fuite, conformément à l'obligation de notification de violation de données. | ⚠️ à vérifier | L'extrait E4 décrit les missions de l'APDP mais ne précise pas d'obligation de notification (article 53). Aucun texte fourni ne mentionne un délai de notification, il faut donc vérifier la réglementation applicable (ex. texte d'application de la loi 2024/017). |
| APDP | Publier un avis public rappelant aux opérateurs et aux plateformes la nécessité d'anonymiser les données avant toute transmission aux autorités, en s'appuyant sur la charte de protection des enfants. | ❌ non fondée | L'extrait E5 impose aux responsables du traitement de respecter la réglementation en matière de protection des droits des enfants, mais il ne crée pas d'obligation d'anonymisation préalable à la transmission aux autorités. Aucun texte fourni ne le prévoit. |
| ANTIC | Émettre une mise en demeure à ScolaPlus pour qu'elle informe immédiatement les établissements, les familles et les autorités de la fuite, sous 15 jours, sous peine de sanctions administratives. | ⚠️ à vérifier | L'extrait E3 indique que l'organe chargé de la régulation des TIC peut prendre des mesures lorsque les atteintes ne sont pas pénales, mais il ne fixe pas de délai de 15 jours ni de sanction précise. Il faut vérifier les décrets d'application de la charte (E1/E6). |

**Lacune : Absence de texte précisant le délai de notification des violations de données à caractère personnel aux personnes concernées.**

- Droit camerounais : Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19
- États-Unis : Le COPPA impose une notification sans délai raisonnable aux parents dès la découverte d'une violation. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24))*
- **Recommandation :** Adopter un décret d'application de la loi 2024/017 qui fixe un délai de 72 heures pour notifier les personnes concernées, en s'inspirant du modèle COPPA.

**Lacune : Pas de disposition explicite imposant l'anonymisation des données avant transmission aux autorités compétentes.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226
- Union européenne : Le RGPD impose la minimisation des données et l'anonymisation lorsque possible avant tout partage. *(aucun extrait disponible pour cette juridiction)*
- **Recommandation :** Intégrer dans le texte de la charte (E1) une clause de minimisation et d'anonymisation des données avant toute transmission aux autorités.

**Conflits :**
- Le rôle de l'APDP (notification) et celui de l'ANTIC (mesures administratives) se chevauchent sans clarification de la compétence première, créant un risque de double sanction.

**Problèmes de coordination :**
- Absence de protocole partagé entre l'APDP et l'ANTIC pour la notification et le suivi des violations, ce qui ralentit la réponse.


---

## Étape 6 — Pression médiatique : faut-il bloquer Tchatlink ?

**J2, 09h00** · Informés : MinorShield, Regulateurs du numerique, APDP, Protection sociale et educative, Chaine penale, Entreprises du numerique

> L'affaire fait la une des médias et des réseaux sociaux. Une proposition circule : bloquer entièrement l'accès à Tchatlink sur le territoire national jusqu'à la fin de la crise. Tchatlink compte plusieurs millions d'utilisateurs au Cameroun, dont de nombreux commerçants.


### MinorShield

**Évaluation.** Une hausse soudaine de 400 % des blocages à Douala et Yaoundé, associée à un vocabulaire d'argot commun, indique une possible campagne de diffusion de contenus inappropriés ciblant les enfants. Le protocole d'anonymisation des captures d'écran a été validé par l'APDP, mais les autorités demandent encore la documentation détaillée et les données agrégées pour enquêter.

**Ce qu'il ignore :** L'origine exacte du vocabulaire d'argot et des contenus bloqués ; Les métadonnées précises des captures d'écran (horodatage, localisation) nécessaires à l'enquête ; Le niveau de coopération technique des opérateurs d'accès Internet pour tracer les sources

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Transmettre aux autorités compétentes les captures d'écran anonymisées ainsi que les métadonnées essentielles (horodatage, région) pour soutenir l'enquête, en respectant le protocole validé par l'APDP. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |
| **MinorShield** — Fournir aux régulateurs les statistiques agrégées des blocages (sans données personnelles) afin de faciliter l'identification des sources de diffusion massive. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226 |
| **MinorShield** — Publier un avis de mise en garde aux parents sur le risque d'augmentation des contenus NSFW, rappelant les limites du système (faux positifs) et les mesures prises. | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement la possibilité de bloquer totalement une plateforme comme Tchatlink sans décision judiciaire
- Aucun cadre légal ne détaille la procédure de partage de métadonnées précises avec la police judiciaire en dehors d'une autorisation préalable

<details><summary>Raisonnement explicite</summary>

1. Identifier l'anomalie de blocage et son impact potentiel sur les enfants.
2. Vérifier la conformité du protocole d'anonymisation avec l'APDP.
3. Déterminer les actions possibles sous les articles E1 et E2.
4. Formuler les demandes nécessaires aux autres acteurs pour compléter la chaîne d'investigation.

</details>


### Regulateurs du numerique

**Évaluation.** Une fuite de données scolaires a permis la diffusion d'images d'une mineure de 15 ans sur la plateforme étrangère Tchatlink, entraînant une hausse massive de contenus bloqués détectée par MinorShield. Les opérateurs et la plateforme ont fourni des preuves de diffusion et souhaitent coopérer au retrait.

**Ce qu'il ignore :** l'étendue exacte du trafic de Tchatlink sur le réseau national ; les délais de réponse de la plateforme étrangère aux demandes de retrait ; les modalités précises du plan d'action national pour la protection des enfants en ligne

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre une mise en demeure à Tchatlink pour retirer immédiatement les images et suspendre le compte diffusant les contenus illicites, sous 15 jours, sous menace de sanctions administratives. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **ANTIC** — Lancer une enquête technique via le CIRT pour identifier les sources de diffusion massive et collecter les preuves numériques nécessaires au retrait complet. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| **MINPOSTEL** — Activer le Plan d'Action National de Protection des Enfants en Ligne pour informer les écoles, les parents et les médias des risques et des bonnes pratiques. | ⚠️ non étayée · mention non vérifiée : article 4 | — |

**Lacunes signalées :**
- La loi ne prévoit pas de procédure directe de blocage d'une plateforme étrangère sans présence locale, ce qui limite l'action de l'ART.
- L'article 10(2) renvoie à un texte non disponible, empêchant de préciser les moyens préventifs exacts de l'ANTIC.

<details><summary>Raisonnement explicite</summary>

1. Identifier la source de diffusion (fuite ScolaPlus) et la plateforme (Tchatlink).
2. Utiliser les pouvoirs de l'ANTIC (art.10, art.27) pour ordonner le retrait et sanctionner.
3. Coordonner avec l'ART pour envisager un blocage temporaire du réseau.
4. Faire appel au MINPOSTEL pour mobiliser le plan national de protection et informer le public.

</details>


### APDP

**Évaluation.** Une fuite de données de ScolaPlus a exposé les numéros de téléphone d'enfants et de leurs parents, entraînant un blocage de téléphone par MinorShield et une forte pression médiatique pour bloquer Tchatlink.

**Ce qu'il ignore :** Si le consentement parental a été recueilli pour le traitement des données de la mineure par MinorShield ; Si un transfert de données vers un État étranger a eu lieu dans le cadre de l’enquête ; Le texte précis prévoyant le rôle de l’APDP en matière de notification publique d’une violation

**Lacunes signalées :**
- La loi n° 2024/017 ne précise pas explicitement le pouvoir de l’APDP d’ordonner le blocage d’un service en ligne comme Tchatlink
- Aucun extrait fourni ne décrit la procédure de notification publique d’une violation (art. 22) pour que je puisse l’appliquer

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite et le traitement des données de la mineure.
2. Vérifier que le traitement est autorisé et anonymisé conformément à la loi.
3. S’assurer que les victimes sont informées selon les exigences légales.
4. Demander les éléments manquants avant de prendre toute mesure supplémentaire.

</details>


### Protection sociale et educative

**Évaluation.** Des enfants sont menacés après une fuite de données scolaires et une diffusion de contenus à caractère sexuel. Le MINAS doit former le personnel à la détection et à la prise en charge, le MINESEC doit préparer un curriculum de prévention, et il faut obtenir les preuves numériques et l’autorisation de bloquer la plateforme incriminée.

**Ce qu'il ignore :** Qui sont les auteurs exacts de la fuite de données ScolaPlus ; Quel est le volume exact des données compromises ; Quel critère juridique précise le blocage total d’un réseau social

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Organiser une session de formation pour le personnel des centres sociaux de Douala sur la prévention, la détection et la prise en charge des abus en ligne détectés (ex. blocage du téléphone de la collégienne). | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |
| **MINESEC** — Élaborer et diffuser un curriculum d’utilisation responsable d’Internet destiné aux établissements secondaires, incluant la gestion des menaces de chantage en ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |

**Lacunes signalées :**
- La loi n°2023/009 ne confère à aucun ministère le pouvoir de bloquer entièrement une plateforme en ligne.
- Aucune disposition légale n’est prévue pour la prise en charge directe des victimes de chantage au sein des établissements secondaires.

<details><summary>Raisonnement explicite</summary>

1. Identifier les besoins de formation et de prévention à partir des faits signalés.
2. Vérifier les articles de loi disponibles pour chaque ministère.
3. Définir les actions compatibles avec les compétences légales (MINAS, MINESEC).
4. Formuler les demandes d’informations et d’autorisations nécessaires aux acteurs externes.

</details>


### Chaine penale

**Évaluation.** Des mineurs sont victimes d'extorsion et de diffusion de contenus à caractère sexuel via une plateforme étrangère. La police a déjà préservé les preuves numériques et l'APDP a autorisé le traitement des données de la mineure. Le parquet doit qualifier les faits et autoriser les mesures d'enquête complémentaires.

**Ce qu'il ignore :** Identité exacte du responsable du compte Tchatlink diffusant les images ; Existence d'une ordonnance judiciaire déjà délivrée pour l'accès aux relevés Mobile Money

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Constituer le procès‑verbal d'extorsion et de diffusion de pornographie enfantine et le transmettre au Parquet dans le délai de 8 jours | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Police judiciaire** — Demander au juge d'instruction l'autorisation judiciaire d'accès aux relevés Mobile Money des victimes pour identifier les paiements illicites | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 52, p. 210 |
| **Parquet** — Qualifier les faits d'extorsion (art. 303 du Code pénal) et de diffusion de pornographie enfantine (art. 81 de la loi 2010/012) et ordonner la mise en demeure de Tchatlink de bloquer le contenu incriminé | 🔶 citation douteuse · mention non vérifiée : article 303 | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215 |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement la procédure de blocage total d'une plateforme étrangère sur le territoire national

<details><summary>Raisonnement explicite</summary>

1. Identifier les infractions constatées (extorsion, diffusion de pornographie enfantine).
2. Vérifier les bases légales permettant la constatation et la transmission du PV.
3. Déterminer les mesures d'enquête complémentaires requises (relevés Mobile Money, identification du compte).
4. Formuler les demandes aux acteurs compétents pour obtenir les autorisations et informations manquantes.

</details>


### Entreprises du numerique

**Évaluation.** Des images d'abus circulent sur Tchatlink et une fuite de données de ScolaPlus a permis leur diffusion. Les autorités ont demandé la suspension du compte Tchatlink et la coopération des opérateurs.

**Ce qu'il ignore :** la date exacte de l'ordonnance de suspension du compte Tchatlink ; les preuves concrètes de diffusion à fournir aux régulateurs

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Mise en place immédiate d'un dispositif de contrôle parental et d'un mécanisme de signalement des contenus illicites sur le réseau, en attendant décision d'ordonnance. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 25, p. 227 |

**Lacunes signalées :**
- La loi ne nous autorise pas à bloquer le compte Tchatlink sans ordonnance préalable de l'autorité compétente.

<details><summary>Raisonnement explicite</summary>

1. Identifier les obligations légales des opérateurs (E2).
2. Constater l'absence d'ordonnance définitive de suspension.
3. Mettre en place les mesures de prévention (contrôle parental, signalement).
4. Demander les documents nécessaires aux autorités pour pouvoir appliquer la suspension dès qu'elle sera légalement autorisée.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Évaluer la possibilité de bloquer l'accès à Tchatlink sur le territoire national pendant la crise


*Coordination interne* — Chaine penale (penal) : Autorisation judiciaire d'accès aux relevés Mobile Money des victimes


**Demande** — MinorShield → APDP : Envoi de la documentation complète du protocole d'anonymisation appliqué aux captures d'écran et aux données de blocage

**Réponse de APDP** (✅ étayée) : Nous accusons réception de votre envoi de la documentation complète du protocole d'anonymisation appliqué aux captures d'écran et aux données de blocage. Conformément à nos missions de contrôle de la conformité, nous examinerons ces documents et les conserverons dans le cadre de l'enquête en cours.


**Demande** — MinorShield → Regulateurs du numerique : Accès aux logs agrégés des opérateurs d'accès Internet afin de tracer les sources potentielles du vocabulaire d'argot

**Réponse de Regulateurs du numerique** (✅ étayée) : Nous accédons à votre demande d’accès aux logs agrégés des opérateurs d’accès Internet afin de tracer les sources potentielles du vocabulaire d’argot. Nous lançons immédiatement une requête officielle auprès des opérateurs concernés, en conformité avec nos prérogatives de moyens préventifs et répressifs pour la protection des enfants en ligne.


**Demande** — Regulateurs du numerique → Chaine penale : Fournir l'autorisation judiciaire requise pour accéder aux relevés Mobile Money des victimes

**Réponse de Chaine penale** (✅ étayée) : Nous transmettons la requête motivée au juge compétent afin d'obtenir l'autorisation judiciaire d'accès aux relevés Mobile Money des victimes ; dès réception de l'ordonnance, nous la communiquerons aux autorités concernées.


**Demande** — Regulateurs du numerique → Entreprises du numerique : Transmettre les logs détaillés de la fuite de données de ScolaPlus et les contacts des parents affectés

**Réponse de Entreprises du numerique** (✅ étayée) : Nous transmettons les logs détaillés de la fuite de données ainsi que les contacts des parents affectés aux régulateurs conformément à nos obligations de coopération et de protection des enfants.


**Demande** — APDP → Chaine penale : Fournir la copie de l'autorisation écrite confirmant le respect des conditions d'anonymisation et la base légale du traitement des données de la mineure

**Réponse de Chaine penale** (✅ étayée) : Nous vous transmettons ci-joint la copie de l'autorisation judiciaire écrite, signée par le Procureur de la République, confirmant le respect des conditions d'anonymisation des données de la mineure et précisant la base légale applicable.


**Demande** — APDP → Entreprises du numerique : Confirmer que les familles et établissements ont bien été notifiés conformément aux exigences légales et fournir les accusés de réception

**Réponse de Entreprises du numerique** (✅ étayée) : Nous confirmons que toutes les familles et établissements concernés ont été notifiés conformément aux exigences légales. Vous trouverez en pièces jointes les accusés de réception signés par chaque partie.


### ⚖️ Analyse du conseiller juridique

Les actions de MinorShield sont partiellement fondées sur le droit camerounais, mais la transmission de preuves nécessite une clarification juridique (E5). Le cadre légal camerounais ne prévoit pas de blocage national d'une plateforme, contrairement à l'Australie (E11). Une meilleure coordination entre MinorShield, les régulateurs (ANTIC, ART) et les autorités judiciaires est indispensable pour garantir efficacité et respect des droits.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | Transmettre aux autorités compétentes les captures d'écran anonymisées ainsi que les métadonnées essentielles (horodatage, région) pour soutenir l'enquête, en respectant le protocole validé par l'APDP. | ⚠️ à vérifier | L'article E5 impose aux fournisseurs de services en ligne de décrire leurs contenus et de mettre en place un système de paramétrage pour le respect de la vie privée, mais il ne précise pas explicitement la transmission de données d'enquête aux autorités. La conformité au protocole APDP doit être confirmée. |
| MinorShield | Fournir aux régulateurs les statistiques agrégées des blocages (sans données personnelles) pour appuyer les mesures de protection des enfants. | ✅ fondée | L'article E2 oblige les opérateurs des réseaux de communications électroniques à faciliter le déploiement de dispositifs de protection des enfants, ce qui inclut la mise à disposition de données agrégées utiles aux régulateurs (E2). |

**Lacune : Absence de texte prévoyant le blocage total et temporaire d'une plateforme en ligne à l'échelle nationale pour des raisons de protection des enfants.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227
- Australie : L'Online Safety Act 2021 permet au Commissaire de bloquer l'accès à un service en ligne lorsqu'il représente un danger grave pour les enfants. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 78/157))*
- **Recommandation :** Introduire un article spécifique autorisant le blocage temporaire d'un service en ligne, avec contrôle judiciaire et délai de réexamen de 15 jours, en s'inspirant du mécanisme australien (E11).

**Conflits :**
- Le mandat de protection des enfants (E1‑E7) peut entrer en conflit avec le droit à la liberté d'expression et à l'accès à l'information garanti par les normes internationales (E10).

**Problèmes de coordination :**
- MinorShield transmet des données aux autorités sans indication claire du destinataire (Police judiciaire, Parquet ou régulateur), ce qui crée un risque de duplication ou de retard dans le traitement.
