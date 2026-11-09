from app.domain.artist.entities import Artist
from app.domain.equipments import EquipmentSet

# ==========================
# Tests Artist
# ==========================

def test_artist_creation():
    """Vérifie la création d'un artiste avec ses équipements requis."""
    equipment = EquipmentSet.from_list(["guitare", "ampli", "micro"])
    artist = Artist(
        id=1,
        name="Gojira",
        genre="Metal",
        required_equipment=equipment,
    )

    assert artist.id == 1
    assert artist.name == "Gojira"
    assert artist.genre == "Metal"
    assert "ampli" in artist.required_equipment.items

