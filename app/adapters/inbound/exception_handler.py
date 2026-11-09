from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# à adapter en fonction des exceptions gérées dans la logique métier (domain/exceptions.py)
from app.domain.exceptions import (
    DomainException,
    EntityNotFoundError,
    ScheduleConflictError,
    FestivalAlreadyPublishedError
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Enregistre tous les gestionnaires d'exceptions globaux sur l'instance FastAPI.
    """

    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
        # Couvre FestivalNotFoundError, ConcertNotFoundError, etc.
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "type": "NOT_FOUND",
                "detail": exc.message
            }
        )

    @app.exception_handler(ScheduleConflictError)
    async def schedule_conflict_handler(request: Request, exc: ScheduleConflictError):
        # Couvre StageOccupiedError et ArtistAlreadyScheduledError (R2 et R3)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "type": "SCHEDULE_CONFLICT",
                "detail": exc.message
            }
        )

    @app.exception_handler(FestivalAlreadyPublishedError)
    async def festival_published_handler(request: Request, exc: FestivalAlreadyPublishedError):
        # Couvre la règle R7 (planning publié)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "type": "FORBIDDEN_ACTION",
                "detail": exc.message
            }
        )

    @app.exception_handler(DomainException)
    async def fallback_domain_handler(request: Request, exc: DomainException):
        # Filet de sécurité pour les autres règles (InvalidTimeRangeError, EquipmentMismatchError...)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "BAD_REQUEST",
                "detail": exc.message
            }
        )

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_handler(request: Request, exc: RequestValidationError):
        # Surcharge de l'erreur native de FastAPI/Pydantic pour uniformiser le format de réponse
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "type": "VALIDATION_ERROR",
                "detail": "Le format des données reçues est invalide.",
                # ``exc.errors()`` peut contenir des objets non sérialisables
                # (par ex. ``ctx.error`` avec une ValueError).
                "errors": jsonable_encoder(exc.errors())
            }
        )