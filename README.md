# EduTrack Analytics

Plateforme d'analyse de la performance academique des etudiants. Elle permet d'importer,
nettoyer, analyser et visualiser des donnees academiques (notes, absences, retards, classes,
modules) pour produire des tableaux de bord, des indicateurs et des alertes d'aide a la decision.

Projet Spe DATA, Maroc Ynov Campus.

Demonstration video: https://drive.google.com/file/d/1yJYg1_yLmzMC4qEJgLP1PmkmyHiqSXLS/view?usp=drive_link

## Stack technique

- **Backend**: FastAPI (Python), SQLAlchemy, Alembic
- **Data**: pandas, NumPy
- **Visualisation**: Recharts (frontend), Matplotlib (rapports PDF)
- **Frontend**: Next.js (React) + Tailwind CSS
- **Base de donnees**: PostgreSQL
- **Authentification**: JWT
- **Rapports**: Jinja2 + WeasyPrint (PDF/HTML)
- **Conteneurisation**: Docker Compose

## Fonctionnalites

- Import de fichiers CSV / Excel avec validation, nettoyage et historique des imports
- Pipeline de traitement: lecture, validation, nettoyage, transformation, chargement
- Tableau de bord: KPIs globaux, analyse par classe, par module, fiche etudiant
- Statistiques descriptives, distribution des notes, correlations, detection d'anomalies
- Detection des etudiants a risque (regles statistiques) et alertes pedagogiques
- Segmentation des etudiants par niveau (excellent, stable, moyen, fragile, a risque)
- Bonus C: generation automatique de rapports PDF / HTML

## Demarrage rapide (Docker)

Prerequis: Docker et Docker Compose.

```bash
# 1. Copier la configuration
cp .env.example .env

# 2. Lancer toute la stack (Postgres + backend + frontend)
docker compose up --build
```

Services disponibles:

- Frontend: http://localhost:3000
- API + documentation interactive: http://localhost:8000/docs
- PostgreSQL: localhost:5432

Compte par defaut: `admin@edutrack.io` / `admin123`.

Un `Makefile` regroupe les commandes courantes: `make up`, `make down`, `make data`,
`make test`, `make schema`, `make clean` (voir `make help`).

### Charger des donnees de demonstration

Le script `data/generate_synthetic.py` cree les fichiers d'exemple. On les importe ensuite
depuis la page **Imports** de l'application:

```bash
python data/generate_synthetic.py   # ou: make data
# Produit data/samples/etudiants.csv, notes.csv, absences.xlsx
# et des fichiers de test dans data/samples/edge_cases/
```

Les colonnes des fichiers sont en francais (code_etudiant, prenom, nom, note, heures...).
Ordre d'import recommande: etudiants, puis notes, puis absences. La detection du type
est automatique, mais le type peut etre force dans le formulaire.

## Developpement local (sans Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://edutrack:edutrack@localhost:5432/edutrack"
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Tests

```bash
cd backend
pytest
```

## Structure du projet

```
backend/                 API FastAPI
  app/
    core/                configuration, base de donnees, securite (JWT)
    models/              modeles SQLAlchemy (schema relationnel)
    schemas/             modeles Pydantic (validation des E/S)
    pipeline/            reader, validator, cleaner, loader, runner
    analytics/           statistiques, correlations, anomalies, risque
    reports/             generation de rapports (Bonus C)
    api/routers/         endpoints REST
  alembic/               migrations
  tests/                 tests unitaires et d'integration
  schema.sql             schema PostgreSQL exporte

frontend/                application Next.js
  app/                   pages : login, dashboard, classes, modules,
                         etudiants, anomalies, alertes, imports, rapports
  components/            Shell (navigation), charts, ui
  lib/                   client API, types, hook de chargement

data/
  generate_synthetic.py  generateur de donnees (entetes francaises)
  samples/               fichiers d'exemple + edge_cases (tests de validation)

notebook/EDA.ipynb       analyse exploratoire (nettoyage, stats, graphiques)
docs/                    rapport technique (RAPPORT.md / .pdf) + captures d'ecran
docker-compose.yml       orchestration db + backend + frontend
```

## Schema de la base de donnees

Tables principales: `users`, `classes`, `modules`, `students`, `grades`, `absences`,
`imports`, `alerts`, `settings`. Le script SQL complet est genere dans `backend/schema.sql`.

## Livrables

- Rapport technique: `docs/RAPPORT.md` (et `docs/RAPPORT.pdf`)
- Notebook d'analyse: `notebook/EDA.ipynb`
- Script SQL: `backend/schema.sql` + migrations Alembic
- Application fonctionnelle: via `docker compose up`
- Video de demonstration: https://drive.google.com/file/d/1yJYg1_yLmzMC4qEJgLP1PmkmyHiqSXLS/view?usp=drive_link
