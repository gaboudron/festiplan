#!/usr/bin/env python3
"""Script pour lancer les tests du domaine FestiPlan (Python standard & uv) :

Commandes d'exécution :
    # Avec uv :
    uv run python tests/run_tests.py
    uv run pytest tests/domain -v

    # Avec Python standard :
    python tests/run_tests.py
    pytest tests/domain -v

Options utiles :
    # Filtrer par mot-clé (ex: uniquement les tests concert)
    uv run python tests/run_tests.py -k concert
    python tests/run_tests.py -k concert

    # S'arrêter dès la première erreur rencontrée
    uv run python tests/run_tests.py -x
    python tests/run_tests.py -x
"""
import sys
from pathlib import Path
import pytest

# Racine du projet (festiplan/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOMAIN_TESTS_DIR = PROJECT_ROOT / "tests" / "domain"

# Garantit que la racine du projet est dans sys.path (permet l'exécution sans PYTHONPATH=.)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    extra_args = sys.argv[1:]
    pytest_args = [str(DOMAIN_TESTS_DIR), "-v"] + extra_args

    print(f"Exécution des tests du domaine FestiPlan ({DOMAIN_TESTS_DIR.name}/)\n")
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
