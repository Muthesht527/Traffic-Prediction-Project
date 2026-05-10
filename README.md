# Traffic Congestion Prediction using Random Forest Classifier

## Project structure

```text
data/
model/
src/
  data_preprocessing.py
  train_model.py
  predict.py
  app.py
  template/
    index.html
requirements.txt
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Train the model

```bash
python src/train_model.py
```

This creates:

- `model/traffic_congestion_model.pkl`
- `model/training_metrics.json`

## Run the Flask API

```bash
python src/app.py
```

API endpoints:

- `GET /health`
- `POST /predict`

## Sample prediction request

```bash
curl -X POST http://127.0.0.1:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Timestamp\":\"01-03-2024 08:30\",\"Latitude\":40.7128,\"Longitude\":-74.0060,\"Vehicle_Count\":180,\"Traffic_Speed_kmh\":28.5,\"Road_Occupancy_%\":76.3,\"Traffic_Light_State\":\"Red\",\"Weather_Condition\":\"Rain\",\"Accident_Report\":0,\"Sentiment_Score\":0.12,\"Ride_Sharing_Demand\":42,\"Parking_Availability\":18,\"Emission_Levels_g_km\":310.4,\"Energy_Consumption_L_h\":12.8}"
```

You can also send batch requests:

```json
{
  "instances": [
    {
      "Timestamp": "01-03-2024 08:30",
      "Latitude": 40.7128,
      "Longitude": -74.0060,
      "Vehicle_Count": 180,
      "Traffic_Speed_kmh": 28.5,
      "Road_Occupancy_%": 76.3,
      "Traffic_Light_State": "Red",
      "Weather_Condition": "Rain",
      "Accident_Report": 0,
      "Sentiment_Score": 0.12,
      "Ride_Sharing_Demand": 42,
      "Parking_Availability": 18,
      "Emission_Levels_g_km": 310.4,
      "Energy_Consumption_L_h": 12.8
    }
  ]
}
```
