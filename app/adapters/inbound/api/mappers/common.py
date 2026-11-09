"""Helpers partagés par les mappers de l'adaptateur entrant."""

from datetime import datetime
from typing import Any


def require_persisted_id(entity_id: int | None) -> int:
    """Garantit qu'une entité possède un identifiant avant exposition API."""
    if entity_id is None:
        raise ValueError(
            "L'entité doit être persistée avant d'être exposée par l'API."
        )
    return entity_id


def equipment_items(value: Any) -> list[str]:
    """Normalise un ensemble d'équipements en liste de chaînes.

    Accepte indifféremment un ``EquipmentSet`` du domaine, une liste ou la
    chaîne CSV utilisée par les modèles ORM historiques.
    """
    if value is None:
        return []

    to_list = getattr(value, "to_list", None)
    if callable(to_list):
        return to_list()

    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]

    return [str(item).strip() for item in value if str(item).strip()]


def status_value(value: Any) -> str:
    """Retourne la valeur texte d'un statut (enum du domaine ou chaîne ORM)."""
    return value.value if hasattr(value, "value") else str(value)


def resolve_time_range(entity: Any) -> tuple[datetime, datetime]:
    """Extrait les bornes temporelles d'une entité du domaine ou d'une ligne ORM."""
    time_range = getattr(entity, "time_range", None)
    if time_range is not None:
        return time_range.start, time_range.end

    if hasattr(entity, "start_date"):
        return entity.start_date, entity.end_date

    return entity.start_time, entity.end_time
