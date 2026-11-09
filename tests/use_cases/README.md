# Tests des cas d'usage

Ce dossier contient les tests de la couche application : les cas d'usage
(`use cases`) qui orchestrent le domaine et les ports sortants.

## Principes

- **Pas de base de données, pas de HTTP.** Un test de cas d'usage ne doit ni
  ouvrir de session SQLAlchemy ni passer par `TestClient`. Les dépendances
  sortantes seront remplacées par des faux adaptateurs en mémoire.
- **Un test vérifie un comportement.** Le nom du test décrit l'action et le
  résultat attendu, pas l'implémentation.
- **Pas de faux repositories pour l'instant.** Ils seront ajoutés quand les
  ports sortants (`app/ports/outbound/`) seront définis, afin que les faux
  respectent les vrais contrats.
- **Aucune assertion sur les détails internes** (nombre d'appels, ordre des
  requêtes) sauf si ce comportement fait partie du contrat.

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
    # Arrange : préparer les entrées et les faux adaptateurs
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
