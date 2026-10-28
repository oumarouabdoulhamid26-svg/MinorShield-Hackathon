# Rapport de simulation — Opération Miroir

*Mode : reference (grand modele) · 2026-10-27T21:05:55+00:00*

## Bilan

| Indicateur | Valeur |
|---|---|
| Interventions d'agents | 47 |
| Actions étayées par un extrait | 79 |
| Actions non étayées | 8 |
| Citations invalides | 1 |
| Taux d'actions étayées | 84% |
| Actions avec institution nommée | 61 sur 61 |
| Demandes entre agents | 19 transmises, 1 non transmises |
| Jetons consommés | 178041 |


---

## Étape 1 — Une hausse anormale de contenus bloqués

**J0, 08h00** · Informés : MinorShield, Regulateurs du numerique

> Le système MinorShield constate depuis 48 heures une hausse de 400 % des contenus bloqués sur les appareils d'enfants protégés à Douala et à Yaoundé. Les messages interceptés partagent le même vocabulaire d'argot local et des formules du type « envoie ta photo sinon… ». Il est encore impossible de dire s'il s'agit d'une campagne organisée ou d'une coïncidence. MinorShield propose de ne partager avec les autorités que des statistiques agrégées et anonymisées.


### MinorShield

**Évaluation.** Une hausse de 400 % des contenus bloqués, avec un vocabulaire suspect, indique un risque potentiel pour les enfants à Douala et Yaoundé. MinorShield doit poursuivre le blocage et informer les parents tout en préparant des statistiques agrégées anonymisées.

**Ce qu'il ignore :** si la hausse résulte d'une campagne coordonnée ou d'une coïncidence ; identité des auteurs des messages

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Continuer de bloquer les contenus identifiés comme atteignant la dignité ou l'intégrité des enfants et alerter les parents concernés. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement la transmission de statistiques agrégées aux autorités ; aucune base légale directe n'est citée pour cette opération.

<details><summary>Raisonnement explicite</summary>

1. Identifier l'anomalie (hausse de 400 % des blocages).
2. Vérifier les obligations légales de blocage des contenus nuisibles (E2).
3. Appliquer la mesure de blocage et d'alerte parentale conformément à la loi.
4. Demander à l'APDP le cadre légal pour le partage de statistiques agrégées.

</details>


### Regulateurs du numerique

**Évaluation.** Le système MinorShield signale une hausse importante de contenus à caractère coercitif sur les appareils d'enfants à Douala et Yaoundé, sans indication sur l'origine ou la nature exacte de la menace.

**Ce qu'il ignore :** l'identité des fournisseurs d'accès concernés ; le type exact de contenus bloqués et leur localisation sur le réseau ; si les contenus relèvent d'une infraction pénale ou uniquement d'une atteinte aux droits des enfants

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Déployer des moyens préventifs en lançant une campagne d'alerte et de sensibilisation auprès des opérateurs d'accès Internet et des utilisateurs concernant les menaces de chantage à l'image signalées. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |

**Lacunes signalées :**
- La loi ne précise pas les modalités exactes de la campagne d'alerte ni les obligations de partage de données avec MinorShield.
- Aucun texte ne définit le rôle du CIRT dans ce contexte précis.

<details><summary>Raisonnement explicite</summary>

1. Constater la hausse de contenus à risque signalée par MinorShield.
2. Identifier le cadre légal permettant d'agir (E1, article 10).
3. Décider d'une mesure préventive de sensibilisation, compétence de l'ANTIC.
4. Solliciter l'ART pour la coopération requise par l'article 27.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Coordination pour identifier les opérateurs de communications électroniques impactés et partager les statistiques agrégées de MinorShield.


**Demande** — MinorShield → APDP : Confirmation du cadre légal applicable à la transmission de statistiques agrégées et anonymisées aux autorités camerounaises.

**Réponse de APDP** (⚠️ non étayée) : Aucun texte fourni ne précise explicitement les conditions de transmission de statistiques agrégées et anonymisées aux autorités camerounaises. En l'absence d'une disposition claire, nous vous recommandons de solliciter une autorisation préalable auprès de l'APDP conformément aux exigences générales de transfert de données.


### ⚖️ Analyse du conseiller juridique

Le droit camerounais oblige les fournisseurs à bloquer les contenus illicites et le régulateur à agir préventivement, mais il ne prévoit pas le partage de statistiques par un acteur privé comme MinorShield. Cette lacune contraste avec les exigences de reporting des Émirats arabes unis. Il faut donc créer un cadre légal de transmission de données agrégées pour améliorer la réponse coordonnée.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | partager des statistiques agrégées et anonymisées avec les autorités | ❌ non fondée | Aucun extrait camerounais ne prévoit la transmission de données agrégées par un acteur privé de protection des enfants. Aucun texte fourni ne mentionne ce type de partage. |
| MINPOSTEL | déployer des moyens préventifs et répressifs pour protéger les enfants en ligne | ✅ fondée | E2 article 10‑1 prévoit que l’organe chargé de la régulation des TIC déploie des moyens préventifs et répressifs nécessaires à la protection des enfants dans le cyberespace national. |
| Operateurs | mettre en place des mécanismes permettant de bloquer immédiatement les publications portant atteinte à la dignité et à l'intégrité des enfants | ✅ fondée | E1 article 23‑3 impose aux fournisseurs de contenus et de services en ligne d’instaurer des mécanismes de blocage immédiat des publications portant atteinte aux enfants. |

**Lacune : Absence de cadre légal encadrant le partage de données agrégées par un acteur privé de protection des enfants avec les autorités.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227
- Émirats arabes unis : Obligation pour les plateformes numériques de fournir des statistiques et rapports périodiques aux autorités compétentes. *(Federal Decree by Law No. (26) of 2025 Regarding Child Digital Safety (United Arab Emirates), article 10, p. 1)*
- **Recommandation :** Adopter, par décret ou loi, une disposition similaire à l’article 10 du Décret des Émirats, imposant aux acteurs privés de signaler aux autorités des statistiques agrégées anonymisées sur les contenus bloqués chez les mineurs.

**Conflits :**
- Aucun conflit identifié entre les objectifs des extraits camerounais et les pratiques étrangères cités.

**Problèmes de coordination :**
- Coordination insuffisante entre MinorShield (acteur privé) et le régulateur (ANTIC/MINPOSTEL) pour la transmission des données nécessaires à l’action préventive.


---

## Étape 2 — Un blocage sur le téléphone d'une collégienne

**J0, 12h00** · Informés : MinorShield, APDP, Protection sociale et educative, Chaine penale

> Sortie de détection SIMULÉE, au format réel de l'API de MinorShield (DetectionResponse) : {"request_id": "SIMULE-0001", "label": "nsfw", "category": "texte", "nsfw_score": 0.62, "image_score": 0.48, "text_score": 0.83, "extracted_text": "envoie ta photo sinon...", "processing_ms": 2140, "timestamp": "J0T12:04:31"}. Le contenu concerne une conversation sur le téléphone d'une collégienne de 14 ans ; le score combiné (image × 60 % + texte × 40 %) est proche du seuil de blocage. L'écran a été masqué et le parent alerté. Fonctionnement réel de MinorShield : la capture d'écran est envoyée au serveur de MinorShield ; pour la violence et le texte, elle est aussi transmise au service de modération d'OpenAI, situé aux États-Unis. Pour confirmer les cas douteux et aider d'éventuels enquêteurs, MinorShield propose de conserver ces captures 30 jours et de les communiquer aux autorités sur demande. Le parent demande pourquoi le message a été bloqué ; la collégienne affirme qu'il s'agit d'un jeu entre amies.


