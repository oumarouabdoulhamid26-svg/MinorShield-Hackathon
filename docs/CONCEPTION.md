# MinorShield Policy Lab — Document de conception

> **Statut :** assistants et scénario validés le 17/10/2026.
> **Hackathon :** ITU AI for Good Lab — agents IA et bases de connaissances politiques.

---

## 1. L'objectif en une phrase

Plusieurs assistants IA, jouant chacun une institution camerounaise et s'appuyant
sur nos lois réelles, gèrent ensemble une crise de protection des enfants en
ligne ; chacun justifie ses décisions par l'article de loi utilisé, et un
conseiller identifie ce qui manque dans nos lois par rapport aux meilleures
pratiques mondiales.

---

## 2. Comment le projet répond à l'énoncé

| Exigence du hackathon | Notre réponse |
|---|---|
| Base de connaissances de lois, stratégies et réglementations | Lois camerounaises + références mondiales, ingérées avec le code de référence de l'UIT (§6) |
| Agent « solution d'IA innovante » | **Agent MinorShield** : signale les tendances détectées sur le terrain |
| Agent « conseiller en politique et juridique » | **Conseiller juridique** : cite la loi, identifie les lacunes face aux pratiques mondiales |
| Agents « participants institutionnels » | **6 institutions** camerounaises (§3) |
| Coordination multi-agents, mandats et informations différents | Protocole par tours, visibilité de l'information propre à chaque agent (§5) |
| Scénario de crise séquencé, informations incomplètes et décalées | **5 étapes** révélées progressivement, chacune à une partie des agents seulement (§4) |
| Journal d'audit et traçabilité du raisonnement | Chaque étape enregistrée : informations vues, extraits de loi retrouvés, raisonnement, décision (§7) |
| Alignement UIT-T Y.3172 et cadre de préparation à l'IA | Correspondance explicite dans l'architecture (§8) |

**Note de l'énoncé à respecter :** l'évaluation porte sur les **lacunes propres
au domaine** et la **pertinence des exemples mondiaux**, plus que sur l'analyse
d'un pays. Le Cameroun est notre terrain d'étude ; la valeur est dans la
comparaison avec le reste du monde.

---

## 3. Les assistants

Chaque assistant a :

- une **mission** (ce qu'il a le droit de faire selon la loi) ;
- un **périmètre d'information** (ce qu'il apprend, et quand) ;
- des **sources prioritaires** dans la base de connaissances.

> **Regroupement validé avec le mentor le 22/10/2026.** Plusieurs institutions
> ne disposaient que d'un article de loi chacune (MINAS, MINPROFF, MINESEC) et
> d'autres partageaient exactement les mêmes textes (police et parquet). Les
> 13 acteurs initiaux sont donc regroupés en **6 agents** par objectif commun,
> sans réunir des acteurs dont les intérêts s'opposent :
>
> | Agent (identifiant) | Institutions représentées (n° du tableau ci-dessous) |
> |---|---|
> | Régulateurs du numérique (`regulateurs`) | ANTIC, ART, MINPOSTEL (1, 2, 3) |
> | Protection des données (`apdp`) | APDP (4) |
> | Chaîne pénale (`penal`) | Police judiciaire, Parquet (8, 9) |
> | Protection sociale et éducative (`social`) | MINAS, MINPROFF, MINESEC (5, 6, 7) |
> | Entreprises du numérique (`entreprises`) | Opérateurs, Tchatlink, ScolaPlus (11, 12, 13) |
> | Agent innovant (`minorshield`) | MinorShield (10) |
>
> Avec le conseiller et l'animateur : **8 assistants**, dont 7 agents IA.
> Un agent qui regroupe plusieurs institutions précise, pour chaque action,
> laquelle agit. Les tableaux ci-dessous détaillent les institutions
> représentées.

**15 assistants** (liste initiale validée le 17/10/2026 après vérification des sources).

### Institutions publiques

