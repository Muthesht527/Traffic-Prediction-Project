# 🚦 AI-Powered Traffic Forecast Visualization Platform

> Predict future traffic congestion and visualize it on an interactive map — Google Maps-style coloured routes powered by machine learning.

<div align="center">

**Phase 1 · Hackathon MVP**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-orange.svg)](https://scikit-learn.org)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900.svg)](https://leafletjs.com)

</div>

---

## 🎯 What This Is

A **Traffic Forecast Visualization Platform** — **NOT** a navigation app.

Users select a **source**, **destination**, **date**, and **time** (up to 7 days ahead). The system fetches the route, retrieves a weather forecast, runs a **Random Forest ML model**, and displays predicted congestion as coloured polylines on an interactive Leaflet map.

### Congestion Score Mapping

| Colour | Score | Meaning |
|--------|-------|---------|
| 🟢 Green | 0–20 | Low Congestion |
| 🟡 Yellow | 21–40 | Light Congestion |
| 🟠 Orange | 41–70 | Moderate Congestion |
| 🔴 Red | 71–100 | Heavy Congestion |
| ⚫ Grey | — | Coverage Not Available |

### Phase 1 Coverage

Only **Chennai, India** is supported. Roads outside the dataset region are shown in grey. **Predictions are never faked.**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Browser)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           FRONTEND (React + Vite + TailwindCSS)         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Landing  │  │ Forecast │  │  TrafficMap (Leaflet) │  │
│  │ Page     │  │ Form     │  │  + RouteLayer + Legend│  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API (JSON)
┌──────────────────────▼──────────────────────────────────┐
│                BACKEND (Flask)                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │          API Layer (routes.py)                    │   │
│  └───────────────────────┬──────────────────────────┘   │
│  ┌──────────┬────────────┼───────────┬──────────────┐   │
│  │ Route    │  Weather   │ Prediction│ Geocoding    │   │
│  │ Service  │  Service   │ Service   │ Service      │   │
│  └────┬─────┘──┬─────────┘─────┬─────┘──────┬───────┘   │
│       │        │               │            │           │
│  ┌────▼────────▼───────────────▼────────────▼───────┐   │
│  │         Feature Engineering Layer                 │   │
│  └───────────────────────┬───────────────────────────┘   │
│  ┌───────────┐  ┌────────▼───────┐  ┌──────────────┐    │
│  │  Model    │  │   Traffic      │  │   Color      │    │
│  │  Loader   │  │   Predictor    │  │   Mapper     │    │
│  └───────────┘  └────────────────┘  └──────────────┘    │
│  ┌──────────────────────────────────────────────────┐   │
│  │         SQLite Database Service                   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Traffic-Prediction-Project/
├── backend/                         # Flask API server
│   ├── api/
│   │   └── routes.py                # 7 API endpoints
│   ├── config/
│   │   └── __init__.py              # Centralised configuration
│   ├── model/
│   │   └── model_loader.py          # Loads classifier + regressor
│   ├── services/
│   │   ├── color_mapper.py          # Score → colour mapping
│   │   ├── database_service.py      # SQLite prediction history
│   │   ├── feature_engineering.py   # Build model features
│   │   ├── geocoding_service.py     # Nominatim integration
│   │   ├── model_trainer.py         # Train both models
│   │   ├── prediction_service.py    # ML prediction pipeline
│   │   ├── route_service.py         # ORS / OSRM / synthetic
│   │   └── weather_service.py       # OpenWeather / synthetic
│   ├── utils/
│   │   ├── dataset_mapper.py        # Configurable column mapping
│   │   └── logger.py                # Centralised logging
│   ├── app.py                       # Flask entry point
│   └── requirements.txt
├── frontend/                        # React + Vite + Leaflet + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── Form/
│   │   │   │   ├── AutocompleteSearch.jsx  # Location autocomplete
│   │   │   │   └── ForecastForm.jsx
│   │   │   ├── Map/
│   │   │   │   ├── Legend.jsx
│   │   │   │   ├── RouteLayer.jsx
│   │   │   │   └── TrafficMap.jsx
│   │   │   └── UI/
│   │   │       ├── Navbar.jsx
│   │   │       └── PredictionSummary.jsx
│   │   ├── pages/
│   │   │   ├── ForecastPage.jsx
│   │   │   └── LandingPage.jsx
│   │   ├── services/api.js
│   │   ├── utils/colorMapper.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                # Animations + Tailwind
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── dataset/
│   └── smart_mobility_dataset.csv   # 5,000 rows
├── model/
│   ├── traffic_congestion_model.pkl # Classifier
│   ├── congestion_regressor.pkl     # Regressor (0-100 score)
│   ├── training_metrics.json        # Classification metrics
│   └── regression_metrics.json      # MAE, RMSE, R²
├── data/
│   ├── smart_mobility_dataset.csv   # Original dataset
│   └── traffic_forecast.db          # SQLite prediction history
└── src/                             # Original training scripts
    ├── data_preprocessing.py
    ├── train_model.py
    └── predict.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Leaflet, React-Leaflet, TailwindCSS, Lucide Icons |