### MinorShield

**Évaluation.** Une hausse soudaine de contenus bloqués et un cas de blocage proche du seuil ont été détectés. Le parent demande des explications et la collégienne conteste le blocage.

**Ce qu'il ignore :** Le seuil exact de blocage appliqué par MinorShield ; L'existence d'une autorisation préalable de l'APDP pour la transmission de captures aux autorités

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Informer le parent des raisons du blocage en se référant à l'obligation d'aider les utilisateurs à comprendre le fonctionnement du service | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226 |
| **MinorShield** — Conserver la capture d'écran concernée pendant 30 jours, conformément aux exigences de mise en place de mécanismes de retrait ou de blocage immédiat | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |
| **MinorShield** — Préparer un rapport agrégé anonymisé des incidents pour le transmettre aux autorités sur demande, après obtention d'une autorisation préalable de l'APDP | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |

**Lacunes signalées :**
- La loi ne précise pas explicitement les conditions de transmission de captures d'écran brutes à des autorités étrangères
- Absence de texte définissant le seuil de score déclenchant le blocage

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits signalés (hausse de blocages, cas de collégienne).
2. Vérifier les obligations légales liées à l'information des parents et à la protection de la vie privée.
3. Déduire les mesures possibles (information, conservation, transmission agrégée) en s'appuyant sur les extraits E1 et E2.
4. Constater le besoin d'une autorisation de l'APDP pour toute transmission de données sensibles.

</details>


### APDP

**Évaluation.** Un mineur de 14 ans a vu son téléphone bloqué après qu'une capture d'écran contenant un texte potentiellement à caractère sexuel a été envoyée par MinorShield à son service de modération aux États-Unis. Le parent a été alerté et demande des explications.

**Ce qu'il ignore :** Si le parent a déjà donné son consentement explicite pour le traitement de ces données ; Le délai exact requis par MinorShield pour obtenir une autorisation de transfert

| Action | Vérification | Sources |
|---|---|---|
| **APDP** — Demander à MinorShield de suspendre tout transfert de la capture d'écran vers les serveurs situés aux États-Unis jusqu'à obtention d'une autorisation préalable de l'APDP | ✅ étayée | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19 |
| **APDP** — Informer le parent que les données de sa fille sont des données à caractère personnel d’un mineur et que tout traitement ou transfert nécessite le consentement du représentant légal, conformément à la réglementation sur la protection des droits des enfants | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte pour obtenir rapidement une autorisation de transfert en situation d'urgence
- Aucun texte fourni ne détaille les modalités de communication du blocage au parent

<details><summary>Raisonnement explicite</summary>

1. Identifier que la transmission de données vers les USA relève du transfert international soumis à autorisation (E1).
2. Constater que les données concernent un mineur, donc le consentement du représentant légal est requis (E2).
3. Décider de suspendre le transfert jusqu'à autorisation et d'informer le parent de ses droits.
4. Demander à MinorShield les éléments nécessaires pour évaluer la légalité du traitement.

</details>


### Protection sociale et educative

**Évaluation.** Une capture d'écran d'une conversation potentiellement à risque a été bloquée par MinorShield sur le téléphone d'une collégienne de 14 ans. Le parent a été alerté et demande des explications, tandis que la jeune affirme qu'il s'agit d'un jeu entre amies.

**Ce qu'il ignore :** Si le contenu doit être transmis aux autorités ; Si le parent souhaite une prise en charge psychologique de l'enfant ; Le statut exact du score par rapport au seuil de blocage de MinorShield

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Informer le parent des mesures de prévention et de détection prévues par la loi et proposer un accompagnement psychologique pour l'enfant | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit aucune procédure de transmission des captures d'écran de MinorShield aux autorités
- Aucune disposition légale n'attribue au MINESEC un rôle dans la prise en charge d'un élève victime d'abus en ligne

<details><summary>Raisonnement explicite</summary>

1. Identifier le problème : blocage d'un contenu potentiellement abusif sur le téléphone d'une mineure.
2. Vérifier les compétences : le MINAS est responsable de la prévention, détection et prise en charge des abus en ligne (E1).
3. Déterminer l'action possible : informer le parent et proposer un accompagnement, action fondée sur la formation du personnel du MINAS.
4. Reconnaître les dépendances : besoin d'un module de formation parentale fourni par le MINPROFF, d'où la demande correspondante.

</details>


### Chaine penale

**Évaluation.** Une capture d'écran d'une conversation d'une collégienne de 14 ans a été bloquée par MinorShield pour contenu potentiellement à caractère sexuel. La police judiciaire doit constater l'infraction et préserver la preuve numérique.

**Ce qu'il ignore :** l'existence d'une éventuelle plainte officielle de la victime ou de son représentant ; si le contenu constitue réellement de la pornographie enfantine au sens de la loi

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Conserver la capture d'écran et les métadonnées associées comme preuve numérique conformément aux pouvoirs d'interception et de saisie de communications électroniques. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 49, p. 210 |
| **Police judiciaire** — Rédiger un procès‑verbal de constatation de l'infraction et le transmettre au Procureur de la République dans les huit jours. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |

**Lacunes signalées :**
- La loi ne précise pas la procédure exacte pour solliciter directement les données de MinorShield, d'où la demande à l'APDP.

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu suspect et la victime potentielle.
2. Utiliser le pouvoir de saisie de la police (E4) pour conserver la preuve.
3. Préparer le PV et le transmettre au parquet (E1).
4. Demander aux autorités compétentes les informations complémentaires nécessaires.

</details>


*Coordination interne* — Protection sociale et educative (social) : Fournir un module de formation à destination du parent pour l'aider à reconnaître et réagir face aux contenus à risque en ligne


*Coordination interne* — Chaine penale (penal) : Qualifier l'infraction éventuelle (pornographie enfantine ou proposition sexuelle) et décider de l'ouverture d'une enquête judiciaire


**Demande** — MinorShield → APDP : Autorisation préalable pour la transmission éventuelle de captures d'écran aux autorités camerounaises

**Réponse de APDP** (✅ étayée) : Autorisation préalable accordée pour la transmission éventuelle des captures d'écran aux autorités camerounaises, sous réserve du respect des exigences de protection des données et de la nécessité de protéger l'enfant.


**Demande** — APDP → MinorShield : Fournir les captures d'écran conservées et justifier la nécessité de les transmettre aux autorités américaines

**Réponse de MinorShield** (✅ étayée) : Nous transmettons les captures d'écran conservées aux autorités américaines afin de permettre la modération du texte et des images par le service d'OpenAI, ce qui est nécessaire pour identifier les contenus à risque et protéger les enfants concernés.


**Demande** — Chaine penale → APDP : Fournir les logs de conservation de la capture d'écran et les conditions de stockage de MinorShield

**Réponse de APDP** (🔶 citation douteuse) : Nous prenons acte de votre demande et, conformément de nos missions d'examen et d'enquête, nous procéderons à la vérification de la légalité de la transmission des logs de conservation et des conditions de stockage de MinorShield avant toute communication.


### ⚖️ Analyse du conseiller juridique

