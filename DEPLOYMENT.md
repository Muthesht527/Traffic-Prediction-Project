# 🚀 Deployment Guide

Two supported deployment paths:

- **Option A — Render + Vercel** (managed, zero servers): Flask API on Render, React frontend on Vercel. Recommended for quick public demos.
- **Option B — Docker Compose** (self-hosted): one-command full stack on any VM.

| File | Purpose |
|------|---------|
| `render.yaml` | Render Blueprint — backend web service (Python 3.11 + Gunicorn) |
| `frontend/vercel.json` | Vercel config — Vite build, SPA fallback, `/api` proxy to Render |
| `backend/Dockerfile` | Flask API image (port 5001) |
| `frontend/Dockerfile` + `frontend/nginx.conf` | Vite build → nginx, `/api` reverse proxy |
| `docker-compose.yml` | One-command full-stack deployment |
| `deploy/ci-cd.yml` | GitHub Actions CI/CD workflow (see activation note below) |

---

## Option A — Render (backend) + Vercel (frontend)

### 1️⃣ Deploy the backend on Render

**Automatic (Blueprint):** Render dashboard → **New → Blueprint** → select this repository. Render detects `render.yaml` and provisions everything.

**Manual (Web Service):** if you prefer, create a **Web Service** on the repo with:

| Setting | Value |
|---------|-------|
| Root Directory | *(leave empty — repo root)* |
| Build Command | `pip install -r backend/requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 "backend.app:create_app()"` |
| Health Check Path | `/api/health` |
| Instance Type | Free |

Either way, note the assigned URL, e.g. **`https://traffic-forecast-api.onrender.com`**.

> **Free-plan caveats:** the service sleeps after ~15 min of inactivity, so the first request after idle takes ~30–60 s. The SQLite history DB is ephemeral on free instances (attach a disk — commented out in `render.yaml` — on a paid plan to persist it).

**Environment variables** (Render dashboard → Environment):

| Variable | Required | Notes |
|----------|----------|-------|
| `PYTHON_VERSION` | Set by blueprint (`3.11.9`) | Only for manual setup |
| `CORS_ORIGINS` | No (default `*`) | Tighten to your Vercel URL if the frontend calls Render directly |
| `OPENWEATHER_API_KEY` | No | Live weather; falls back to synthetic data |
| `OPENROUTESERVICE_API_KEY` | No | Real routes; falls back to synthetic data |

Verify: `curl https://<your-service>.onrender.com/api/health` → `{"status":"ok"}`.

### 2️⃣ Deploy the frontend on Vercel

1. **Edit `frontend/vercel.json` first** — replace `https://traffic-forecast-api.onrender.com` with your actual Render URL from step 1. This rewrite proxies `/api/*` through Vercel, so **no CORS and no env vars are needed**.
2. Vercel dashboard → **Add New → Project** → import the repo.
3. Set **Root Directory** to `frontend` (Vercel auto-detects Vite; `vercel.json` supplies the rest).
4. Deploy. ✅

**Alternative (direct API calls):** instead of the proxy rewrite, you can set the env var `VITE_API_BASE=https://<your-service>.onrender.com/api` in the Vercel project and remove the `/api` rewrite. In that case also set `CORS_ORIGINS=https://<your-app>.vercel.app` on Render — the backend ships with `flask-cors` preconfigured for this.

---

## Option B — Docker Compose (self-hosted)

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
