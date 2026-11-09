from app.domain.equipments import EquipmentSet


class EquipmentMapper:
    @staticmethod
    def to_domain(raw: str | None) -> EquipmentSet:
        if not raw:
            return EquipmentSet(items=frozenset())
        items = [x.strip() for x in raw.split(",") if x.strip()]
        return EquipmentSet.from_list(items)

    @staticmethod
    def to_orm(equipment: EquipmentSet) -> str:
        return ",".join(equipment.to_list())

