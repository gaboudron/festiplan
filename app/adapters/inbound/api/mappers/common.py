"""Helpers partagés par les mappers de l'adaptateur entrant."""

from datetime import datetime
from typing import Any

from app.domain.equipments import EquipmentSet


def require_persisted_id(entity_id: int | None) -> int:
    """Garantit qu'une entité possède un identifiant avant exposition API."""
    if entity_id is None:
        raise ValueError(
            "L'entité doit être persistée avant d'être exposée par l'API."
        )
    return entity_id


def equipment_items(equipment: EquipmentSet | None) -> list[str]:
    """Extrait la liste d'équipements depuis un ``EquipmentSet`` du domaine."""
    if equipment is None:
        return []
    return equipment.to_list()


def status_value(status: Any) -> str:
    """Retourne la valeur texte d'un statut (énumération du domaine)."""
    return status.value if hasattr(status, "value") else str(status)


def resolve_time_range(entity: Any) -> tuple[datetime, datetime]:
    """Extrait les bornes temporelles d'une entité du domaine."""
    time_range = entity.time_range
    return time_range.start, time_range.end