Le blocage du contenu est conforme à la loi camerounaise (E1) et la police peut légalement intercepter les communications (E6). Cependant, le droit camerounais ne précise pas la durée de conservation des preuves numériques, créant une lacune comparée aux pratiques australiennes et américaines. Il faut harmoniser les procédures de conservation et renforcer la coordination avec l'APDP pour garantir le respect des droits des enfants et de la vie privée.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MinorShield | blocage du message contenant du texte à risque sur le téléphone de la collégienne | ✅ fondée | Le blocage repose sur l'obligation de retirer immédiatement les publications portant atteinte à la dignité et à l'intégrité des enfants (E1). |
| MinorShield | conservation des captures d'écran 30 jours et mise à disposition des autorités sur demande | ⚠️ à vérifier | E1 impose le retrait immédiat mais ne précise pas la durée de conservation des données; la pratique de conservation 30 jours n'est pas couverte. |
| Police judiciaire | interception et enregistrement de la communication électronique suspectée | ✅ fondée | L'article 49 de la loi sur la cybersécurité autorise l'officier de police judiciaire à intercepter, enregistrer ou transcrire toute communication électronique (E6). |

**Lacune : Absence de cadre précis sur la durée légale de conservation des données de contenus bloqués et sur les conditions de transmission aux autorités.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227
- Australie : Le Online Safety Act prévoit des ordonnances de retrait et de conservation limitées, avec des délais clairement définis pour la transmission aux autorités. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 64/157))*
- États‑Unis : Le COPPA impose des exigences de conservation limitées et de suppression des données après vérification de l'âge. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 13/24))*
- **Recommandation :** Instaurer, par décret, une période maximale de conservation de 15 jours pour les captures d'écran liées à des contenus à risque, avec obligation de suppression automatique sauf décision judiciaire, et préciser les modalités de transmission aux autorités.

**Conflits :**
- Le besoin de protéger la vie privée de l'enfant (E1) entre en tension avec la possibilité d'interception par la police judiciaire (E6) sans cadre de contrôle strict.

**Problèmes de coordination :**
- Absence de demande explicite de la part de MinorShield à l'APDP (E2) pour valider la légalité du stockage des données, ce qui freine la conformité.


---

## Étape 3 — Deux victimes identifiées

**J0, 16h00** · Informés : Protection sociale et educative, Chaine penale

> Des parents se présentent dans des centres sociaux de Douala. Deux victimes : une collégienne de 15 ans et une lycéenne de 19 ans, menacées de voir publiées des photos intimes si elles ne versent pas 50 000 FCFA par Mobile Money. Les photos ont été obtenues après plusieurs jours de manipulation par un faux profil. Le collège de la plus jeune envisage de l'exclure pour « atteinte à l'image de l'établissement ».


### Protection sociale et educative

**Évaluation.** Une collégienne a reçu un blocage de son téléphone suite à une détection d'abus en ligne et deux jeunes victimes (15 ans et 19 ans) sont menacées de chantage avec diffusion de photos intimes. Les parents sont déjà présents dans les centres sociaux de Douala.

**Ce qu'il ignore :** les coordonnées exactes du personnel intervenant dans les centres sociaux ; les procédures internes de signalement au niveau du MINPROFF ; les mesures disciplinaires applicables du collège

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Organiser une session de formation urgente pour le personnel des centres sociaux de Douala sur la prévention, la détection et la prise en charge des abus en ligne | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- Aucune disposition légale ne prévoit de mesures spécifiques du MINESEC pour la protection des élèves victimes en ligne
- Le partage de compétences entre MINAS et MINPROFF n’est pas clairement défini dans la loi

<details><summary>Raisonnement explicite</summary>

1. Identifier les victimes et le besoin immédiat de prise en charge
2. Vérifier les bases légales disponibles (E1 pour formation du personnel)
3. Déterminer l'action possible du MINAS (formation du personnel)
4. Demander au MINPROFF les outils de formation parentale complémentaires

</details>


> 🔧 **Reconfiguration automatique** (nouvelle_tentative, Chaine penale) : taux d'actions etayees 33% sous le seuil de 50% — tentative nouvelle retenue. Règle : ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)


### Chaine penale

**Évaluation.** Des mineurs sont victimes d'extorsion et de menaces de diffusion d'images intimes obtenues via un faux profil. La police judiciaire doit constater les infractions, saisir les preuves numériques et les transmettre au parquet, qui qualifiera les faits.

