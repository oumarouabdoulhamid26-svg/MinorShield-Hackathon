# app/schemas/response.py
# Définit la forme exacte des réponses JSON
# retournées à l'application Android.
#
# Pydantic valide automatiquement que les données
# respectent bien ces schémas avant d'être envoyées.

from pydantic import BaseModel, Field
from typing import Optional


class DetectionResponse(BaseModel):
    """
    Réponse complète retournée à l'Android après analyse d'une image.

    Exemple de réponse JSON que recevra l'application Android :
    {
        "request_id"    : "a1b2c3d4-e5f6-...",
        "nsfw_score"    : 0.89,
        "label"         : "nsfw",
        "image_score"   : 0.92,
        "text_score"    : 0.81,
        "extracted_text": "texte détecté sur l'écran...",
        "processing_ms" : 245,
        "timestamp"     : "2024-01-15T14:32:01.123456"
    }
    """

    request_id : str = Field(
        description = "Identifiant unique de chaque requête — utile pour le débogage"
    )

    nsfw_score : float = Field(
        ge          = 0.0,
        le          = 1.0,
        description = "Score combiné final (image × 60% + texte × 40%) — entre 0.0 et 1.0"
    )

    label : str = Field(
        description = "Décision finale : 'safe' si contenu approprié, 'nsfw' si inapproprié"
    )

    category : Optional[str] = Field(
        default      = None,
        description  = "Raison du blocage si label='nsfw' : 'nudite', 'violence' ou 'texte'. None si safe."
    )

    image_score : float = Field(
        ge          = 0.0,
        le          = 1.0,
        description = "Score brut de l'analyse visuelle uniquement"
    )

    text_score : float = Field(
        ge          = 0.0,
        le          = 1.0,
        description = "Score brut de l'analyse textuelle uniquement"
    )

    extracted_text : Optional[str] = Field(
        default     = None,
        description = "Texte extrait de l'image par OCR — None si aucun texte détecté"
    )

    processing_ms : int = Field(
        description = "Temps total de traitement en millisecondes"
    )

    timestamp : str = Field(
        description = "Horodatage de l'analyse au format ISO 8601"
    )


class HealthResponse(BaseModel):
    """
    Réponse du endpoint /health.
    Permet à l'Android de vérifier que le serveur est opérationnel.

    Exemple :
    {
        "status"        : "ok",
        "message"       : "MinorShield API opérationnelle",
        "version"       : "1.0.0",
        "environment"   : "development",
        "models_loaded" : true,
        "timestamp"     : "2024-01-15T14:32:01"
    }
    """

    status        : str  = Field(description="Statut du serveur : 'ok' ou 'error'")
    message       : str  = Field(description="Message descriptif du statut")
    version       : str  = Field(description="Version actuelle de l'API")
    environment   : str  = Field(description="Environnement : development ou production")
    models_loaded : bool = Field(description="True si les modèles IA sont chargés et prêts")
    timestamp     : str  = Field(description="Horodatage de la vérification")