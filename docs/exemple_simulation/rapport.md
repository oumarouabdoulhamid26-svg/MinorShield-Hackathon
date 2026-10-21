# Rapport de simulation — Opération Miroir

*Mode : reference (grand modele) · 2026-10-17T20:19:20+00:00*

## Bilan

| Indicateur | Valeur |
|---|---|
| Interventions d'agents | 56 |
| Actions étayées par un extrait | 109 |
| Actions non étayées | 12 |
| Citations invalides | 1 |
| Taux d'actions étayées | 88% |
| Jetons consommés | 159930 |


---

## Étape 1 — Une hausse anormale de contenus bloqués

**J0, 08h00** · Informés : MinorShield, ANTIC

> Le système MinorShield constate depuis 48 heures une hausse de 400 % des contenus bloqués sur les appareils d'enfants protégés à Douala et à Yaoundé. Les messages interceptés partagent le même vocabulaire d'argot local et des formules du type « envoie ta photo sinon… ». Il est encore impossible de dire s'il s'agit d'une campagne organisée ou d'une coïncidence. MinorShield ne détient que des données agrégées et anonymisées.


### MinorShield

**Évaluation.** MinorShield observe une hausse de 400 % des contenus bloqués sur les appareils d'enfants protégés à Douala et Yaoundé depuis 48 heures. Les contenus détectés contiennent un vocabulaire d'argot local et des menaces du type « envoie ta photo sinon… », ce qui correspond à des contenus potentiellement inappropriés au sens de l'article 3 de la loi (E1). Aucun message individuel n'est disponible, seules des statistiques agrégées sont détenues.

**Ce qu'il ignore :** L'origine exacte de cette hausse (campagne organisée ou phénomène isolé) ; L'identité ou le profil des auteurs des messages ; Le type précis de contenu (ex. extorsion, harcèlement, diffusion d'images) ; L'existence éventuelle de signalements déjà effectués par les opérateurs ou les fournisseurs de services

| Action | Vérification | Sources |
|---|---|---|
| Continuer la collecte et l'analyse agrégée des données de blocage, en renforçant les filtres sur les expressions identifiées, et préparer un rapport synthétique à destination de l'organe de régulation des TIC. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 3, p. 224<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |

**Lacunes signalées :**
- La loi ne précise pas les procédures techniques exactes que MinorShield doit suivre pour partager ses données agrégées avec les autorités, ni les seuils de déclenchement d'une alerte officielle.

<details><summary>Raisonnement explicite</summary>

1. Identifier la hausse de blocages comme potentiellement liée à des contenus inappropriés (E1).
2. Vérifier que la loi prévoit que l'organe de régulation des TIC peut intervenir (E4).
3. Décider de poursuivre la surveillance et de préparer un rapport, action permise par E1.
4. Solliciter l'ANTIC pour coordination et les opérateurs pour activation de leurs mécanismes de signalement (E2, E4).
5. Noter les limites légales (absence de procédure détaillée) dans les lacunes.

</details>


### ANTIC

**Évaluation.** Une hausse anormale de contenus bloqués (400%) a été détectée par MinorShield sur les appareils d'enfants à Douala et Yaoundé, avec des messages de chantage. Aucun signalement individuel n'est encore reçu. La situation indique un risque potentiel d'atteinte à la dignité et à l'intégrité des enfants en ligne.

**Ce qu'il ignore :** L'identité précise des auteurs des messages ; Les plateformes ou services où les messages circulent ; Les preuves numériques détaillées permettant d'identifier les comptes concernés

| Action | Vérification | Sources |
|---|---|---|
| Déployer des moyens préventifs en informant les fournisseurs d'accès à Internet de la nécessité de renforcer les guides de bonnes pratiques et les mécanismes de signalement auprès des utilisateurs, conformément à l'article 10. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |

**Lacunes signalées :**
- L'article 10 (2) renvoie à un texte particulier non disponible, limitant la précision de nos actions préventives.
- Aucun cadre légal explicite ne prévoit la mise en demeure directe des fournisseurs d'accès en l'absence de preuve d'infraction pénale.

<details><summary>Raisonnement explicite</summary>

1. Identifier le phénomène anormal via les données de MinorShield.
2. Vérifier les bases légales applicables (E1, E3, E4).
3. Décider de déployer des mesures préventives (E1) et de solliciter la coopération des opérateurs et plateformes (E3).
4. Formuler des demandes aux acteurs concernés pour obtenir les informations nécessaires à une enquête plus approfondie.
5. Noter les limites légales et les inconnues qui devront être comblées avant d'envisager des mesures répressives.

</details>


**Demande** — MinorShield → ANTIC : Demande de coordination pour analyser la tendance anormale et activer les mesures de prévention prévues par l'article 27 (E4).

**Réponse de ANTIC** (✅ étayée) : Nous prenons acte de la hausse anormale de contenus bloqués signalée par MinorShield. Conformément à l'article 10 qui confère à l'ANTIC le pouvoir de déployer des moyens préventifs pour la protection des enfants en ligne, nous allons initier une coordination avec les parties concernées (ART, MINPOSTEL, MINAS, etc.) afin d’analyser la tendance et d’activer les mesures de prévention prévues à l'article 27. Nous vous tiendrons informés des actions entreprises et des résultats de l’analyse dans les meilleurs délais.


**Demande** — MinorShield → Operateurs de telecommunications et fournisseurs d'acces a Internet : Invitation à activer leurs mécanismes de signalement (article 24, E2) concernant les contenus suspectés d'extorsion ou de harcèlement afin d'obtenir des informations complémentaires.

**Réponse de Operateurs de telecommunications et fournisseurs d'acces a Internet** (✅ étayée) : Nous activons immédiatement les mécanismes de signalement demandés par MinorShield afin de recueillir les informations complémentaires sur les contenus suspectés d'extorsion ou de harcèlement, conformément aux obligations qui nous incombent en tant qu'opérateur d'accès à Internet.


**Demande** — ANTIC → Operateurs de telecommunications et fournisseurs d'acces a Internet : Faciliter la collecte de données techniques (logs, adresses IP, horodatage) relatives aux messages de chantage détectés, afin de permettre une investigation numérique conforme à l'article 25.

**Réponse de Operateurs de telecommunications et fournisseurs d'acces a Internet** (⚠️ non étayée) : Nous confirmons notre capacité à faciliter la collecte des données techniques (logs, adresses IP, horodatage) relatives aux messages de chantage détectés, conformément aux exigences de l'ANTIC.


**Demande** — ANTIC → Tchatlink : Mettre à disposition tout contenu signalé ou suspect lié aux messages de chantage, et activer les mécanismes de signalement prévus par l'article 20.

**Réponse de Tchatlink** (✅ étayée) : Nous confirmons la mise à disposition des contenus signalés ou suspects relatifs aux messages de chantage ainsi que l’activation des mécanismes de signalement prévus par l’article 20. Conformément à l’article 20, nous publierons des guides de bonnes pratiques et activerons les outils de signalement afin de protéger la dignité et l’intégrité des enfants.


### ⚖️ Analyse du conseiller juridique

La hausse des contenus bloqués déclenche des actions majoritairement fondées sur les articles 10, 20 et 27 de la loi camerounaise, mais plusieurs lacunes techniques et procédurales subsistent, notamment le partage de données agrégées et la définition précise du rôle de l'ANTIC. Les pratiques australiennes et britanniques offrent des modèles de notification et de seuils d'alerte qui pourraient être adaptés. Une meilleure coordination institutionnelle et un texte d'application détaillé sont nécessaires pour combler ces vides.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | Continuer la collecte et l'analyse agrégée des données de blocage, renforcer les filtres sur les expressions identifiées, préparer un rapport synthétique à destination de l'organe de régulation des TIC. | ⚠️ à vérifier | E4 définit les notions de contenu inapproprié et de contrôle parental, mais ne prévoit pas explicitement le cadre technique de collecte et de transmission de données agrégées par un tiers comme MinorShield. E1 indique que l'organe de régulation peut prendre des mesures, mais ne précise pas les modalités de partage de données agrégées. La base légale est donc partielle. |
| ANTIC | Déployer des moyens préventifs en informant les fournisseurs d'accès à Internet de la nécessité de renforcer les guides de bonnes pratiques et les mécanismes de signalement auprès des utilisateurs. | ✅ fondée | E2 article 10 (1) confère à l'ANTIC le pouvoir de déployer des moyens préventifs pour la protection des enfants en ligne, ce qui justifie l'information et la sensibilisation des fournisseurs d'accès. |
| ANTIC | Initiation d'une coordination avec les parties concernées (ART, MINPOST) suite à la hausse anormale de contenus bloqués. | ✅ fondée | E1 article 27 prévoit que l'organe chargé de la régulation des TIC agit en collaboration avec les organes de régulation des télécommunications et des médias. La coordination annoncée est donc fondée. |
| Operateurs de telecommunications et fournisseurs d'acces a Internet | Activation des mécanismes de signalement demandés par MinorShield afin de recueillir les informations complémentaires sur les contenus suspectés d'extorsion ou de harcèlement. | ✅ fondée | E3 article 20 (2) impose aux fournisseurs d'accès d'instaurer des mécanismes de signalement des contenus ou comportements portant atteinte à la dignité et à l'intégrité des enfants. L'action est donc conforme. |
| Operateurs de telecommunications et fournisseurs d'acces a Internet | Faciliter la collecte des données techniques (logs, adresses IP, horodatage) relatives aux messages de chantage détectés, conformément aux exigences de l'ANTIC. | ❌ non fondée | Aucun extrait fourni (E1‑E5) n'impose explicitement aux opérateurs de transmettre des logs ou des données techniques à l'ANTIC. L'obligation n'est donc pas clairement prévue par le droit camerounais. |
| Tchatlink | Mise à disposition des contenus signalés ou suspects et activation des mécanismes de signalement prévus par l’article 20. | ✅ fondée | E3 article 20 (1‑2) oblige les fournisseurs d’accès à mettre à disposition des guides et des mécanismes de signalement. La réponse de Tchatlink s’appuie correctement sur cet article. |

**Lacune : Absence de procédure détaillée pour le partage de données agrégées entre MinorShield et l'ANTIC, ainsi que l'absence de seuils quantitatifs déclenchant une alerte officielle.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 3, p. 224
- Australie : L'Online Safety Act 2021 impose aux fournisseurs de services Internet de fournir rapidement des informations techniques (logs, IP) aux autorités dès réception d'un avis de retrait ou d'une demande d'enquête. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157))*
- Royaume-Uni : L'Online Safety Act 2023 prévoit des obligations de notification et de coopération entre les plateformes et le régulateur dès qu'un risque grave pour les enfants est identifié, avec des seuils de gravité clairement définis. *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 55/388))*
- **Recommandation :** Instaurer, par règlement d'application, un protocole de transmission de données agrégées incluant des seuils d'alerte (ex. hausse > 200% sur 24h) et préciser les formats et délais de remise des informations à l'ANTIC.