| # | Assistant | Mission | Sources prioritaires | Vérification |
|---|---|---|---|---|
| 1 | **ANTIC** — Agence nationale des TIC, dont le **CIRT national** | Réponse aux incidents informatiques, collecte de preuves numériques, coopération internationale (INTERPOL, AfricaCERT) | Loi 2010/012 | ✅ CIRT logé à l'ANTIC depuis 2012 |
| 2 | **ART** — Agence de régulation des télécommunications | Régulation et sanction des opérateurs | Loi 2010/013 (modifiée par la loi 2015/006), décret 2012/203 | ✅ |
| 3 | **MINPOSTEL** — Ministère des Postes et Télécommunications | Politique publique du numérique ; plan d'action national de protection des enfants en ligne ; dialogue avec les plateformes | Loi 2023/009 | ✅ A porté la loi 2023/009 |
| 4 | **APDP** — Autorité de protection des données personnelles | Contrôle des traitements de données, violations de données | Loi 2024/017 (art. 53) | ✅ En vigueur depuis le 23/06/2026 |
| 5 | **MINAS** — Ministère des Affaires sociales | Protection sociale de l'enfance, prise en charge des victimes | Loi 2023/009 | ✅ Direction de la protection sociale de l'enfance |
| 6 | **MINPROFF** — Ministère de la Promotion de la femme et de la famille | Protection de la famille et de l'enfant | Loi 2023/009, décret 2012/638 | ✅ Chevauchement avec le MINAS, **non délimité par les textes** |
| 7 | **MINESEC** — Ministère des Enseignements secondaires | Encadrement des établissements et des élèves | Loi 2023/009 | ⚠️ Aucune directive trouvée sur la protection des élèves en ligne |
| 8 | **Police judiciaire** | Enquête, préservation et analyse des preuves | Loi 2010/012, art. 52 à 59 | ⚠️ Compétences exactes à lire dans le texte |
| 9 | **Parquet** (ministère public) | Poursuites, autorisations judiciaires | Loi 2010/012, art. 52 à 59 et 60 à 89 | ⚠️ Compétences exactes à lire dans le texte |

### Acteurs privés

| # | Assistant | Mission | Sources prioritaires |
|---|---|---|---|
| 10 | **MinorShield** — *rôle « solution d'IA innovante »* | Détecte et remonte les tendances anormales ; ne détient que des **données agrégées et anonymisées** | Documentation technique MinorShield |
| 11 | **Opérateurs télécoms** | Fournisseurs d'accès : contrôle parental et filtrage **imposés par la loi 2023/009** ; exécution d'éventuels blocages | Loi 2023/009, loi 2010/013 |
| 12 | **Plateforme de messagerie étrangère** (fictive) | Siège hors du Cameroun ; applique ses propres règles de modération | Politiques internes ; références mondiales (DSA, Online Safety Act) |
| 13 | **Éditeur de l'application scolaire** (fictif) | Responsable du traitement des données des élèves | Loi 2024/017 |

### Rôles transversaux

| # | Assistant | Rôle dans l'énoncé | Mission |
|---|---|---|---|
| 14 | **Conseiller juridique et politique** | Conseiller en politique | Vérifie la base légale de chaque décision ; compare avec les pratiques mondiales ; signale lacunes et conflits |
| 15 | **Animateur de la simulation** | Coordination multi-agents | Révèle les étapes, transmet les demandes entre assistants, synthétise. **Ne joue aucune institution et ne décide de rien.** |

> **Constat issu de la vérification :** aucun organe national formel de
> coordination de crise numérique n'a été identifié. C'est pourquoi l'animateur
> est neutre — et cette **absence de mécanisme formel de coordination** est
> elle-même une lacune que la simulation doit faire apparaître.

> **Noms fictifs :** la plateforme étrangère et l'application scolaire sont
> inventées, pour ne mettre en cause aucune entreprise réelle.

---

## 4. Le scénario de crise — « Opération Miroir »

