from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, field_validator

from app.adapters.inbound.exception_handler import register_exception_handlers
from app.domain.exceptions import (
    ConcertNotFoundError,
    DomainException,
    EntityNotFoundError,
    EquipmentMismatchError,
    FestivalAlreadyPublishedError,
    ScheduleConflictError,
    StageOccupiedError,
)
from app.main import app


def test_handlers_are_registered_on_the_application():
    assert EntityNotFoundError in app.exception_handlers
    assert ScheduleConflictError in app.exception_handlers
    assert FestivalAlreadyPublishedError in app.exception_handlers
    assert DomainException in app.exception_handlers


def _build_client() -> TestClient:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/conflict")
    def conflict():
        raise StageOccupiedError()

    @test_app.get("/forbidden")
    def forbidden():
        raise FestivalAlreadyPublishedError()

    @test_app.get("/missing")
    def missing():
        raise ConcertNotFoundError(42)

    @test_app.get("/invalid")
    def invalid():
        raise EquipmentMismatchError()

    @test_app.get("/validated")
    def validated(count: int):
        return {"count": count}

    class Payload(BaseModel):
        name: str

        @field_validator("name")
        @classmethod
        def reject_forbidden_value(cls, value: str) -> str:
            if value == "boom":
                raise ValueError("valeur interdite")
            return value

    @test_app.post("/payload")
    def payload(body: Payload):
        return {"name": body.name}

    return TestClient(test_app)


def test_schedule_conflict_maps_to_409():
    response = _build_client().get("/conflict")

    assert response.status_code == 409
    assert response.json()["type"] == "SCHEDULE_CONFLICT"


def test_published_festival_maps_to_403():
    response = _build_client().get("/forbidden")

    assert response.status_code == 403
    assert response.json()["type"] == "FORBIDDEN_ACTION"


def test_entity_not_found_maps_to_404():
    response = _build_client().get("/missing")

    assert response.status_code == 404
    assert response.json()["type"] == "NOT_FOUND"


def test_other_domain_errors_map_to_400():
    response = _build_client().get("/invalid")

    assert response.status_code == 400
    assert response.json()["type"] == "BAD_REQUEST"


def test_validation_errors_use_the_unified_format():
    response = _build_client().get("/validated", params={"count": "abc"})

    assert response.status_code == 422
    assert response.json()["type"] == "VALIDATION_ERROR"


def test_validation_error_details_are_json_serializable():
    response = _build_client().post("/payload", json={"name": "boom"})

    assert response.status_code == 422
    body = response.json()
    assert body["type"] == "VALIDATION_ERROR"
    assert body["errors"][0]["msg"] == "Value error, valeur interdite"
