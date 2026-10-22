from dataclasses import dataclass

@dataclass(frozen=True)
class EquipmentSet:
    items: frozenset[str]

    @classmethod
    def from_list(cls, items: list[str]) -> EquipmentSet:
        cleaned = {item.strip() for item in items if item.strip()}
        return cls(items=frozenset(cleaned))

    def satisfies(self, required: EquipmentSet) -> bool:
        """Vérifie si tous les équipements requis sont bien disponibles."""
        return required.items.issubset(self.items)

    def to_list(self) -> list[str]:
        return sorted(list(self.items))
