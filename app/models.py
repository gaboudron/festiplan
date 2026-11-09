# app/models.py — Simple pont / façade de réexport
from app.adapters.outbound.repository.models import (
    Artist,
    Concert,
    Festival,
    Incident,
    Stage,
)

__all__ = ["Festival", "Artist", "Stage", "Concert", "Incident"]