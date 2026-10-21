# `app/models/` — modèles de **données**, pas modèles d'IA

Ce dossier ne contient que les modèles de données SQLAlchemy
(`db_models.py` : parents, enfants, détections, abonnements).

**La logique d'intelligence artificielle ne se trouve pas ici.** Elle est dans
[`app/services/`](../services/) :

| Rôle | Fichier |
|---|---|
| Enchaînement et décision finale | `../services/detection_service.py` |
| Détection de nudité (NudeNet) | `../services/image_service.py` |
| Détection de violence (OpenAI) | `../services/violence_service.py` |
| Analyse de texte + lexique camerounais | `../services/text_service.py` |
| Extraction OCR (Tesseract) | `../services/ocr_service.py` |

Aucun poids de modèle n'est versionné : voir
[ARCHITECTURE_IA.md](../../../ARCHITECTURE_IA.md) à la racine du dépôt pour le
détail des modèles utilisés et du calcul des scores.
