from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.adapters.outbound.repository import models  # noqa
from app.adapters.inbound.api.routers import (
    festivals,
    artists,
    stages,
    concerts,
    incidents,
)
from app.adapters.inbound.exception_handler import register_exception_handlers

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API de gestion d'un festival fictif",
)

register_exception_handlers(app)

for router in (
    festivals.router,
    artists.router,
    stages.router,
    concerts.router,
    incidents.router,
):
    app.include_router(router)


@app.get("/")
def health():
    return {"message": "Bienvenue sur FestiPlan", "status": "ok"}
