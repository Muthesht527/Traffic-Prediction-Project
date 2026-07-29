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
        {/* Left sidebar */}
        <div className="lg:w-[400px] flex-shrink-0 space-y-4 order-2 lg:order-1">
          <ForecastForm onSubmit={handleForecast} loading={loading} />

          {/* Error display */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-100 rounded-2xl animate-fade-in">
              <div className="flex items-start gap-2">
                <div className="w-5 h-5 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-red-500 text-xs font-bold">!</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-red-800">Something went wrong</p>
                  <p className="text-xs text-red-600 mt-0.5">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Prediction summary */}
          {forecastData && <PredictionSummary data={forecastData} />}
        </div>

        {/* Right: Map */}
        <div className="flex-1 flex flex-col min-h-[500px] lg:min-h-0 relative order-1 lg:order-2">
          <TrafficMap forecastData={forecastData} loading={loading} />
          <Legend />
        </div>
      </div>
    </div>
  );
}
