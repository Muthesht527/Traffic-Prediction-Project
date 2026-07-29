import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Submit a forecast request to the backend.
 */
export async function submitForecast(payload) {
  const response = await api.post('/forecast', payload);
  return response.data;
}

/**
 * Geocode a place name to lat/lng (used by autocomplete).
 */
export async function geocode(query) {
  const response = await api.get('/geocode', { params: { q: query } });
  return response.data;
}

/**
 * Get the currently supported coverage region.
 */
export async function getCoverage() {
  const response = await api.get('/coverage');
  return response.data;
}

/**
 * Get model info (metrics, feature importances).
 */
export async function getModelInfo() {
  const response = await api.get('/model/info');
  return response.data;
}

/**
 * Get prediction history.
 */
export async function getPredictionHistory(limit = 20) {
  const response = await api.get('/history', { params: { limit } });
  return response.data;
}

export default api;
