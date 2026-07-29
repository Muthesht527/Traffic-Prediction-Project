# AI-Powered Traffic Forecast Visualization Platform

> Predict future traffic congestion and visualize it on an interactive map — Google Maps-style coloured routes powered by machine learning.

## 🎯 What This Is

A **Traffic Forecast Visualization Platform** — **NOT** another Google Maps clone.

Users select a source, destination, date, and time. The system fetches the route, retrieves a weather forecast, runs an ML model, and displays predicted congestion as coloured polylines on an interactive Leaflet map.

| Colour | Score | Meaning |
|--------|-------|---------|
| 🟢 Green | 0–20 | Low Congestion |
| 🟡 Yellow | 21–40 | Light Congestion |
| 🟠 Orange | 41–70 | Moderate Congestion |
| 🔴 Red | 71–100 | Heavy Congestion |
| ⚫ Grey | — | Coverage Not Available |

## 📁 Project Structure

```
Traffic-Prediction-Project/
├── backend/                  # Flask API server
│   ├── api/
│   │   └── routes.py         # API endpoints (health, forecast, geocode, coverage)
│   ├── config/
│   │   └── __init__.py       # Centralised configuration
│   ├── model/
│   │   └── model_loader.py   # Load trained ML model
│   ├── services/
│   │   ├── color_mapper.py   # Score → colour mapping
│   │   ├── feature_engineering.py  # Build model features from inputs
│   │   ├── geocoding_service.py    # Nominatim geocoding
│   │   ├── prediction_service.py   # ML prediction pipeline
│   │   ├── route_service.py        # OpenRouteService / OSRM routing
│   │   └── weather_service.py      # OpenWeather forecast
│   ├── utils/
│   │   └── logger.py
│   ├── app.py                # Flask entry point
│   ├── .env.example
│   └── requirements.txt
├── frontend/                 # React + Vite + Leaflet + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── Form/
│   │   │   │   └── ForecastForm.jsx
│   │   │   ├── Map/
│   │   │   │   ├── TrafficMap.jsx
│   │   │   │   ├── RouteLayer.jsx
│   │   │   │   └── Legend.jsx
│   │   │   └── UI/
│   │   │       ├── Navbar.jsx
│   │   │       └── PredictionSummary.jsx
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx
│   │   │   └── ForecastPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── utils/
│   │   │   └── colorMapper.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
├── dataset/
│   └── smart_mobility_dataset.csv
├── model/
│   ├── traffic_congestion_model.pkl
│   └── training_metrics.json
├── src/                      # Original training scripts
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   └── app.py
└── README.md
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Leaflet, React-Leaflet, TailwindCSS, Lucide Icons |
| **Backend** | Python, Flask, Scikit-learn, Pandas |
| **ML Model** | Random Forest (300 trees), probability-weighted scoring |
| **Maps** | Leaflet + OpenStreetMap tiles |
| **Routing** | OpenRouteService (primary), OSRM (fallback), synthetic (offline) |
| **Weather** | OpenWeather API (with synthetic fallback) |
| **Geocoding** | Nominatim (OpenStreetMap) |

## 🚀 Quick Start

### Backend

```bash
cd Traffic-Prediction-Project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# (Optional) Set API keys
cp backend/.env.example backend/.env
# Edit backend/.env with your keys

# Start backend server
python -m backend.app
# → http://localhost:5001
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (proxies /api → backend on :5001)
npm run dev
# → http://localhost:3000
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/coverage` | Supported region info |
| `GET` | `/api/coverage/check?lat=…&lng=…` | Check if point is in coverage |
| `GET` | `/api/geocode?q=…` | Geocode a place name |
| `POST` | `/api/forecast` | **Main forecast endpoint** |

### Forecast Request

```json
{
  "source": "Adyar, Chennai",
  "destination": "T. Nagar, Chennai",
  "date": "2024-03-15",
  "time": "08:30"
}
```

Or with coordinates:

```json
{
  "source": {"lat": 13.0827, "lng": 80.2707},
  "destination": {"lat": 13.0418, "lng": 80.2341},
  "date": "2024-03-15",
  "time": "08:30"
}
```

### Forecast Response

```json
{
  "source": {"lat": 13.0418, "lng": 80.2341, "query": "Adyar, Chennai"},
  "destination": {"lat": 13.0336, "lng": 80.2186, "query": "T. Nagar, Chennai"},
  "target_datetime": "2024-03-15T08:30:00",
  "route": {"distance_m": 5200, "duration_s": 624, "source": "osrm"},
  "weather": {"temperature": 31.0, "humidity": 70, "wind_speed": 8, "rain_1h": 0, "source": "synthetic"},
  "prediction": {
    "congestion_score": 83.6,
    "predicted_condition": "High",
    "class_probabilities": {"High": 0.95, "Low": 0.0, "Medium": 0.05}
  },
  "segments": [
    {"coordinates": [[80.27, 13.08], ...], "color": "#ef4444", "congestion_score": 83.6, "label": "Heavy Congestion"}
  ],
  "coverage": {"available": true, "region": "Chennai"}
}
```

## 🧠 ML Model

The model is a **Random Forest Classifier** (300 trees) trained on 5,000 samples from the Smart Mobility Dataset.

- **Training accuracy**: 99.9%
- **Input features**: 14 columns (temporal, geospatial, traffic, weather, contextual)
- **Output**: Categorical (High / Medium / Low) → converted to a continuous 0–100 score via probability weighting

**Score derivation**: `score = P(High) × 85 + P(Medium) × 55 + P(Low) × 10`

## 🗺️ Current Coverage

**Phase 1** supports only **Chennai, India**. Routes outside this region are displayed in grey with the label "Coverage Not Available". No fake predictions are ever generated.

## 🔮 Future Phases (Not Yet Implemented)

- Road-level prediction (multiple coloured segments per route)
- Live traffic from CCTV / YOLO
- IoT and government sensor integration
- Automatic model retraining
- ETA prediction
- City-wide expansion
- Authentication and admin dashboard

## 📝 Problem Statement

> Rapid urbanization and increasing vehicle usage have led to frequent traffic congestion. Existing navigation apps provide real-time traffic updates but limited capability to **forecast** future conditions. This platform fills that gap by combining historical traffic data, weather forecasts, and temporal analysis to predict and visualize future congestion on an interactive map.