**Lacune : Manque de texte détaillé précisant le rôle exact de l'ANTIC en matière de protection des enfants en ligne, comme évoqué dans l'alinéa 2 de l'article 10.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225
- États-Unis : Le COPPA (Children's Online Privacy Protection Rule) définit précisément les obligations des services en ligne envers les enfants, incluant des exigences de transparence, de consentement parental et de sécurité des données. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 7/24))*
- **Recommandation :** Adopter un texte d'application détaillant les missions de l'ANTIC, inspiré des exigences du COPPA, afin de clarifier les prérogatives et les procédures opérationnelles.

**Conflits :**
- Potential overlap between the preventive role of ANTIC (article 10) and the collaborative measures envisagées by the organ of telecom regulation (article 27) sans clarification des responsabilités respectives.

**Problèmes de coordination :**
- Absence d'un cadre formel de coordination entre l'ANTIC, l'ART et les opérateurs, ce qui ralentit la mise en œuvre des mesures de signalement et de collecte de données.


---

## Étape 2 — Deux victimes identifiées

**J0, 16h00** · Informés : MINAS, MINPROFF, Police judiciaire, MINESEC

> Des parents se présentent dans des centres sociaux de Douala. Deux victimes : une collégienne de 15 ans et une lycéenne de 19 ans, menacées de voir publiées des photos intimes si elles ne versent pas 50 000 FCFA par Mobile Money. Les photos ont été obtenues après plusieurs jours de manipulation par un faux profil. Le collège de la plus jeune envisage de l'exclure pour « atteinte à l'image de l'établissement ».


### MINAS

**Évaluation.** Deux mineures victimes d'extorsion et de menaces de diffusion d'images intimes se sont présentées dans les centres sociaux de Douala. Elles sont en situation de vulnérabilité et nécessitent une prise en charge psychosociale immédiate ainsi qu'une protection juridique contre les auteurs du délit de diffusion d'images pédopornographiques.

**Ce qu'il ignore :** Identité et localisation exacte des auteurs du faux profil ; Le support technique utilisé pour la diffusion (plateforme, opérateur) ; Le statut juridique du collège concernant la décision d'exclusion

| Action | Vérification | Sources |
|---|---|---|
| Déclencher le dispositif d'accueil et d'accompagnement psychosocial des deux victimes au sein des centres sociaux, en assurant leur confidentialité et en les orientant vers une prise en charge médicale et psychologique. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 38, p. 229 |
| Notifier immédiatement les autorités judiciaires de la situation afin d'initier les poursuites contre les auteurs du délit d'extorsion et de menace de diffusion d'images intimes. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 38, p. 229 |

**Lacunes signalées :**
- La loi n'établit pas de procédure détaillée pour la prise en charge sociale et psychologique des victimes au sein du MINAS.
- Aucun cadre légal n'est fourni pour la coordination directe avec les établissements scolaires concernant les décisions d'exclusion.

<details><summary>Raisonnement explicite</summary>

1. Étape 1 : Identifier la nature du délit (extorsion, menace de diffusion d'images pédopornographiques).
2. Étape 2 : Vérifier les dispositions légales applicables (E1 pour la diffusion d'images, E2 pour la protection de l'identité).
3. Étape 3 : Déterminer les actions relevant du MINAS (prise en charge sociale, signalement aux autorités).
4. Étape 4 : Formuler les demandes aux acteurs compétents (police, MINPROFF).
5. Étape 5 : Identifier les lacunes légales pour anticiper les besoins de coordination supplémentaire.

</details>


### MINPROFF

**Évaluation.** Deux adolescentes sont victimes d'extorsion et de chantage en ligne. Leur situation relève de la protection de l'enfant et de la famille, ainsi que de la prévention de la diffusion d'images illicites. Le ministère doit agir conformément à l'article 7 qui impose l'élaboration de modules de formation des parents à l'usage d'Internet.

**Ce qu'il ignore :** Le nombre exact de parents concernés dans la zone de Douala ; Les ressources pédagogiques déjà existantes au sein du MINPOSTEL ; Le délai souhaité par le collège pour la mise en place d'une réponse éducative

| Action | Vérification | Sources |
|---|---|---|
| Lancer la conception d'un module de formation à la parentalité positive sur l'usage sécurisé d'Internet, en partenariat avec le MINPOSTEL, à destination des parents des victimes et du quartier concerné. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 7, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas de procédure d'intervention immédiate auprès des victimes ni de mesures de protection d'urgence au sein du cadre légal fourni.
- Aucun texte ne précise les modalités de financement ou de diffusion des modules de formation.

<details><summary>Raisonnement explicite</summary>

1. Identifier le crime (extorsion, chantage, menace de diffusion d'images illicites).
2. Vérifier les dispositions légales applicables : E1 (sanction du diffuseur) et E2 (obligation de former les parents).
3. Déterminer les actions relevant de ma mission : élaboration de modules de formation.
4. Préparer les demandes aux acteurs compétents pour la mise en œuvre (MINPOSTEL) et la répression (Police).
5. Noter les limites de la loi (absence de mesures d'urgence) dans les lacunes.

</details>


### Police judiciaire

**Évaluation.** Deux mineures (15 ans et 19 ans) sont victimes d'extorsion par menace de diffusion d'images intimes obtenues via un faux profil. Le délit consiste en l'enregistrement et la diffusion non consentie d'images portant atteinte à l'intégrité corporelle, ainsi qu'en une tentative d'extorsion financière par Mobile Money.

**Ce qu'il ignore :** Identité du ou des auteurs du faux profil et du dispositif de diffusion ; Localisation des serveurs ou comptes utilisés pour le Mobile Money ; Existence éventuelle d'autres victimes ou d'une chaîne de diffusion

| Action | Vérification | Sources |
|---|---|---|
| Constater les infractions d'enregistrement et diffusion non consentie d'images intimes et d'extorsion, rédiger le procès‑verbal et initier l'enquête judiciaire | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 75, p. 214 |
| Presser la conservation des preuves numériques (messages, captures d'écran, traces de Mobile Money) auprès des opérateurs de télécommunications et du fournisseur du service de messagerie | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi citée ne prévoit pas explicitement la procédure de saisie immédiate de données chez les opérateurs ou les plateformes de messagerie ; il faut se référer aux articles de procédure (art. 52 à 59) qui ne sont pas fournis dans les extraits.

<details><summary>Raisonnement explicite</summary>

1. Étape 1 : Identifier les faits pertinents (extorsion, diffusion d'images intimes).
2. Étape 2 : Rechercher les bases légales applicables parmi les extraits fournis.
3. Étape 3 : Constater l'infraction selon l'article 75 (E1) qui sanctionne la diffusion non consentie d'images à but lucratif.
4. Étape 4 : Déterminer les actions possibles (rédaction du PV, demande de conservation de preuves).
5. Étape 5 : Identifier les acteurs dont les données sont nécessaires et formuler les demandes correspondantes.
6. Étape 6 : Noter les lacunes légales pour les mesures de saisie de données numériques.

</details>


### MINESEC

**Évaluation.** Deux mineures sont victimes d'extorsion et de menaces de diffusion de photos intimes. Les parents ont signalé la situation aux centres sociaux de Douala. Le collège envisage une sanction disciplinaire contre la collégienne, alors que la priorité doit être la protection des victimes et la prévention de tels abus en ligne.

**Ce qu'il ignore :** Identité exacte du fraudeur (faux profil) et les moyens techniques utilisés ; Si les photos ont déjà été diffusées ou seulement menacées d'être diffusées ; Le statut juridique du paiement exigé par Mobile Money (exigence de restitution ou blocage) ; Les procédures internes du collège concernant les sanctions disciplinaires liées à l'image de l'établissement

| Action | Vérification | Sources |
|---|---|---|
| Lancer, avec le Ministère des Télécommunications, l'élaboration d'un curriculum de formation à l'utilisation responsable d'Internet et des réseaux sociaux, incluant la prévention du chantage et la protection des enfants en ligne, conformément à l'article 6 de la loi. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |

**Lacunes signalées :**
- Aucune disposition légale n'est fournie concernant la prise en charge immédiate des victimes (soutien psychologique, assistance juridique) dans le cadre de ma mission.
- La loi ne précise pas les procédures disciplinaires internes des établissements scolaires en cas d'atteinte à l'image de l'établissement.

<details><summary>Raisonnement explicite</summary>

1. Étape 1 : Identifier les faits rapportés (chantage, menace de diffusion, implication d'élèves).
2. Étape 2 : Vérifier les bases légales disponibles – seul E1 autorise l'action de mise en place de curricula.
3. Étape 3 : Déterminer les actions possibles dans le cadre de la mission du MINESEC – création de programmes éducatifs.
4. Étape 4 : Identifier les acteurs complémentaires à solliciter (MINPOSTEL pour la partie télécom, Police pour l'enquête pénale).
5. Étape 5 : Noter les lacunes légales (absence de mesures de protection directe des victimes et de procédures disciplinaires).

</details>


**Demande** — MINAS → Police judiciaire : Lancer une enquête urgente pour identifier et appréhender les auteurs du faux profil et du chantage, en se basant sur les preuves fournies par les victimes.

**Réponse de Police judiciaire** (✅ étayée) : Nous lançons immédiatement une enquête conformément à l'article 52 de la loi n° 2010/012, afin d'identifier et d'appréhender les auteurs du faux profil et du chantage, en utilisant les preuves fournies par les victimes.


**Demande** — MINAS → MINPROFF : Intervenir auprès du collège de la collégienne afin d'empêcher toute mesure d'exclusion discriminatoire et de garantir le respect des droits de l'enfant conformément aux principes de protection.

**Réponse de MINPROFF** (✅ étayée) : Nous prenons acte de la demande de MINAS et intervenons immédiatement auprès du collège de la collégienne afin d’empêcher toute mesure d’exclusion discriminatoire. Conformément à notre mandat de protection de la famille et de l’enfant, nous rappelons que le Ministère en charge de la femme et de la famille, en collaboration avec le Ministère des télécommunications, doit veiller à la protection des droits de l’enfant, notamment en évitant toute sanction qui porterait atteinte à son bien‑être et à son droit à l’éducation. Nous solliciterons une réunion avec les responsables du collège, les parents de la victime et les services compétents pour garantir le respect de ces principes et proposer un accompagnement adapté à la situation.


**Demande** — MINPROFF → MINPOSTEL : Coordination pour la création conjointe de modules de formation à la parentalité positive sur l'usage d'Internet, incluant supports pédagogiques, calendrier de diffusion et moyens de suivi.

**Réponse de MINPOSTEL** (✅ étayée) : Nous acceptons de coordonner avec le Ministère de la Femme et de la Famille la création conjointe de modules de formation à la parentalité positive sur l'usage d'Internet, incluant les supports pédagogiques, le calendrier de diffusion et les moyens de suivi, conformément aux dispositions légales qui nous imposent cette collaboration.


**Demande** — MINPROFF → Police judiciaire : Ouverture d'une enquête pour extorsion, chantage et diffusion potentielle d'images pédopornographiques conformément à l'article 38.

**Réponse de Police judiciaire** (✅ étayée) : Nous ouvrons immédiatement une enquête pour extorsion, chantage et diffusion potentielle d'images pédopornographiques conformément à la demande du ministère de la femme et de la famille. Les victimes seront entendues, les preuves numériques seront préservées et les perquisitions nécessaires seront demandées au parquet.


### ⚖️ Analyse du conseiller juridique

Les actions de MINAS manquent de fondement juridique, tandis que MINPROFF s'appuie correctement sur l'article 7 (E1). La police agit conformément aux articles 75 et 52 (E3, E5). Le droit camerounais présente des lacunes majeures en matière de prise en charge psychosociale, de coordination inter‑ministérielle et de financement des programmes éducatifs, contrairement aux pratiques observées en Australie, au Royaume‑Uni et dans l'UE. Des décrets d'application et des protocoles inter‑institutionnels sont nécessaires pour combler ces vides.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MINAS | Déclencher le dispositif d'accueil et d'accompagnement psychosocial des deux victimes au sein des centres sociaux, en assurant leur confidentialité et en les orientant vers une prise en charge médicale et psychologique. | ❌ non fondée | L'extrait E2 sanctionne la diffusion d'images pédophiliennes mais ne prévoit aucune disposition relative à l'accueil ou à l'accompagnement psychosocial des victimes. Aucun texte fourni ne crée un tel dispositif. |
| MINAS | Notifier immédiatement les autorités judiciaires de la situation afin d'initier les poursuites contre les auteurs du délit d'extorsion et de menace de diffusion d'images intimes. | ⚠️ à vérifier | E2 prévoit la peine pour diffusion d'images, mais ne décrit la procédure de notification. L'article 52 de la loi de 2010 (E5) confère aux officiers de police judiciaire le pouvoir d'enquêter, ce qui pourrait justifier la notification, mais le texte exact de la notification n'est pas cité. |
| MINPROFF | Lancer la conception d'un module de formation à la parentalité positive sur l'usage sécurisé d'Internet, en partenariat avec le MINPOSTEL, à destination des parents des victimes et du quartier concerné. | ✅ fondée | L'article 7 de la charte de protection des enfants en ligne (E1) prévoit explicitement que le ministère de la femme et de la famille, en collaboration avec le ministère des télécommunications, élabore des modules de formation à l'usage d'Internet pour les parents. |
| Police judiciaire | Constater les infractions d'enregistrement et diffusion non consentie d'images intimes et d'extorsion, rédiger le procès‑verbal et initier l'enquête judiciaire. | ✅ fondée | L'article 75 de la loi de 2010 sur la cybersécurité (E3) punit l'enregistrement et la diffusion d'images sans consentement, et l'article 52 (E5) habilite les officiers de police judiciaire à mener les enquêtes. Ces deux extraits soutiennent l'action. |

**Lacune : Absence de cadre légal détaillé pour la prise en charge psychosociale et médicale des victimes d'extorsion en ligne.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 38, p. 229
- Australie : L'Online Safety Act 2021 prévoit des mesures de soutien aux victimes, incluant l'accès à des services de conseil et la possibilité de demander des ordonnances de protection. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 65/157))*
- Royaume-Uni : L'Online Safety Act 2023 impose aux plateformes de fournir des outils de signalement et d'assistance aux victimes de contenus préjudiciables. *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 368/388))*
- **Recommandation :** Adopter, par décret, un protocole national d'accompagnement psychosocial des victimes d'abus en ligne, inspiré des dispositions australiennes (E7) et britanniques (E8), incluant la création d'équipes pluridisciplinaires au sein des centres sociaux.

**Lacune : Manque de procédure formalisée de coordination entre les ministères de l'éducation et les établissements scolaires pour la gestion des cas de chantage en ligne.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225
- Union européenne : Le Digital Services Act (E10) impose aux plateformes et aux États membres de mettre en place des mécanismes de coopération avec les autorités éducatives pour la protection des mineurs en ligne. *(Règlement (UE) 2022/2065 du 19 octobre 2022 relatif à un marché unique des services numériques (Digital Services Act))*
- **Recommandation :** Élaborer, sur la base de l'article 6 (E4), un protocole inter‑ministériel précisant les rôles du ministère de l'éducation, du ministère des télécommunications et des établissements scolaires dans la détection, le signalement et la prise de mesures éducatives contre le chantage en ligne.

**Lacune : Aucun texte ne précise les modalités de financement et de diffusion des modules de formation à la parentalité positive.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 7, p. 225
- États‑Unis : Le COPPA (E9) prévoit des exigences de transparence financière pour les services destinés aux enfants, incluant la publication des coûts associés aux programmes éducatifs. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 13/24))*
- **Recommandation :** Inclure, dans le décret d'application de l'article 7 (E1), une clause budgétaire définissant les sources de financement (budget national, partenaires privés, fonds internationaux) et les critères de diffusion des modules.

**Conflits :**
- Le dispositif d'exclusion envisagé par le collège (mesure disciplinaire) peut entrer en conflit avec le principe de protection de l'image de l'établissement prévu par la loi, sans cadre juridique clair pour concilier sanction scolaire et droits de la victime.

**Problèmes de coordination :**
- Absence de protocole de communication entre MINAS, MINPROFF, le MINPOSTEL et les établissements scolaires, ce qui risque de fragmenter la réponse et de retarder les mesures de protection.


---

## Étape 3 — Les images circulent sur une plateforme étrangère

**J1, 10h00** · Informés : MINPOSTEL, ART, Operateurs de telecommunications et fournisseurs d'acces a Internet, Tchatlink, Police judiciaire, Parquet

> Des images de la victime de 15 ans circulent dans des groupes de la messagerie Tchatlink, dont le siège est hors du Cameroun. Sollicitée, Tchatlink répond qu'elle traitera la demande « selon ses délais habituels de modération », sans s'engager sur une date. Les opérateurs de télécommunications sont sollicités pour un filtrage.


### MINPOSTEL

**Évaluation.** Des images d'une victime de 15 ans circulent sur la messagerie Tchatlink, plateforme étrangère. Tchatlink indique un délai de modération non précisé. Les opérateurs de télécommunications sont sollicités pour un filtrage. Le ministère de la Femme et de la Famille (MINPROFF) propose de créer des modules de formation à la parentalité positive sur l'usage d'Internet.

**Ce qu'il ignore :** Délais exacts que Tchatlink peut respecter pour la suppression du contenu ; Capacité technique et juridique des opérateurs à mettre en place un filtrage ciblé en temps réel ; Coordination précise avec les ministères de l'éducation et de la jeunesse pour le volet formation

| Action | Vérification | Sources |
|---|---|---|
| Lancer la mise en œuvre du Plan d'Action National de Protection des Enfants en Ligne en activant le volet de coopération avec les plateformes étrangères pour accélérer la suppression du contenu illicite. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |
| Demander aux opérateurs de télécommunications de préparer un dispositif de filtrage temporaire du contenu signalé, en attendant la suppression par Tchatlink. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |
| Proposer à MINPROFF la co‑construction des modules de formation à la parentalité positive, en les intégrant au Plan d'Action National. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas de pouvoir d'imposer directement à une plateforme étrangère un délai de suppression, ni d'imposer un filtrage obligatoire sans accord préalable des opérateurs.

<details><summary>Raisonnement explicite</summary>

1. Identifier le problème urgent : diffusion d'images d'une mineure sur une plateforme étrangère.
2. Vérifier les bases légales disponibles : E1 autorise le ministère à mettre en œuvre le Plan d'Action National et à coordonner les acteurs.
3. Déterminer les actions possibles dans le cadre de ce mandat : solliciter la plateforme, mobiliser les opérateurs, et collaborer avec MINPROFF et le ministère de l'éducation.
4. Relever les inconnues qui peuvent influencer l'efficacité des actions.
5. Noter les limites légales (lacunes) qui empêchent d'imposer des mesures contraignantes à Tchatlink.

</details>


### ART

**Évaluation.** Des images d'une victime de 15 ans circulent sur la plateforme étrangère Tchatlink. Tchatlink, hors du Cameroun, ne donne pas de délai précis de modération. Les opérateurs de télécommunications ont été sollicités pour mettre en place un filtrage, mais leur rôle est encadré par la loi.

**Ce qu'il ignore :** Si Tchatlink possède une entité ou un serveur au Cameroun permettant d'appliquer une mesure de blocage local ; Le délai exact que Tchatlink respectera pour la suppression des contenus

| Action | Vérification | Sources |
|---|---|---|
| Informer les opérateurs de télécommunications de leur obligation de faciliter le déploiement d'un dispositif de filtrage des contenus illicites conformément à l'article 25 de la loi 2023/009 | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 25, p. 227 |

**Lacunes signalées :**
- L'ART n'a pas d'autorité directe sur une plateforme étrangère sans présence au Cameroun, ce qui limite notre capacité à imposer un blocage ou une suppression directe

<details><summary>Raisonnement explicite</summary>

1. Étape 1 : Identifier la nature du contenu (atteinte à la dignité d'une mineure) et la plateforme concernée (Tchatlink, hors du Cameroun).
2. Étape 2 : Vérifier les obligations légales des opérateurs et de l'organe TIC (ART) via les extraits E1 et E27.
3. Étape 3 : Constater que l'ART ne peut pas agir directement sur Tchatlink, mais peut mobiliser les opérateurs et l'ANTIC.
4. Étape 4 : Formuler une action envers les opérateurs (obligation de filtrage) et une demande de coordination à l'ANTIC.
5. Étape 5 : Signaler les limites de notre mandat (absence d'autorité sur plateforme étrangère).

</details>


### Operateurs de telecommunications et fournisseurs d'acces a Internet

**Évaluation.** Des images d'une victime mineure circulent sur la plateforme étrangère Tchatlink. Les autorités (minorshield et antic) demandent respectivement l'activation de mécanismes de signalement et la collecte de données techniques. En tant qu'opérateur, je dois mettre à disposition des outils de contrôle parental et préparer la collecte de logs si une demande officielle d'autorité compétente m'est adressée.

**Ce qu'il ignore :** La demande officielle d'autorité compétente pour suspendre l'accès ou ordonner le blocage du contenu (article 14 ou 16). ; Les modalités précises de la collecte de données techniques requises par antic (type de logs, durée de conservation).

| Action | Vérification | Sources |
|---|---|---|
| Mettre à disposition des dispositifs de contrôle parental et des moyens techniques de filtrage conformément aux exigences de protection des enfants en ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 21, p. 227 |

**Lacunes signalées :**
- Aucun extrait fourni ne précise la base légale permettant à l'opérateur de collecter les données techniques demandées par antic (article 25 non présent).
- L'opérateur ne peut pas suspendre l'accès sans une demande explicite d'une autorité compétente, ce qui n'est pas encore reçu.

<details><summary>Raisonnement explicite</summary>

1. Identifier les exigences légales applicables aux opérateurs (E4 pour contrôle parental).
2. Vérifier l'existence d'une demande d'autorité compétente pour suspension (absente).
3. Constater la demande de collecte de données de antic sans base légale explicite (lacune).
4. Proposer les actions permises (contrôle parental) et formuler des demandes d'information complémentaires aux acteurs concernés.

</details>


### Tchatlink

**Évaluation.** Des images à caractère sexuel impliquant une victime de 15 ans circulent sur Tchatlink. L'organe de régulation ANTIC a demandé la mise à disposition du contenu suspect et l'activation des mécanismes de signalement prévus par l'article 20. En tant que promoteur de réseau social, Tchatlink doit agir conformément à la loi n°2023/009 et à ses propres règles de modération, tout en protégeant les droits de ses utilisateurs et en évitant une sanction disproportionnée.

**Ce qu'il ignore :** La date précise à laquelle ANTIC attend la mise à disposition du contenu ; L'étendue exacte du contenu demandé (tous les messages ou uniquement ceux signalés) ; Les éventuelles instructions supplémentaires du ministère ou du parquet concernant la procédure de conservation des preuves

| Action | Vérification | Sources |
|---|---|---|
| Supprimer immédiatement les images à caractère sexuel impliquant l'enfant et bloquer les comptes diffusant ces contenus, conformément à l'obligation de protection des enfants en ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 43, p. 230 |
| Conserver les preuves (captures d'écran, logs) et les mettre à disposition d'ANTIC conformément à sa demande de mise à disposition du contenu suspect. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 3, p. 224 |
| Activer les mécanismes de signalement internes prévus par nos conditions d'utilisation et informer les utilisateurs concernés des mesures prises. | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi n°2023/009 ne précise pas les modalités exactes de transmission des preuves aux autorités, ni le délai de réponse requis par l'article 20 mentionné par ANTIC.

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu illicite (images à caractère sexuel d'un mineur).
2. Vérifier les dispositions légales applicables (E3 pour la suppression, E1 pour la coopération).
3. Décider de supprimer le contenu et de conserver les preuves conformément aux exigences légales.
4. Activer les procédures internes de signalement et informer les autorités.
5. Formuler des demandes de clarification et de coopération aux acteurs concernés (operateurs, ANTIC).

</details>


### Police judiciaire

**Évaluation.** Deux victimes, mineures, sont victimes de chantage et de diffusion d'images intimes via un faux profil et la plateforme Tchatlink. Les faits constituent des infractions d'extorsion, de chantage et de diffusion d'images pédopornographiques, relevant de la charte de protection des enfants en ligne. En tant qu'officier de police judiciaire, je dois constater les infractions, saisir les preuves numériques et transmettre le procès‑verbal au parquet.

**Ce qu'il ignore :** Identité exacte du ou des auteurs du faux profil ; Adresses IP et logs de connexion associés aux comptes incriminés sur Tchatlink ; Numéros de téléphone Mobile Money utilisés pour le paiement du chantage ; Disponibilité immédiate des preuves numériques détenues par les victimes (captures d'écran, messages) ; Délais de réponse et procédures internes de Tchatlink pour la conservation des données

| Action | Vérification | Sources |
|---|---|---|
| Constater les infractions d'extorsion, de chantage et de diffusion d'images pédopornographiques et rédiger le procès‑verbal, en saisissant les preuves numériques fournies par les victimes (captures d'écran, messages, traces de paiement Mobile Money). | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |

**Lacunes signalées :**
- La loi ne précise pas les modalités exactes de coopération avec une plateforme étrangère (Tchatlink) hors du territoire camerounais ; il faut se référer aux accords internationaux ou à la demande d'entraide judiciaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits reprochés et les qualifier juridiquement (chantage, diffusion d'images pédopornographiques).
2. Vérifier la compétence du police judiciaire pour constater ces infractions (E1).
3. Décider de la constatation et de la saisie des preuves numériques disponibles.
4. Préparer les demandes d'information complémentaires aux acteurs techniques (Tchatlink, opérateurs).
5. Planifier la transmission du PV au parquet dans le délai légal.

</details>


### Parquet

**Évaluation.** Des images d'une victime de 15 ans circulent sur la plateforme étrangère Tchatlink et sont relayées via des groupes de messagerie. Tchatlink a indiqué qu'elle traitera la demande selon ses délais habituels, sans préciser de date. Les opérateurs de télécommunications ont été sollicités pour un filtrage, mais aucune mesure concrète n'est encore en place.

**Ce qu'il ignore :** Le délai exact que Tchatlink appliquera pour la modération et la suppression des images ; Les capacités techniques et la volonté des opérateurs de télécommunications de mettre en place un filtrage efficace ; L'existence éventuelle d'accords internationaux facilitant la coopération avec le siège étranger de Tchatlink

| Action | Vérification | Sources |
|---|---|---|
| Demander à Tchatlink la suppression immédiate des images et la transmission des données d'identification des comptes ayant diffusé le contenu | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 3, p. 224 |
| Ordonner aux opérateurs de télécommunications de mettre en place un filtrage temporaire des flux contenant les images incriminées, en conformité avec leurs obligations de sécurité des réseaux | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 40, p. 209 |

**Lacunes signalées :**
- La loi ne précise pas les délais exacts que doit respecter un promoteur de réseau social étranger pour répondre à une demande de suppression émanant du parquet camerounais.

<details><summary>Raisonnement explicite</summary>

1. Identifier le fait incriminé : diffusion d'images d'une mineure, violation de la charte de protection des enfants en ligne (E1).
2. Vérifier les obligations des acteurs concernés : Tchatlink, en tant que promoteur de réseau social, doit coopérer pour la suppression du contenu (E1). Les opérateurs, en tant que transmetteurs, peuvent être tenus de filtrer le contenu (E4).
3. Formuler les actions que le parquet peut ordonner directement : demande de suppression et de transmission de données à Tchatlink, et ordre de filtrage aux opérateurs.
4. Identifier les informations manquantes nécessaires à la mise en œuvre efficace de ces mesures (délais de Tchatlink, capacités techniques des opérateurs).
5. Prévoir des demandes complémentaires aux acteurs pertinents (APDP pour la protection des données).

</details>


**Demande** — MINPOSTEL → Tchatlink : Demande urgente de suppression immédiate des images de la victime de 15 ans, avec communication d'un délai précis de traitement.

**Réponse de Tchatlink** (✅ étayée) : Tchatlink confirme la prise en compte de la demande de MINPOSTEL et s’engage à suspendre immédiatement l’accès aux images de la victime de 15 ans diffusées sur sa plateforme, conformément aux obligations prévues à l’article 14 de la loi n° 2023/009. Le délai de traitement sera communiqué dès que la suppression technique sera effectuée, en respectant nos procédures internes de modération tout en assurant la protection de l’enfant.


**Demande** — MINPOSTEL → Operateurs de telecommunications et fournisseurs d'acces a Internet : Mise en place d'un filtrage temporaire du contenu signalé sur leurs réseaux, en conformité avec le Plan d'Action National.

**Réponse de Operateurs de telecommunications et fournisseurs d'acces a Internet** (✅ étayée) : Nous confirmons la mise en place d’un filtrage temporaire du contenu signalé sur nos réseaux, conformément au Plan d’Action National et aux dispositions de l’article 21 qui nous impose de fournir des moyens techniques de filtrage et de blocage des sites portant atteinte à la dignité et à l’intégrité des enfants.


**Demande** — MINPOSTEL → MINESEC : Coordination pour l'intégration de curricula de formation sur l'usage responsable d'Internet, conformément à l'article 6.

**Réponse de MINESEC** (✅ étayée) : Nous confirmons notre disponibilité à coordonner l'intégration du curricula de formation sur l'usage responsable d'Internet au sein des établissements secondaires. Nous proposerons un cadre pédagogique adapté aux niveaux collégial et lycée, en concertation avec le MINPOSTEL et les acteurs concernés, afin de répondre aux exigences de l'article 6 de la loi n° 2023/009. Nous initierons dès à présent les réunions de travail et la mise à jour des programmes scolaires.


**Demande** — ART → ANTIC : Coordonner avec l'ART la mise en place d'un dispositif de filtrage et de collecte de données pour les images circulant sur Tchatlink, conformément à l'article 27 de la loi 2023/009

**Réponse de ANTIC** (✅ étayée) : ANTIC accepte de coordonner avec l'ART la mise en place d’un dispositif de filtrage et de collecte de données pour les images circulant sur Tchatlink, conformément aux dispositions de l’article 27 de la loi n° 2023/009. Nous proposerons un plan d’action conjoint, définirons les modalités techniques avec les opérateurs et Tchatlink, et assurerons le suivi de la mise en œuvre afin de prévenir toute atteinte aux droits des enfants en ligne.


### ⚖️ Analyse du conseiller juridique

Le MINPOSTEL agit sur une base légale solide pour le plan d'action (E1), mais la mise en œuvre du filtrage nécessite une clarification du rôle de l'ANTIC (E4). Le droit camerounais manque de dispositions précises sur les délais de retrait pour les plateformes étrangères, contrairement aux pratiques australiennes et britanniques. Une meilleure coordination inter‑institutionnelle et un cadre procédural détaillé sont indispensables pour combler ces lacunes.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MINPOSTEL | Lancer la mise en œuvre du Plan d'Action National de Protection des Enfants en Ligne en activant le volet de coopération avec les plateformes étrangères pour accélérer la suppression du contenu illicite. | ✅ fondée | L'action s'appuie sur l'article 4 de la Charte de protection des enfants en ligne (E1) qui impose aux pouvoirs publics, dont le ministère des télécommunications, d'élaborer et de mettre en œuvre un plan d'action national incluant la coopération avec les plateformes étrangères. |
| MINPOSTEL | Demander aux opérateurs de télécommunications de préparer un dispositif de filtrage temporaire du contenu signalé. | ⚠️ à vérifier | Le dispositif de filtrage repose partiellement sur l'article 21 (E2) qui impose aux fournisseurs d'accès de mettre à disposition des moyens techniques de contrôle, mais l'article 25 (E4) confie la mise en œuvre de tels dispositifs à l'organe de régulation des TIC (ANTIC) et non directement aux opérateurs sans mandat explicite du ministère. Une clarification du rôle de l'ANTIC est donc nécessaire. |

**Lacune : Absence de cadre juridique précis pour contraindre les plateformes étrangères à supprimer rapidement du contenu illicite et pour définir les délais de réponse.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225
- Australie : L'Online Safety Act 2021 prévoit un « removal notice » contraignant les fournisseurs de services à retirer le contenu dans un délai déterminé. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157))*
- Royaume-Uni : L'Online Safety Act 2023 impose aux plateformes de mettre en place des procédures de retrait rapide et de signalement obligatoire. *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 54/388))*
- **Recommandation :** Adopter un texte d'application précisant les délais de réponse des plateformes étrangères et instituer un mécanisme de notification officielle (ex. « notice of removal ») avec sanctions en cas de non‑conformité.

**Lacune : Manque de procédure claire de coordination entre le MINPOSTEL, l'ANTIC et les opérateurs pour le filtrage temporaire du contenu.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 21, p. 227 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 25, p. 227
- UE : Le Digital Services Act (E10) impose aux plateformes de désigner un interlocuteur unique et de coopérer avec les autorités nationales via des procédures harmonisées. *(Règlement (UE) 2022/2065 du 19 octobre 2022 relatif à un marché unique des services numériques (Digital Services Act), article 25)*
- **Recommandation :** Instaurer un protocole de coordination inter‑institutionnelle, piloté par l'ANTIC, définissant les responsabilités de chaque acteur (MINPOSTEL, opérateurs, police judiciaire) et les modalités de mise en œuvre du filtrage.

**Conflits :**
- Potential conflict between the duty of operators to faciliter le filtrage (E4) and the protection des droits des utilisateurs selon la loi sur la cybersécurité (E7) qui limite la responsabilité des fournisseurs sauf s'ils sont à l'origine du contenu.

**Problèmes de coordination :**
- Absence d'un point de contact unique entre le MINPOSTEL et l'ANTIC pour la mise en œuvre du plan d'action, ce qui peut entraîner des doublons ou des retards dans les demandes de filtrage.


---

## Étape 4 — L'origine : une fuite de données scolaires

**J1, 18h00** · Informés : APDP, ANTIC, ScolaPlus, MINESEC, Police judiciaire, Parquet

> L'enquête établit que les escrocs ont obtenu les numéros de téléphone des victimes et de leurs parents par une fuite de données de l'application de gestion scolaire ScolaPlus, utilisée par 300 établissements. L'éditeur de ScolaPlus avait détecté une anomalie trois semaines plus tôt mais n'a encore prévenu ni les établissements, ni les familles, ni aucune autorité.


### APDP

**Évaluation.** Une fuite de données provenant de l'application scolaire ScolaPlus a exposé les numéros de téléphone d'élèves et de leurs parents. L'éditeur a détecté l'anomalie trois semaines avant mais n'a informé ni les établissements, ni les familles, ni aucune autorité. En tant qu'APDP, je dois vérifier le respect des obligations de notification et de sécurité des données à caractère personnel, notamment pour les enfants.

**Ce qu'il ignore :** Identité exacte du responsable du traitement (éditeur de ScolaPlus) et de son représentant légal ; Nature précise des mesures de sécurité qui ont échoué ; Si une notification aux personnes concernées a été faite, et le contenu de celle‑ci ; Si d'autres autorités nationales (ex. MINAS, MINPOSTEL) ont déjà été informées

| Action | Vérification | Sources |
|---|---|---|
| Ordonner à l'éditeur de ScolaPlus de communiquer toutes les informations relatives à la fuite (description du incident, mesures de sécurité, registre des traitements, listes des personnes affectées, preuves de la notification aux victimes). | ✅ étayée | Règlement (UE) 2016/679 du 27 avril 2016 relatif à la protection des données à caractère personnel (RGPD), article 58, p. 69 |

**Lacunes signalées :**
- Le texte intégral de la loi n° 2024/017 n'est pas disponible ; je ne peux pas citer d'articles précis de cette loi au‑delà de l'art. 53.
- Aucune procédure nationale détaillée n'est encore codifiée pour les notifications de violations impliquant des données d'enfants.

<details><summary>Raisonnement explicite</summary>

1. Identifier la nature de la violation et les parties concernées (données d'enfants).
2. Vérifier les pouvoirs de l'APDP via le RGPD (E3) pour obtenir les informations nécessaires.
3. Formuler une demande d'information à l'éditeur de ScolaPlus.
4. Impliquer les ministères compétents (MINAS, MINPOSTEL) pour la protection des enfants et la coordination technique.
5. Noter les lacunes législatives et la faible confiance due à l'absence de texte national complet.

</details>


### ANTIC

**Évaluation.** Une hausse massive de contenus de chantage ciblant des enfants a été détectée (MinorShield). L'enquête a identifié une fuite de données scolaires provenant de ScolaPlus, qui a omis de notifier les parties concernées. Les opérateurs et Tchatlink ont confirmé leur coopération pour la collecte de logs et la mise à disposition des contenus suspectés. L'ART a été sollicité pour le filtrage. Nous devons activer les mesures prévues par l'article 27 (E3) et coordonner les actions avec les acteurs privés conformément aux articles 10 (E1) et 25 (E4).

**Ce qu'il ignore :** Identité des auteurs des messages de chantage ; Étendue exacte des données compromises chez ScolaPlus ; Si la fuite constitue une infraction pénale ou uniquement administrative

| Action | Vérification | Sources |
|---|---|---|
| Activer les mesures préventives et répressives prévues par l'article 27 pour mettre fin à la diffusion des contenus de chantage, en coordination avec l'ART et les opérateurs. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| Émettre une mise en demeure à ScolaPlus pour manquement à son obligation de notification de la fuite de données et demander la remise des informations nécessaires à l'enquête. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227<br>Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas de sanction pénale directe de notre part ; toute poursuite pénale relève du parquet.
- L'article 27 ne détaille pas les procédures exactes de mise en demeure, nous devons nous appuyer sur les pratiques administratives habituelles.

<details><summary>Raisonnement explicite</summary>

1. Identifier la hausse de contenus de chantage (MinorShield) et la cause probable (fuite ScolaPlus).
2. Vérifier les réponses de coopération des opérateurs et Tchatlink (article 25).
3. Appliquer l'article 27 pour activer mesures préventives et répressives en coordination avec l'ART.
4. Utiliser l'article 10 pour justifier le rôle de l'ANTIC dans la protection des enfants.
5. Formuler des demandes précises aux acteurs concernés afin de collecter preuves et protéger les victimes.

</details>


### ScolaPlus

**Évaluation.** Une fuite de données a exposé les numéros de téléphone d'élèves et de leurs parents provenant de l'application ScolaPlus. L'éditeur a détecté l'anomalie trois semaines avant mais n'a informé aucun établissement, famille ou autorité.

**Ce qu'il ignore :** Quelles sont les obligations précises de notification prévues par la loi n°2023/009 art. 17 et le décret n°2012/1643/PM au Cameroun ; Si un audit de sécurité a déjà été réalisé et quels en étaient les résultats ; L'existence d'éventuelles consignes internes de ScolaPlus concernant la communication d'incidents

| Action | Vérification | Sources |
|---|---|---|
| Préparer une communication interne rappelant les obligations de notification prévues par les cadres légaux applicables, en s'appuyant sur les principes de transparence et de protection des données des enfants | ✅ étayée | Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24) |

**Lacunes signalées :**
- Aucun extrait de la législation camerounaise (loi n°2023/009, décret n°2012/1643/PM, loi n°2024/017) n'est disponible dans la base fournie, ce qui empêche de citer précisément les obligations de notification ou les sanctions applicables

<details><summary>Raisonnement explicite</summary>

1. Identifier le fait principal : fuite de données contenant des numéros de téléphone d'enfants et de leurs parents.
2. Vérifier les bases légales disponibles : seuls les extraits COPPA (E1‑E4) sont fournis, aucun texte camerounais.
3. Utiliser l'extrait E1 qui impose une obligation de notification aux parents pour les données d'enfants, afin de justifier une action interne de communication.
4. Formuler des demandes d'information aux acteurs compétents (ANTIC, APDP, MINAS) pour combler les inconnues légales locales.
5. Mentionner les lacunes liées à l'absence de texte camerounais dans la base de connaissances.

</details>


### MINESEC

**Évaluation.** Deux élèves, âgées de 15 et 19 ans, sont victimes d'extorsion après une fuite de données de l'application scolaire ScolaPlus. Les parents ont signalé la situation aux centres sociaux. Le collège envisage d'exclure la plus jeune pour atteinte à l'image de l'établissement. Le ministère des télécommunications (MINPOSTEL) a proposé une coordination pour mettre en place des curricula d'usage responsable d'Internet.

**Ce qu'il ignore :** Qui est responsable juridiquement de la fuite de données de ScolaPlus ? ; Quelles mesures concrètes de protection des victimes en ligne sont prévues par la législation camerounaise ? ; Quel est le statut juridique de l'exclusion scolaire envisagée ?

| Action | Vérification | Sources |
|---|---|---|
| Lancer, avec MINPOSTEL, la mise en œuvre du curriculum de formation à l'usage responsable d'Internet et des réseaux sociaux, incluant la prévention du sextorsion et la protection des données personnelles des élèves. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |

**Lacunes signalées :**
- Aucune disposition légale n'est fournie concernant la prise en charge directe des victimes d'extorsion en ligne ou la procédure d'exclusion scolaire pour atteinte à l'image de l'établissement.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits connus : fuite de données, extorsion, menace de diffusion de photos, réaction du collège.
2. Vérifier la base légale disponible : seul l'extrait E1 autorise l'action de mise en place de curricula avec MINPOSTEL.
3. Déterminer les actions possibles dans le cadre de ma mission (MINESEC) : je peux lancer la coordination pour le curriculum.
4. Identifier les acteurs complémentaires nécessaires (MINPOSTEL, opérateurs, Tchatlink) et formuler des demandes.
5. Reconnaître les lacunes légales (absence de texte sur protection des victimes et procédures disciplinaires).

</details>


### Police judiciaire

**Évaluation.** Les faits indiquent un chantage par extorsion de fonds et la diffusion d'images à caractère pédopornographique impliquant une collégienne de 15 ans et une lycéenne de 19 ans. Les auteurs ont exploité une fuite de données de l'application scolaire ScolaPlus pour obtenir les numéros de téléphone des victimes et ont utilisé la plateforme de messagerie Tchatlink pour diffuser les images. Les victimes et leurs parents se sont présentés aux centres sociaux de Douala, fournissant des éléments de preuve numériques (captures d'écran, échanges de messages, traces de paiement Mobile Money). Le ministère des affaires sociales (MINAS) et le ministère de la femme et de la famille (MINPROFF) ont demandé l'ouverture d'enquêtes.

**Ce qu'il ignore :** Identité précise des auteurs du faux profil ; Localisation exacte des serveurs hébergeant les contenus sur Tchatlink ; Existence de logs d'accès et de métadonnées conservés par les opérateurs de télécommunications ; État des sauvegardes et des journaux de ScolaPlus relatifs à la fuite de données

| Action | Vérification | Sources |
|---|---|---|
| Saisie et conservation des preuves numériques fournies par les victimes (captures d'écran, relevés Mobile Money, échanges de messages) conformément à la procédure de constatation d'infractions électroniques. | ✅ étayée | Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24) |
| Rédaction d'un procès‑verbal de constatation d'extorsion, de chantage et de diffusion d'images pédopornographiques, à transmettre au Parquet dans les 8 jours. | 🔶 citation douteuse · mention non vérifiée : article 32 · texte absent de la base : 2023/009 | Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24) |

**Lacunes signalées :**
- Absence d'extraits de la législation camerounaise précise concernant la coopération internationale avec un service hébergé hors du territoire (Tchatlink)
- Manque de texte légal national sur l'obligation de notification des fuites de données par les éditeurs de logiciels éducatifs

<details><summary>Raisonnement explicite</summary>

1. Identification des infractions (extorsion, chantage, diffusion d'images pédopornographiques).
2. Vérification des obligations de constatation et de transmission du PV (art.32 loi 2023/009).
3. Recherche d'une base légale pour la saisie et la conservation des preuves numériques (extrait E1).
4. Détermination des acteurs capables de fournir les éléments techniques nécessaires (opérateurs, Tchatlink, MINPOSTEL).
5. Formulation des demandes d'information et de mesures de retrait conformément aux exigences de protection des mineurs.
6. Identification des lacunes légales pour informer le parquet et solliciter éventuellement une adaptation législative ou une coopération internationale.

</details>


### Parquet

**Évaluation.** Des images d'une victime mineure de 15 ans circulent sur la plateforme Tchatlink (siège à l'étranger). La fuite provient de l'application scolaire ScolaPlus, qui n'a pas informé les autorités ni les familles. Les opérateurs de télécommunications sont sollicités pour un filtrage. Le parquet doit qualifier les faits (diffusion d'images d'une mineure, violation du secret des données scolaires) et initier les mesures d'enquête nécessaires.

**Ce qu'il ignore :** Identité précise des responsables de la fuite chez ScolaPlus ; Existence d'une ordonnance judiciaire déjà délivrée pour le filtrage des opérateurs ; Existence d'une plainte officielle déposée par la famille de la victime ; Cadre juridique camerounais exact applicable à la diffusion d'images de mineurs et à la fuite de données scolaires

| Action | Vérification | Sources |
|---|---|---|
| Ordonner l'ouverture d'une enquête pénale pour diffusion d'images d'une mineure et violation du secret des données scolaires, et demander la saisie des serveurs de Tchatlink et de ScolaPlus | ⚠️ non étayée | — |

**Lacunes signalées :**
- Les extraits fournis concernent la législation américaine (COPPA) et ne permettent pas de citer un article de loi camerounais applicable aux faits
- Le parquet ne peut pas, seul, ordonner le filtrage des opérateurs sans autorisation judiciaire, ce qui nécessite une demande auprès du juge compétent

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits graves (diffusion d'images d'une mineure, fuite de données scolaires).
2. Vérifier les acteurs impliqués (Tchatlink, ScolaPlus, opérateurs, police).
3. Constater l'absence de base légale camerounaise dans les extraits fournis.
4. Décider d'ouvrir une enquête et de solliciter les autorités compétentes pour les mesures d'investigation et de protection.
5. Formuler les demandes aux acteurs concernés en respectant les limites du mandat du parquet.

</details>


**Demande** — APDP → MINAS : Veuillez préparer, en coordination avec l'APDP, les mesures de protection et d'accompagnement des enfants et de leurs familles affectés par la fuite de données de ScolaPlus.

**Réponse de MINAS** (✅ étayée) : En coordination avec l'APDP, le MINAS propose de mettre en place : 1) un dispositif d’accueil et d’écoute psychologique pour les enfants victimes et leurs familles, assuré par des travailleurs sociaux formés aux spécificités des abus en ligne ; 2) une formation accélérée du personnel des centres sociaux et des établissements scolaires concernés, conformément à l'article 8 qui impose au Ministère des affaires sociales de fournir une formation appropriée en matière de prévention, détection et prise en charge des abus en ligne ; 3) la création d’un protocole d’intervention rapide incluant la collecte sécurisée des preuves numériques, le signalement aux autorités compétentes (police judiciaire) et le suivi juridique des victimes ; 4) une campagne d’information ciblée auprès des parents et des jeunes sur les risques de chantage numérique et les recours disponibles, en partenariat avec l’APDP pour garantir la conformité au respect des données personnelles. Ces mesures seront élaborées conjointement avec l’APDP afin d’assurer la protection des données des enfants et le respect de leurs droits.


**Demande** — APDP → MINPOSTEL : Merci de vérifier si des obligations de notification aux opérateurs de télécommunications sont requises dans le cadre de cette fuite.

**Réponse de MINPOSTEL** (⚠️ non étayée) : Selon les extraits dont je dispose, aucune disposition ne prévoit explicitement une obligation de notification aux opérateurs de télécommunications dans le cadre de la diffusion d'images d'enfants. L'article 4 (E1) indique que le Ministère élabore et met en œuvre le Plan d'Action National, mais ne détaille pas d'obligation de notification. En l'absence de texte légal le prévoyant, je ne peux pas confirmer une telle obligation.


**Demande** — ANTIC → ART : Coordonner la mise en place d'un dispositif de filtrage et de collecte de données pour les images et messages de chantage circulant sur Tchatlink, conformément à l'article 27.

**Réponse de ART** (✅ étayée) : L'ART accepte de coordonner avec l'ANTIC la mise en place d’un dispositif de filtrage et de collecte de données concernant les images et messages de chantage circulant sur la plateforme Tchatlink, conformément à l’article 27 de la loi n° 2023/009. Nous proposerons un plan d’action conjoint, définirons les modalités techniques avec les opérateurs de télécommunications et, dans la mesure du possible, avec Tchatlink, et assurerons le suivi de la mise en œuvre pour protéger les droits des enfants en ligne.


**Demande** — ANTIC → Operateurs de telecommunications et fournisseurs d'acces a Internet : Transmettre les logs détaillés (adresses IP, horodatage, métadonnées) relatifs aux messages de chantage détectés afin de permettre une investigation numérique conforme à l'article 25.

**Réponse de Operateurs de telecommunications et fournisseurs d'acces a Internet** (⚠️ non étayée) : Nous ne disposons pas d'un extrait légal nous autorisant explicitement à transmettre les logs détaillés demandés. Aucun des extraits fournis (E1, E2, E3) ne couvre l'obligation de remise de données techniques aux autorités dans le cadre de l'article 25. En l'absence de base légale identifiable, nous ne pouvons pas satisfaire la demande d'ANTIC.


### ⚖️ Analyse du conseiller juridique

Les actions de l'APDP et du MINESec sont solidement fondées sur le droit camerounais, tandis que celles de l'ANTIC, de ScolaPlus et de la police manquent de bases légales nationales explicites. Le droit camerounais ne précise pas la procédure de notification des violations de données, contrairement aux exigences du RGPD et de la CCPA. Une meilleure coordination inter‑institutionnelle et l'adoption de textes détaillés sont nécessaires pour combler ces lacunes.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| APDP | Ordonner à l'éditeur de ScolaPlus de communiquer toutes les informations relatives à la fuite (description du incident, mesures de sécurité, registre des traitements, listes des personnes affectées, preuves de la notification aux victimes) | ✅ fondée | L'article 58 du RGPD (E4) confère à l'autorité de contrôle le pouvoir d'ordonner au responsable du traitement de fournir toute information nécessaire à l'exercice de ses missions. |
| ANTIC | Activer les mesures préventives et répressives prévues par l'article 27 pour mettre fin à la diffusion des contenus de chantage, en coordination avec l'ART et les opérateurs | ⚠️ à vérifier | L'article 27 (E1) prévoit que l'organe chargé de la régulation des TIC intervient lorsque les atteintes aux droits des enfants en ligne ne constituent pas des infractions pénales. Le chantage constitue une infraction pénale, donc l'application de cet article nécessite clarification. |
| ANTIC | Émettre une mise en demeure à ScolaPlus pour manquement à son obligation de notification de la fuite de données et demander la remise des informations nécessaires à l'enquête | ❌ non fondée | Aucun des extraits fournis (E1, E3) ne prévoit explicitement le pouvoir de mise en demeure de l'ANTIC à l'égard d'un éditeur de logiciel. Le texte de l'article 27 décrit des mesures générales, mais pas de procédure de mise en demeure. |
| ScolaPlus | Préparer une communication interne rappelant les obligations de notification prévues par les cadres légaux applicables, en s'appuyant sur les principes de transparence et de protection des données des enfants | ❌ non fondée | L'extrait invoqué (E2) est la COPPA américaine, qui ne constitue pas une source de droit camerounais. Aucun texte camerounais n'est cité pour justifier cette action. |
| MINESEC | Lancer, avec MINPOSTEL, la mise en œuvre du curriculum de formation à l'usage responsable d'Internet et des réseaux sociaux, incluant la prévention du sextorsion et la protection des données personnelles des élèves | ✅ fondée | L'article 6 (E5) impose aux ministères de l'éducation et des télécommunications de mettre en place des curricula de formation sur l'utilisation responsable d'Internet et la protection des enfants en ligne. |
| Police judiciaire | Saisie et conservation des preuves numériques fournies par les victimes (captures d'écran, relevés Mobile Money, échanges de messages) conformément à la procédure de constatation d'infractions électroniques | ❌ non fondée | L'extrait invoqué (E2) concerne la COPPA (USA) et ne fournit pas de base légale camerounaise pour la saisie et la conservation de preuves numériques. |

**Lacune : Absence de texte national détaillant la procédure de notification des violations de données à caractère personnel, y compris les délais, le contenu minimal de la notification et les sanctions en cas de non‑notification.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227
- UE : Le RGPD impose un délai de 72 heures pour notifier la violation à l'autorité de contrôle et aux personnes concernées, sous peine d'amendes administratives. *(Règlement (UE) 2016/679 du 27 avril 2016 relatif à la protection des données à caractère personnel (RGPD), article 58, p. 69)*
- États‑Unis : La loi de Californie (CCPA) prévoit des notifications dans les 30 jours et des sanctions financières en cas de manquement. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24))*
- **Recommandation :** Adopter, par décret ou loi, une procédure de notification conforme aux standards du RGPD (délai 72 h, contenu de la notification, sanctions administratives) afin de combler le vide législatif.

**Conflits :**
- Conflit potentiel entre l'ANTIC, qui invoque l'article 27 (E1) pour intervenir sur des contenus de chantage, et le cadre pénal qui considère le chantage comme une infraction pénale, créant une incertitude sur la compétence exclusive.

**Problèmes de coordination :**
- Manque de coordination formalisée entre l'APDP, l'ANTIC, le MINPOSTEL et la police judiciaire pour le partage d'informations relatives à la fuite de données et aux enquêtes pénales.


---

## Étape 5 — Pression médiatique : faut-il bloquer Tchatlink ?

**J2, 09h00** · Informés : MinorShield, ANTIC, ART, MINPOSTEL, APDP, MINAS, MINPROFF, MINESEC, Police judiciaire, Parquet, Operateurs de telecommunications et fournisseurs d'acces a Internet, Tchatlink, ScolaPlus

> L'affaire fait la une des médias et des réseaux sociaux. Une proposition circule : bloquer entièrement l'accès à Tchatlink sur le territoire national jusqu'à la fin de la crise. Tchatlink compte plusieurs millions d'utilisateurs au Cameroun, dont de nombreux commerçants.


### MinorShield

**Évaluation.** MinorShield a détecté une hausse de 400 % des contenus bloqués sur les appareils d'enfants protégés à Douala et Yaoundé, avec un vocabulaire d'argot local et des menaces de type « envoie ta photo sinon… ». Les opérateurs ont activé les mécanismes de signalement (article 24, E2) et l'ANTIC a confirmé la prise en compte de la tendance et l'activation des mesures prévues à l'article 27. Aucun élément ne permet encore de déterminer s'il s'agit d'une campagne coordonnée ou d'événements isolés.

**Ce qu'il ignore :** L'existence d'un groupe organisé derrière ces messages ; L'identité ou le nombre d'utilisateurs impliqués ; L'ampleur réelle du risque d'extorsion ou de harcèlement au‑delà des données agrégées

| Action | Vérification | Sources |
|---|---|---|
| Continuer la collecte et l'analyse des données agrégées et anonymisées sur les contenus bloqués, en appliquant les filtres de détection d'argot suspect et en générant un rapport d'évolution quotidien. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 5, p. 225 |
| Transmettre le rapport d'évolution à l'ANTIC et aux opérateurs afin de soutenir la coordination déjà engagée. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas de pouvoir d'imposer un blocage total de la plateforme Tchatlink ; seule une décision des autorités compétentes (ANTIC, ART, MINPOSTEL) pourrait le faire.
- MinorShield ne dispose d'aucune autorité pour identifier ou sanctionner les auteurs des messages, ce qui nécessite l'intervention des forces de l'ordre.

<details><summary>Raisonnement explicite</summary>

1. Analyse des faits rapportés et des réponses reçues des acteurs (ANTIC, opérateurs).
2. Identification des obligations légales applicables (E1, E2, E10).
3. Détermination des actions que MinorShield peut réaliser dans son cadre (monitoring, partage d'agrégats).
4. Formulation des demandes de coordination aux acteurs disposant du pouvoir de décision et d'action technique.
5. Mention des limites légales (absence de pouvoir de blocage total, besoin d'enquête).

</details>


### ANTIC

**Évaluation.** Une hausse massive de contenus de chantage ciblant des enfants a été détectée (MinorShield). L'origine semble être une fuite de données de ScolaPlus, non signalée aux autorités. Les opérateurs ont confirmé leur capacité à fournir les logs techniques, mais invoquent l'absence d'extrait légal explicite (E1‑E3). Tchatlink a accepté de mettre à disposition les contenus suspects et d'activer les mécanismes de signalement. L'ART a accepté de coopérer pour le filtrage et la collecte de données sur Tchatlink. Il faut donc activer les mesures prévues par l'article 27 (E2) et, en cas de refus ou de manquement, appliquer l'article 28 (E4).

**Ce qu'il ignore :** Existence d'un texte particulier précisant le rôle de l'ANTIC (article 10(2)) – non disponible ; Délai exact de la fuite de données ScolaPlus et les responsabilités contractuelles de l'éditeur ; Si les opérateurs considèrent que les logs demandés relèvent de l'article 25 ou nécessitent un autre texte

| Action | Vérification | Sources |
|---|---|---|
| Lancer la mise en œuvre des mesures préventives et répressives prévues par l'article 27 pour stopper la diffusion des contenus de chantage, en coordination avec l'ART et les opérateurs. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| Émettre une mise en demeure aux opérateurs et à Tchatlink pour obtenir les logs détaillés (adresses IP, horodatage, métadonnées) nécessaires à l'investigation, conformément à l'article 28 en cas de manquement. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 28, p. 228 |

**Lacunes signalées :**
- Absence d'extrait légal explicite autorisant la transmission obligatoire de logs détaillés aux autorités (article 25 mentionne la facilitation mais ne précise pas l'obligation).
- Le texte particulier mentionné à l'article 10(2) n'est pas disponible, limitant la précision du rôle de l'ANTIC.

<details><summary>Raisonnement explicite</summary>

1. Identifier la nature de la menace (chantage d'enfants) et son origine (fuite ScolaPlus).
2. Vérifier les bases légales disponibles : E2 pour les mesures de prévention, E4 pour la mise en demeure, E25 pour la collecte de données (mais base légale manquante).
3. Décider d'activer les mesures de l'article 27 en coordination avec l'ART et les opérateurs.
4. Préparer une mise en demeure selon l'article 28 pour obtenir les logs nécessaires.
5. Formuler des demandes aux acteurs concernés (MINPOSTEL, opérateurs, Tchatlink, ART) afin de combler les lacunes d'information et de garantir la coopération.

</details>


### ART

**Évaluation.** Des images d'exploitation d'une mineure de 15 ans circulent sur la plateforme étrangère Tchatlink. ANTIC a accepté de coordonner avec l'ART la mise en place d'un dispositif de filtrage et de collecte de données, conformément à l'article 27 de la loi 2023/009. L'ART doit donc activer son rôle de régulation des télécommunications en mobilisant les opérateurs pour appliquer le filtrage demandé, tout en respectant ses limites d'autorité sur une plateforme hors du territoire.

**Ce qu'il ignore :** Le délai exact que Tchatlink accepte de respecter pour la modération des contenus ; Les capacités techniques précises des opérateurs camerounais pour filtrer les contenus provenant de Tchatlink ; L'existence éventuelle d'une décision judiciaire ou d'une ordonnance du parquet concernant ces images

| Action | Vérification | Sources |
|---|---|---|
| Lancer la procédure de mise en place d'un dispositif de filtrage et de collecte de données sur le réseau national, en coordination avec ANTIC et les opérateurs, afin d'empêcher la diffusion des images incriminées. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |

**Lacunes signalées :**
- L'ART ne dispose d'aucune compétence directe pour ordonner le blocage total de la plateforme Tchatlink, qui n'a pas de présence juridique au Cameroun.
- La loi ne précise pas de procédure d'urgence permettant de contraindre Tchatlink à supprimer immédiatement les contenus sans son accord préalable.

<details><summary>Raisonnement explicite</summary>

1. Identifier le problème : diffusion d'images d'une mineure sur Tchatlink, plateforme étrangère.
2. Vérifier les compétences de l'ART : possible de coordonner le filtrage avec les opérateurs, mais pas de bloquer la plateforme elle‑même.
3. S'appuyer sur l'article 27 (E3) qui autorise la coopération entre l'organe TIC et l'organe télécom pour mettre fin aux atteintes non pénales.
4. Décider d'initier le dispositif de filtrage et de collecte de données, en demandant à ANTIC le plan d'action et aux opérateurs la mise en œuvre technique.
5. Noter les limites légales (impossibilité de bloquer Tchatlink) et les inconnues qui devront être clarifiées avant toute action supplémentaire.

</details>


### MINPOSTEL

**Évaluation.** Le MINPOSTEL a reçu la confirmation de Tchatlink de suspendre immédiatement les images de la victime et attend un délai précis. Les opérateurs ont mis en place un filtrage temporaire du contenu signalé. Le MINPROFF propose des modules de formation à la parentalité positive, le MINESEC propose d'intégrer un curricula sur l'usage responsable d'Internet, et l'APDP demande si une notification aux opérateurs est requise. Une pression médiatique propose de bloquer totalement Tchatlink, mais cette mesure relève d'une décision inter‑ministerielle et/ou de l'organe de régulation (ANTIC/ART).

**Ce qu'il ignore :** Le délai exact que Tchatlink pourra fournir pour la suppression technique des images ; Les modalités précises de notification aux opérateurs exigées par l'APDP ; L'avis de l'ANTIC ou de l'ART sur la possibilité de bloquer l'accès à Tchatlink au niveau national

| Action | Vérification | Sources |
|---|---|---|
| Confirmer la poursuite du suivi de la suppression des images avec Tchatlink et rappeler l'obligation de communiquer le délai de traitement dès que possible. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |
| Valider le filtrage temporaire mis en place par les opérateurs et demander le suivi du dispositif jusqu'à la complète suppression du contenu illicite. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |
| Accepter la proposition du MINPROFF et lancer la co‑construction des modules de formation à la parentalité positive, en précisant le calendrier et les moyens de suivi. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 4, p. 225 |
| Valider la participation du MINESEC à l'intégration du curricula sur l'usage responsable d'Internet, conformément à l'article 6. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |
| Demander à l'APDP de préciser les obligations de notification aux opérateurs dans le cadre de la fuite d'images. | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne prévoit pas que le MINPOSTEL puisse, seul, ordonner le blocage total d'une plateforme étrangère ; cela relève de la compétence de l'ANTIC ou de l'ART.

<details><summary>Raisonnement explicite</summary>

1. Analyser les réponses reçues de chaque acteur et les aligner avec les exigences du Plan d'Action National.
2. Identifier les actions que le MINPOSTEL peut légitimement prendre (suivi de suppression, validation du filtrage, coordination de formations).
3. Repérer les décisions qui dépassent son mandat (blocage complet de Tchatlink) et les orienter vers les autorités compétentes.
4. Vérifier les bases légales disponibles (E1, E4) pour chaque action et noter les absences de texte pour les demandes de clarification.
5. Formuler les demandes précises aux partenaires afin d'assurer la mise en œuvre efficace du plan et la protection de l'enfant.

</details>


### APDP

**Évaluation.** Une fuite de données de l'application scolaire ScolaPlus a exposé les numéros de téléphone d'enfants et de leurs parents. L'éditeur n'a pas informé les parties concernées. La pression médiatique propose de bloquer totalement Tchatlink, mais aucune disposition légale ne prévoit une telle mesure générale. Le MINAS a proposé des mesures d'accompagnement des victimes, tandis que le MINPOSTEL indique l'absence d'obligation de notification aux opérateurs.

**Ce qu'il ignore :** Identité précise des personnes à l'origine de la diffusion des données (pour appliquer l'article E1) ; Existence d'une décision judiciaire ou d'une ordonnance du parquet autorisant le blocage total de Tchatlink

| Action | Vérification | Sources |
|---|---|---|
| Demander à l'ANTIC, en tant qu'organe chargé de la régulation des TIC, de préciser les procédures à suivre pour contraindre les fournisseurs d'accès et les promoteurs de réseaux sociaux à suspendre l'accès aux comptes identifiés comme à l'origine de la diffusion illicite, conformément à l'article E1. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |
| Coordonner avec le MINAS la mise en œuvre des mesures d'accompagnement des enfants et de leurs familles déjà proposées (dispositif psychologique, formation du personnel, protocole d'intervention, campagne d'information). | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi n° 2024/017 (art. 53) n'est pas disponible dans la base, je ne peux donc pas citer d'article spécifique de cette loi.
- Aucun texte ne prévoit une obligation de notification aux opérateurs de télécommunications dans ce type de fuite (confirmé par MINPOSTEL).
- Aucune disposition ne permet de bloquer l'ensemble d'une plateforme comme Tchatlink sans identifier les comptes fautifs.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits connus : fuite de données ScolaPlus, proposition de blocage total de Tchatlink.
2. Vérifier les bases légales disponibles : E1 impose suspension pour les auteurs de contenus illicites, E2/E4 concernent le rôle de l'ANTIC et la coopération des opérateurs.
3. Constater l'absence de texte autorisant le blocage complet d'une plateforme.
4. Déduire que l'action légale possible est de demander la suspension des comptes incriminés via l'ANTIC.
5. Proposer la coordination avec le MINAS pour les mesures d'accompagnement, qui ne sont pas explicitement prévues mais compatibles avec la mission de l'APDP.
6. Formuler des demandes aux acteurs compétents (ANTIC, police, parquet) pour obtenir les informations et autorisations nécessaires.
7. Lister les lacunes légales qui limitent l'étendue de l'action.

</details>


### MINAS

**Évaluation.** Deux mineures sont victimes d'un chantage en ligne avec diffusion de photos intimes. La police a lancé une enquête et le MINPROFF intervient auprès du collège. Le MINAS doit assurer la prise en charge psychosociale des victimes, coordonner les mesures de protection et préparer la formation du personnel intervenant.

**Ce qu'il ignore :** Identité précise des auteurs du faux profil et du chantage ; Étendue de la diffusion des photos et des données personnelles ; Capacité des centres sociaux de Douala à fournir un suivi psychologique immédiat ; Ressources budgétaires disponibles pour la prise en charge et la formation

| Action | Vérification | Sources |
|---|---|---|
| Déployer une équipe de prise en charge psychosociale dans les centres sociaux de Douala pour accompagner les deux victimes et leurs familles, conformément au Plan d'Action National de Protection des Enfants en Ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 5, p. 225 |
| Lancer la préparation d'un module de formation urgent pour le personnel des centres sociaux et des écoles sur la détection, la prévention et la prise en charge des abus en ligne, en s'appuyant sur les objectifs du Plan d'Action National de Protection des Enfants en Ligne. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 5, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement le blocage total d'une plateforme (Tchatlink) au niveau national ; l'article 14 ne permet que la suspension du compte fautif, pas la coupure d'accès généralisée.

<details><summary>Raisonnement explicite</summary>

1. Identifier les besoins immédiats des victimes (soutien psychologique, sécurisation des données).
2. Vérifier les bases légales disponibles (E1 pour la prise en charge, E2/E14 pour la suspension du compte).
3. Déterminer les actions que le MINAS peut réaliser directement (déploiement d'équipes, formation).
4. Formuler les demandes aux acteurs compétents pour les actions hors de mon mandat (suspension du compte à Tchatlink, coordination avec APDP).
5. Noter les limites légales (impossibilité de bloquer l'ensemble de la plateforme).

</details>


### MINPROFF

**Évaluation.** Deux adolescentes victimes de chantage en ligne sont menacées de diffusion d'images intimes. Le collège envisage de les exclure, ce qui constitue une mesure discriminatoire. Le MINPOSTEL a confirmé sa coopération pour créer des modules de formation à la parentalité positive sur l'usage d'Internet. Le MINAS a demandé d'intervenir auprès du collège pour protéger les droits de l'enfant.

**Ce qu'il ignore :** Le calendrier précis et les ressources humaines et financières disponibles pour la conception et la diffusion des modules de formation ; Les modalités exactes d'intervention du MINAS auprès du collège (qui contacter, quelles procédures suivre) ; L'ampleur de la pression médiatique et les éventuelles décisions politiques concernant le blocage de Tchatlink

| Action | Vérification | Sources |
|---|---|---|
| Lancer la conception conjointe des modules de formation à la parentalité positive sur l'usage d'Internet avec le MINPOSTEL, en précisant le contenu pédagogique, le calendrier de diffusion et les moyens de suivi. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 7, p. 225 |
| Transmettre au MINAS une demande d'intervention auprès du collège de la collégienne afin d'empêcher toute mesure d'exclusion discriminatoire et de garantir le respect des droits de l'enfant. | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne prévoit pas de mesure permettant de bloquer ou restreindre l'accès à Tchatlink ; aucune base légale n'est disponible pour justifier un tel blocage.

<details><summary>Raisonnement explicite</summary>

1. Identifier les besoins immédiats de protection des victimes et de prévention de mesures discriminatoires.
2. Vérifier les obligations légales (E1) qui imposent la création de modules de formation avec le MINPOSTEL.
3. Constater que le MINPOSTEL a déjà accepté la coopération, il faut donc initier la phase de conception.
4. Le MINAS a demandé d'agir auprès du collège ; aucune base légale explicite n'est fournie, mais l'action est compatible avec la mission de protection de l'enfant.
5. Noter que la proposition de bloquer Tchatlink n'est pas couverte par les extraits légaux disponibles, il faut donc s'abstenir de cette mesure et signaler la lacune.

</details>


### MINESEC

**Évaluation.** Deux adolescentes victimes d'extorsion sexuelle en ligne suite à une fuite de données de l'application scolaire ScolaPlus. Le collège envisage d'exclure la plus jeune. La presse réclame le blocage total de Tchatlink. Le ministère des télécommunications a sollicité une coordination pour des curricula d'usage responsable d'Internet.

**Ce qu'il ignore :** Qui est juridiquement responsable de la fuite de données de ScolaPlus et quelles mesures coercitives peuvent être imposées ; Quel est le protocole exact pour ordonner le blocage d'un réseau social (compétence de l'ANTIC, de l'ART ou du MINPOSTEL) ; Si le collège a le pouvoir disciplinaire d'exclure la victime sans procédure interne

| Action | Vérification | Sources |
|---|---|---|
| Lancer la mise en place, avec MINPOSTEL, des curricula de formation sur l'usage responsable d'Internet et la protection des enfants en ligne, conformément à la mission du ministère. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |
| Demander au MINPOSTEL, en s'appuyant sur l'article 14 (E1), d'évaluer la possibilité de suspendre l'accès à Tchatlink pour les comptes identifiés comme à l'origine de la diffusion de contenus portant atteinte à la dignité des enfants. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |

**Lacunes signalées :**
- La loi ne prévoit aucune disposition explicite permettant d'imposer une sanction disciplinaire (exclusion) à un élève victime d'extorsion.
- Aucune procédure n'est détaillée pour obliger l'éditeur ScolaPlus à notifier les autorités ou les victimes d'une fuite de données.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits pertinents : extorsion, fuite de données, pression médiatique.
2. Rechercher les articles de la charte qui encadrent nos prérogatives : E2 pour les curricula, E1 pour la suspension d'accès.
3. Déterminer les actions que le ministère peut légitimement entreprendre : élaboration de curricula et demande de suspension de contenus.
4. Identifier les acteurs à solliciter pour les mesures hors de notre champ (blocage complet, notification de fuite).
5. Noter les lacunes légales qui limitent notre capacité d'action directe sur les victimes ou l'éditeur.

</details>


### Police judiciaire

**Évaluation.** Des victimes mineures ont été victimes de chantage et de diffusion d'images intimes via la plateforme Tchatlink. Les auteurs ont obtenu les numéros de téléphone grâce à une fuite de données de l'application scolaire ScolaPlus. Les autorités demandent d'identifier les auteurs, de préserver les preuves numériques et de faire cesser la diffusion en ligne.

**Ce qu'il ignore :** Identité exacte des auteurs du faux profil et du chantage ; Logs d'accès et de diffusion détenus par Tchatlink ; Données de connexion et de localisation des victimes fournies par les opérateurs ; Preuve de la fuite de données de ScolaPlus (qui a détecté l'anomalie mais n'a pas alerté) ; Consentement ou autorisation légale pour intercepter les communications (article 44)

| Action | Vérification | Sources |
|---|---|---|
| Demander à Tchatlink, à la demande de l'autorité compétente, la suspension immédiate du contenu illicite et la transmission des logs d'accès relatifs aux comptes impliqués. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |
| Ordonner aux opérateurs de télécommunications de mettre en place un filtrage temporaire du trafic vers Tchatlink et de fournir les données de trafic (numéros de téléphone, horodatage, adresse IP) liées aux victimes. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |
| Consigner un constat d’infraction et sécuriser les preuves numériques fournies par les victimes (captures d’écran, messages Mobile Money, identifiants du faux profil). | ⚠️ non étayée | — |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte pour obtenir une autorisation d’interception de communications (article 44) ; il faut donc solliciter le parquet ou le ministère compétent.
- Aucun extrait ne prévoit explicitement la responsabilité du développeur de ScolaPlus en cas de fuite de données, ce qui nécessite une analyse juridique complémentaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier les infractions (chantage, diffusion d'images pédopornographiques, fuite de données).
2. Chercher les bases légales permettant d'agir contre le contenu en ligne et d'obtenir la coopération des fournisseurs.
3. Utiliser l'article 14 (E1) pour demander la suspension du contenu et le filtrage du trafic.
4. Noter les actions qui ne sont pas directement couvertes par les extraits (interception, responsabilité du fournisseur de ScolaPlus).
5. Formuler les demandes aux acteurs compétents pour obtenir les moyens techniques et juridiques nécessaires.

</details>


### Parquet

**Évaluation.** Des images d'une victime mineure de 15 ans circulent sur la plateforme Tchatlink, dont le siège est hors du Cameroun. Tchatlink a indiqué qu'elle traitera la demande de modération selon ses délais habituels, sans préciser de date. Les opérateurs de télécommunications sont sollicités pour un filtrage. L'origine de la fuite provient de l'application scolaire ScolaPlus, qui n'a pas informé les autorités ni les familles après avoir détecté une anomalie. La presse et les réseaux sociaux réclament le blocage complet de Tchatlink sur le territoire national.

**Ce qu'il ignore :** Le délai exact nécessaire pour obtenir une décision judiciaire d'ordonnance de suspension ou de blocage ; L'existence d'une procédure d'urgence prévue par la loi pour le blocage temporaire d'un service en ligne ; Les preuves techniques précises permettant d'identifier les responsables de la fuite chez ScolaPlus

| Action | Vérification | Sources |
|---|---|---|
| Demander à Tchatlink, à la demande des autorités compétentes, de suspendre l'accès au contenu portant atteinte à la dignité et à l'intégrité de l'enfant | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |
| Ordonner aux opérateurs de télécommunications de mettre en place un filtrage temporaire du contenu incriminé afin d'empêcher sa diffusion supplémentaire | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |

**Lacunes signalées :**
- Aucun texte légal fourni ne prévoit explicitement le blocage complet et définitif d'une plateforme en ligne sur le territoire national, ce qui rend difficile de justifier une telle mesure sans passer par une décision judiciaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier le fait illicite (diffusion d'images d'une mineure) et la responsabilité potentielle de Tchatlink.
2. Rechercher la base légale applicable à la suspension de contenu portant atteinte aux enfants.
3. Trouver l'article 14 (E1) qui impose aux fournisseurs de contenus de suspendre l'accès à la demande des autorités.
4. Décider d'une demande de suspension à Tchatlink et d'un filtrage aux opérateurs, actions que le parquet peut ordonner.
5. Reconnaître l'absence de texte autorisant le blocage total du service, d'où la mention de lacune.
6. Formuler les demandes aux acteurs compétents (Tchatlink, opérateurs, police, MINPOSTEL) pour la mise en œuvre et l'enquête.

</details>


### Operateurs de telecommunications et fournisseurs d'acces a Internet

**Évaluation.** Des images d'exploitation d'une mineure circulent sur la plateforme Tchatlink. Les autorités (ANTIC, MINPOSTEL) demandent un filtrage, la collecte de logs et la suspension éventuelle d'accès. Les fournisseurs doivent mettre en place contrôle parental et mécanismes de signalement, et fournir les données techniques demandées.

**Ce qu'il ignore :** La décision finale de bloquer totalement Tchatlink (requiert autorisation explicite d'une autorité compétente) ; Les délais précis de modération de Tchatlink ; Les modalités exactes de transmission des logs (format, période) demandées par l'ANTIC

| Action | Vérification | Sources |
|---|---|---|
| Déployer des dispositifs de contrôle parental et de filtrage des contenus illicites conformément aux exigences de protection des enfants | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 21, p. 227 |
| Mettre à disposition des guides de bonnes pratiques et des mécanismes de signalement pour les utilisateurs | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 20, p. 226 |
| Transmettre les logs techniques (adresses IP, horodatage, métadonnées) relatifs aux messages de chantage détectés à l'ANTIC | ⚠️ non étayée · mention non vérifiée : article 25 | — |
| Suspendre l'accès au compte identifié comme à l'origine de la publication du contenu illicite, à la demande de l'ANTIC ou du MINPOSTEL | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |

**Lacunes signalées :**
- Absence d'extrait légal précisant l'obligation de fournir les logs (article 25 non fourni)
- Pas de base légale explicite pour demander le blocage total de Tchatlink sans décision d'une autorité compétente

<details><summary>Raisonnement explicite</summary>

1. Identifier les exigences légales applicables aux fournisseurs d'accès (E1, E2, E3).
2. Vérifier les demandes reçues des autorités (ANTIC, MINPOSTEL, Minorshield).
3. Sélectionner les actions que nous pouvons entreprendre directement (contrôle parental, signalement, transmission de logs, suspension de compte).
4. Noter les actions qui nécessitent une autorisation explicite (blocage total de Tchatlink) et les exclure de notre champ d'action.
5. Formuler les demandes complémentaires aux autres acteurs pour obtenir les informations ou confirmations manquantes.

</details>


### Tchatlink

**Évaluation.** Des images d'une victime mineure de 15 ans circulent sur Tchatlink. Le MINPOSTEL exige une suppression immédiate avec délai précis. L'ANTIC demande la mise à disposition du contenu suspect et l'activation du mécanisme de signalement. Tchatlink doit agir conformément à ses obligations de promoteur de réseau social et à la loi n°2023/009, article 14, qui impose la suspension ou la suppression de contenus portant atteinte à la dignité et à l'intégrité des enfants à la demande des autorités compétentes.

**Ce qu'il ignore :** Le délai exact exigé par le MINPOSTEL pour la suppression ; Les modalités précises de mise à disposition du contenu demandé par l'ANTIC

| Action | Vérification | Sources |
|---|---|---|
| Supprimer immédiatement toutes les images de la victime de 15 ans présentes sur la plateforme et bloquer tout accès futur à ce contenu depuis le territoire camerounais. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |
| Activer le mécanisme de signalement interne prévu par nos conditions d'utilisation pour les contenus signalés et notifier les équipes de modération afin d'accélérer le traitement. | ⚠️ non étayée | — |

**Lacunes signalées :**
- Aucun extrait fourni ne détaille les obligations précises de mise à disposition du contenu demandé par l'ANTIC (article 20).
- La loi n°2010/012, article 44, limite l'interception et le stockage des communications, mais ne précise pas les procédures de transmission de preuves aux autorités dans ce contexte.

<details><summary>Raisonnement explicite</summary>

1. Identifier les exigences légales applicables aux contenus illicites impliquant un mineur.
2. Vérifier que l'article 14 (E1) impose la suppression ou suspension à la demande des autorités.
3. Décider de supprimer immédiatement le contenu et de bloquer tout accès futur depuis le Cameroun.
4. Noter l'absence d'extraits couvrant la demande de l'ANTIC et formuler une demande de précisions.
5. Formuler les actions et demandes dans le cadre de la mission de Tchatlink, en évitant toute mesure disproportionnée comme le blocage total du service.

</details>


### ScolaPlus

**Évaluation.** Une fuite de données de l'application ScolaPlus a exposé les numéros de téléphone d'élèves et de leurs parents. L'éditeur a détecté l'anomalie trois semaines auparavant mais n'a encore informé ni les établissements, ni les familles, ni aucune autorité. La presse réclame le blocage de Tchatlink, mais aucune disposition légale ne nous impose de le faire.

**Ce qu'il ignore :** Quel délai légal exact est imposé pour la notification des victimes et des autorités après la découverte d'une fuite de données contenant des informations d'enfants ; Si une ordonnance de suspension d'un réseau social (Tchatlink) a été ou peut être émise par l'ANTIC ou une autre autorité compétente

| Action | Vérification | Sources |
|---|---|---|
| Informer immédiatement les établissements utilisateurs de ScolaPlus ainsi que les parents concernés de la fuite de données, en précisant les risques encourus et les mesures de protection à prendre. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 24, p. 207 |

**Lacunes signalées :**
- Aucun extrait fourni ne précise l'obligation de l'éditeur de notifier les autorités publiques (ex. MINPOSTEL, PARQUET) dans un délai donné après la découverte d'une fuite de données impliquant des enfants.
- La législation citée ne prévoit pas explicitement que l'éditeur doit bloquer l'accès à un réseau social tiers (Tchatlink) ; cette mesure relèverait d'une décision des autorités de régulation (ANTIC) et non de notre compétence directe.

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits connus : fuite de données, retard de notification, pression médiatique pour bloquer Tchatlink.
2. Rechercher les bases légales applicables aux obligations de l'éditeur en matière de sécurité et d'information des usagers.
3. Utiliser l'article 24 de la loi 2010/012 (E4) qui impose d'informer les usagers du danger, ce qui justifie l'action d'information immédiate.
4. Constater que les articles fournis (E1, E3) concernent les fournisseurs d'accès et les opérateurs, pas l'éditeur, donc aucune base légale directe pour bloquer Tchatlink.
5. Formuler des demandes aux autorités compétentes (APDP, ANTIC, MINESec) afin d'obtenir les instructions précises et combler les lacunes légales.
6. Mentionner les lacunes où la loi ne prévoit pas d'obligation de notification aux autorités ou de blocage de Tchatlink.

</details>


**Demande** — MinorShield → ART : Participer à la réunion de coordination pour analyser la hausse anormale et définir les mesures techniques de prévention conformément à l'article 27.

**Réponse de ART** (✅ étayée) : Nous confirmons la participation de l'ART à la réunion de coordination avec MinorShield afin d'analyser la hausse anormale et de définir les mesures techniques de prévention concernant les images et messages circulant sur Tchatlink, conformément à l'article 27 de la loi n° 2023/009.


**Demande** — MinorShield → MINPOSTEL : Fournir les capacités de filtrage réseau supplémentaires nécessaires pour renforcer le blocage des contenus suspectés d'extorsion.

**Réponse de MINPOSTEL** (✅ étayée) : MINPOSTEL s'engage à soutenir MinorShield dans le renforcement des capacités de filtrage réseau nécessaires pour bloquer les contenus suspectés d'extorsion. Nous allons mobiliser les opérateurs de télécommunications afin qu'ils mettent à disposition les ressources techniques additionnelles (bandes passantes, filtres DPI, listes noires actualisées) requises. Une fois les capacités identifiées, nous coordonnerons leur déploiement conformément au Plan d'Action National de Protection des Enfants en Ligne.


**Demande** — MinorShield → MINAS : Apporter un soutien en matière de sensibilisation des familles et des éducateurs aux bonnes pratiques de sécurité en ligne.

**Réponse de MINAS** (✅ étayée) : Nous allons mobiliser nos équipes pour concevoir et déployer des sessions de sensibilisation destinées aux familles et aux éducateurs, portant sur les bonnes pratiques de sécurité en ligne, la prévention du chantage numérique et la protection de la vie privée des enfants. Ces actions s'inscriront dans le cadre de la formation obligatoire du personnel intervenant auprès des enfants prévue par la loi.


**Demande** — MinorShield → APDP : Confirmer que le traitement des données agrégées et anonymisées respecte les exigences de protection des données personnelles des enfants.

**Réponse de APDP** (✅ étayée) : Le traitement des données agrégées et anonymisées peut être considéré conforme aux exigences de protection des données à caractère personnel des enfants, dans la mesure où les informations permettant d'identifier directement ou indirectement un enfant sont définitivement supprimées. Selon l'article 57 du RGPD (extrait E1), les autorités de contrôle doivent porter une attention particulière aux activités destinées spécifiquement aux enfants et veiller à ce que les traitements respectent les garanties requises. En l'absence d'identifiants personnels, le traitement ne constitue pas une violation du principe de minimisation ni du droit à la protection des données des enfants. Toutefois, il convient de vérifier que le processus d'anonymisation est irréversible et documenté, et de maintenir une traçabilité afin de pouvoir démontrer la conformité en cas de contrôle.


### ⚖️ Analyse du conseiller juridique

Le cadre juridique camerounais autorise la suspension ciblée de contenus illicites (E1) et donne à l'ANTIC le pouvoir d'agir en l'absence d'infractions pénales (E4), mais il ne prévoit pas le blocage total d'une plateforme ni une procédure claire de partage de logs. Ces lacunes contrastent avec les pratiques australienne et britannique qui offrent des mécanismes de blocage plus étendus. Il est recommandé d'amender la charte pour inclure un pouvoir de blocage total encadré juridiquement et d'établir un protocole de coopération entre ANTIC, ART et les opérateurs.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | Continuer la collecte et l'analyse des données agrégées et anonymisées sur les contenus bloqués, en appliquant les filtres de détection d'argot suspect et en générant un rapport d'évolution quotidien. | ⚠️ à vérifier | Aucun extrait de droit camerounais n'est invoqué pour justifier explicitement la collecte de données agrégées. Le principe de protection des enfants (E5, E6) suggère une action préventive, mais la base légale précise n'est pas citée. |
| MinorShield | Transmettre le rapport d'évolution à l'ANTIC et aux opérateurs afin de soutenir la coordination déjà engagée. | ⚠️ à vérifier | Aucun extrait ne prévoit spécifiquement la transmission de rapports par un tiers privé. La coopération entre autorités (E4, E6) est prévue, mais la légitimité de MinorShield à le faire n'est pas explicitée. |
| ANTIC | Lancer la mise en œuvre des mesures préventives et répressives prévues par l'article 27 pour stopper la diffusion des contenus de chantage, en coordination avec l'ART et les opérateurs. | ✅ fondée | L'action s'appuie sur l'article 27 (E4) qui confère à l'organe de régulation des TIC le pouvoir de prendre des mesures lorsque les atteintes ne constituent pas d'infractions pénales. |
| ANTIC | Émettre une mise en demeure aux opérateurs et à Tchatlink pour obtenir les logs détaillés (adresses IP, horodatage) afin d'identifier les auteurs des contenus illicites. | ❌ non fondée | L'article 14 (E1) autorise la suspension d'accès à la demande des autorités, mais ne prévoit pas explicitement la demande de logs détaillés. Aucun extrait ne justifie ce type de mise en demeure. |

**Lacune : Absence de pouvoir légal permettant un blocage total d'une plateforme de réseau social sur l'ensemble du territoire.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226
- Australie : L'Online Safety Act 2021 autorise le Commissaire à ordonner le blocage d'un service en ligne lorsqu'il contient du matériel préjudiciable aux enfants. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 78/157))*
- Royaume-Uni : L'Online Safety Act 2023 permet à un tribunal d'émettre une ordonnance d'interdiction d'accès temporaire à un service en ligne. *(Online Safety Act 2023 (United Kingdom, 2023 c. 50)] (partie 193/388))*
- **Recommandation :** Introduire un article spécifique (ex. article X) dans la Charte de protection des enfants en ligne prévoyant le blocage total d'une plateforme à la demande de l'ANTIC, après avis de l'ART et sous contrôle judiciaire, afin d'harmoniser le cadre avec les pratiques australienne et britannique.

**Lacune : Manque de procédure claire pour la collecte et le partage de données de logs par les fournisseurs d'accès à Internet avec les autorités de régulation.**

- Droit camerounais : E14
- États-Unis : Le COPPA prévoit que les opérateurs peuvent fournir des informations aux autorités pour des enquêtes de sécurité publique, sous réserve de garanties de confidentialité. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 16/24))*
- **Recommandation :** Élaborer un protocole national (décret d'application) détaillant les obligations de remise de logs aux autorités, incluant des garanties de protection des données conformément à la loi sur la protection des données personnelles (APDP).

**Conflits :**
- Article 27 (E4) autorise des mesures préventives sans sanction pénale, alors que l'article 14 (E1) ne prévoit que la suspension ciblée d'un utilisateur, créant une tension entre la possibilité de bloquer un contenu spécifique et l'absence de pouvoir de bloquer une plateforme entière.

**Problèmes de coordination :**
- La proposition de MinorShield de transmettre des rapports directement aux opérateurs contourne le processus de coordination prévu entre l'ANTIC, l'ART et les opérateurs (E4, E6), ce qui risque de créer des doublons et des incohérences dans les réponses.
