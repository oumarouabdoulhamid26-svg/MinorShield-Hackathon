# Lacunes de politiques et de normes — protection des mineurs en ligne

> Tableau de référence pour le rapport technique (critère « identification des
> lacunes », le plus valorisé par les organisateurs). Chaque lacune est
> formulée **pour le domaine** (protection des mineurs en ligne), le Cameroun
> servant de terrain d'illustration ; elle suit le format demandé : **constat,
> source, conséquence, exemples internationaux**.
>
> Toutes les références ont été vérifiées le 23/10/2026 dans les textes
> officiels de la base de connaissances (`bd/InputDocs/`, provenance dans
> `bd/SOURCES.md`). La ligne « Simulation de référence » indique, après
> relecture humaine du journal (`docs/exemple_simulation/`), si la simulation a
> fait apparaître la lacune, à quelle étape et par quel agent.

## A. Lacunes de politiques

### 1. Signalement par les outils tiers de protection de l'enfance
- **Constat.** La loi oblige les fournisseurs d'accès à signaler les contenus portant atteinte aux enfants, mais ne prévoit ni canal ni seuil d'alerte pour un outil tiers (contrôle parental, détecteur) ni pour des signaux agrégés et anonymisés.
- **Source.** Cameroun, loi n° 2023/009, art. 33 (amende de 25 à 250 millions FCFA pour le fournisseur d'accès qui ne signale pas) ; art. 16 (signalement de la pédopornographie par les fournisseurs et promoteurs de réseaux sociaux).
- **Conséquence.** Un outil qui détecte une campagne (hausse de 400 % des blocages, étape 1) ne sait ni à qui, ni sous quelle forme, ni à partir de quel seuil alerter ; l'alerte dépend du bon vouloir de chacun.
- **Exemples internationaux.** Royaume-Uni, Online Safety Act 2023, s. 66 : obligation pour les fournisseurs, y compris étrangers, de signaler à la National Crime Agency les contenus d'exploitation et d'abus sexuels d'enfants détectés. Émirats arabes unis, décret-loi n° 26/2025, art. 10(1)(h) et 11(1)(d) : signalement immédiat aux autorités par les plateformes et les fournisseurs d'accès. UE, DSA, art. 18 : notification des soupçons d'infraction pénale menaçant la vie ou la sécurité.
- **Simulation de référence (24/10/2026).** ✅ **Relevée** (étape 1) par le conseiller, MinorShield et les régulateurs : pas de cadre pour partager des statistiques agrégées avec les autorités ; comparaison avec l'Australie.

### 2. Délai de retrait des contenus
- **Constat.** Le seul délai prévu est une mise en demeure de quinze jours avant sanction, inadapté à des images intimes qui circulent en quelques heures.
- **Source.** Loi n° 2023/009, art. 28 (mise en demeure de 15 jours) et art. 29 (pénalités).
- **Conséquence.** Pendant deux semaines, les images d'une victime de chantage peuvent continuer à circuler sans manquement constaté.
- **Exemples internationaux.** Australie, Online Safety Act 2021, s. 77 : avis de retrait des images intimes diffusées sans consentement, à exécuter sous **24 heures** (aussi s. 65 pour le cyberharcèlement d'un enfant). UE, DSA, art. 16 (mécanismes de notification et d'action) et art. 17 (exposé des motifs des décisions).
- **Simulation de référence (24/10/2026).** 🔶 **Partiellement relevée** (étape 4) : le conseiller recommande une procédure de retrait sous 48 heures en citant l'avis de retrait australien sous 24 heures, mais ne désigne pas le délai de 15 jours de l'art. 28 comme la cause.

### 3. Plateformes étrangères et portée extraterritoriale
- **Constat.** La loi impose des obligations aux promoteurs de réseaux sociaux sans préciser si elles s'appliquent à une plateforme établie à l'étranger, ni exiger de représentant local.
- **Source.** Loi n° 2023/009, art. 2 (champ : « activités impliquant les enfants dans le cyberespace »), art. 14 à 16 ; aucune disposition sur l'établissement ou la représentation.
- **Conséquence.** Une plateforme étrangère peut répondre qu'elle traitera la demande « selon ses délais habituels » (étape 4) ; la seule mesure à portée de main devient le blocage national.
- **Exemples internationaux.** UE, DSA, art. 2 (application aux services proposés dans l'Union « quel que soit le lieu d'établissement des fournisseurs ») et art. 13 (représentant légal obligatoire). Émirats arabes unis, décret-loi n° 26/2025, art. 3 (plateformes opérant dans le pays ou « dirigées vers ses utilisateurs »).
- **Simulation de référence (24/10/2026).** ✅ **Relevée** (étapes 1, 4, 5 et 6) par les régulateurs et le conseiller : aucune procédure pour contraindre une plateforme étrangère sans présence locale ; comparaisons avec l'Australie, le Royaume-Uni et les Émirats.

### 4. Violations de données concernant des enfants
- **Constat.** La loi impose d'informer l'autorité et les personnes concernées « sans délai », sans délai chiffré ni règle propre aux mineurs (information des parents).
- **Source.** Loi n° 2024/017, art. 22.
- **Conséquence.** Un éditeur peut attendre trois semaines (étape 5) en soutenant qu'il agit « sans délai » ; les familles exposées au chantage ne sont pas prévenues.
- **Exemples internationaux.** UE, RGPD, art. 33 (notification à l'autorité **dans les 72 heures**) et art. 34 (communication aux personnes concernées).
- **Simulation de référence (24/10/2026).** ✅ **Relevée** (étape 5) par le conseiller, qui recommande un délai de 72 heures. ⚠️ Deux défauts : la comparaison invoque la règle COPPA, qui ne contient aucune obligation de notification des violations (erreur non détectée par le vérificateur) ; et l'art. 22 n'a pas été fourni à l'APDP à cette étape, qui l'a signalé comme « absent de la base ».

### 5. Seuils d'âge incohérents
- **Constat.** Les textes fixent des âges différents pour la même protection : l'« enfant » de la charte a moins de 18 ans, alors que le Code pénal protège spécialement les mineurs de 16 à 21 ans.
- **Source.** Loi n° 2023/009, art. 3 (enfant : moins de 18 ans) ; Code pénal (loi n° 2016/007), art. 347 (infractions « sur la personne d'un mineur de seize à vingt et un ans »).
- **Conséquence.** Une victime de 19 ans (étape 3) est mineure au sens pénal mais hors du champ de la charte : ni signalement, ni retrait, ni prise en charge prévus par celle-ci.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 1 (enfant : moins de 18 ans, définition unique pour toute la loi) ; ONU, Observation générale n° 25 (2021), qui s'applique à toute personne de moins de 18 ans.
- **Simulation de référence (24/10/2026).** ❌ **Non relevée**, pour la troisième simulation consécutive : aucun agent ne vérifie que la victime de 19 ans entre dans le champ de la charte, alors que la définition (art. 3) et l'art. 347 du Code pénal étaient disponibles. C'est en soi un enseignement : un agent ne contrôle pas spontanément le champ d'application d'un texte.

### 6. Surveillance de l'écran d'un enfant et consentement
- **Constat.** Hormis l'exigence du consentement parental pour un mineur, aucun texte ne dit quand un outil privé peut surveiller l'écran d'un enfant, avec quelle proportionnalité, ni quelle place donner à l'avis de l'enfant.
- **Source.** Loi n° 2024/017, art. 9(3) (consentement d'un mineur de moins de 18 ans valable seulement avec celui de ses parents ou représentant légal).
- **Conséquence.** Un outil comme MinorShield (étape 2) peut analyser toutes les conversations d'une collégienne avec le seul accord du parent, sans limite de finalité ni information de l'enfant.
- **Exemples internationaux.** ONU, Observation générale n° 25, par. 75 : la surveillance numérique des enfants ne doit pas être systématique, sans discernement ou à leur insu, et doit privilégier les moyens les moins intrusifs. UE, RGPD, art. 8 (consentement parental en dessous de 16 ans, abaissable à 13). Émirats arabes unis, décret-loi n° 26/2025, art. 13(1)(a) (surveillance par le responsable de l'enfant « en respectant son autonomie numérique selon son âge ») et art. 7 (consentement parental vérifiable pour les moins de 13 ans).
- **Simulation de référence (24/10/2026).** ❌ **Non relevée** : le consentement n'est discuté que pour la transmission des captures à la police, jamais pour la surveillance de l'écran elle-même.

### 7. Transfert de données d'enfants vers des services d'IA étrangers
- **Constat.** Tout transfert vers un État étranger exige une autorisation préalable de l'autorité, mais rien n'encadre les services d'IA étrangers appelés en temps réel (analyse de contenu par API).
- **Source.** Loi n° 2024/017, art. 32.
- **Conséquence.** Un outil de protection qui envoie les captures d'un enfant à un service de modération étranger (cas réel de MinorShield, étape 2) doit obtenir une autorisation que l'autorité, en place depuis juin 2026, n'a pas encore les procédures pour délivrer.
- **Exemples internationaux.** UE, RGPD, art. 44 et 45 (principe général et décisions d'adéquation pour les transferts).
- **Simulation de référence (24/10/2026).** 🔶 **Partiellement relevée** (étape 2) : la chaîne pénale constate qu'aucune procédure ne permet d'obtenir des données hébergées à l'étranger (serveur d'OpenAI) ; l'APDP impose l'anonymisation avant toute transmission, mais personne n'invoque l'autorisation préalable de l'art. 32.

### 8. Responsabilité en cas d'erreur de l'outil de protection
- **Constat.** Aucun texte ne désigne qui répond d'un blocage injustifié ou d'une détection manquée, ni ne donne à l'enfant ou au parent un droit d'explication et de recours.
- **Source.** Loi n° 2023/009 et loi n° 2024/017 : aucune disposition (absence constatée dans les textes de la base).
- **Conséquence.** Un faux positif (« un jeu entre amies », étape 2) ou une détection manquée reste sans responsable ni recours.
- **Exemples internationaux.** UE, DSA, art. 17 (exposé des motifs de toute restriction) et art. 20 (système interne de traitement des réclamations).
- **Simulation de référence (24/10/2026).** 🔶 **Partiellement relevée** (étape 2) : MinorShield explique au parent le risque de faux positif et les recours, mais ne trouve aucun texte pour fonder cette réponse (action « non étayée », ce qui illustre la lacune).

### 9. Coordination institutionnelle
- **Constat.** Plusieurs ministères ont chacun une mission partielle, sans organe de coordination ni partage des compétences ; les missions du ministère des affaires sociales et de celui de la famille se chevauchent.
- **Source.** Loi n° 2023/009, art. 6 (MINESEC), 7 (MINPROFF), 8 (MINAS), 4 et 5 (plan d'action national) ; aucun organe de coordination de crise identifié.
- **Conséquence.** Dans la simulation, l'animateur doit rester neutre faute d'institution compétente ; la prise en charge des victimes (étape 3) dépend de qui est saisi en premier.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 4 et 5 (Conseil de la sécurité numérique des enfants, présidé par le ministre, qui coordonne les autorités). ONU, Observation générale n° 25, par. 27 (désigner un organe gouvernemental chargé de coordonner les politiques relatives aux droits de l'enfant dans l'environnement numérique).
- **Simulation de référence (24/10/2026).** ✅ **Relevée** à chaque étape (rubrique « coordination » du conseiller) ; le chevauchement MINAS / MINPROFF à l'étape 3, avec renvoi à l'Observation générale n° 25.

### 10. Blocage d'une plateforme et proportionnalité
- **Constat.** La loi permet de suspendre un utilisateur, pas de bloquer une plateforme entière ; un blocage national n'a donc ni base légale ni garanties de proportionnalité.
- **Source.** Loi n° 2023/009, art. 14 (suspension d'un utilisateur à la demande des autorités).
- **Conséquence.** Sous pression médiatique (étape 6), la mesure la plus spectaculaire est envisagée sans cadre, au risque de toucher des millions d'utilisateurs et de commerçants.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 10(3) (fermeture, blocage partiel ou total après constat d'une violation, par les autorités compétentes). UE, DSA, art. 17 et 20 (motivation et recours pour toute restriction).
- **Simulation de référence (24/10/2026).** ✅ **Relevée** (étape 6) par le conseiller et cinq agents ; conflit protection de l'enfance / liberté d'expression explicitement noté. ⚠️ Le conseiller surestime les pouvoirs australiens : les avis de blocage de l'Online Safety Act 2021 (partie 8) visent seulement les contenus de violence odieuse, pas tout danger pour les enfants.

## B. Lacunes de normes

| N° | Lacune | Source examinée | Proposition |
|---|---|---|---|
| N1 | Le pipeline UIT-T Y.3172 n'a pas d'étape pour vérifier qu'une sortie de modèle de langage est fondée sur ses sources | Y.3172, nœuds SRC → C → PP → M → P → D → SINK | Ajouter un nœud de vérification entre M et SINK ; deux indicateurs : taux de citations étayées et rappel des lacunes attendues (mis en œuvre dans ce projet) |
| N2 | Le rapport AI Readiness 2.0 ne couvre pas l'IA agentique (délégation, coordination multi-agents, autonomie de décision) | Rapport Readiness 2.0, clause 3 (p. 17), 13 dimensions | Ajouter des indicateurs agentiques : traçabilité des échanges entre agents, respect des mandats, taux d'actions étayées |
| N3 | Aucune norme pour mesurer et publier les performances d'un détecteur de contenus sur l'appareil, ni pour expliquer un blocage à l'enfant | Base de normes de l'UIT ; ISO/IEC JTC 1/SC 42 (à vérifier) | Protocole commun de mesure (faux positifs par catégorie et par langue) et format d'explication adapté à l'âge |
| N4 | Les lois camerounaises ne sont publiées qu'en PDF (souvent scannés), sans format ouvert article par article | Recueil de l'ART (2023), loi n° 2024/017 scannée (prc.cm) | Publication dans un format lisible par machine (par exemple Akoma Ntoso) |
| N5 | Deux fichiers du dépôt de référence de l'UIT sont tronqués et 20 documents sur 67 avaient un pays erroné | Dépôt CrashingGuru/ITUAIReadiness | Contrôle d'intégrité et de métadonnées à l'ingestion (corrigé dans ce projet) |

## C. Relecture humaine de la simulation de référence (24/10/2026)

### Lacunes attendues : 7 retrouvées, 3 partiellement, 5 manquées (sur 15)

Le rapprochement automatique (`agent/scripts/indicateurs.py`, similarité de
sens) n'en retenait qu'une : il est trop sévère pour trancher seul. Bilan après
relecture du journal :

| Étape | Lacune attendue (scénario) | Verdict | Où |
|---|---|---|---|
| 1 | Pas de canal ni de seuil pour qu'un outil tiers alerte les autorités | ✅ | Conseiller, MinorShield, régulateurs |
| 2 | Surveillance de l'écran d'un enfant et consentement | ❌ | — |
| 2 | Transfert vers un service d'IA étranger (art. 32) | 🔶 | Chaîne pénale (données hébergées chez OpenAI) ; l'art. 32 n'est pas invoqué |
| 2 | Responsabilité d'un blocage injustifié | 🔶 | MinorShield (faux positif et recours, sans base légale) |
| 2 | Absence de norme de performance des détecteurs | ❌ | — |
| 2 | « Contenu inapproprié » contre catégories du détecteur | ❌ | — |
| 3 | Victime de 19 ans hors du champ de la charte | ❌ | — |
| 3 | Chevauchement MINAS / MINPROFF | ✅ | Conseiller, protection sociale |
| 3 | Pas de directive scolaire pour les élèves victimes | ✅ | Protection sociale (étapes 2, 3, 5, 6) |
| 4 | Portée limitée face aux plateformes étrangères | ✅ | Conseiller, régulateurs |
| 4 | Mise en demeure de 15 jours inadaptée | 🔶 | Conseiller (procédure sous 48 h proposée, art. 28 non désigné) |
| 5 | Autorité de protection des données récente | ❌ | — |
| 5 | Notification « sans délai », sans délai chiffré | ✅ | Conseiller |
| 6 | Protection de l'enfance contre liberté d'expression | ✅ | Conseiller (rubrique « conflits ») |
| 6 | Pas de mécanisme formel de coordination de crise | ✅ | Conseiller, à chaque étape |

Les lacunes manquées se concentrent à l'étape 2 (surveillance, normes,
définition) : ce sont des questions que le droit ne pose pas encore, et que les
agents, raisonnant à partir des textes, ne posent pas non plus. Elles restent
au rapport, issues de l'analyse humaine, et sont présentées comme telles.

### Lacunes non prévues, relevées par la simulation

- **Accès aux données de paiement** (étapes 3 à 5, chaîne pénale et conseiller) :
  aucun texte de la base ne précise comment la police obtient auprès des
  opérateurs les relevés Mobile Money d'une rançon.
- **Anonymisation avant transmission aux autorités** (étape 5, conseiller).
- **Chevauchement APDP / ANTIC** face à une même fuite de données, avec un
  risque de double sanction (étape 5, conseiller).
- **Texte d'application manquant** : l'art. 10(2) de la loi n° 2023/009 renvoie à
  un texte précisant le rôle de l'ANTIC, introuvable (étape 6, régulateurs).

### Erreurs de l'IA

| Erreur | Détectée par le vérificateur automatique ? |
|---|---|
| Identifiant d'extrait inventé (« E25 », étape 4) | ✅ oui (citation invalide) |
| Articles mentionnés sans figurer dans l'extrait cité (4 cas) | ✅ oui (citations douteuses) |
| Actions sans aucune source (10 cas, souvent des mesures pratiques) | ✅ oui (non étayées) |
| DSA art. 25 présenté comme une obligation de retrait rapide (il porte sur la conception des interfaces) | ❌ non : relecture humaine |
| Obligation de notification des violations attribuée à la règle COPPA (elle n'en contient pas) | ❌ non : relecture humaine |
| Pouvoirs de blocage australiens surestimés (limités aux contenus de violence odieuse) | ❌ non : relecture humaine |
| Durée de conservation déclarée « non définie » alors que l'art. 13 de la loi n° 2024/017 la renvoie à l'autorisation de traitement | ❌ non : relecture humaine |

Le vérificateur contrôle que chaque affirmation **cite un extrait réellement
fourni** ; il ne peut pas contrôler qu'un extrait correctement cité **dit bien**
ce que l'agent affirme. D'où la lacune de normes N1 et l'obligation d'une
relecture juridique humaine.
