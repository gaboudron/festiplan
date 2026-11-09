"""Helpers de gestion des dates : convention unique UTC aware.

Convention du projet :
- tout datetime qui circule dans le domaine est **aware** et en UTC ;
- les datetimes naïfs reçus à la frontière sont interprétés comme de l'UTC ;
- la persistance stocke des datetimes naïfs UTC et les restitue en aware UTC.
"""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator
from sqlalchemy.types import DateTime, TypeDecorator


def ensure_utc(value: datetime) -> datetime:
    """Normalise un datetime en UTC aware (naïf => considéré UTC)."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def ensure_utc_or_none(value: datetime | None) -> datetime | None:
    return None if value is None else ensure_utc(value)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# Types Pydantic à utiliser dans les DTO entrants / sortants.
UTCDatetime = Annotated[datetime, AfterValidator(ensure_utc)]
UTCDatetimeOrNone = Annotated[datetime | None, AfterValidator(ensure_utc_or_none)]


class UTCDateTime(TypeDecorator):
    """Type SQLAlchemy stockant l'UTC naïf et restituant de l'UTC aware."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return ensure_utc(value).replace(tzinfo=None)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return ensure_utc(value)
