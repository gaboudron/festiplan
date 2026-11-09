# Checklist de la migration hexagonale — décisions arbitrées

État de référence : `main` à jour avec `origin/main` (PR #2 et #3 fusionnées).
Suite complète : **162 tests passent** (`python tests/run_tests.py -q`, identique à `pytest -q`).

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
| 8 | Périmètre | **[R] A**, amendé : le collègue n'a pas le temps, donc **nous reprenons aussi les use cases**. Restent au collègue : la persistance et les arbitrages qu'il avait en cours. |
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
- [x] Valider `test_sqlalchemy_repositories.py` et relancer `test_timezone.py` (suite verte).
- [x] Vérifier que `pytest -q` (découverte libre) et `python tests/run_tests.py` donnent le même résultat.
- [x] `UTCDateTime` sait désormais servir de type d'annotation Pydantic (`__get_pydantic_core_schema__`) ; alias `UTCDateTimeOrNone` ajouté et réexportés depuis `app/models.py` (collègue, `bf4d592`).

### B. Use cases — repris par nous (collègue indisponible)

- [x] Définir le **port de transaction** dans `app/ports/outbound/transaction/` (`commit` / `rollback`) — décision 5.
- [x] Définir le **port de bus d'événements** dans `app/ports/outbound/events/` — décision 6, versant use case.
- [x] **Point 6** : `FestivalPolicy` dans `app/domain/services/` + tests unitaires — décision 7.
- [x] Implémenter les 5 services applicatifs dans `app/use_cases/` (`ArtistService`, `StageService`, `FestivalService`, `ConcertService`, `IncidentService`) — décisions 9, 10.
- [x] Rendre le changement de scène effectif : `Concert.reschedule(..., new_stage_id=...)` est appelé par `ConcertService`.
- [x] Écrire les tests unitaires des use cases avec `MagicMock(spec=...)` (décision 11) : 43 tests.
- [x] **Adaptateur du bus** : implémentation concrète (`InMemoryEventBusAdapter` dans `app/adapters/outbound/events/`) + handlers de notification (`register_notification_handlers`) traduisant les événements en appels à `NotificationOutboundPort` + tests unitaires (8 tests).
- [x] **Retirer le `commit()` des repositories SQLAlchemy** : fait par le collègue (`ab169f7`), `save()` ne fait plus qu'un `flush()`. Le port de transaction est donc le seul propriétaire du commit. `SqlAlchemyTransactionAdapter` est implémenté et testé.
- [ ] ⬜ Ajouter le document d'architecture (décision n°7) au dépôt et consigner les arbitrages 5/6/7.

### C. Notre périmètre inbound

- [x] `app/adapters/inbound/api/dependencies.py` + `Depends()` (décision 12, câblage complet repositories, transaction, bus d'événements et 5 use cases) : 5 tests.
- [ ] ⬜ Basculer les 5 routeurs sur les ports entrants uniquement : plus de `Session` ni de `db.query` (`get_concert`, `routers/incidents.py`).
- [ ] ⬜ Simplifier `mappers/common.py` et supprimer la compatibilité ORM/CSV.
- [ ] ⬜ Retirer les `try/except ValueError/RuntimeError` quand les use cases lèveront les exceptions du domaine.
- [ ] ⬜ Corriger les 404 des entités liées à la création d'un concert.
- [ ] ⬜ Réécrire les tests d'intégration HTTP avec `app.dependency_overrides` avant la suppression du legacy.
- [ ] ⬜ **Nettoyage final** : supprimer `app/services/`, `app/repositories/` et le pont `app/models.py` de l'arbre de travail. Conservés dans l'historique git pour la traçabilité (décision 1).

### D. Livraison

- [ ] ⏸ Stratégie de branche : le travail a été fait directement sur `main` ; à redécider pour la suite si besoin.
- [x] Push de `main` effectué sur demande explicite (7 commits rebasés + ce correctif). Règle conservée : pas de push sans demande ; PR à ouvrir si besoin.

---

## Ordre conseillé

1. ✅ Préalables, pull, suite verte.
2. ✅ Ports de transaction / événements, `FestivalPolicy`, use cases, tests unitaires.
3. ⏭ DI (décision 12) : instancier repositories + use cases, fournir l'adaptateur du port de transaction (`commit`/`rollback` sur la session), implémenter le bus et ses handlers.
4. Puis, côté inbound : routeurs sur ports → mappers/catches/404 → réécriture des tests HTTP.
5. Enfin : nettoyage legacy, documentation, branche, PR.

## Points de vigilance

- Les tests HTTP actuels passent par les services legacy : la suppression finale les cassera si elle n'est pas précédée de leur réécriture.
- Le pont `app/models.py` est **transitoire** : ne pas le considérer comme de l'architecture cible.
- ✅ La décision 5 est respectée côté persistance : les repositories ne font plus que `flush()`. **Il manque encore l'adaptateur concret de `TransactionOutboundPort`** (à câbler avec le DI) : sans lui, les écritures des use cases ne sont pas validées en base.
- Les routeurs appellent encore les services legacy : les use cases ne sont pas exposés à l'API tant que le DI n'est pas fait.
