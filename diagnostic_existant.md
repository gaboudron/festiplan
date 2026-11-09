# Diagnostic Architectural de l'Existant — Projet FestiPlan

## 1. Contexte et Architecture Initiale

- **Projet :** FestiPlan (planification de festivals, gestion des scènes, artistes, concerts et incidents).
- **Structure initiale :** Architecture en couches (`api` -> `services` -> `repositories` -> `models.py`).
- **Paradigme :** Data-Driven / CRUD centré sur l'ORM SQLAlchemy et le framework FastAPI.

---

## 2. Ce qui ne va pas dans le code de base

### Couplage fort et fuite des responsabilités
- **Accès SQL direct dans les contrôleurs :** `app/api/concerts.py` exécute directement des requêtes `db.query(Concert)` dans les routes `get_concert` et `reschedule_concert`.
- **Double requête inutile :** le contrôleur de replanification interroge la base, puis appelle le service qui recharge à nouveau l'entité via son dépôt.
- **Absence totale de couche intermédiaire pour les incidents :** `app/api/incidents.py` manipule directement la session SQL (`db.add`, `db.commit`, `db.refresh`) sans service ni repository.
- **Duplication de logique :** la méthode `publish` est implémentée deux fois, dans `FestivalService` et dans `PublicationService`.
- **Transformation de données dans l'API :** les routes de `stages.py` et `artists.py` parsent manuellement les chaînes de caractères (`split(",")`) au lieu de déléguer à des adaptateurs ou DTOs.

### Entités passives sans logique métier
- **Explication du concept :** les entités ne sont que des coquilles vides contenant des colonnes de base de données (données passives), sans aucune règle de gestion ni méthode d'action. La logique se retrouve donc éparpillée dans les services ou les contrôleurs.
- **Entités réduites à des sacs de données :** les classes de `app/models.py` héritent de SQLAlchemy et n'embarquent aucune méthode métier.
- **Absence d'encapsulation :** tous les champs sont mutables publiquement depuis l'extérieur sans contrôle d'état (`concert.status = ...`).
- **Incapacité d'auto-validation :** une entité peut être instanciée dans un état invalide (ex: un concert avec une date de fin antérieure à la date de début).

### Absence d'objets métiers dédiés : utilisation excessive de types basiques (chaînes de caractères, dates brutes)
- **Explication :** au lieu de créer des objets métiers spécifiques avec leurs propres règles, le code utilise uniquement des types primitifs (textes, dates isolées).
- **Plages temporelles non modélisées :** gestion par couples de dates brutes (`start_time`, `end_time`) au lieu d'un objet créneau horaire, avec appel manuel à une fonction utilitaire procédurale `overlaps()`.
- **Équipements stockés sous forme de texte brut :** stockage sous forme d'une simple chaîne délimitée par des virgules (`"micro,ampli,batterie"`), nettoyée et découpée à la volée (`split(",")`) à plusieurs endroits du code.
- **Statuts sous forme de chaînes libres :** utilisation de `str` au lieu d'énumérations strictes, exposant le code aux erreurs de saisie silencieuses (par exemple une faute de frappe comme `"canceld"`).

### Invariants non protégés et failles logiques critiques
- **Faille majeure lors de la replanification (`reschedule_concert`) :**
  - Les conflits de scène ne sont pas vérifiés (deux concerts en même temps sur la même scène).
  - Les conflits d'artistes ne sont pas vérifiés (un artiste sur deux scènes à la fois).
  - Le respect des dates du festival n'est pas contrôlé.
  - La compatibilité des équipements n'est pas revalidée.
  - La replanification n'est pas bloquée si le festival est déjà publié.
- **Publication non sécurisée :** passage du festival à `published` sans validation globale de l'intégrité du planning.
- **Asymétrie de validation :** la création d'un concert applique des contrôles stricts, mais la mise à jour les ignore totalement.

### Effets de bord et gestion transactionnelle défaillante
- **Couplage technique dur :** `NotificationService` dépend directement de la fonction technique `send_email`.
- **Désynchronisation post-commit :** la notification est envoyée après `self.db.commit()`. Si l'envoi d'email échoue, l'API renvoie une erreur HTTP 500 alors que les données sont déjà enregistrées en base.
- **Absence d'événements de domaine (Domain Events) :** aucun découplage entre la logique métier et les actions secondaires.

### Testabilité compromise
- **Dépendance totale à l'infrastructure :** impossible de tester une simple règle métier sans créer un fichier de base SQLite temporaire et exécuter les migrations.
- **Tests de bout en bout obligatoires :** obligation de passer par `TestClient(app)` et des requêtes HTTP pour valider un calcul horaire.
- **Exécution lente :** lenteur des entrées/sorties disque et réinitialisation manuelle des tables entre chaque test.

---

## 3. Ce qui aurait posé problème en continuant sans l'Architecture Hexagonale

