# DjangoTestProject

A Django REST API for searching GitHub users, repositories, and issues, with Redis caching.

## Stack

- Python 3.13, Django 6, Django REST Framework
- Redis (via `django-redis`) for response caching
- `uv` for dependency management
- Docker / Docker Compose

## Setup

### 1. Clone and configure environment

```bash
cp .env.sample .env
```

Fill in `.env`:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | `True` for development, `False` for production |
| `GITHUB_TOKEN` | GitHub personal access token |
| `REDIS_URL` | Redis connection URL (default: `redis://localhost:6379/0`) |

### 2. Run with Docker Compose

```bash
docker compose up --build
```

The app will be available at `http://localhost:8000`.

### 3. Run locally

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Redis must be running locally. Start it with:

```bash
docker compose up -d redis
```

## API

### `POST /api/search/`

Search GitHub for users, repositories, or issues.

**Request body:**

```json
{
  "text": "django",
  "type": "repositories",
  "per_page": 10,
  "page": 1
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | Search query |
| `type` | string | yes | `users`, `repositories`, or `issues` |
| `per_page` | integer | no | Results per page (1–100, default: 10) |
| `page` | integer | no | Page number (default: 1) |

**Response:**

```json
{
  "total_count": 1234,
  "page": 1,
  "per_page": 10,
  "items": [...]
}
```

Results are cached in Redis for 2 hours. Identical requests within that window are served from cache.

### `POST /api/clear-cache/`

Clears all cached search results.

**Response:** `204 No Content`

## Tests

```bash
uv run pytest
```

Tests use an in-memory cache and mock all GitHub API calls — no Redis or network required.