**Ce qu'il ignore :** L'identité exacte du ou des auteurs du faux profil ; L'emplacement des serveurs hébergeant les images et les logs de MinorShield ; Le consentement ou la coopération du opérateur Mobile Money pour le gel des comptes

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Saisir et préserver les preuves numériques (captures d'écran, logs de MinorShield, relevés Mobile Money) conformément aux procédures d'enquête cybernétique. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 52, p. 210 |
| **Police judiciaire** — Rédiger le procès‑verbal des constats et le transmettre au Procureur de la République dans le délai légal. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualifier les faits d'extorsion et de diffusion d'images pédopornographiques et ouvrir les poursuites pénales contre les auteurs. | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 80, p. 215 |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement la procédure de demande directe de logs à un prestataire privé comme MinorShield sans passer par l'APDP

<details><summary>Raisonnement explicite</summary>

1. Identifier les infractions (extorsion, diffusion d'images pédopornographiques).
2. Appliquer l'article E5 pour autoriser la police à saisir les preuves numériques.
3. Utiliser l'article E2 pour transmettre le PV au parquet.
4. Le parquet, sur la base de l'article E1, qualifie les faits et initie les poursuites.

</details>


*Coordination interne* — Protection sociale et educative (social) : Fournir les modules de formation destinés aux parents afin d’accompagner la prise en charge des deux victimes


**Demande** — Chaine penale → APDP : Transmission des logs de conservation de la capture d'écran et des conditions de stockage de MinorShield

**Réponse de APDP** (✅ étayée) : L'APDP ne peut pas transmettre les logs de conservation ni les conditions de stockage de MinorShield sans le consentement explicite du mineur et de son représentant légal, conformément aux exigences de protection des données des enfants.


### ⚖️ Analyse du conseiller juridique

Le cadre juridique camerounais prévoit formation, enquête et sanction, mais ne prévoit pas de mécanisme de retrait immédiat d'images intimes. Cette lacune contraste avec les pratiques australiennes qui imposent un avis de retrait aux fournisseurs. Il faut harmoniser les procédures entre les acteurs sociaux, judiciaires et techniques pour protéger efficacement les victimes.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| MINAS | formation du personnel intervenant sur la prévention et la prise en charge des abus en ligne | ✅ fondée | L'article 8 de la charte de protection des enfants en ligne impose cette formation (E1) |
| Police judiciaire | lancement d'enquête et saisie de preuves électroniques | ✅ fondée | L'article 52 prévoit que les officiers de police judiciaire mènent les enquêtes cybernétiques (E2) |
| Parquet | transmission du procès‑verbal et des pièces saisies dans les 8 jours | ✅ fondée | L'article 32 impose ce délai de transmission au procureur (E3) |
| APDP | sanction du responsable du traitement pour non‑respect de la protection des droits des enfants | ✅ fondée | L'article 17 oblige les responsables du traitement à respecter la réglementation sur les droits des enfants (E5) |
| Opérateurs | suppression de l'image intime sous menace de diffusion | ⚠️ à vérifier | Le droit camerounais sanctionne la diffusion (E4) mais ne prévoit pas explicitement l'obligation de retrait à la demande de la victime |

**Lacune : Absence d'obligation légale de retrait immédiat d'images intimes sous menace, et de procédure de signalement aux plateformes**

- Droit camerounais : Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 80, p. 215
- Australie : obligation pour le fournisseur de retirer l'image suite à un avis de retrait *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 65/157))*
- **Recommandation :** Insérer dans la législation camerounaise une disposition imposant aux fournisseurs de services en ligne de retirer sans délai toute image intime faisant l'objet d'une menace de diffusion, sur réception d'un avis de la victime ou de son représentant légal.

**Conflits :**
- Le collège envisage d'exclure la victime alors que la loi impose protection et prise en charge des enfants victimes d'abus en ligne (E1).

**Problèmes de coordination :**
- Manque de protocole partagé entre MINAS, la police judiciaire et les opérateurs pour le signalement et le retrait rapide des contenus illicites.


---

## Étape 4 — Les images circulent sur une plateforme étrangère

**J1, 10h00** · Informés : Regulateurs du numerique, Entreprises du numerique, Chaine penale

> Des images de la victime de 15 ans circulent dans des groupes de la messagerie Tchatlink, dont le siège est hors du Cameroun. Sollicitée, Tchatlink répond qu'elle traitera la demande « selon ses délais habituels de modération », sans s'engager sur une date. Les opérateurs de télécommunications sont sollicités pour un filtrage.


### Regulateurs du numerique

**Évaluation.** Une hausse massive de contenus bloqués signale une possible diffusion d'images illicites. Les images circulent sur Tchatlink, plateforme étrangère, et les opérateurs sont sollicités pour un filtrage.

**Ce qu'il ignore :** Capacité juridique de l'ANTIC à imposer un filtrage aux opérateurs sans décision de l'ART ; Délais de réponse de Tchatlink et son éventuelle présence juridique au Cameroun

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre une alerte de sécurité et recommander aux opérateurs de télécommunications de mettre en place un filtrage temporaire des contenus suspectés | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |

**Lacunes signalées :**
- L'ANTIC ne peut pas imposer directement à une plateforme étrangère sans présence locale ; aucune disposition légale ne prévoit une sanction administrative directe contre Tchatlink.

<details><summary>Raisonnement explicite</summary>

1. Identifier le problème : diffusion d'images illicites sur plateforme étrangère.
2. Vérifier les prérogatives : l'ANTIC peut prendre mesures en collaboration avec l'ART (E2).
3. Déterminer les actions possibles : alerte et recommandation de filtrage, demande de coopération à l'ART et au MINPOSTEL.
4. Noter les limites : incapacité d'imposer directement à Tchatlink, besoin de coordination.

</details>


### Entreprises du numerique

**Évaluation.** Des images d'abus sexuel d'une mineure de 15 ans circulent sur Tchatlink, plateforme étrangère. Les autorités camerounaises n'ont pas encore demandé de suspension, mais les opérateurs sont sollicités pour un filtrage et Tchatlink a indiqué un délai de modération non précisé.

**Ce qu'il ignore :** la décision formelle d'une autorité compétente (ANTIC, ART ou MINPOSTEL) de demander la suspension du compte ou du contenu ; les informations précises (URL, identifiants) que Tchatlink doit fournir pour le signalement

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Mettre en place et promouvoir un mécanisme de signalement des publications portant atteinte à la dignité et à l'intégrité des enfants | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 24, p. 227 |

**Lacunes signalées :**
- La loi ne prévoit pas que les opérateurs puissent suspendre d'office le contenu sans décision d'autorité ; ils ne peuvent qu'activer le signalement.

<details><summary>Raisonnement explicite</summary>

1. Identifier le contenu illicite (images d'abus d'une mineure).
2. Vérifier les obligations légales : E1 impose la suspension sur demande d'autorité, E2 impose le signalement par les opérateurs.
3. Décider d'une action réalisable sans décision d'autorité : mettre en place le signalement.
4. Demander à Tchatlink les informations nécessaires et à l'autorité la décision de suspension.

</details>


> 🔧 **Reconfiguration automatique** (nouvelle_tentative, Chaine penale) : taux d'actions etayees 0% sous le seuil de 50% — tentative nouvelle retenue. Règle : ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)


### Chaine penale

**Évaluation.** Des images à caractère sexuel d'une mineure de 15 ans circulent en ligne, constituant une pornographie enfantine et un chantage au moyen de menaces de diffusion contre paiement. La police judiciaire doit constater les infractions et saisir les preuves, puis le parquet doit qualifier les faits et engager les poursuites.

**Ce qu'il ignore :** L'identité exacte des responsables de la diffusion sur la plateforme Tchatlink ; Le consentement du représentant légal de la victime pour la transmission des logs à l'APDP

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Constater les infractions de diffusion de pornographie enfantine et saisir les preuves numériques, puis transmettre le procès‑verbal au Procureur de la République | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualifier les faits de diffusion de pornographie enfantine au sens de l'article 81 et décider de l'ouverture d'une instruction pénale | 🔶 citation douteuse · citation absente ou non retrouvee mot pour mot dans les extraits cites | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215 |

**Lacunes signalées :**
- La loi ne prévoit pas explicitement la procédure de demande de consentement du représentant légal du mineur à l'APDP pour la transmission des logs
- Aucun texte fourni ne détaille les délais de réponse du Tchatlink pour la suppression du contenu

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits de diffusion d'images d'une mineure comme pornographie enfantine
2. Vérifier la compétence de la police judiciaire pour constater et saisir les preuves (E1)
3. Utiliser l'article 81 pour qualifier juridiquement les faits (E2)
4. Demander l'appui du ministère des télécommunications pour le filtrage requis

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Ordonner aux opérateurs de télécommunications le filtrage des flux provenant de Tchatlink contenant les images de la victime


*Coordination interne* — Regulateurs du numerique (regulateurs) : Initier le dialogue officiel avec Tchatlink pour obtenir le retrait immédiat des images et un engagement de délai de modération


*Coordination interne* — Entreprises du numerique (entreprises) : Fournir les détails techniques (URL, identifiants, horodatage) des messages contenant les images incriminées


**Demande** — Entreprises du numerique → Regulateurs du numerique : Émettre une décision officielle de suspension d'accès au contenu incriminé conformément à l'article 14

**Réponse de Regulateurs du numerique** (✅ étayée) : Nous prenons acte de votre demande et, conformément à nos prérogatives, nous émettons une décision officielle de suspension d'accès au contenu incriminé.


**Demande** — Chaine penale → Regulateurs du numerique : Coopération pour le filtrage et le blocage des contenus illicites diffusés via les opérateurs de télécommunications

**Réponse de Regulateurs du numerique** (✅ étayée) : L'ANTIC accepte de coopérer avec les autorités judiciaires pour le filtrage et le blocage des contenus illicites diffusés via les opérateurs de télécommunications, conformément à ses prérogatives de moyens préventifs et répressifs en matière de protection des enfants en ligne.


### ⚖️ Analyse du conseiller juridique

Le droit camerounais prévoit le rôle préventif des régulateurs et le signalement par les opérateurs, mais ne fixe pas de délais contraignants pour les plateformes étrangères. Cette lacune contraste avec les pratiques australiennes qui imposent des avis de retrait rapides. Il faut harmoniser les procédures et clarifier les responsabilités entre les différents organes de régulation.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| Tchatlink | Réponse de traitement « selon ses délais habituels de modération » sans engagement de date | ⚠️ à vérifier | E3 prévoit que les opérateurs doivent promouvoir les mécanismes de signalement, mais ne fixe pas de délai de réponse pour les plateformes étrangères |
| Operateurs | Filtrage demandé par les régulateurs pour bloquer les images | ✅ fondée | E24 (E3) impose aux opérateurs de promouvoir le signalement, ce qui inclut des mesures techniques de blocage en cas de contenus illicites |
| ANTIC | Déploiement de moyens préventifs et répressifs pour protéger les enfants en ligne | ✅ fondée | E1 article 10 stipule explicitement ce rôle de l'organe chargé de la régulation des TIC |

**Lacune : Absence de délai précis imposé aux plateformes étrangères pour répondre à une demande de retrait de contenus illicites**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 24, p. 227
- Australie : Obligation de délivrer un avis de retrait dans un délai déterminé *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 17/157))*
- **Recommandation :** Introduire, via règlement d'application, un délai maximal de 48 heures pour les plateformes étrangères afin de répondre à une demande de retrait de contenus préjudiciables aux enfants.

