# FestiPlan — Frontend Web (React + TypeScript)

Interface web complète et réactive pour l'application **FestiPlan**, conçue avec un thème sombre et immersif inspiré du festival **Hellfest** (noir abyssal, rouge feu, vert toxique/acide et typographie gothique).

---

## ⚡ Stack Technique

- **Framework** : React 18 & TypeScript
- **Bundler & Dev Server** : Vite 6 (avec HMR ultra-rapide et proxy API `/api`, `/festivals`, etc.)
- **Styling** : Tailwind CSS (palette custom `hell-red`, `hell-green`, `hell-black`, ombres néon `shadow-flame` et `shadow-acid`)
- **Iconographie** : Lucide React (Flame, Skull, ShieldCheck, Sparkles, AlertTriangle...)
- **Polices** : Google Fonts *Cinzel*, *Cinzel Decorative*, *Inter*

---

## 🤘 Fonctionnalités Clés

1. **Running Order & Timetable (Programmation Interactive)** :
   - Affichage en colonnes par scènes (Mainstage, Warzone, Valley, Temple) style Hellfest.
   - Filtre par jour (Vendredi 18, Samedi 19, Dimanche 20 Juin 2027 ou tous les jours).
   - Filtre par scène et recherche dynamique par groupe ou genre musical.
   - Vérification visuelle de compatibilité technique (matériel requis par l'artiste vs matériel installé sur scène).
   - Déplacement de concert (reschedule modal) et annulation directe.

2. **Respect des Invariants Métier (Tactical DDD)** :
   - **Règle R7 (Festival Publié)** : Bouton de publication avec confirmation. Dès que le festival est publié, les modifications de concerts sont verrouillées.
   - **Conflits de scènes & artistes (R2 & R3)** : Messages d'erreurs clairs remontés depuis l'API en cas de chevauchement.
   - **Adéquation technique (R6)** : Alerte visuelle avant soumission si la scène ne dispose pas du rider de l'artiste.

3. **Lineup & Artistes** :
   - Annuaire complet des groupes avec badges de sous-genres (Heavy metal, Thrash metal, Power metal, Hardcore, Stoner, Doom...).
   - Fiche technique de chaque groupe (besoins en matériel : charpente lourde, éclairage FX, pyrotechnie...).
   - Modal d'ajout d'artiste avec sélection de matériel.

4. **Scènes & Installations Techniques** :
   - Jauge et capacité des arènes (50k festivaliers sur la Mainstage, 15k sur la Warzone...).
   - Liste des équipements techniques disponibles par scène.
   - Modal de création de scène.

5. **Tour de Contrôle des Incidents** :
   - Suivi en temps réel des incidents techniques et de sécurité déclarés en régie.
   - Déclaration d'incident avec association directe au concert concerné.

6. **Onglet Architecture & Invariants** :
   - Vue pédagogique résumant l'organisation hexagonale (Domain, Ports, Adapters) et les 7 règles d'invariants métier.

---

## 🚀 Démarrage

### 1. Démarrer le Backend FastAPI (dans le terminal 1)
```bash
uv run python -m app.seed
uv run uvicorn app.main:app --reload
```
Le backend tourne sur `http://127.0.0.1:8000`.

### 2. Démarrer le Frontend (dans le terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Ouvrez ensuite votre navigateur sur **http://localhost:5173**.