Une campagne de **chantage sexuel (sextorsion)** vise des élèves
camerounais. L'information arrive **par morceaux, à des moments différents, et
pas aux mêmes institutions** — comme dans une vraie crise. Certaines
informations sont **incertaines** au moment où elles arrivent.

Les noms d'entreprises sont fictifs : la messagerie étrangère s'appelle
**« Tchatlink »** et l'application de gestion scolaire **« ScolaPlus »**.

### Le déroulé

| Étape | Moment | Ce qui se passe | Qui est informé |
|---|---|---|---|
| **1** | J0, 08h | MinorShield constate une **hausse de 400 %** des contenus bloqués sur des appareils de Douala et Yaoundé, avec le même vocabulaire d'argot local et des messages type « envoie ta photo sinon… ». **On ne sait pas encore s'il s'agit d'une campagne organisée.** | MinorShield, ANTIC |
| **2** | J0, 16h | Des parents se présentent dans des centres sociaux. **Deux victimes** : une collégienne de **15 ans** et une lycéenne de **19 ans**, menacées de voir publiées des photos intimes si elles ne paient pas. Le collège de la plus jeune **envisage de l'exclure**. | MINAS, MINPROFF, Police judiciaire, MINESEC |
| **3** | J1, 10h | Des images circulent sur **Tchatlink**, dont le siège est à l'étranger. La plateforme répond qu'elle traitera la demande « selon ses délais habituels ». Les opérateurs sont sollicités pour un filtrage. | MINPOSTEL, ART, Opérateurs, Tchatlink, Police judiciaire, Parquet |
| **4** | J1, 18h | Les escrocs ont obtenu les numéros des victimes par une **fuite de données de ScolaPlus**, utilisée par 300 établissements. L'éditeur **n'a encore notifié personne**. | APDP, ANTIC, ScolaPlus, MINESEC, Police judiciaire, Parquet |
| **5** | J2, 09h | Pression médiatique ; une proposition circule : **bloquer entièrement Tchatlink** dans le pays. | Tous |

Le **conseiller juridique** intervient à chaque étape. L'**animateur** gère la
circulation de l'information. Chacun des 13 acteurs intervient au moins une
fois avant l'étape 5. Depuis le regroupement du 22/10/2026, les destinataires
de chaque étape sont les 6 agents correspondants (voir
`agent/scenarios/operation_miroir.json`).

### Ce que chaque étape doit faire émerger

| Étape | Questions juridiques attendues | Lacunes ou conflits attendus | Comparaison mondiale |
|---|---|---|---|
| **1** | Un outil privé peut-il alerter les autorités ? Avec quelles données, sans violer la vie privée des enfants ? | Pas de cadre de signalement entre acteurs privés et autorités | Obligation de signalement des plateformes (DSA) ; signalement des contenus pédocriminels (États-Unis) |
| **2** | Prise en charge des victimes ; qualification pénale ; qui pilote : MINAS ou MINPROFF ? Une école peut-elle exclure une victime ? | **La victime de 19 ans n'est pas couverte** par la loi 2023/009 (moins de 18 ans, alors que la majorité civile est à 21 ans) ; **chevauchement MINAS/MINPROFF** ; aucune directive scolaire | Observation générale n° 25 de l'ONU : intérêt supérieur de l'enfant, ne pas punir la victime |
| **3** | Peut-on contraindre une plateforme étrangère ? Dans quel délai ? Les opérateurs peuvent-ils filtrer un contenu précis ? | Portée extraterritoriale limitée ; absence de délai légal de retrait | DSA européen ; Online Safety Act britannique ; pouvoirs de retrait en 24 h du commissaire australien |
| **4** | Obligation et délai de notification de la fuite ; responsabilité de ScolaPlus ; sanctions | APDP en place depuis juin 2026 seulement : procédures en construction | Notification en 72 h (RGPD) ; données des moins de 13 ans (COPPA) |
| **5** | Un blocage national est-il proportionné ? Qui peut l'ordonner ? | **Conflit d'objectifs** : protection de l'enfance contre liberté d'expression et impact économique ; **absence de mécanisme formel de coordination de crise** | Exigences de proportionnalité dans les cadres européens et onusiens |

