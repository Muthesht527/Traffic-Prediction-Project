# Traffic Forecast API — Flask backend image.
#
# Build from the REPOSITORY ROOT (the backend needs model/ and dataset/
# next to the backend/ package):
#
#   docker build -f backend/Dockerfile -t traffic-forecast-backend .
#
# (docker-compose.yml already sets this build context up for you.)

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5001 \
    FLASK_DEBUG=false

WORKDIR /app

# Install dependencies first for better layer caching.
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt

# Application code + runtime artifacts (model pickles, coverage dataset).
COPY backend/ backend/
COPY model/ model/
COPY dataset/ dataset/

# SQLite database lives here (mounted as a volume by docker-compose).
RUN mkdir -p data

EXPOSE 5001

# App-factory pattern: gunicorn calls create_app() on each worker.
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "120", "backend.app:create_app()"]
