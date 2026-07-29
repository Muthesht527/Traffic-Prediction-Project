# 🚀 Deployment Guide

This project ships with Docker-based deployment configs and a GitHub Actions
CI/CD pipeline (added in the `arena/019fae6f-traffic-prediction-project` branch).

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Flask API image (Python 3.11 + Gunicorn, port 5001) |
| `frontend/Dockerfile` | Vite/React build → nginx static hosting (port 80) |
| `frontend/nginx.conf` | SPA fallback + `/api` reverse proxy to the backend |
| `docker-compose.yml` | One-command full-stack deployment |
| `deploy/ci-cd.yml` | GitHub Actions CI/CD workflow (see activation note below) |

---

## Quick Start (Docker Compose)

```bash
docker compose up --build
```

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:5001 (`/api/health` for health checks)

The frontend container proxies `/api/*` requests to the backend container over
Docker's internal network, so no CORS or extra configuration is needed.

### Optional environment variables

The app works out of the box with **synthetic weather/route fallbacks**. For
live data, export these (or place them in a `.env` file next to
`docker-compose.yml`) before running `docker compose up`:

| Variable | Purpose |
|----------|---------|
| `OPENWEATHER_API_KEY` | Live weather forecasts (openweathermap.org) |
| `OPENROUTESERVICE_API_KEY` | Real route geometry (openrouteservice.org) |

## Model artifacts

`model/traffic_congestion_model.pkl` is tracked in the repo and baked into the
backend image at build time. To swap in a retrained model **without rebuilding**:

```yaml
# add under services.backend.volumes in docker-compose.yml
- ./model:/app/model:ro
```

## Data persistence

The SQLite prediction-history DB (`data/traffic_forecast.db`) is stored in the
named volume `backend_data` and survives container restarts. Remove it with
`docker compose down -v`.

## Individual images

```bash
# Backend — build context MUST be the repository root:
docker build -f backend/Dockerfile -t traffic-forecast-backend .
docker run -p 5001:5001 traffic-forecast-backend

# Frontend:
docker build -t traffic-forecast-frontend ./frontend
docker run -p 8080:80 traffic-forecast-frontend   # expects a reachable "backend" host for /api
```

## CI/CD pipeline

A ready-to-use GitHub Actions workflow ships at `deploy/ci-cd.yml`. It runs on
every push and PR to `main`:

1. **Backend job** — installs deps, `compileall`, and a `create_app()` smoke test.
2. **Frontend job** — `npm install` + `npm run build`.
3. **Docker job** — builds both images, boots the compose stack, and verifies
   `/api/health` plus the frontend before tearing down.

> **⚠️ Activation required:** the workflow is not yet at
> `.github/workflows/ci-cd.yml` because it was authored by a GitHub App whose
> token lacks the **`workflows` permission** (GitHub blocks such apps from
> adding workflow files). To activate CI, move it into place and push:
>
> ```bash
> mkdir -p .github/workflows
> git mv deploy/ci-cd.yml .github/workflows/ci-cd.yml
> git commit -m "ci: activate CI/CD workflow" && git push
> ```

No secrets are required for CI. To add an actual deploy stage (Render, ECS,
VM, …), append a job that consumes these images with your platform credentials.