### Inspiration réelle

L'étape 2 s'inspire d'un **cas réel survenu en février 2025** : une
collégienne camerounaise a été exclue de son établissement après la diffusion
d'une vidéo compromettante ; des défenseurs des droits de l'enfant ont dénoncé
une victime sanctionnée au lieu d'être accompagnée.

---

## 5. Le protocole de coordination

La simulation se déroule **étape par étape**. À chaque étape :

```
1. Le coordinateur révèle l'étape — uniquement aux assistants concernés.
2. Chaque assistant concerné :
     a. lit ce qu'il sait (étapes reçues + messages qui lui sont adressés) ;
     b. cherche dans la base les articles de loi pertinents ;
     c. produit une réponse structurée (voir ci-dessous).
3. Le coordinateur transmet les demandes d'un assistant à un autre
   (ex. : la Police demande à l'APDP l'identité de l'éditeur de l'application).
4. Le conseiller juridique vérifie la base légale de chaque décision
   et relève les lacunes.
5. Tout est enregistré dans le journal d'audit.
```

**La réponse de chaque assistant contient toujours :**

| Champ | Contenu |
|---|---|
| `evaluation` | Sa lecture de la situation, avec ce qu'il sait — et ce qu'il **ignore** |
| `actions` | Les actions qu'il prend, **dans les limites de sa mission** |
| `base_legale` | Pour chaque action : l'article de loi et l'extrait exact retrouvé dans la base |
| `demandes` | Ce qu'il demande aux autres assistants |
| `lacunes` | Ce que la loi ne lui permet pas de faire, ou ne prévoit pas |
| `confiance` | Son niveau de certitude (0 à 1) |
| `raisonnement` | Les étapes de son raisonnement, explicitées |

**Règle centrale :** un assistant n'agit **qu'avec l'information qu'il a
reçue**. Il ne peut pas « deviner » une étape qu'on ne lui a pas montrée. C'est
ce qui rend la simulation réaliste, et c'est ce que l'énoncé demande.

---

## 6. La base de connaissances

Elle est construite avec le **code d'ingestion de référence de l'UIT**, que nous
avons amélioré sur deux points mesurés :

| Amélioration | Mesure |
|---|---|
| Classeur multilingue `bge-m3` à la place de `nomic-embed-text` | Test sur des textes juridiques français : 3/3 questions réussies au lieu de 2/3, marge moyenne 0,285 au lieu de 0,025 |
| Correction de la détection du pays d'un document | 20 documents sur 67 étaient mal étiquetés (dont 3 attribués à tort à l'Inde) |

### Documents à intégrer

**Cameroun**

| Texte | Statut |
|---|---|
| Loi n° 2023/009 du 25 juillet 2023 portant charte de protection des enfants en ligne | Existence vérifiée — texte officiel à récupérer |
| Loi n° 2024/017 du 23 décembre 2024 relative à la protection des données à caractère personnel | Existence vérifiée — texte officiel à récupérer |
| Loi n° 2010/012 du 21 décembre 2010 relative à la cybersécurité et la cybercriminalité | Texte disponible en ligne |
| Loi n° 2010/013 du 21 décembre 2010 régissant les communications électroniques | À vérifier |

**Références mondiales**

| Texte | Pourquoi |
|---|---|
| Online Safety Act 2023 (Royaume-Uni) | Devoir de vigilance des plateformes envers les enfants |
| Digital Services Act (Union européenne), dont l'art. 28 | Protection des mineurs, retrait des contenus, portée extraterritoriale |
| RGPD, art. 8 (Union européenne) | Consentement des mineurs aux traitements de données |
| COPPA (États-Unis) | Données des enfants de moins de 13 ans |
| Online Safety Act 2021 (Australie) | Commissaire indépendant à la sécurité en ligne, pouvoirs de retrait rapide |
| Observation générale n° 25 (ONU, 2021) | Droits de l'enfant dans l'environnement numérique |

