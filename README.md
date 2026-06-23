# Property Management System

A Django-based vacation rental property management system with geospatial search and AI-powered semantic search capabilities.

---

## Tech Stack

- **Backend:** Django 6, Python 3.12, Django REST Framework
- **Database:** PostgreSQL 16 with PostGIS (geospatial) and PGVector (vector search)
- **Infrastructure:** Docker, Docker Compose
- **Data:** Pandas (CSV import), Pillow (image handling)
- **AI:** Sentence Transformers (`all-MiniLM-L6-v2`)

---

## Project Structure

```
.
├── core/                   # Django project config (settings, urls, wsgi)
├── property/               # Main app
│   ├── data/
│   │   ├── properties.csv  # Sample property data
│   │   └── images/         # Local property images
│   ├── management/
│   │   └── commands/
│   │       └── import_properties.py
│   ├── migrations/
│   ├── templates/          # Property-specific templates
│   ├── admin.py
│   ├── models.py
│   └── views.py
├── api/                    # REST API app
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── templates/              # Global base templates and partials
├── static/                 # CSS and JS assets
├── docker/
│   ├── postgres/
│   │   ├── Dockerfile
│   │   └── init/
│   │       └── 01_postgis_pgvector_extensions.sql
│   └── django/
│       └── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/200215-Moynul-Islam/property-management-system-moynul.git
cd property-management-system-moynul
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Update `.env` with your values (defaults work for local development):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=propertydb
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_PORT=8000
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=your_secret_key
```

### 3. Start Services

```bash
docker compose up --build
```

This starts PostgreSQL (with PostGIS + PGVector extensions) and the Django server.

### 4. Run Migrations

```bash
docker compose exec web python manage.py migrate
```

### 5. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Import Sample Data

```bash
docker compose exec web python manage.py import_properties --file property/data/properties.csv
```

> This also generates and stores `all-MiniLM-L6-v2` embeddings for each location.

---

## Features

- PostgreSQL 16 with PostGIS and PGVector via Docker
- Django configured with GeoDjango (`django.contrib.gis`)
- Models: `Location`, `Property`, `PropertyImage`
- CSV import via Pandas management command with automatic embedding generation
- Django Admin with image previews and filters
- Homepage with semantic location autocomplete
- Property listing page with pagination and configurable page size
- Property detail page with image gallery and distance from city center
- Location autocomplete REST API using cosine similarity search (HNSW index)

---

## Models

### `Location`

| Field       | Type        | Notes                             |
| ----------- | ----------- | --------------------------------- |
| `name`      | CharField   | City/area name                    |
| `point`     | PointField  | Lat/lng (PostGIS, geography=True) |
| `embedding` | VectorField | 384-dim (PGVector, HNSW index)    |

### `Property`

| Field         | Type                      | Notes                |
| ------------- | ------------------------- | -------------------- |
| `location`    | ForeignKey                | → Location           |
| `title`       | CharField                 |                      |
| `description` | TextField                 |                      |
| `price`       | DecimalField              |                      |
| `bedrooms`    | PositiveSmallIntegerField |                      |
| `bathrooms`   | PositiveSmallIntegerField |                      |
| `point`       | PointField                | Property coordinates |

### `PropertyImage`

| Field      | Type       | Notes                           |
| ---------- | ---------- | ------------------------------- |
| `property` | ForeignKey | → Property                      |
| `image`    | ImageField | Uploaded to `properties/%Y/%m/` |
| `caption`  | CharField  |                                 |

---

## Admin

Access at `http://localhost:8000/admin/`

- **Location** — GIS map widget, search by name
- **Property** — Filterable by location, bedrooms, bathrooms, price; inline image management with previews
- **PropertyImage** — Thumbnail previews in list view

---

## API

| Endpoint                                    | Description                    |
| ------------------------------------------- | ------------------------------ |
| `GET /health/`                              | Health check                   |
| `GET /api/location-autocomplete/?q=<query>` | Semantic location autocomplete |
