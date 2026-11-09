#!/usr/bin/env python3
"""Script pour lancer les tests de FestiPlan (Python standard & uv).

Commandes d'exécution :
    # Avec uv :
    uv run python tests/run_tests.py
    uv run pytest tests/domain tests/ports tests/use_cases tests/adapters/inbound -v

    # Avec Python standard :
    python tests/run_tests.py
    pytest tests/domain tests/ports tests/use_cases tests/adapters/inbound -v

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

# Ajouter ici chaque nouveau dossier de tests.
TEST_DIRS = [
    PROJECT_ROOT / "tests" / "domain",
    PROJECT_ROOT / "tests" / "ports" / "inbound",
    PROJECT_ROOT / "tests" / "use_cases",
    PROJECT_ROOT / "tests" / "adapters" / "inbound",
]

# Garantit que la racine du projet est dans sys.path (permet l'exécution sans PYTHONPATH=.)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    extra_args = sys.argv[1:]
    test_dirs = [str(directory) for directory in TEST_DIRS if directory.exists()]
    pytest_args = test_dirs + ["-v"] + extra_args

    print("Lancement des tests FestiPlan :")
    for directory in test_dirs:
        print(f"  - {directory}")
    print()

    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
