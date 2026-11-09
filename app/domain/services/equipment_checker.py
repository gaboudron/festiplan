from app.domain.artist.entities import Artist
from app.domain.exceptions import EquipmentMismatchError
from app.domain.festival.entities import Stage


class EquipmentChecker:
    @staticmethod
    def check(artist: Artist, stage: Stage) -> None:
        """Vérifie que la scène fournit tous les équipements requis par l'artiste."""
        if not stage.available_equipment.satisfies(artist.required_equipment):
            raise EquipmentMismatchError()
