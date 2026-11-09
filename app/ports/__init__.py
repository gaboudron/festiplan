"""Ports de l'architecture hexagonale.

Deux familles de contrats abstraits (``abc.ABC``) :

- ``app.ports.inbound`` : cas d'usage appelés par l'adaptateur entrant ;
- ``app.ports.outbound`` : persistance, transaction, notifications et bus
  d'événements utilisés par les cas d'usage.

Ces ports ne connaissent ni HTTP ni SQLAlchemy : ils manipulent uniquement
des entités du domaine.
"""
