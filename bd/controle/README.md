# Contrôle de la base de connaissances

- `requetes_controle.json` : 15 questions formulées comme un agent les poserait
  pendant la crise, chacune avec l'article attendu, vérifié à la main dans le
  texte officiel.
- `resultats_controle.md` : dernière mesure, produite par
  `python bd/scripts/controle_recherche.py` (aucun appel au modèle de langage).

## Mesure du 23 octobre 2026

| Mode | Article attendu en 1re position | Article attendu trouvé | MRR |
|---|---|---|---|
| Recherche brute (5 premiers résultats) | 7/15 | 7/15 | 0,47 |
| Recherche de l'agent (4 extraits reçus) | 11/15 | **14/15** | 0,82 |

La recherche brute est dominée par les longs textes étrangers (RGPD, Online
Safety Acts, Observation générale n° 25) : le texte national qui fonde le
mandat de l'agent n'apparaît pas. D'où les deux règles de la recherche des
agents (`agent/agent1_institutions/agent.py`) : les deux articles clés de son
mandat les plus pertinents (fiche de l'agent, `articles_cles`), au moins un
extrait de son texte principal, la moitié des extraits réservée à ses textes
prioritaires s'ils sont assez pertinents, et au plus deux extraits par texte.
Les articles clés ont fait passer Q11 (victime de 19 ans, Code pénal art. 347)
de « non trouvé » à trouvé.
La seconde règle a fait passer Q13 (organe de coordination émirien) de
« non trouvé » à trouvé.

## Échecs restants

- **Q10 (chantage)** : la question emploie le vocabulaire courant (« photos
  intimes », « si la victime ne paie pas ») alors que le Code pénal parle
  d'« imputation diffamatoire » ; la couche texte du PDF de l'OMPI a en outre
  perdu ses accents. Dans la simulation, les agents rédigent eux-mêmes leurs
  recherches en termes juridiques : ce test est plus sévère que l'usage réel.
  Les questions n'ont pas été reformulées pour réussir le test.