- **Services fourre-tout concentrant toute la logique applicative :**
  - Gonflement continu et incontrôlé de fichiers comme `SchedulingService` à mesure que s'ajoutent de nouvelles règles (billetterie, balances sonores, pauses techniques, jauges de sécurité).
  - Enchevêtrement de conditions `if/else`, de requêtes SQL et d'appels externes au même endroit, rendant la maintenance très difficile.
- **Multiplication des contournements de règles (Bypass) :**
  - Tout nouveau contrôleur, script batch ou tâche asynchrone aurait pu modifier directement les entités SQL sans exécuter les validations nécessaires.
  - Perte progressive de la maîtrise de l'intégrité des données en base.
- **Dépendance bloquante aux technologies externes (dépendance au framework et à l'ORM) :**
  - **Explication :** la logique métier est intimement liée à FastAPI et SQLAlchemy. L'application devient prisonnière de ces outils, ce qui rend tout changement technologique extrêmement lourd.
  - Logique métier dépendante des détails de la base de données et du framework web à tous les niveaux.
  - Impossibilité de changer de base de données (ex: passer de SQLite à une base PostgreSQL optimisée ou NoSQL) ou de remplacer l'ORM sans devoir réécrire l'ensemble du projet.
  - Impossibilité d'isoler des modèles optimisés pour la lecture (séparation lecture / écriture).
- **Incapacité à supporter d'autres interfaces d'accès :**
  - La logique étant parfois écrite directement dans les routes HTTP FastAPI, elle est impossible à réutiliser dans d'autres contextes (Interface en ligne de commande, Application mobile, etc).
- **Pannes en cascade causées par les services externes :**
  - Appels synchrones vers des services tiers (SMS, mail, impression de badges) bloquant les threads applicatifs et saturant le pool de connexions à la base de données.
- **Paralysie des équipes et régression permanente :**
  - Explosion du temps d'exécution de la suite de tests.
  - Peur de modifier le code existant en raison du manque de tests unitaires rapides et isolés.

---

## 4. Apports de l'Architecture Hexagonale et du DDD Tactique

- **Domaine pur et sanctuarisé (`domain/`) :**
  - Zéro dépendance vis-à-vis de frameworks (aucun import de FastAPI, SQLAlchemy ou Pydantic).
  - Exécution en mémoire pure, garantissant des tests unitaires exécutés en quelques millisecondes.
- **Agrégats protecteurs (`Festival`, `Concert`) :**
  - Encapsulation totale de l'état interne.
  - Modifications obligatoirement opérées via des méthodes métier explicites (`reschedule`, `publish`, `cancel`) garantissant les invariants.
- **Value Objects auto-validés :**
  - `TimeRange` : encapsule la validation chronologique et le calcul de chevauchement.
  - `EquipmentSet` : structure immuable normalisant et validant la compatibilité technique.
  - Statuts typés par des énumérations strictes.
- **Inversion de dépendance par Ports et Adaptateurs :**
  - *Ports d'entrée (`ports/in/`) :* contrats abstraits exposant les cas d'usage (indépendants du protocole HTTP).
  - *Ports de sortie (`ports/out/`) :* interfaces abstraites pour les dépôts et notifications.
  - *Adaptateurs (`adapters/`) :* implémentations interchangeables reléguées au rang de détails techniques.
- **Domain Events et découplage des effets de bord :**
  - Émission d'événements métier (`FestivalPublishedEvent`, `ConcertRescheduledEvent`).
  - Traitement sécurisé des notifications sans risque de corrompre les transactions en base de données.

---

## 5. Synthèse Comparative : Approche Initiale vs Approche Hexagonale

| Axe d'Analyse | Architecture Initiale (CRUD en Couches) | Architecture Cible (Hexagonale & DDD) |
| :--- | :--- | :--- |
| **Couplage technique** | Élevé (contrôleurs dépendants du SQL et de l'ORM) | Nul dans le domaine (dépendances inversées par des ports) |
| **Modèle métier** | Modèle passif sans logique métier ("modèle anémique") | Modèle riche (agrégats autonomes protégeant leurs invariants) |
| **Gestion des types** | Types basiques simples (chaînes à virgule, dates brutes) | Value Objects immuables auto-validés (`TimeRange`, `EquipmentSet`) |
| **Replanification** | Faille majeure (conflits et contraintes ignorés) | Sécurisée (application systématique des règles de programmation) |
| **Effets de bord** | Dépendance synchrone post-commit (erreurs 500) | Événements de domaine découplés et résilients aux pannes tierces |
| **Testabilité** | Lente (dépendante de SQLite sur disque et de HTTP) | Instantanée (tests unitaires purs en mémoire en quelques millisecondes) |
| **Évolutivité** | Risque de services fourre-tout et de régression continue | Forte maintenabilité, extensibilité multi-canal sans dépendance bloquante |
