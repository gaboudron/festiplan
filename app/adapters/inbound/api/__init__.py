"""Adaptateur entrant HTTP de FestiPlan.

Regroupe les DTO, les mappers, les routeurs FastAPI et l'injection de
dépendances. Aucune logique métier ne vit ici : les routeurs appellent les
ports entrants (``app/ports/inbound``), implémentés par ``app/use_cases``.
"""
