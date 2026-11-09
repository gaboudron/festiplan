# Checklist de la migration hexagonale — décisions arbitrées

État de référence : `main` à jour avec `origin/main` (PR #2 et #3 fusionnées).
Suite complète : **102 tests passent** (`python tests/run_tests.py -q`).

Légende : ✅ fait · 🔄 en cours · ⏸ reporté · ⬜ à faire · **[R]** retenu

---

## Décisions

| # | Sujet | Décision |
|---|---|---|
| 1 | Pont `app/models.py` / legacy | Refacto à terme, donc **supprimé à terme**. Le code legacy reste **dans le versioning pour la traçabilité** (historique git), mais disparaît de l'arbre de travail à la fin. |
| 2 | Organisation des tests | ✅ Réalisé par le collègue. Classement **par couche**, plus explicite : `tests/adapters/outbound/`, `tests/ports/outbound/`. |
| 3 | Lanceur de tests | ✅ Réalisé par le collègue : `TEST_DIRS` couvre `tests/ports/outbound` et `tests/adapters/outbound`. |
| 4 | `test_sqlalchemy_repositories.py` | 🔄 En cours chez le collègue (5 tests passent déjà localement). |
| 5 | Frontière de transaction | **[R] A** — découpler au maximum : **le cas d'usage appelle le port qui effectue la transaction**. Le use case ne commit pas lui-même ; un port de transaction (UoW) porte le commit. |
| 6 | Point 4 — événements & notifications | **[R] A** — événements de domaine + bus/outbox, handlers après commit. Dépend du collègue. |
| 7 | Point 6 — règles d'état | **[R] B** — services de domaine : `SchedulingConflictChecker`, `EquipmentChecker`, + un `FestivalPolicy`. Dépend du collègue. |
| 8 | Périmètre | **[R] A** — nous : inbound (DTO, mappers, routeurs, DI, handlers). Collègue : domaine, use cases, persistance. |
| 9 | Style des use cases | **[R] A** — services d'application implémentant les ABC (`ConcertService(ConcertInboundPort)`, …, `IncidentService`). |
| 10 | Implémentation des use cases | **[R] A** — orchestrer entités + `SchedulingConflictChecker` + `EquipmentChecker` + ports sortants. |
| 11 | Tests unitaires des use cases | **[R] B** — `unittest.mock.MagicMock` (avec `spec=` sur les ABC), pas de faux repositories. Les fabriques/fixtures restent pour les entités. Convention mise à jour dans `tests/use_cases/README.md`. |
| 12 | Injection de dépendances | ⏸ On verra plus tard. |

---

## Reste à faire

### A. Préalables (presque terminés)

- [x] Aligner les modèles ORM sur `UTCDateTime` / `utc_now` (le collègue l'a fait de son côté ; notre commit local doublon a été absorbé par le rebase).
- [x] Pont de réexport `app/models.py`.
- [x] Renommer/déplacer les tests sortants et éviter la collision de noms.
- [x] Mettre `TEST_DIRS` à jour.
- [ ] 🔄 Valider `test_sqlalchemy_repositories.py` à 100% et relancer `test_timezone.py` après coup (collègue).
- [ ] Vérifier que `pytest -q` (découverte libre) et `python tests/run_tests.py` donnent le même résultat.

### B. À trancher / livrer par le collègue

- [ ] ⬜ Définir le **port de transaction** (UoW) dans `app/ports/outbound/` : signature, qui l'implémente, quand le commit a lieu (décision 5).
- [ ] ⬜ **Point 4** : mode de déclenchement des événements et des notifications (bus/outbox, handlers après commit) — décision 6.
- [ ] ⬜ **Point 6** : `FestivalPolicy` et la liste des exceptions d'état à lever — décision 7.
- [ ] ⬜ Implémenter les use cases dans `app/use_cases/` (décisions 8, 9, 10), dont `IncidentService`.
- [ ] ⬜ Rendre le changement de scène effectif : `Concert.reschedule(..., new_stage_id=...)` doit être appelé par le use case.
- [ ] ⬜ Écrire les tests unitaires des use cases avec `MagicMock(spec=...)` (décision 11).
- [ ] ⬜ Ajouter le document d'architecture (décision n°7) au dépôt et consigner les arbitrages 5/6/7.

### C. Notre périmètre inbound

- [ ] ⏸ `app/adapters/inbound/api/dependencies.py` + `Depends()` (décision 12, plus tard).
- [ ] ⬜ Basculer les 5 routeurs sur les ports entrants uniquement : plus de `Session` ni de `db.query` (`get_concert`, `routers/incidents.py`).
- [ ] ⬜ Simplifier `mappers/common.py` et supprimer la compatibilité ORM/CSV.
- [ ] ⬜ Retirer les `try/except ValueError/RuntimeError` quand les use cases lèveront les exceptions du domaine.
- [ ] ⬜ Corriger les 404 des entités liées à la création d'un concert.
- [ ] ⬜ Réécrire les tests d'intégration HTTP avec `app.dependency_overrides` avant la suppression du legacy.
- [ ] ⬜ **Nettoyage final** : supprimer `app/services/`, `app/repositories/` et le pont `app/models.py` de l'arbre de travail. Conservés dans l'historique git pour la traçabilité (décision 1).

### D. Livraison

- [ ] ⬜ Stratégie de branche : nouvelle branche depuis `main` (les deux PR sont fusionnées).
- [ ] ⬜ Push / PR : pas de push sans demande explicite.

---

## Ordre conseillé

1. Finir le point 4 et vérifier la suite complète.
2. Le collègue livre les arbitrages 5/6/7 et le port de transaction.
3. Use cases + tests unitaires.
4. Puis, côté inbound : DI → routeurs sur ports → mappers/catches/404 → nettoyage legacy.
5. Enfin : documentation, branche, PR.

## Points de vigilance

- Les tests HTTP actuels passent par les services legacy : la suppression finale les cassera si elle n'est pas précédée de leur réécriture.
- Le pont `app/models.py` est **transitoire** : ne pas le considérer comme de l'architecture cible.
- La décision 5 implique que les repositories ne doivent plus porter le `commit()` eux-mêmes (ils le font aujourd'hui dans `save()`).
