import { useState } from 'react';
import { MapPin, Calendar, Clock, Loader2, Search, AlertCircle } from 'lucide-react';
import AutocompleteSearch from './AutocompleteSearch';

const BIAS = { lat: 13.0827, lng: 80.2707 }; // Chennai

export default function ForecastForm({ onSubmit, loading }) {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [sourceCoords, setSourceCoords] = useState(null);
  const [destCoords, setDestCoords] = useState(null);

  // Default to tomorrow at 08:30
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const defaultDate = tomorrow.toISOString().split('T')[0];
  const [date, setDate] = useState(defaultDate);
  const [time, setTime] = useState('08:30');
  const [validationError, setValidationError] = useState('');

  function handleSourceChange(value, coords) {
    setSource(value);
    if (coords) setSourceCoords(coords);
  }

  function handleDestChange(value, coords) {
    setDestination(value);
    if (coords) setDestCoords(coords);
  }

  function handleSubmit(e) {
    e.preventDefault();
    setValidationError('');

    if (!source.trim()) {
      setValidationError('Please select a source location.');
      return;
    }
    if (!destination.trim()) {
      setValidationError('Please select a destination location.');
      return;
    }

    // Prefer coordinates if available, otherwise send the string
    const sourcePayload = sourceCoords || source;
    const destPayload = destCoords || destination;

    onSubmit({
      source: sourcePayload,
      destination: destPayload,
      date,
      time,
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="p-5 bg-white rounded-2xl border border-gray-100 shadow-sm space-y-4 animate-fade-in"
    >
      <div className="flex items-center gap-2 pb-1">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
          <Search className="w-4 h-4 text-white" />
        </div>
        <h2 className="text-base font-bold text-gray-900">Plan Your Forecast</h2>
      </div>

      {/* Source */}
      <AutocompleteSearch
        id="source-input"
        label="Source"
        value={source}
        onChange={handleSourceChange}
        placeholder="e.g. Adyar, Chennai"
        defaultBias={BIAS}
      />

      {/* Destination */}
      <AutocompleteSearch
        id="destination-input"
        label="Destination"
        value={destination}
        onChange={handleDestChange}
        placeholder="e.g. T. Nagar, Chennai"
        defaultBias={BIAS}
      />

      {/* Date + Time */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">
            <Calendar className="w-3.5 h-3.5 inline mr-1 text-gray-400" />
            Date
          </label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
            min={new Date().toISOString().split('T')[0]}
            max={(() => { const d = new Date(); d.setDate(d.getDate() + 7); return d.toISOString().split('T')[0]; })()}
            className="w-full px-3 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-400 text-sm transition-all bg-white"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">
            <Clock className="w-3.5 h-3.5 inline mr-1 text-gray-400" />
            Time
          </label>
          <input
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            required
            className="w-full px-3 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-400 text-sm transition-all bg-white"
          />
        </div>
      </div>

      {/* Validation error */}
      {validationError && (
        <div className="flex items-center gap-2 p-2.5 bg-red-50 rounded-xl text-red-600 text-xs animate-fade-in">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {validationError}
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white font-bold rounded-xl hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-orange-500/20 hover:shadow-orange-500/30 active:scale-[0.98]"
      >
        {loading ? (
          <>
            <div className="spinner" />
            <span>Forecasting…</span>
          </>
        ) : (
          <>
            <MapPin className="w-4 h-4" />
            <span>Forecast Traffic</span>
          </>
        )}
      </button>

      {/* Coverage hint */}
      <p className="text-[11px] text-center text-gray-400">
        Currently supporting Chennai region • Up to 7 days ahead
      </p>
    </form>
  );
}