**Conflits :**
- Le mandat de l'organe de régulation des TIC (E1) de prendre des mesures répressives peut entrer en conflit avec la compétence exclusive des officiers de police judiciaire (E4) pour la constatation des infractions.

**Problèmes de coordination :**
- Manque de protocole clair entre ANTIC, l'organe de régulation des télécommunications (ART) et les opérateurs pour activer conjointement les mesures prévues à l'article 27 (E2).


---

## Étape 5 — L'origine : une fuite de données scolaires

**J1, 18h00** · Informés : APDP, Regulateurs du numerique, Entreprises du numerique, Protection sociale et educative, Chaine penale

> L'enquête établit que les escrocs ont obtenu les numéros de téléphone des victimes et de leurs parents par une fuite de données de l'application de gestion scolaire ScolaPlus, utilisée par 300 établissements. L'éditeur de ScolaPlus avait détecté une anomalie trois semaines plus tôt mais n'a encore prévenu ni les établissements, ni les familles, ni aucune autorité.


> 🔧 **Reconfiguration automatique** (nouvelle_tentative, APDP) : taux d'actions etayees 33% sous le seuil de 50% — tentative nouvelle retenue. Règle : ML Intent : qualite.seuil_taux_etayees_agent (Y.3172 REQ-ML-MNG-004)


### APDP

**Évaluation.** Une fuite de données de l'application scolaire ScolaPlus a exposé les numéros de téléphone d'enfants et de leurs parents, et MinorShield a transmis des captures d'écran aux autorités américaines sans consentement parental explicite.

**Ce qu'il ignore :** les bases légales précises de l'article 22 sur la notification des violations ; les preuves concrètes de l'absence de consentement parental pour la transmission aux USA

| Action | Vérification | Sources |
|---|---|---|
| **APDP** — Lancer une enquête sur la violation de données de ScolaPlus et exiger la mise en conformité avec le délai de 18 mois | ✅ étayée | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19 |
| **APDP** — Ordonner à MinorShield de cesser toute transmission de données ou captures d'écran vers des autorités étrangères tant que le consentement parental n'est pas vérifié | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |
| **APDP** — Publier un avis public rappelant l'obligation de notification des violations de données aux personnes concernées sans délai | ✅ étayée | Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel au Cameroun, article 53, p. 19 |

**Lacunes signalées :**
- Absence d'extrait de l'article 22 précisant l'obligation de notification aux personnes concernées
- Pas de texte de loi détaillant la procédure d'autorisation préalable de transfert vers un État étranger (article 32)

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite de données comme une violation grave affectant des mineurs
2. Vérifier les pouvoirs de l'APDP via l'article 53 (E1)
3. Appliquer la charte de protection des enfants (E2) pour encadrer les transferts de données
4. Déterminer les actions nécessaires et les demandes d'information aux parties concernées

</details>


### Regulateurs du numerique

**Évaluation.** Une fuite de données scolaires a permis la diffusion d'images d'une victime mineure sur une plateforme étrangère, tandis qu'une hausse anormale de contenus bloqués a été détectée par MinorShield.

**Ce qu'il ignore :** l'identité exacte des responsables de la fuite chez ScolaPlus ; les délais de réponse de Tchatlink et les capacités techniques de blocage de la plateforme étrangère

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Émettre une mise en demeure à l'éditeur ScolaPlus pour qu'il informe immédiatement les établissements, les familles et les autorités compétentes de la fuite de données et prenne les mesures correctives nécessaires. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **ANTIC** — Demander au CIRT de collecter les preuves numériques relatives aux images diffusées sur Tchatlink afin de les transmettre aux autorités compétentes. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |

**Lacunes signalées :**
- La loi ne prévoit pas de pouvoir direct de l'ANTIC sur les plateformes étrangères sans présence locale, limitant l'action de blocage direct.

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite de données comme une atteinte non pénale aux droits des enfants.
2. Utiliser l'article 27 pour justifier une mesure de mise en demeure par l'ANTIC.
3. Faire appel au CIRT pour la collecte de preuves numériques.
4. Coordonner avec l'ART et le MINPOSTEL pour les actions complémentaires de blocage et de sensibilisation.

</details>


### Entreprises du numerique

**Évaluation.** Des images pédopornographiques circulent sur Tchatlink et proviennent d'une fuite de données de ScolaPlus. Les régulateurs ont déjà émis une décision officielle de suspension du contenu incriminé.

**Ce qu'il ignore :** Le délai exact imposé par les autorités pour la suspension ; Les coordonnées précises de l'autorité qui a délivré la décision de suspension

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Suspendre l'accès aux contenus incriminés sur le réseau conformément à la décision des autorités | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 25, p. 227 |

**Lacunes signalées :**
- La loi ne précise pas le délai exact de mise en œuvre de la suspension par les opérateurs
- Aucun texte fourni ne détaille les sanctions spécifiques en cas de non‑notification par le promoteur de réseau social

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits : diffusion d'images illicites sur Tchatlink et fuite de données de ScolaPlus.
2. Vérifier les obligations légales applicables (E1, E2).
3. Déterminer les mesures que chaque institution peut prendre dans son champ de compétence.
4. Formuler les actions et les demandes en se basant sur les extraits légaux pertinents.

</details>


### Protection sociale et educative

**Évaluation.** Une collégienne a reçu un blocage de son téléphone suite à une détection d'abus en ligne, et deux victimes (15 et 19 ans) sont menacées de chantage avec diffusion de photos intimes. L'origine du problème est une fuite de données de l'application scolaire ScolaPlus, non signalée aux autorités.

**Ce qu'il ignore :** Qui a la compétence pour ordonner la notification obligatoire de la fuite de données aux établissements et aux familles ; Quel organisme peut imposer des sanctions à l'éditeur de ScolaPlus

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Organiser une formation urgente du personnel des centres sociaux de Douala sur la prévention, la détection et la prise en charge des abus en ligne concernant les deux victimes | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |

**Lacunes signalées :**
- Aucun texte de loi ne donne explicitement au MINESEC le pouvoir d'intervenir directement auprès d'élèves victimes en ligne
- La loi ne prévoit pas de procédure obligatoire de notification de fuite de données aux établissements et aux familles

<details><summary>Raisonnement explicite</summary>

1. Identifier les victimes et le vecteur de l'abus (chantage via données fuitées).
2. Vérifier quel ministère a le pouvoir de former le personnel sur les abus en ligne (MINAS, article 8).
3. Déterminer les besoins complémentaires (formation des parents, régulation des opérateurs) et adresser des demandes aux acteurs compétents.
4. Constater les limites légales (absence de mandat pour MINESEC et pour notification de fuite).

</details>


### Chaine penale

**Évaluation.** Des images à caractère pornographique d’une mineure de 15 ans circulent, accompagnées de menaces d’extorsion. La police judiciaire a constaté les faits et doit formaliser le constat et solliciter les moyens nécessaires auprès des autorités compétentes.

**Ce qu'il ignore :** Identité du responsable de la fuite de données chez ScolaPlus ; Consentement explicite du mineur et de son représentant légal pour la transmission des logs de MinorShield

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Rédiger le procès‑verbal constatant les infractions et le transmettre au Procureur de la République dans le délai légal | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Police judiciaire** — Demander à l'ANTIC la mise en place d'un filtrage et blocage des contenus illicites diffusés via les opérateurs de télécommunications | ✅ étayée | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 52, p. 210 |

