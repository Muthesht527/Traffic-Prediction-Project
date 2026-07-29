import { useState } from 'react';
import { MapPin, Calendar, Clock, Loader2 } from 'lucide-react';

const DEFAULT_SOURCE = 'Adyar, Chennai, India';
const DEFAULT_DESTINATION = 'T. Nagar, Chennai, India';

export default function ForecastForm({ onSubmit, loading }) {
  const [source, setSource] = useState(DEFAULT_SOURCE);
  const [destination, setDestination] = useState(DEFAULT_DESTINATION);

  // Default to tomorrow at 08:30
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const defaultDate = tomorrow.toISOString().split('T')[0];
  const [date, setDate] = useState(defaultDate);
  const [time, setTime] = useState('08:30');

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ source, destination, date, time });
  }

  return (
    <form onSubmit={handleSubmit} className="p-5 bg-white rounded-2xl border border-gray-200 shadow-sm space-y-4">
      <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
        <MapPin className="w-5 h-5 text-primary" />
        Route Forecast
      </h2>

      {/* Source */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
        <input
          type="text"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="e.g. Adyar, Chennai"
          required
          className="w-full px-3 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm"
        />
      </div>

      {/* Destination */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
        <input
          type="text"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="e.g. T. Nagar, Chennai"
          required
          className="w-full px-3 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm"
        />
      </div>

      {/* Date + Time */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            <Calendar className="w-3.5 h-3.5 inline mr-1" />
            Date
          </label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
            className="w-full px-3 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            <Clock className="w-3.5 h-3.5 inline mr-1" />
            Time
          </label>
          <input
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            required
            className="w-full px-3 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-primary text-white font-bold rounded-xl hover:bg-secondary transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Forecasting…
          </>
        ) : (
          'Forecast Traffic'
        )}
      </button>
    </form>
  );
}
