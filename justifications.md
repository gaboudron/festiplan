# Choix d'Implémentation & Architecture de FestiPlan

Ce document explique simplement la nouvelle organisation du projet **FestiPlan**, dossier par dossier et composant par composant, ainsi que les raisons pour lesquelles chaque choix a été fait.

---

## 1. Vue d'ensemble : Pourquoi cette architecture ?

Avant la refactorisation, tout le code était mélangé : les routes de l'API exécutaient directement des requêtes SQL, la logique métier était dispersée partout, et envoyer un simple email pouvait faire planter toute l'application même si les données étaient déjà enregistrées.

Nous avons réorganisé le code en **Architecture Hexagonale** avec une approche **DDD**.

Le principe fondamental est simple :
- **Le cœur métier (`domain/`) ne dépend de rien** : aucune base de données, aucun framework web, aucun outil externe.
- **Les cas d'usage (`use_cases/`) orchestrent les actions** : ils appliquent les règles métier et coordonnent la sauvegarde.
- **Les ports (`ports/`) définissent des contrats** : ils précisent ce que l'application sait faire (en entrée) et ce dont elle a besoin (en sortie).
- **Les adaptateurs (`adapters/`) gèrent la technique** : l'API FastAPI, la base de données SQLAlchemy, l'envoi d'emails.

---

## 2. Le Cœur Métier Pur : `app/domain/`

C'est la partie la plus importante de l'application. Elle contient uniquement du code Python standard, sans dépendance externe (pas de FastAPI, pas de SQLAlchemy, pas de Pydantic).

### Pourquoi un sous-dossier par concept (`festival/`, `concert/`, `artist/`, `incident/`) ?
Pour regrouper tout ce qui concerne une même idée au même endroit : l'entité, son statut, et ses événements. Cela évite de chercher des fichiers dispersés aux quatre coins du projet.

### Les Entités Riches (plutôt que des simples conteneurs de données)
- **Le problème avant :** Les entités étaient passives. N'importe quelle partie du code pouvait modifier `concert.status = "annulé"` ou changer une date sans vérifier si c'était cohérent.
- **Le choix fait :** Les entités contiennent désormais leur propre logique métier sous forme de méthodes explicites :
  - `concert.reschedule(...)` : reprogramme le concert.
  - `concert.cancel()` : annule le concert.
  - `festival.publish()` : publie la programmation.
  - `incident.mark_resolved()` : clôture un incident.
- **Pourquoi :** Une entité ne peut jamais se retrouver dans un état incohérent ou invalide.

### Les Objets de Valeur (`time_range.py`, `equipments.py`)
- **`TimeRange` (créneau horaire) :**
  - Au lieu de manipuler deux dates séparées (`start` et `end`), on utilise un objet unique `TimeRange`.
  - Il s'auto-valide dès sa création : la date de fin doit obligatoirement être après la date de début.
  - Il sait lui-même calculer s'il chevauche un autre créneau (`overlaps_with`) ou s'il est compris dans les dates du festival (`is_within`).