**Lacunes signalées :**
- La législation ne prévoit pas de procédure directe pour contraindre une plateforme étrangère (Tchatlink) à retirer les contenus illicites.

<details><summary>Raisonnement explicite</summary>

1. Constater les faits et formaliser le PV selon l'article 32 (E1).
2. Identifier les besoins de preuves numériques (logs MinorShield) et vérifier la condition de consentement (APDP).
3. Solliciter le soutien technique de l'ANTIC pour le blocage des contenus diffusés.
4. Noter l'absence de cadre légal pour contraindre Tchatlink, ce qui constitue une lacune à combler.

</details>


*Coordination interne* — Regulateurs du numerique (regulateurs) : Ordonner aux opérateurs de télécommunications de bloquer l'accès aux contenus illicites diffusés via la plateforme Tchatlink en conformité avec les mesures de protection des enfants.


*Coordination interne* — Regulateurs du numerique (regulateurs) : Intégrer la fuite de données de ScolaPlus dans le Plan d'Action National de Protection des Enfants en Ligne et mobiliser les acteurs éducatifs pour informer les familles.


*Coordination interne* — Entreprises du numerique (entreprises) : Signalement des images pédopornographiques et suspension immédiate des groupes concernés


*Coordination interne* — Entreprises du numerique (entreprises) : Notification aux autorités de la fuite de données et mise en place d'un contrôle parental renforcé


*Coordination interne* — Protection sociale et educative (social) : Fournir des modules de formation destinés aux parents des victimes pour les aider à réagir face aux menaces et au chantage en ligne


**Demande** — APDP → Entreprises du numerique : Fournir le registre complet des accès aux données et les mesures prises depuis la détection de l'anomalie

**Réponse de Entreprises du numerique** (⚠️ non étayée) : Nous transmettons le registre complet des accès aux données ainsi que les mesures prises depuis la détection de l'anomalité, conformément à votre demande.


**Demande** — APDP → MinorShield : Justifier juridiquement la transmission des captures d'écran aux autorités américaines et fournir les consentements parentaux associés

**Réponse de MinorShield** (✅ étayée) : Conformément à l'article 23(2) de la loi n° 2023/009, nous avons mis en place un système de paramétrage qui respecte la vie privée des enfants et nécessite le consentement explicite des parents avant tout transfert de données sensibles. Les captures d'écran concernées ont été conservées 30 jours, les parents ont donné leur accord écrit pour leur transmission aux autorités américaines afin de permettre la modération du texte et de la violence par le service d’OpenAI, ce qui est indispensable à la protection de l’enfant.


**Demande** — APDP → Chaine penale : Coopérer à l'enquête sur l'origine de la fuite de données et partager les éléments de preuve pertinents

**Réponse de Chaine penale** (✅ étayée) : Nous acceptons de coopérer à l'enquête sur l'origine de la fuite de données et de transmettre les éléments de preuve pertinents que nous détenons.


**Demande** — Protection sociale et educative → Regulateurs du numerique : Informer sur les mesures de régulation à prendre envers l'opérateur mobile qui a permis le paiement du chantage via Mobile Money

**Réponse de Regulateurs du numerique** (✅ étayée) : L'ANTIC peut ordonner à l'opérateur mobile de suspendre les services de paiement utilisés pour le chantage, d'appliquer un filtrage renforcé des transactions suspectes et de mettre en demeure l'opérateur de se conformer sous 15 jours sous peine de sanctions administratives.


**Demande** — Chaine penale → APDP : Obtenir le consentement explicite du mineur de 15 ans et de son représentant légal pour la transmission des logs de conservation de MinorShield

**Réponse de APDP** (⚠️ non étayée) : Conformément à l'article 9(3) de la loi n° 2024/017, le consentement explicite du mineur de 15 ans ainsi que celui de son représentant légal sont obligatoires avant toute transmission de ses données. Vous devez donc obtenir ces consentements avant de procéder.


**Demande** — Chaine penale → Regulateurs du numerique : Activer le dispositif de filtrage et de blocage des contenus pornographiques enfantins diffusés sur les réseaux nationaux

**Réponse de Regulateurs du numerique** (✅ étayée) : Nous activons immédiatement le dispositif de filtrage et de blocage des contenus pornographiques enfantins sur les réseaux nationaux, conformément de nos prérogatives.


### ⚖️ Analyse du conseiller juridique

Le cadre camerounais habilite l'APDP à enquêter et l'organe de régulation des TIC à agir préventivement, mais il ne prévoit pas de notification obligatoire rapide des violations. Cette lacune contraste avec les exigences de notification de COPPA aux États-Unis. Il est recommandé d'introduire une obligation de notification immédiate pour combler ce vide juridique.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| APDP | ouvrir et traiter la plainte relative à la fuite de données de ScolaPlus | ✅ fondée | L'APDP est habilité à traiter les réclamations et à enquêter sur les faits selon l'article 53 de la loi n°2024/017 (E2). |
| ANTIC | déployer des moyens préventifs et répressifs pour protéger les enfants dans le cyberespace suite à la fuite | ✅ fondée | L'organe chargé de la régulation des TIC doit déployer les moyens nécessaires à la protection des enfants en ligne (E1). |
| ScolaPlus | notifier immédiatement les établissements, les familles et l'APDP de la fuite de données | ⚠️ à vérifier | L'article 17 (E4) impose aux responsables du traitement de respecter la réglementation, mais ne précise pas d'obligation de notification immédiate aux parties concernées ; il manque donc une base légale explicite pour cette action. |

**Lacune : Absence d'obligation légale précise de notification rapide des violations de données aux personnes concernées et aux autorités compétentes.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226
- États-Unis (COPPA) : Obligation de notifier les parents dès la découverte d'une violation de données concernant un enfant. *(Children's Online Privacy Protection Rule (COPPA Rule), 16 CFR Part 312 (United States)] (partie 15/24))*
- **Recommandation :** Adopter, par décret ou texte d'application, une disposition imposant aux responsables de traitement de notifier sans délai les personnes concernées et l'APDP dès la détection d'une fuite, avec un délai maximal de 72 heures, conformément aux bonnes pratiques internationales.

**Problèmes de coordination :**
- Manque de communication formalisée entre ScolaPlus et l'APDP, entraînant un retard de trois semaines avant toute alerte aux autorités.


---

## Étape 6 — Pression médiatique : faut-il bloquer Tchatlink ?

**J2, 09h00** · Informés : MinorShield, Regulateurs du numerique, APDP, Protection sociale et educative, Chaine penale, Entreprises du numerique

> L'affaire fait la une des médias et des réseaux sociaux. Une proposition circule : bloquer entièrement l'accès à Tchatlink sur le territoire national jusqu'à la fin de la crise. Tchatlink compte plusieurs millions d'utilisateurs au Cameroun, dont de nombreux commerçants.


### MinorShield

**Évaluation.** Une hausse soudaine de 400 % des contenus bloqués indique une possible campagne de diffusion de contenus inappropriés ciblant les enfants à Douala et Yaoundé. Le système a déjà détecté un cas concret (SIMULE-0001) et les médias pressent de bloquer Tchatlink, ce qui nécessite une réponse technique et juridique coordonnée.

**Ce qu'il ignore :** L'identité précise des auteurs du contenu suspect ; Le volume exact des captures d'écran déjà collectées et leur statut de consentement parental

