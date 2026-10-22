from dataclasses import dataclass
from app.domain.equipments import EquipmentSet

@dataclass
class Artist:
    id   : int | None
    name : str
    genre: str
    required_equipment: EquipmentSet