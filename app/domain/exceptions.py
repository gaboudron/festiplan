class DomainException(Exception):
    """Exception de base pour toutes les erreurs métiers du domaine."""
    def __init__(self, message: str = "Une erreur métier est survenue."):
        self.message = message
        super().__init__(self.message)


# ==============================================================================
# Erreurs de validation & invariants (Créneaux, Matériel, etc.)
# ==============================================================================

class InvalidTimeRangeError(DomainException):
    """Levée quand la date de fin est antérieure ou égale à la date de début."""
    def __init__(self, message: str = "La date de fin doit être postérieure à la date de début."):
        super().__init__(message)


class EquipmentMismatchError(DomainException):
    """Levée quand la scène ne dispose pas de tous les équipements requis par l'artiste."""
    def __init__(self, message: str = "La scène ne dispose pas de tous les équipements requis."):
        super().__init__(message)


# ==============================================================================
# Erreurs de conflits de planning (Concerts, Scènes, Artistes)
# ==============================================================================

class ScheduleConflictError(DomainException):
    """Exception générique pour tout conflit de programmation."""
    pass


class StageOccupiedError(ScheduleConflictError):
    """Levée si la scène est déjà réservée sur ce créneau."""
    def __init__(self, message: str = "Conflit : la scène est déjà occupée sur ce créneau."):
        super().__init__(message)


class ArtistAlreadyScheduledError(ScheduleConflictError):
    """Levée si l'artiste est déjà programmé sur une autre scène sur ce créneau."""
    def __init__(self, message: str = "Conflit : l'artiste est déjà programmé sur ce créneau."):
        super().__init__(message)


# ==============================================================================
# Erreurs de cohérence du Festival & États
# ==============================================================================

class ConcertOutsideFestivalDatesError(DomainException):
    """Levée si un concert est programmé en dehors des dates du festival."""
    def __init__(self, message: str = "Le concert doit se dérouler pendant les dates du festival."):
        super().__init__(message)


class StageDoesNotBelongToFestivalError(DomainException):
    """Levée si on tente d'associer un concert à une scène qui n'est pas celle du festival."""
    def __init__(self, message: str = "La scène n'appartient pas à ce festival."):
        super().__init__(message)


class FestivalAlreadyPublishedError(DomainException):
    """Levée si on tente de modifier arbitrairement un concert dans un festival déjà publié."""
    def __init__(self, message: str = "Impossible de modifier un concert : le festival est déjà publié."):
        super().__init__(message)


# ==============================================================================
# Erreurs de non-trouvé (Entity Not Found)
# ==============================================================================
class EntityNotFoundError(DomainException):
    """Classe de base quand une entité recherchée n'existe pas."""
    pass


class FestivalNotFoundError(EntityNotFoundError):
    def __init__(self, festival_id: int):
        super().__init__(f"Festival #{festival_id} introuvable.")


class ConcertNotFoundError(EntityNotFoundError):
    def __init__(self, concert_id: int):
        super().__init__(f"Concert #{concert_id} introuvable.")


class StageNotFoundError(EntityNotFoundError):
    def __init__(self, stage_id: int):
        super().__init__(f"Scène #{stage_id} introuvable.")


class ArtistNotFoundError(EntityNotFoundError):
    def __init__(self, artist_id: int):
        super().__init__(f"Artiste #{artist_id} introuvable.")
