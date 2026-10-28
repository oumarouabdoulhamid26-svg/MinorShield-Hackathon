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
> relecture humaine du journal de la simulation du 27/10/2026 (`docs/exemple_simulation/`), si la simulation a
> fait apparaître la lacune, à quelle étape et par quel agent.

## A. Lacunes de politiques

### 1. Signalement par les outils tiers de protection de l'enfance
- **Constat.** La loi oblige les fournisseurs d'accès à signaler les contenus portant atteinte aux enfants, mais ne prévoit ni canal ni seuil d'alerte pour un outil tiers (contrôle parental, détecteur) ni pour des signaux agrégés et anonymisés.
- **Source.** Cameroun, loi n° 2023/009, art. 33 (amende de 25 à 250 millions FCFA pour le fournisseur d'accès qui ne signale pas) ; art. 16 (signalement de la pédopornographie par les fournisseurs et promoteurs de réseaux sociaux).
- **Conséquence.** Un outil qui détecte une campagne (hausse de 400 % des blocages, étape 1) ne sait ni à qui, ni sous quelle forme, ni à partir de quel seuil alerter ; l'alerte dépend du bon vouloir de chacun.
- **Exemples internationaux.** Royaume-Uni, Online Safety Act 2023, s. 66 : obligation pour les fournisseurs, y compris étrangers, de signaler à la National Crime Agency les contenus d'exploitation et d'abus sexuels d'enfants détectés. Émirats arabes unis, décret-loi n° 26/2025, art. 10(1)(h) et 11(1)(d) : signalement immédiat aux autorités par les plateformes et les fournisseurs d'accès. UE, DSA, art. 18 : notification des soupçons d'infraction pénale menaçant la vie ou la sécurité.
- **Simulation de référence (27/10/2026).** ✅ **Relevée** (étapes 1 et 6) par le conseiller, MinorShield et les régulateurs : aucun cadre pour qu'un acteur privé de protection transmette des statistiques agrégées aux autorités ; comparaison avec les Émirats (décret-loi n° 26/2025, art. 10 : statistiques et rapports périodiques aux autorités), citation vérifiée mot pour mot.

### 2. Délai de retrait des contenus
- **Constat.** Le seul délai prévu est une mise en demeure de quinze jours avant sanction, inadapté à des images intimes qui circulent en quelques heures.
- **Source.** Loi n° 2023/009, art. 28 (mise en demeure de 15 jours) et art. 29 (pénalités).
- **Conséquence.** Pendant deux semaines, les images d'une victime de chantage peuvent continuer à circuler sans manquement constaté.
- **Exemples internationaux.** Australie, Online Safety Act 2021, s. 77 : avis de retrait des images intimes diffusées sans consentement, à exécuter sous **24 heures** (aussi s. 65 pour le cyberharcèlement d'un enfant). UE, DSA, art. 16 (mécanismes de notification et d'action) et art. 17 (exposé des motifs des décisions).
- **Simulation de référence (27/10/2026).** 🔶 **Partiellement relevée** (étapes 3 et 4) : le conseiller propose un délai maximal de 48 heures pour les plateformes étrangères et relève l'absence d'obligation de retrait d'une image intime sous menace de diffusion ; mais il présente la situation comme une absence de délai, sans désigner le délai de 15 jours de l'art. 28.

### 3. Plateformes étrangères et portée extraterritoriale
- **Constat.** La loi impose des obligations aux promoteurs de réseaux sociaux sans préciser si elles s'appliquent à une plateforme établie à l'étranger, ni exiger de représentant local.
- **Source.** Loi n° 2023/009, art. 2 (champ : « activités impliquant les enfants dans le cyberespace »), art. 14 à 16 ; aucune disposition sur l'établissement ou la représentation.
- **Conséquence.** Une plateforme étrangère peut répondre qu'elle traitera la demande « selon ses délais habituels » (étape 4) ; la seule mesure à portée de main devient le blocage national.
- **Exemples internationaux.** UE, DSA, art. 2 (application aux services proposés dans l'Union « quel que soit le lieu d'établissement des fournisseurs ») et art. 13 (représentant légal obligatoire). Émirats arabes unis, décret-loi n° 26/2025, art. 3 (plateformes opérant dans le pays ou « dirigées vers ses utilisateurs »).
- **Simulation de référence (27/10/2026).** ✅ **Relevée** (étapes 4, 5 et 6) par les régulateurs, la chaîne pénale et le conseiller : l'ANTIC ne peut rien imposer directement à une plateforme étrangère sans présence locale ; comparaisons avec l'Australie.

### 4. Violations de données concernant des enfants
- **Constat.** La loi impose d'informer l'autorité et les personnes concernées « sans délai », sans délai chiffré ni règle propre aux mineurs (information des parents).
- **Source.** Loi n° 2024/017, art. 22.
- **Conséquence.** Un éditeur peut attendre trois semaines (étape 5) en soutenant qu'il agit « sans délai » ; les familles exposées au chantage ne sont pas prévenues.
- **Exemples internationaux.** UE, RGPD, art. 33 (notification à l'autorité **dans les 72 heures**) et art. 34 (communication aux personnes concernées).
- **Simulation de référence (27/10/2026).** 🔶 **Partiellement relevée** (étape 5) par le conseiller et la protection sociale (aucune procédure pour prévenir établissements et familles). ⚠️ Le conseiller parle d'une **absence** d'obligation de notification, alors que l'art. 22 impose d'informer « sans délai » : l'article ne lui a pas été fourni à cette étape (l'APDP l'a signalé comme manquant). Et la comparaison attribue de nouveau à la règle COPPA une obligation de notifier les parents d'une violation, qu'elle ne contient pas : la phrase citée existe bien mot pour mot, mais porte sur l'usage des coordonnées des parents (erreur non détectée par le vérificateur).

### 5. Seuils d'âge incohérents
- **Constat.** Les textes fixent des âges différents pour la même protection : l'« enfant » de la charte a moins de 18 ans, alors que le Code pénal protège spécialement les mineurs de 16 à 21 ans.
- **Source.** Loi n° 2023/009, art. 3 (enfant : moins de 18 ans) ; Code pénal (loi n° 2016/007), art. 347 (infractions « sur la personne d'un mineur de seize à vingt et un ans »).
- **Conséquence.** Une victime de 19 ans (étape 3) est mineure au sens pénal mais hors du champ de la charte : ni signalement, ni retrait, ni prise en charge prévus par celle-ci.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 1 (enfant : moins de 18 ans, définition unique pour toute la loi) ; ONU, Observation générale n° 25 (2021), qui s'applique à toute personne de moins de 18 ans.
- **Simulation de référence (27/10/2026).** ❌ **Non relevée**, pour la quatrième simulation consécutive : aucun agent ne vérifie que la victime de 19 ans entre dans le champ de la charte, alors que la définition (art. 3) et l'art. 347 du Code pénal sont dans la base. Un agent ne contrôle pas spontanément le champ d'application d'un texte.

### 6. Surveillance de l'écran d'un enfant et consentement
- **Constat.** Hormis l'exigence du consentement parental pour un mineur, aucun texte ne dit quand un outil privé peut surveiller l'écran d'un enfant, avec quelle proportionnalité, ni quelle place donner à l'avis de l'enfant.
- **Source.** Loi n° 2024/017, art. 9(3) (consentement d'un mineur de moins de 18 ans valable seulement avec celui de ses parents ou représentant légal).
- **Conséquence.** Un outil comme MinorShield (étape 2) peut analyser toutes les conversations d'une collégienne avec le seul accord du parent, sans limite de finalité ni information de l'enfant.
- **Exemples internationaux.** ONU, Observation générale n° 25, par. 75 : la surveillance numérique des enfants ne doit pas être systématique, sans discernement ou à leur insu, et doit privilégier les moyens les moins intrusifs. UE, RGPD, art. 8 (consentement parental en dessous de 16 ans, abaissable à 13). Émirats arabes unis, décret-loi n° 26/2025, art. 13(1)(a) (surveillance par le responsable de l'enfant « en respectant son autonomie numérique selon son âge ») et art. 7 (consentement parental vérifiable pour les moins de 13 ans).
- **Simulation de référence (27/10/2026).** ❌ **Non relevée** : le consentement n'est discuté que pour la transmission des captures (aux autorités, à l'étranger), jamais pour la surveillance de l'écran elle-même.

### 7. Transfert de données d'enfants vers des services d'IA étrangers
- **Constat.** Tout transfert vers un État étranger exige une autorisation préalable de l'autorité, mais rien n'encadre les services d'IA étrangers appelés en temps réel (analyse de contenu par API).
- **Source.** Loi n° 2024/017, art. 32.
- **Conséquence.** Un outil de protection qui envoie les captures d'un enfant à un service de modération étranger (cas réel de MinorShield, étape 2) doit obtenir une autorisation que l'autorité, en place depuis juin 2026, n'a pas encore les procédures pour délivrer.
- **Exemples internationaux.** UE, RGPD, art. 44 et 45 (principe général et décisions d'adéquation pour les transferts).
- **Simulation de référence (27/10/2026).** ✅ **Relevée** (étapes 2, 5 et 6) : dès l'étape 2, l'APDP demande à MinorShield de suspendre tout transfert de la capture vers son service de modération aux États-Unis jusqu'à l'autorisation préalable de l'art. 32, et constate qu'aucune procédure ne permet de la délivrer rapidement ; elle le redit aux étapes 5 et 6. ⚠️ L'APDP parle ensuite de transmission « aux autorités américaines », confondant le service de modération avec une autorité.

### 8. Responsabilité en cas d'erreur de l'outil de protection
- **Constat.** Aucun texte ne désigne qui répond d'un blocage injustifié ou d'une détection manquée, ni ne donne à l'enfant ou au parent un droit d'explication et de recours.
- **Source.** Loi n° 2023/009 et loi n° 2024/017 : aucune disposition (absence constatée dans les textes de la base).
- **Conséquence.** Un faux positif (« un jeu entre amies », étape 2) ou une détection manquée reste sans responsable ni recours.
- **Exemples internationaux.** UE, DSA, art. 17 (exposé des motifs de toute restriction) et art. 20 (système interne de traitement des réclamations).
- **Simulation de référence (27/10/2026).** ❌ **Non relevée** : MinorShield note qu'aucun texte ne fixe le seuil de score qui déclenche un blocage (ce qui relève plutôt de la lacune de normes N3), mais la question de la responsabilité en cas de faux positif n'est pas posée.

### 9. Coordination institutionnelle
- **Constat.** Plusieurs ministères ont chacun une mission partielle, sans organe de coordination ni partage des compétences ; les missions du ministère des affaires sociales et de celui de la famille se chevauchent.
- **Source.** Loi n° 2023/009, art. 6 (MINESEC), 7 (MINPROFF), 8 (MINAS), 4 et 5 (plan d'action national) ; aucun organe de coordination de crise identifié.
- **Conséquence.** Dans la simulation, l'animateur doit rester neutre faute d'institution compétente ; la prise en charge des victimes (étape 3) dépend de qui est saisi en premier.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 4 et 5 (Conseil de la sécurité numérique des enfants, présidé par le ministre, qui coordonne les autorités). ONU, Observation générale n° 25, par. 27 (désigner un organe gouvernemental chargé de coordonner les politiques relatives aux droits de l'enfant dans l'environnement numérique).
- **Simulation de référence (27/10/2026).** ✅ **Relevée** à chaque étape (rubrique « coordination » du conseiller : absence de protocole partagé entre MINAS, police et opérateurs, entre ANTIC, ART et opérateurs) ; chevauchement MINAS / MINPROFF relevé par la protection sociale à l'étape 3.

### 10. Blocage d'une plateforme et proportionnalité
- **Constat.** La loi permet de suspendre un utilisateur, pas de bloquer une plateforme entière ; un blocage national n'a donc ni base légale ni garanties de proportionnalité.
- **Source.** Loi n° 2023/009, art. 14 (suspension d'un utilisateur à la demande des autorités).
- **Conséquence.** Sous pression médiatique (étape 6), la mesure la plus spectaculaire est envisagée sans cadre, au risque de toucher des millions d'utilisateurs et de commerçants.
- **Exemples internationaux.** Émirats arabes unis, décret-loi n° 26/2025, art. 10(3) (fermeture, blocage partiel ou total après constat d'une violation, par les autorités compétentes). UE, DSA, art. 17 et 20 (motivation et recours pour toute restriction).
- **Simulation de référence (27/10/2026).** ✅ **Relevée** (étape 6) par le conseiller et quatre agents (régulateurs, chaîne pénale, protection sociale, entreprises) : aucune base légale pour bloquer une plateforme entière ; conflit protection de l'enfance / liberté d'expression noté. Le conseiller cite exactement la durée maximale de 3 mois des avis de blocage australiens, mais étend leur champ à tout « matériel jugé préjudiciable » alors qu'ils visent les contenus de violence odieuse (partie 8).

## B. Lacunes de normes

| N° | Lacune | Source examinée | Proposition |
|---|---|---|---|
| N1 | Le pipeline UIT-T Y.3172 n'a pas d'étape pour vérifier qu'une sortie de modèle de langage est fondée sur ses sources | Y.3172, nœuds SRC → C → PP → M → P → D → SINK | Ajouter un nœud de vérification entre M et SINK ; deux indicateurs : taux de citations étayées et rappel des lacunes attendues (mis en œuvre dans ce projet) |
| N2 | Le rapport AI Readiness 2.0 ne couvre pas l'IA agentique (délégation, coordination multi-agents, autonomie de décision) | Rapport Readiness 2.0, clause 3 (p. 17), 13 dimensions | Ajouter des indicateurs agentiques : traçabilité des échanges entre agents, respect des mandats, taux d'actions étayées |
| N3 | Aucune norme pour mesurer et publier les performances d'un détecteur de contenus sur l'appareil, ni pour expliquer un blocage à l'enfant | Base de normes de l'UIT ; ISO/IEC JTC 1/SC 42 (à vérifier) | Protocole commun de mesure (faux positifs par catégorie et par langue) et format d'explication adapté à l'âge |
| N4 | Les lois camerounaises ne sont publiées qu'en PDF (souvent scannés), sans format ouvert article par article | Recueil de l'ART (2023), loi n° 2024/017 scannée (prc.cm) | Publication dans un format lisible par machine (par exemple Akoma Ntoso) |
| N5 | Deux fichiers du dépôt de référence de l'UIT sont tronqués et 20 documents sur 67 avaient un pays erroné | Dépôt CrashingGuru/ITUAIReadiness | Contrôle d'intégrité et de métadonnées à l'ingestion (corrigé dans ce projet) |

## C. Relecture humaine de la simulation de référence (27/10/2026)

Simulation `docs/exemple_simulation/` (gpt-oss-120b), la première avec la
citation mot pour mot vérifiée par le code. La simulation précédente
(24/10/2026) est archivée dans `docs/archives/reference_20261024/` ; son bilan
était de 7 lacunes retrouvées, 3 partiellement et 5 manquées, avec 4 erreurs
de l'IA non détectées.

### Lacunes attendues : 7 retrouvées, 3 partiellement, 5 manquées (sur 15)

Le rapprochement automatique (`agent/scripts/indicateurs.py`, similarité de
sens) n'en retient que 3 : il est trop sévère pour trancher seul. Bilan après
relecture du journal :

| Étape | Lacune attendue (scénario) | Verdict | Où |
|---|---|---|---|
| 1 | Pas de canal ni de seuil pour qu'un outil tiers alerte les autorités | ✅ | Conseiller, MinorShield, régulateurs |
| 2 | Surveillance de l'écran d'un enfant et consentement | ❌ | — |
| 2 | Transfert vers un service d'IA étranger (art. 32) | ✅ | APDP : suspendre tout transfert vers le service de modération aux États-Unis jusqu'à l'autorisation préalable ; aucune procédure pour l'obtenir en urgence |
| 2 | Responsabilité d'un blocage injustifié | ❌ | — |
| 2 | Absence de norme de performance des détecteurs | 🔶 | MinorShield (aucun texte ne fixe le seuil de score du blocage) |
| 2 | « Contenu inapproprié » contre catégories du détecteur | ❌ | — |
| 3 | Victime de 19 ans hors du champ de la charte | ❌ | — |
| 3 | Chevauchement MINAS / MINPROFF | ✅ | Protection sociale |
| 3 | Pas de directive scolaire pour les élèves victimes | ✅ | Protection sociale (étapes 2, 3, 5, 6) |
| 4 | Portée limitée face aux plateformes étrangères | ✅ | Régulateurs, chaîne pénale, conseiller |
| 4 | Mise en demeure de 15 jours inadaptée | 🔶 | Conseiller (48 heures proposées, art. 28 non désigné) |
| 5 | Autorité de protection des données récente | ❌ | — |
| 5 | Notification « sans délai », sans délai chiffré | 🔶 | Conseiller, protection sociale (présentée comme une absence d'obligation) |
| 6 | Protection de l'enfance contre liberté d'expression | ✅ | Conseiller (rubrique « conflits ») |
| 6 | Pas de mécanisme formel de coordination de crise | ✅ | Conseiller, à chaque étape |

Même total qu'au 24/10, avec des déplacements : le transfert vers le service
d'IA étranger progresse (🔶 → ✅, l'APDP applique l'art. 32) et la norme de
performance aussi (❌ → 🔶) ; la notification des violations recule (✅ → 🔶,
faute d'avoir eu l'art. 22 sous les yeux) et la responsabilité d'un blocage
aussi (🔶 → ❌). Les lacunes manquées restent celles de l'étape 2
(surveillance, responsabilité, définition) et le seuil d'âge : des questions
que le droit ne pose pas encore, et que des agents raisonnant à partir des
textes ne posent pas non plus. Elles figurent au rapport comme issues de
l'analyse humaine.

### Lacunes non prévues, relevées par la simulation

- **Image intime sous menace, avant publication** (étape 3, conseiller) : les
  obligations de retrait visent des publications existantes (art. 23(3)) ; rien
  ne permet d'agir quand l'auteur menace seulement de diffuser.
- **Accès de la police aux données d'un outil privé de protection** (étapes 2
  à 4, chaîne pénale) : aucune procédure propre pour obtenir les journaux de
  MinorShield ; l'agent croit devoir passer par l'APDP (à nuancer : le Code de
  procédure pénale permet les réquisitions).
- **Texte d'application manquant** : l'art. 10(2) de la loi n° 2023/009 renvoie à
  un texte précisant le rôle de l'ANTIC, introuvable (étape 6, régulateurs).

### Erreurs de l'IA

| Erreur | Détectée par le vérificateur automatique ? |
|---|---|
| Identifiant d'extrait inventé (« E24 », étape 4) | ✅ oui (citation invalide) |
| Citations qui sautent un élément de liste ou un mot sans « ... » (6 cas, contenu fidèle) | ✅ oui (citations douteuses) |
| Actions sans aucune source (8 cas, surtout des mesures pratiques : sensibilisation, modules d'information) | ✅ oui (non étayées) |
| Obligation de notifier les parents d'une violation attribuée à la règle COPPA (étape 5) ; la phrase citée existe, mais porte sur l'usage des coordonnées des parents | ❌ non : relecture humaine |
| « Ordonnances de conservation » et délais de transmission australiens (étape 2) ; la phrase citée porte sur des déclarations publiques du Commissaire | ❌ non : relecture humaine |
| Avis de blocage australiens étendus à tout « matériel jugé préjudiciable » (étape 6) ; ils visent la violence odieuse | ❌ non : relecture humaine |
| Notification des violations présentée comme absente (étape 5) alors que l'art. 22 de la loi n° 2024/017 impose d'informer « sans délai » | ❌ non : relecture humaine |
| Durée de conservation présentée comme non définie (étape 2) alors que l'art. 13 de la loi n° 2024/017 la renvoie à l'autorisation de traitement | ❌ non : relecture humaine |
| « Compétence exclusive » des officiers de police judiciaire pour constater (étape 4) alors que l'art. 32(1) de la loi n° 2023/009 habilite aussi les agents assermentés de l'ANTIC | ❌ non : relecture humaine |
| Faits inventés par MinorShield (étape 5) : accord écrit des parents, transmission « aux autorités américaines » | ❌ non : relecture humaine (échantillon de précision) |
| Pouvoirs de l'ANTIC déduits du seul art. 10 (suspendre des paiements Mobile Money, bloquer une plateforme) | ❌ non : relecture humaine (échantillon de précision) |

Le vérificateur contrôle désormais que chaque affirmation **cite un extrait
réellement fourni** et **en recopie une phrase mot pour mot**. Il ne peut pas
contrôler que cette phrase **justifie** ce que l'agent affirme : les erreurs
COPPA et australiennes ci-dessus s'appuient sur des citations exactes. La
précision mesurée par relecture (`docs/precision/`) le chiffre : 50 % des
affirmations « étayées » sont entièrement fondées (IC 95 % 33–67 %), 77 % au
moins en partie. D'où la lacune de normes N1 et l'obligation d'une relecture
juridique humaine.
