# Vite/React frontend — multi-stage build, static bundle served by nginx.
# Built from the frontend/ directory (docker-compose sets this context).

# ── Stage 1: build the static bundle ────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app

# No lockfile is committed, so use npm install (not npm ci).
COPY package.json ./
RUN npm install --no-audit --no-fund

COPY . .

# VITE_API_BASE defaults to "/api" in src/services/api.js, which the
# nginx reverse proxy (nginx.conf) forwards to the backend container.
RUN npm run build

# ── Stage 2: serve with nginx ────────────────────────────────────────────
FROM nginx:1.25-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