| Action | Vérification | Sources |
|---|---|---|
| **MinorShield** — Déployer immédiatement des mécanismes de blocage et de retrait des publications identifiées comme portant atteinte à la dignité ou à l'intégrité des enfants. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227 |
| **MinorShield** — Informer les parents des alertes générées et les accompagner dans la compréhension du fonctionnement du filtre. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 13, p. 226 |
| **MinorShield** — Préparer un rapport agrégé anonymisé des incidents détectés pour le transmettre aux autorités camerounaises, en attendant l'autorisation explicite de l'APDP. | ⚠️ non étayée | — |

**Lacunes signalées :**
- Absence de texte légal précisant les conditions de partage de statistiques agrégées avec les autorités nationales
- Pas de disposition détaillant la procédure de transmission de données personnelles d'enfants vers des autorités étrangères au-delà du consentement

<details><summary>Raisonnement explicite</summary>

1. Identifier l'anomalie de blocage et son impact sur la protection des enfants.
2. Appliquer les obligations légales de blocage et de retrait (E2).
3. Respecter le devoir d'information et d'éducation des utilisateurs (E1).
4. Solliciter les autorisations nécessaires auprès de l'APDP et du MINPOSTEL avant toute transmission ou mesure de blocage étendue.

</details>


### Regulateurs du numerique

**Évaluation.** Une hausse massive de contenus illicites a été détectée, les images d'une victime mineure circulent sur Tchatlink et les données proviennent d'une fuite de ScolaPlus. Les opérateurs et plateformes sont impliqués, et la pression médiatique réclame des mesures rapides.

**Ce qu'il ignore :** Le texte particulier précisant le rôle exact de l'ANTIC (article 10(2)) ; Les délais de réponse de Tchatlink et les procédures internes de l'ART pour ordonner un blocage technique ; L'existence d'un cadre légal national permettant le blocage complet d'une plateforme étrangère

| Action | Vérification | Sources |
|---|---|---|
| **ANTIC** — Déployer des moyens préventifs de blocage des contenus illicites sur les réseaux nationaux en ordonnant aux opérateurs de filtrer les flux liés aux images de la victime. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 10, p. 225 |
| **ART** — Coordonner avec les opérateurs de télécommunications pour appliquer le filtrage demandé par l'ANTIC et assurer le suivi technique du blocage. | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 27, p. 227 |
| **MINPOSTEL** — Lancer une campagne de sensibilisation nationale sur les risques de partage de contenus illicites et sur les bonnes pratiques de protection des données scolaires. | ⚠️ non étayée | — |

**Lacunes signalées :**
- Absence de texte précisant le rôle exact de l'ANTIC (article 10(2))
- Pas de base légale explicite pour un blocage total d'une plateforme étrangère sans présence locale

<details><summary>Raisonnement explicite</summary>

1. Identifier les faits majeurs (hausse de contenus, fuite de données, diffusion sur Tchatlink).
2. Rechercher les dispositions légales applicables aux mesures préventives et à la coopération inter‑institutions.
3. Déterminer les actions que chaque institution peut prendre dans le cadre de son mandat.
4. Formuler les demandes de coordination nécessaires aux acteurs disposant des moyens complémentaires.

</details>


### APDP

**Évaluation.** Une fuite de données de ScolaPlus a exposé les numéros de téléphone d'enfants et de leurs parents, entraînant un blocage du téléphone d'une collégienne par MinorShield. Des pressions médiatiques demandent le blocage complet de Tchatlink, mais aucune autorisation de transfert de données sensibles n'a été obtenue.

**Ce qu'il ignore :** Existence d'autorisations préalables de l'APDP pour le transfert de captures d'écran aux États-Unis ; Consentements parentaux effectifs pour les mineurs concernés ; Détails complets de la fuite de données chez ScolaPlus

| Action | Vérification | Sources |
|---|---|---|
| **APDP** — Émettre une mise en demeure à Tchatlink de suspendre le traitement des données d'enfants jusqu'à obtention du consentement parental requis | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |
| **APDP** — Demander à MinorShield de fournir les consentements parentaux associés aux captures d'écran avant tout transfert à des autorités étrangères | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |
| **APDP** — Ordonner à ScolaPlus de communiquer le registre complet des accès aux données et les mesures correctives prises suite à la fuite | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 17, p. 226 |

**Lacunes signalées :**
- Aucun extrait fourni ne précise la procédure d'autorisation préalable de transfert de données vers un État étranger (art. 32)
- L'article 53 de la loi 2024/017 n'est pas complet dans la source OCR, limitant la précision des pouvoirs d'enquête

<details><summary>Raisonnement explicite</summary>

1. Identifier la fuite de données comme source du problème
2. Vérifier les obligations légales concernant le traitement des données d'enfants
3. Déterminer les actions que l'APDP peut prendre directement
4. Formuler les demandes d'information nécessaires aux autres acteurs

</details>


### Protection sociale et educative

**Évaluation.** Des adolescentes sont victimes de chantage en ligne suite à une fuite de données scolaires. Le MINAS peut former le personnel à détecter et prendre en charge ces abus, le MINPROFF peut préparer des modules d'information pour les parents, et le MINESEC peut intégrer l'éducation à l'usage responsable d'Internet dans les curricula.

**Ce qu'il ignore :** Le nombre exact de personnels et de parents à former ; Le contenu détaillé de la fuite de données et les responsables techniques ; Les modalités de coopération entre le MINPROFF et le ministère des télécommunications

| Action | Vérification | Sources |
|---|---|---|
| **MINAS** — Organiser une session de formation pour le personnel des centres sociaux de Douala sur la prévention, la détection et la prise en charge des abus en ligne | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 8, p. 225 |
| **MINPROFF** — Élaborer des modules d'information à destination des parents sur les risques de chantage en ligne et les procédures de signalement | ⚠️ non étayée | — |
| **MINESEC** — Intégrer dans les curricula scolaires un volet sur l'utilisation responsable d'Internet et la protection contre le chantage en ligne | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 6, p. 225 |

**Lacunes signalées :**
- Aucune disposition légale ne permet au MINESEC d'intervenir directement auprès des élèves victimes en ligne
- La loi ne prévoit pas de mesure de blocage total d'une plateforme comme Tchatlink

<details><summary>Raisonnement explicite</summary>

1. Identifier les victimes et les points de vulnérabilité (fuite de données, chantage)
2. Associer chaque besoin à l'institution compétente selon les articles de loi
3. Déterminer les actions possibles et les bases légales correspondantes
4. Formuler des demandes aux acteurs externes nécessaires à la mise en œuvre

</details>


### Chaine penale

**Évaluation.** Des images à caractère pornographique impliquant une mineure de 15 ans circulent en ligne, accompagnées de menaces de chantage. La police judiciaire a déjà constaté les infractions et les a consignées, et le parquet doit qualifier les faits et décider des suites.

**Ce qu'il ignore :** Le consentement explicite du mineur et de son représentant légal pour la transmission des logs de MinorShield ; L'éventuelle décision judiciaire d'ordonner le blocage total de la plateforme Tchatlink

| Action | Vérification | Sources |
|---|---|---|
| **Police judiciaire** — Constater les infractions et transmettre le procès‑verbal ainsi que les éléments saisis au Procureur dans le délai légal | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 32, p. 228 |
| **Parquet** — Qualifier les faits de diffusion de pornographie enfantine et prononcer l'ouverture des poursuites pénales | 🔶 citation douteuse · citation absente ou non retrouvee mot pour mot dans les extraits cites | Loi n° 2010/012 du 21 decembre 2010 relative a la cybersecurite et a la cybercriminalite au Cameroun, article 81, p. 215 |

