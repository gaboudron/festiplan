# Réexport des modèles déplacés dans l'adaptateur de persistance
# pour préserver le fonctionnement du code legacy (app/repositories/) sans le modifier.
from app.adapters.outbound.repository.models import (
    Artist,
    Concert,
    Festival,
    Incident,
    Stage,
)

__all__ = ["Festival", "Artist", "Stage", "Concert", "Incident"]