| **Backend** | Python, Flask, Pandas, SQLite |
| **ML Models** | Random Forest Classifier (99.9% acc) + Random Forest Regressor (R² = 0.94) |
| **Maps** | Leaflet + OpenStreetMap tiles |
| **Routing** | OpenRouteService → OSRM → synthetic fallback |
| **Weather** | OpenWeather API → synthetic fallback |
| **Geocoding** | Nominatim (OpenStreetMap) |

---

## 🧠 ML Models

### Classifier (Original)
- **Algorithm**: Random Forest (300 trees)
- **Accuracy**: 99.9%
- **Output**: Categorical (High / Medium / Low)
- **Score derivation**: Probability-weighted: `P(High)×85 + P(Medium)×55 + P(Low)×10`

### Regressor (Enhanced)
- **Algorithm**: Random Forest Regressor (300 trees)
- **MAE**: 4.0 | **RMSE**: 5.06 | **R²**: 0.94
- **Output**: Direct congestion score (0–100)
- **Top features**: Traffic Speed, Vehicle Count, Road Occupancy

### Training
```bash
python backend/services/model_trainer.py
```

---

## 🚀 Quick Start

### Backend

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# (Optional) Set API keys
cp backend/.env.example backend/.env

# Train models (already trained — artifacts exist)
python backend/services/model_trainer.py

# Start server
python -m backend.app
# → http://localhost:5001
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → http://localhost:3000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/coverage` | Supported region info |
| `GET` | `/api/coverage/check?lat=…&lng=…` | Check if point is in coverage |
| `GET` | `/api/geocode?q=…` | Geocode a place name |
| `POST` | `/api/forecast` | **Main forecast endpoint** |
| `GET` | `/api/history` | Prediction history (SQLite) |
| `GET` | `/api/model/info` | Model metadata + metrics |

### Forecast Example

```bash
curl -X POST http://localhost:5001/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "source": "Adyar, Chennai",
    "destination": "T. Nagar, Chennai",
    "date": "2024-03-15",
    "time": "08:30"
  }'
```

### Response

```json
{
  "source": {"lat": 13.0418, "lng": 80.2341, "query": "Adyar, Chennai"},
  "destination": {"lat": 13.0336, "lng": 80.2186, "query": "T. Nagar, Chennai"},
  "target_datetime": "2024-03-15T08:30:00",
  "route": {"distance_m": 5200, "duration_s": 624, "source": "osrm"},
  "weather": {"temperature": 31.0, "humidity": 70, "wind_speed": 8, "rain_1h": 0, "source": "synthetic"},
  "prediction": {
    "congestion_score": 83.4,
    "predicted_condition": "High",
    "class_probabilities": {"High": 0.68, "Medium": 0.28, "Low": 0.04},
    "model": "regressor"
  },
  "segments": [{"coordinates": [...], "color": "#ef4444", "congestion_score": 83.4, "label": "Heavy Congestion"}],
  "coverage": {"available": true, "region": "Chennai"}
}
```

---

## 🧪 Sample Predictions (Tested)

| Scenario | Time | Score | Condition | Color |
|----------|------|-------|-----------|-------|
| Peak Morning | 08:30 | 83.4 | Heavy | 🔴 Red |
| Afternoon | 14:00 | 53.4 | Moderate | 🟠 Orange |
| Late Night | 02:00 | 11.1 | Low | 🟢 Green |
| Evening Rush | 18:00 | 83.6 | Heavy | 🔴 Red |
| Outside Coverage | Any | — | N/A | ⚫ Grey |

---

## 🔮 Future Phases (Not Implemented)

The architecture is designed for seamless expansion:

- 🔴 Road-level prediction (multi-segment coloured routes)
- 📹 CCTV + YOLO vehicle detection
- 📡 IoT and government sensor integration
- 🔄 Automatic model retraining
- 🚗 ETA and travel time prediction
- 🏙️ City-wide expansion
- 🔐 Authentication and admin dashboard
- 📱 Mobile application
- 📊 Prediction confidence intervals

---

## 📝 Problem Statement

> Rapid urbanization and increasing vehicle usage have led to frequent traffic congestion. Existing navigation apps provide real-time updates but limited capability to **forecast** future conditions. This platform fills that gap by combining historical traffic data, weather forecasts, and temporal analysis to predict and visualize future congestion on an interactive map.

---

## 🐳 Deployment

**Managed (recommended):** backend on **Render** (`render.yaml` blueprint) + frontend on **Vercel** (`frontend/vercel.json`).

**Self-hosted:** the stack is fully containerised:

```bash
docker compose up --build
```

- **Frontend:** http://localhost:8080 · **Backend:** http://localhost:5001

A ready-to-use GitHub Actions CI/CD workflow ships at `deploy/ci-cd.yml` (backend smoke test → frontend build → Docker build + health check) — move it to `.github/workflows/` to activate. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step guides, environment variables, and persistence notes.

---

## 📄 License

Hackathon project — Phase 1 MVP.
