import { useState, useCallback } from 'react';
import Navbar from '../components/UI/Navbar';
import ForecastForm from '../components/Form/ForecastForm';
import TrafficMap from '../components/Map/TrafficMap';
import PredictionSummary from '../components/UI/PredictionSummary';
import Legend from '../components/Map/Legend';
import { submitForecast } from '../services/api';

export default function ForecastPage() {
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleForecast = useCallback(async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const data = await submitForecast(payload);
      setForecastData(data);
    } catch (err) {
      const message =
        err.response?.data?.error || err.message || 'Forecast failed. Please try again.';
      setError(message);
      setForecastData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />

      <div className="flex-1 flex flex-col lg:flex-row gap-4 p-4 max-w-[1600px] mx-auto w-full">
        {/* Left sidebar: form + summary */}
        <div className="lg:w-[380px] flex-shrink-0 space-y-4">
          <ForecastForm onSubmit={handleForecast} loading={loading} />

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}

          {forecastData && <PredictionSummary data={forecastData} />}
        </div>

        {/* Right: Map + Legend */}
        <div className="flex-1 flex flex-col min-h-[500px] lg:min-h-0 relative">
          <TrafficMap forecastData={forecastData} />
          <Legend />
        </div>
      </div>
    </div>
  );
}
