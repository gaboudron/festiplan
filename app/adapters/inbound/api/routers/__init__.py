"""Routeurs HTTP de l'adaptateur entrant.

Chaque module expose un ``APIRouter`` FastAPI pour un agrégat du domaine.
Les routeurs traduisent les DTO entrants en entités du domaine via les
mappers, puis exposent des DTO de réponse.
"""
