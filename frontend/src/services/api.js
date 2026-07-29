import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Submit a forecast request to the backend.
 *
 * @param {{ source: string|object, destination: string|object, date: string, time: string }} payload
 * @returns {Promise<object>} Forecast response
 */
export async function submitForecast(payload) {
  const response = await api.post('/forecast', payload);
  return response.data;
}

/**
 * Geocode a place name to lat/lng.
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
 * Check if a lat/lng is within coverage.
 */
export async function checkCoverage(lat, lng) {
  const response = await api.get('/coverage/check', { params: { lat, lng } });
  return response.data;
}

export default api;
