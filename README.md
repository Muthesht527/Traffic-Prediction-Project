# Traffic Speed Prediction Using Linear Regression

This is a simple machine learning mini project. It trains a Linear Regression
model to predict `Traffic_Speed_kmh` from:

- `Vehicle_Count`
- `Road_Occupancy_%`
- `Accident_Report`

## Project structure

```text
data/
model/
src/
  data_preprocessing.py
  train_model.py
  predict.py
  app.py
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

- `model/traffic_speed_model.pkl`
- `model/training_metrics.json`

## Run the Flask app

```bash
python src/app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Sample API request

```bash
curl -X POST http://127.0.0.1:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Vehicle_Count\":180,\"Road_Occupancy_%\":65,\"Accident_Report\":0}"
```
