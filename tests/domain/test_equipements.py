import pytest
from app.domain.equipments import EquipmentSet

# ==========================
# Tests Equipements
# ==========================

def test_equipment_items_immutable():
    """Vérifie que l'attribut items est bien immuable."""
    equipments = EquipmentSet(items=["lumières"])

    with pytest.raises(AttributeError, match="'frozenset' object has no attribute 'append'"):
        equipments.items.append("pyro")


def test_equipement_from_list_cleans_and_deduplicates():
    """Vérifie que la conversion list -> frozenset -> list fonctionne correctement."""
    items = [" lumières ", "pyro", "  ", "", "pyro"]
    equipments = EquipmentSet.from_list(items)

    assert equipments.to_list() == ["lumières", "pyro"]


def test_equipment_set_satisfies_required_equipment():
    """Vérifie que satisfies retourne True si la scène dispose de tous les équipements requis."""
    stage_equipments = EquipmentSet.from_list(["lumières", "son", "fumée", "pyro"])
    artist_required = EquipmentSet.from_list(["lumières", "son"])

    assert stage_equipments.satisfies(artist_required) is True


def test_equipment_set_fails_when_equipment_missing():
    """Vérifie que satisfies retourne False s'il manque au moins un équipement requis."""
    stage_equipments = EquipmentSet.from_list(["lumières", "son"])
    artist_required = EquipmentSet.from_list(["lumières", "son", "pyro"])

    assert stage_equipments.satisfies(artist_required) is False


