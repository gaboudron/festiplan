"""Routeurs HTTP de l'adaptateur entrant.

Chaque module expose un ``APIRouter`` FastAPI pour un agrégat du domaine.
Les routeurs reçoivent les ports entrants par injection de dépendances
(``app.adapters.inbound.api.dependencies``), traduisent les DTO entrants en
entités du domaine via les mappers, puis exposent des DTO de réponse.
"""