- **`EquipmentSet` (ensemble d'équipements) :**
  - Au lieu de stocker du texte avec des virgules (ex: `"micro,ampli,batterie"`) et de le découper manuellement partout dans le code, on utilise un ensemble immuable.
  - Il nettoie automatiquement les espaces, supprime les doublons, et sait vérifier si une scène possède tous les équipements demandés par un artiste (`is_satisfied_by`).
- **Les Statuts (`FestivalStatus`, `ConcertStatus`) :**
  - Des énumérations strictes (`PREPARATION`, `PUBLISHED`, `CANCELLED`).
  - Évite les fautes de frappe qui passaient inaperçues avec du simple texte libre (comme `"canceld"`).

### Les Services de Domaine (`app/domain/services/`)
Quand une règle métier concerne plusieurs entités en même temps, elle ne peut pas appartenir à une seule entité. On la place donc dans un service de domaine :
- **`conflict_checker.py` (`SchedulingConflictChecker`) :** Vérifie qu'un artiste n'est pas programmé à deux endroits en même temps, et qu'une scène n'accueille pas deux concerts en simultané.
- **`equipment_checker.py` (`EquipmentChecker`) :** Vérifie que la scène choisie a bien tout le matériel dont l'artiste a besoin.
- **`festival_policy.py` (`FestivalPolicy`) :** Vérifie les règles globales du festival (interdiction de modifier si le festival est déjà publié, vérification que le concert a lieu pendant le festival, vérification que la scène appartient bien au festival).

### Les Exceptions Métier (`app/domain/exceptions.py`)
Toutes les erreurs du domaine ont un nom explicite (`ArtistAlreadyScheduledError`, `StageOccupiedError`, `FestivalNotFoundError`, `InvalidTimeRangeError`). Cela permet de savoir immédiatement ce qui ne va pas sans avoir à interpréter un message d'erreur générique.

---

## 3. Les Ports : `app/ports/`

Les ports sont des contrats d'interface. Ils définissent **quoi faire**, mais jamais **comment le faire**.

### Pourquoi utiliser des classes abstraites (`abc.ABC`) ?
Nous avons choisi `abc.ABC` avec `@abstractmethod`. Si une classe technique oublie d'implémenter une méthode obligatoire, Python bloque immédiatement au démarrage avec une erreur claire, évitant ainsi les mauvaises surprises en cours d'exécution.

### A. Les Ports d'Entrée (`app/ports/inbound/`)
Ce sont les portes d'entrée de notre application. Ils listent tout ce que le monde extérieur a le droit de demander au système :
- `FestivalInboundPort` : lister, créer, publier un festival.
- `ConcertInboundPort` : lister, récupérer, programmer, replanifier, annuler un concert.
- `StageInboundPort` : lister et créer les scènes.
- `ArtistInboundPort` : lister et créer les artistes.
- `IncidentInboundPort` : déclarer et lister les incidents.

L'API FastAPI s'adresse uniquement à ces interfaces, sans jamais savoir ce qu'il y a derrière.

### B. Les Ports de Sortie (`app/ports/outbound/`)
Ce sont les besoins de notre application envers l'extérieur :

1. **Les Repositories (`ports/outbound/repository/`) :**
   - Une interface par entité (`FestivalRepositoryOutboundPort`, etc.).
   - **Une seule méthode `save(entity)`** : Elle sert à la fois pour la création et la mise à jour. Le cas d'usage n'a pas besoin de savoir si l'objet est nouveau ou s'il existe déjà en base.
   - **Pas de méthode `delete`** : Dans notre métier, on ne supprime pas de données physiquement. On change leur état (un concert annulé reste en base pour l'historique et pour prévenir les festivaliers).
   - **Nommage clair des listes** : `list_all()` pour tout récupérer, et `list_by_<id>()` pour filtrer (on évite le nom `list` tout court qui est déjà un mot réservé en Python).

2. **La Transaction (`ports/outbound/transaction/transaction_outbound_port.py`) :**
   - Définit les méthodes `commit()` et `rollback()`.
   - **Pourquoi un port dédié plutôt que de mettre le commit dans chaque dépôt ?**
     Quand un cas d'usage touche à plusieurs dépôts en même temps (ex: un incident et un concert), il ne doit y avoir qu'une seule transaction globale. Si chaque dépôt faisait son propre commit, on risquerait de valider une partie des données et d'échouer sur l'autre, laissant la base dans un état bancal.

3. **Le Bus d'Événements (`ports/outbound/events/domain_event_bus_outbound_port.py`) :**
   - Permet de publier des événements une fois que les données sont bien enregistrées en base.

4. **Les Notifications (`ports/outbound/notification/notification_outbound_port.py`) :**
   - Contrat pour envoyer des messages sans savoir si c'est par email, SMS ou notification mobile.

---

## 4. Les Cas d'Usage : `app/use_cases/`

Ce dossier contient les services applicatifs. Ils jouent le rôle de **chef d'orchestre** :
1. Ils reçoivent une demande venant d'un port d'entrée.
2. Ils vont chercher les entités dans les dépôts.
3. Ils demandent au domaine d'appliquer les règles métier.
4. Ils sauvegardent les entités.
5. Ils valident la transaction.
6. Ils publient un événement si tout s'est bien passé.

### Le fichier d'aide `_support.py`
Pour éviter de répéter du code dans chaque cas d'usage, deux mécanismes y sont centralisés :
- **`in_transaction(transaction, operation)`** : Exécute l'action de sauvegarde. Si ça réussit, il fait le `commit()`. Si une erreur survient, il fait automatiquement le `rollback()` pour nettoyer la base.
- **Les fonctions `require_*`** : Vont chercher une entité en base et lèvent immédiatement une erreur propre (ex: `ConcertNotFoundError`) si elle n'existe pas.

### Pourquoi des tests avec des doublures (Mocks) ?
Dans `tests/use_cases/`, on utilise des mocks Python (`MagicMock(spec=...)`). Comme les use cases ne dépendent que des interfaces des ports, on peut simuler les dépôts et la transaction sans créer de fichier de base de données. Les tests s'exécutent ainsi en quelques millisecondes.

---

## 5. Le Découpage des Mappers (Entrants et Sortants)

Les **Mappers** ont un rôle unique : traduire les données d'un format à un autre. Nous avons fait le choix de créer **un fichier par entité**, à la fois côté entrant et côté sortant.

### Pourquoi tout découper fichier par fichier ?
1. **Bien tout différencier** : Chaque entité a ses propres spécificités. Avoir un fichier par entité évite de mélanger la conversion d'un festival avec celle d'un artiste.
2. **Des tests beaucoup plus simples** : On peut tester le mapping d'une scène de manière complètement isolée, sans dépendre du reste de l'application.
3. **Moins de risques d'erreurs** : Modifier la façon de transformer un concert ne risque pas de casser la transformation d'un incident.

### A. Les Mappers Entrants (`app/adapters/inbound/api/mappers/`)
- Rôle : Traduire les requêtes HTTP (DTOs Pydantic) vers les entités du domaine, et traduire les entités du domaine vers les réponses HTTP.
- Ils travaillent **uniquement avec des objets du domaine pur** : plus aucune manipulation de dictionnaires complexes ou de chaînes CSV.

### B. Les Mappers Sortants (`app/adapters/outbound/repository/mappers/`)
- Rôle : Traduire les entités du domaine vers les tables de la base de données (SQLAlchemy), et inversement.
- **Support de la mise à jour en place (*in-place update*)** : La fonction `to_orm(entity, existing_orm)` sait soit créer une nouvelle ligne de base de données, soit mettre à jour une ligne existante déjà attachée à la session pour que SQLAlchemy suive les modifications tout seul.

---

## 6. Les Adaptateurs Techniques : `app/adapters/`

C'est ici que vit toute la technique. Si demain on change de framework ou de base de données, seul ce dossier est impacté.

### A. Adaptateurs d'Entrée : L'API FastAPI (`app/adapters/inbound/`)

1. **Les Routeurs (`api/routers/`) :**
   - Chaque routeur (`festivals.py`, `concerts.py`, `stages.py`, `artists.py`, `incidents.py`) est maintenant très court et très lisible.
   - Il ne fait plus aucune requête SQL directe (`db.query` a totalement disparu).
   - Il reçoit le DTO, appelle le service injecté, et renvoie la réponse.

2. **L'Injection de Dépendances (`api/dependencies.py`) :**
   - C'est l'endroit unique qui assemble tous les morceaux : il instancie la session de base de données, les dépôts, la transaction, le bus d'événements, et les injecte dans les use cases.
   - Grâce à FastAPI `Depends()`, tous les dépôts utilisés pendant une même requête HTTP partagent exactement la même session de base de données.
   - Permet de remplacer facilement n'importe quel service par un faux lors des tests d'intégration.

3. **Le Gestionnaire Global d'Exceptions (`exception_handler.py`) :**
   - Plutôt que d'écrire des blocs `try / except` dans chaque route de l'API, les erreurs du domaine sont interceptées au niveau global et traduites automatiquement en codes HTTP :
     - Entité non trouvée $\rightarrow$ **404 Not Found** (corrige le problème où un festival inexistant renvoyait une erreur 400).
     - Conflit d'horaire ou de scène $\rightarrow$ **409 Conflict**.
     - Action interdite (festival déjà publié) $\rightarrow$ **403 Forbidden**.
     - Donnée invalide (dates inversées, etc.) $\rightarrow$ **400 Bad Request**.
     - Format de requête invalide $\rightarrow$ **422 Unprocessable Entity**.

### B. Adaptateurs de Sortie : Infrastructure (`app/adapters/outbound/`)

1. **Les Modèles de Base de Données (`repository/models.py`) :**
   - Les tables SQLAlchemy sont rangées ici, car la base de données est un détail technique de stockage, pas une règle métier.
   - Les dates sont gérées avec un type personnalisé `UTCDateTime` pour garantir que tout est stocké et manipulé en temps universel (UTC).

2. **Les Repositories SQLAlchemy (`repository/*_sqlalchemy_repository.py`) :**
   - Implémentent les interfaces de sortie.
   - Font un simple `flush()` pour obtenir l'identifiant généré par la base, sans faire de `commit()`.

3. **L'Adaptateur de Transaction (`transaction/transaction_sqlalchemy_adapter.py`) :**
   - Implémente le port de transaction en appelant `self.db.commit()` ou `self.db.rollback()`.

4. **Le Bus d'Événements en Mémoire (`events/in_memory_event_bus_adapter.py`) :**
   - Permet de relier les événements du domaine aux notifications.
   - **Protection contre les pannes d'email :** Si le service d'envoi de mail tombe en panne, l'erreur est notée dans les logs mais ne bloque pas la réponse HTTP. L'utilisateur reçoit quand même sa confirmation puisque les données ont déjà été enregistrées avec succès en base de données.

5. **L'Adaptateur de Notification (`notification/email_notification_adapter.py`) :**
   - Formate et envoie les emails aux équipes de production.

---

## 7. Suppression Complète du Code Ancien (Legacy)

Une fois tous les routeurs branchés sur les cas d'usage et les tests validés, les anciens dossiers ont été complètement supprimés de l'arbre de travail :
- `app/services/` (anciens services procéduraux couplés) $\rightarrow$ supprimé.
- `app/repositories/` (anciens dépôts sans inversion de dépendance) $\rightarrow$ supprimé.
- `app/models.py` (ancienne façade temporaire) $\rightarrow$ supprimé.

### Pourquoi les supprimer totalement ?
- **Clarté :** Aucun doute possible pour un développeur arrivant sur le projet, il n'y a qu'une seule façon de faire les choses.
- **Sécurité :** Empêche d'importer par erreur un ancien fichier qui contournerait les validations métier.
- **Confiance :** Tout l'historique reste conservé dans Git en cas de besoin, le code mort n'a donc pas besoin de rester dans le projet actif.