**Déjà fournis par l'UIT :** 57 documents, dont la stratégie continentale de
l'Union africaine, la déclaration de Kigali, les stratégies du Kenya, du
Nigeria et du Rwanda, la norme Y.3172 et le cadre de préparation à l'IA.

---

## 7. Traçabilité et journal d'audit

Chaque étape de la simulation produit une entrée de journal :

| Élément enregistré | Exemple |
|---|---|
| Horodatage, étape, assistant | `J1-10h · étape 3 · ART` |
| Informations visibles par l'assistant | étapes 3 ; message de MINPOSTEL |
| Extraits retrouvés dans la base | `Loi_2023-009.pdf`, morceau 14, proximité 0,71 |
| Raisonnement explicité | « La plateforme est étrangère, donc… » |
| Décision et base légale | « Mise en demeure du fournisseur d'accès — art. X » |
| Modèle utilisé | `openai/gpt-oss-120b` |

Le journal est exporté en **JSON** (pour l'analyse) et en **page lisible**
(pour le jury). Une décision sans source retrouvée dans la base est **signalée
comme non étayée** — on ne cache pas les faiblesses.

---

## 8. Alignement avec la norme UIT-T Y.3172

| Nœud Y.3172 | Dans notre projet |
|---|---|
| **SRC** (sources de données) | Textes de loi et stratégies ; signaux agrégés de MinorShield |
| **Collector / Preprocessor** | Ingestion : extraction du texte, découpage, embeddings `bge-m3` |
| **ML Function** | Les assistants (recherche dans la base + raisonnement du modèle de langage) |
| **SINK** | Décisions, recommandations, rapport de lacunes |
| **Sandbox** | La simulation de crise elle-même : on teste des politiques sans conséquence réelle |

Dimensions du cadre de préparation de l'UIT principalement concernées :
**D4** (contextualisation et impact régional), **D7** (alignement stratégique),
**D10** (IA et politiques), **D11** (IA pour l'inclusion).

---

## 9. Interface de démonstration

Une **page web** pour la vidéo et le jury :

- une ligne du temps des 5 étapes ;
- les messages de chaque assistant, avec son institution ;
- pour chaque décision, l'article de loi cité, consultable ;
- le rapport final de lacunes, comparé aux pratiques mondiales.

---

## 10. Livrables

| Livrable | Contenu |
|---|---|
| Rapport technique | 5 pages maximum, modèle fourni par l'UIT |
| Dépôt GitHub | Code, documentation, instructions d'installation |
| Base de connaissances | Documents sources + script d'ingestion |
| Vidéo de démonstration | 7 minutes maximum (obligatoire si présélection) |

---

## 11. Contraintes connues

| Contrainte | Conséquence | Parade |
|---|---|---|
| Quota Groq gratuit : 200 000 jetons par jour et par modèle | Environ 2 à 3 simulations complètes par jour sur le grand modèle | Essais sur le petit modèle (quota séparé) ; extraits de loi plus courts |
| PC sans carte graphique | Remplissage de la base lent (~3 s par morceau) | Opération faite une seule fois, en arrière-plan |
| Textes officiels pas encore récupérés | Les assistants ne peuvent pas encore citer nos lois | Étape suivante : collecte et vérification |

---

## 12. Points à valider

1. La liste des **9 assistants** convient-elle ? Faut-il en ajouter ou en retirer ?
2. Le **scénario « Opération Miroir »** est-il le bon ? (Alternative possible :
   une fuite de données d'enfants par une application éducative.)
3. Les **5 étapes** et la répartition de l'information sont-elles réalistes ?
4. Nom du projet : **MinorShield Policy Lab** — à garder ?
