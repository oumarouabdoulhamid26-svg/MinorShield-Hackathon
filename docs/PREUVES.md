# Annoncé, prouvé, limite

> Chaque affirmation que le rapport technique peut faire, avec la preuve qui
> la soutient et sa limite. Règle de rédaction : **une affirmation sans preuve
> dans ce tableau ne figure pas dans le rapport**. Chiffres de la simulation de
> référence du 24/10/2026 (`docs/exemple_simulation/`, gpt-oss-120b), sauf
> mention contraire. Tableau établi le 25/10/2026.

| Ce qu'on annonce | Preuve | Limite |
|---|---|---|
| Base de connaissances de textes officiels, citables article par article | 13 textes camerounais et 7 références internationales ; 8 344 passages ; provenance de chaque fichier dans `bd/SOURCES.md` | La loi n° 2024/017 provient d'un scan (OCR relu par sondage) ; le Code pénal a perdu ses accents dans la source de l'OMPI ; version australienne de 2021 (avant la réforme de 2024) |
| La recherche retrouve le bon article | 15 requêtes de contrôle vérifiées à la main : 14/15 trouvées, 11/15 en première position, MRR 0,82, contre 7/15 pour une recherche brute (`bd/controle/`) | 15 questions, rédigées par l'équipe ; une question en langage courant (chantage) échoue encore |
| Les agents justifient leurs actions par des extraits réels | 86,4 % des 110 affirmations vérifiées sont étayées par un extrait fourni (95 étayées, 4 douteuses, 10 non étayées, 1 invalide) ; APDP 100 %, conseiller 95 % | Le vérificateur ne contrôle pas que l'extrait dit bien ce que l'agent affirme : 4 erreurs de ce type trouvées à la relecture humaine (`docs/LACUNES.md`, section C) |
| Coordination entre agents aux mandats différents | 25 demandes transmises entre agents, aucune perdue ; 29 destinataires écrits avec le nom d'une institution redirigés vers le bon agent ; 13 passations internes (police → parquet…) | 10 demandes écartées par la limite de 6 par étape fixée dans le ML Intent (choix d'économie de jetons) |
| Chaque action dit quelle institution agit | 69 actions sur 69 avec une institution valide | Contrôle de forme : il ne juge pas si l'institution est la bonne |
| Information révélée progressivement et inégalement | Chaque étape n'est révélée qu'à ses destinataires (événement `etape_revelee`) ; l'information circule ensuite par les demandes | Scénario unique, écrit par l'équipe |
| Identification des lacunes du droit, comparées au monde | 15 lacunes attendues : 7 retrouvées, 3 partiellement, 5 manquées (relecture humaine) ; 4 lacunes non prévues relevées ; 10 lacunes documentées avec références internationales vérifiées (`docs/LACUNES.md`) | Les lacunes manquées (surveillance, normes, définition, âge) viennent de l'analyse humaine et sont présentées comme telles ; 3 comparaisons internationales du conseiller étaient inexactes |
| Alignement avec UIT-T Y.3172 | 15 exigences sur 20 mises en œuvre, 4 partiellement, 2 non, chacune avec sa preuve (`docs/Y3172.md`) | Application par analogie : Y.3172 vise les réseaux de télécommunications |
| ML Intent déclaratif | `agent/intent.json` lu au démarrage ; son empreinte figure dans le journal ; test `test_intent_configure_les_modules` | Ajouter un agent demande encore une fiche dans `roles.py` |
| Reconfiguration automatique | 2 nouvelles tentatives dans la référence (protection sociale et chaîne pénale, étape 3, toutes deux améliorées), 5 dans la v1 ; bascule de modèle prouvée par test | La bascule de modèle n'a pas eu lieu dans la référence (quota suffisant) : prouvée par test et par un essai réel du 23/10 |
| Reprise d'une simulation interrompue | Tests `test_reprise_ne_rejoue_pas_les_etapes_terminees` et `test_arret_propre_si_aucun_modele_ne_repond` | Jamais utilisée sur une simulation de référence réelle |
| Journal d'audit complet et traçable | `journal.jsonl` : informations vues, extraits fournis, raisonnement, réponse, vérification, modèle et jetons de chaque intervention ; page de démonstration ; rejeu sans modèle | Le raisonnement journalisé est celui que l'agent explicite, pas la réflexion interne du modèle |
| Fonctionne avec des moyens modestes | 165 279 jetons et 21 minutes pour une simulation complète, sur un ordinateur portable sans GPU, avec des modèles à poids ouverts gratuits | Quota gratuit de 200 000 jetons par jour : une seule simulation complète par jour |
| Cas d'usage réel | Architecture réelle de l'application MinorShield (code dans `application/`) ; sortie de détection au format réel de son API | La sortie de détection est simulée : la simulation n'appelle pas l'application |
| Robustesse du code | 9 tests de l'orchestrateur, avec un faux modèle (aucun jeton) | Pas de test de bout en bout avec le vrai modèle dans la suite de tests |
