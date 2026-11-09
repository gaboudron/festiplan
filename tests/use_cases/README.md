# Tests des cas d'usage

Ce dossier contient les tests de la couche application : les cas d'usage
(`use cases`) qui orchestrent le domaine et les ports sortants.

## Principes

- **Pas de base de données, pas de HTTP.** Un test de cas d'usage ne doit ni
  ouvrir de session SQLAlchemy ni passer par `TestClient`.
- **Doublures avec `unittest.mock.MagicMock`.** Les dépendances sortantes
  (repositories, notification, transaction) sont remplacées par des
  `MagicMock` calés sur les ABC de `app/ports/outbound/` via `spec=`, pour
  rester alignés sur les vrais contrats sans écrire de faux repositories.
- **Un test vérifie un comportement.** Le nom du test décrit l'action et le
  résultat attendu, pas l'implémentation.
- **Aucune assertion sur les détails internes** (nombre d'appels, ordre des
  requêtes) sauf si l'appel fait partie du contrat : c'est le cas de la
  transaction et des notifications, dont on vérifie le déclenchement.

## Doublures des dépendances

Les fabriques et fixtures de ce dossier construisent de **vraies entités du
domaine** ; seules les dépendances sortantes sont doublées :

```python
from unittest.mock import MagicMock

from app.ports.outbound.repository.concert_repository_outbound_port import (
    ConcertRepositoryOutboundPort,
)
from app.ports.outbound.notification.notification_outbound_port import (
    NotificationOutboundPort,
)

repository = MagicMock(spec=ConcertRepositoryOutboundPort)
repository.get.return_value = concert
notifications = MagicMock(spec=NotificationOutboundPort)
```

Décision d'architecture associée : **le cas d'usage ne porte pas le commit**.
Il appelle un port de transaction qui effectue la transaction, afin de
découpler au maximum la logique applicative de la persistance. Ce port sera
lui aussi doublé par un `MagicMock`, et l'on vérifiera qu'il a été appelé.

## Organisation

- Un fichier par cas d'usage : `test_<nom_du_cas_usage>.py`.
- Regrouper dans un même fichier les tests d'un même cas d'usage.
- Utiliser les fabriques et les fixtures partagées plutôt que de construire
  les entités à la main.

| Élément | Rôle |
|---|---|
| `factories.py` | Fabriques d'entités : `make_artist`, `make_stage`, `make_festival`, `make_concert`, `make_incident`. |
| `conftest.py` | Fixtures de base : `artist`, `stage`, `festival`, `concert`, `incident`, plus les créneaux par défaut. |

Les fabriques acceptent des valeurs par défaut surchargeables par mot-clé :

```python
from factories import make_concert, make_stage

concert = make_concert(stage_id=3)
scene = make_stage(name="Second Stage", capacity=2_000)
```

Les fixtures renvoient des objets neufs à chaque test. Un test peut donc
modifier son entité sans impacter les autres tests.

## Structure d'un test

Suivre le schéma *Arrange / Act / Assert* et commenter chaque étape :

```python
def test_<comportement>_<resultat_attendu>(concert):
    # Arrange : préparer les entités et les MagicMock des ports sortants
    nouvelle_plage = TimeRange(...)

    # Act : appeler le cas d'usage
    resultat = use_case.execute(concert.id, nouvelle_plage)

    # Assert : vérifier le résultat ou l'exception
    assert resultat.time_range == nouvelle_plage
```

Pour les cas d'erreur, vérifier l'exception du domaine :

```python
import pytest

from app.domain.exceptions import StageOccupiedError

def test_<comportement>_leve_une_erreur(...):
    with pytest.raises(StageOccupiedError):
        use_case.execute(...)
```

> Les noms de cas d'usage ci-dessus sont illustratifs. Utiliser les noms
> réels dès qu'ils seront implémentés.

## Conventions de date

Toutes les dates manipulées par le domaine sont **UTC aware**. Les fabriques
produisent déjà des dates conformes ; ne pas introduire de
`datetime.utcnow()` naïf dans les tests.

## Exécution

```bash
# Tous les tests du projet
python tests/run_tests.py

# Uniquement les cas d'usage
python -m pytest tests/use_cases -v
```

Le dossier `tests/use_cases` est déjà enregistré dans `TEST_DIRS`
(`tests/run_tests.py`).