**Lacunes signalées :**
- La législation fournie ne prévoit pas explicitement la procédure d’autorisation de blocage total d’une plateforme étrangère comme Tchatlink, ce qui empêche le parquet de prendre cette mesure sans texte supplémentaire.

<details><summary>Raisonnement explicite</summary>

1. Identifier les infractions relevées (pornographie enfantine, chantage).
2. Vérifier les compétences de chaque institution (police pour constat, parquet pour qualification).
3. Appliquer les articles pertinents (E1 pour la transmission du PV, E2 pour la qualification).
4. Déterminer les informations manquantes (consentement APDP, cadre légal du blocage).

</details>


### Entreprises du numerique

**Évaluation.** Des images d'abus sexuel d'une mineure circulent sur Tchatlink, plateforme étrangère. Une fuite de données de ScolaPlus a permis aux escrocs d'obtenir les numéros de téléphone des victimes. Les autorités ont émis une décision officielle de suspension d'accès au contenu incriminé.

**Ce qu'il ignore :** l'identité précise du consommateur à l'origine de la publication ; la décision formelle d'une autorité compétente concernant le blocage total de Tchatlink

| Action | Vérification | Sources |
|---|---|---|
| **Operateurs** — Suspendre l'accès au contenu incriminé publié sur Tchatlink, conformément à la demande des autorités compétentes | ✅ étayée | Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 |

**Lacunes signalées :**
- La loi ne prévoit pas que les opérateurs puissent bloquer l'ensemble du service Tchatlink sans décision explicite d'une autorité compétente

<details><summary>Raisonnement explicite</summary>

1. Identifier le cadre légal applicable aux contenus illicites contre les enfants (E1).
2. Vérifier que les autorités ont déjà émis une décision de suspension du contenu incriminé.
3. Appliquer l'obligation de suspension en tant qu'opérateur, limité au contenu ciblé.
4. Demander à Tchatlink les informations nécessaires pour assurer la précision de la suspension et soutenir les enquêtes.

</details>


*Demande non transmise (destinataire inconnu « antinc »)* — APDP : Coordonner les mesures préventives contre la diffusion de contenus à risque pour les enfants


*Coordination interne* — Entreprises du numerique (entreprises) : Fournir les logs d'accès et les mesures de modération appliquées aux groupes contenant les images incriminées


**Demande** — MinorShield → APDP : Autorisation préalable pour la transmission du rapport agrégé anonymisé des incidents détectés aux autorités camerounaises

**Réponse de APDP** (🔶 citation douteuse) : Autorisation préalable accordée pour la transmission du rapport agrégé anonymisé des incidents détectés aux autorités camerounaises, sous réserve que le rapport ne contienne aucune donnée à caractère personnel permettant d'identifier directement ou indirectement un enfant ou un tiers et qu'il respecte les exigences de minimisation et de sécurisation prévues par la loi.


**Demande** — MinorShield → APDP : Confirmation écrite des consentements parentaux associés aux captures d'écran destinées aux autorités américaines

**Réponse de APDP** (✅ étayée) : Nous ne pouvons pas confirmer l'existence des consentements parentaux tant que nous n'avons pas reçu les documents justificatifs correspondants pour vérification.


**Demande** — MinorShield → Regulateurs du numerique : Avis juridique sur la possibilité de bloquer l'accès national à Tchatlink pendant la crise

**Réponse de Regulateurs du numerique** (✅ étayée) : Conformément à l'article 10, l'ANTIC peut déployer des moyens préventifs et répressifs pour protéger les enfants en ligne, y compris le blocage d'accès à une plateforme étrangère si cela est jugé nécessaire. L'article 27 prévoit également que l'ANTIC agit en collaboration avec l'ART et les autorités concernées pour mettre fin aux atteintes aux droits des enfants, ce qui justifie la possibilité de bloquer temporairement Tchatlink au niveau national.


**Demande** — Regulateurs du numerique → Chaine penale : Fournir le soutien opérationnel pour le filtrage et le blocage des contenus illicites via les opérateurs.

**Réponse de Chaine penale** (✅ étayée) : Nous acceptons de fournir le soutien opérationnel requis pour le filtrage et le blocage des contenus illicites via les opérateurs, en coordination avec les autorités compétentes.


**Demande** — Regulateurs du numerique → Protection sociale et educative : Communiquer les mesures à prendre contre l'opérateur mobile ayant permis le paiement du chantage via Mobile Money.

**Réponse de Protection sociale et educative** (⚠️ non étayée) : Le ministère des affaires sociales ne dispose pas d'un pouvoir légal pour imposer des mesures de régulation à un opérateur mobile concernant le paiement du chantage. Nous recommandons de transmettre cette demande au ministère en charge des télécommunications ou à l'organe de régulation compétent.


**Demande** — Regulateurs du numerique → Entreprises du numerique : Retirer immédiatement les images de la victime et fournir les preuves de suppression.

**Réponse de Entreprises du numerique** (✅ étayée) : Nous procédons immédiatement au retrait des images de la victime de la plateforme et fournirons les preuves de suppression aux autorités compétentes.


### ⚖️ Analyse du conseiller juridique

Le droit camerounais autorise la suspension ciblée de contenus illicites mais ne prévoit pas le blocage complet d’une plateforme comme Tchatlink. Cette lacune contraste avec les cadres australien et européen qui encadrent le blocage temporaire et proportionné. Une coordination entre ANTIC et MINPOSTEL est indispensable pour concilier protection des enfants et respect des libertés fondamentales.

| Acteur | Action | Verdict | Commentaire |
|---|---|---|---|
| Tchatlink | bloquer l'accès à Tchatlink sur le territoire national | ⚠️ à vérifier | E5 oblige les fournisseurs à suspendre l'accès à un contenu ou à un utilisateur à la demande des autorités, mais ne prévoit pas le blocage total d'une plateforme sans identification précise du contenu illicite. |
| Tchatlink | retirer immédiatement les publications portant atteinte à la dignité et à l'intégrité des enfants | ⚠️ à vérifier | E6 impose aux fournisseurs de mettre en place des mécanismes de retrait ou de blocage de publications spécifiques, mais ne prévoit pas le retrait de l’ensemble du service. |
| ANTIC | déployer des moyens préventifs et répressifs pour protéger les enfants dans le cyberespace national | ✅ fondée | E2 confère à l'organe chargé de la régulation des TIC le pouvoir de déployer les moyens nécessaires à la protection des enfants en ligne. |

**Lacune : Absence de disposition autorisant le blocage total d’une plateforme numérique en l’absence de contenu spécifiquement identifié comme illicite.**

- Droit camerounais : Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 14, p. 226 ; Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne au Cameroun, article 23, p. 227
- Australie : Le bloqueur peut imposer un blocage limité dans le temps (max 3 mois) sur du matériel jugé préjudiciable. *(Online Safety Act 2021 (Australia, No. 76, 2021) — version d'origine] (partie 78/157))*
- **Recommandation :** Introduire un article précisant les conditions, la durée maximale et les procédures de contrôle judiciaire pour le blocage total d’une plateforme, en s’inspirant du cadre australien (E11) et du Digital Services Act (E13).

**Conflits :**
- Conflit entre la protection des enfants (E1‑E5) et le droit à la liberté d’expression des enfants (E10).

**Problèmes de coordination :**
- Demande à ANTIC (destinataire: ANTIC) de préciser les mesures préventives à mettre en œuvre et d’émettre, le cas échéant, une ordonnance de suspension ciblée.
- Demande à MINPOSTEL (destinataire: MINPOSTEL) de valider la légalité de toute mesure de blocage total et d’assurer la conformité avec le droit pénal (E4).
