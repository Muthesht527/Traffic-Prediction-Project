import { useState, useEffect, useRef, useCallback } from 'react';
import { Search, MapPin, X, Loader2 } from 'lucide-react';
import axios from 'axios';

const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
const DEBOUNCE_MS = 350;

export default function AutocompleteSearch({
  value,
  onChange,
  placeholder = 'Search location…',
  label,
  id,
  defaultBias, // { lat, lng } to bias results toward a region
}) {
  const [query, setQuery] = useState(value || '');
  const [results, setResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);
  const timerRef = useRef(null);

  // Sync external value changes
  useEffect(() => {
    if (value !== undefined && value !== query) {
      setQuery(value);
    }
  }, [value]);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const searchLocations = useCallback(async (q) => {
    if (q.length < 3) {
      setResults([]);
      setIsOpen(false);
      return;
    }
    setLoading(true);
    try {
      const params = {
        q,
        format: 'json',
        limit: 5,
        addressdetails: 1,
      };
      if (defaultBias) {
        params.viewbox = `${defaultBias.lng - 0.5},${defaultBias.lat + 0.5},${defaultBias.lng + 0.5},${defaultBias.lat - 0.5}`;
        params.bounded = 0;
      }
      const resp = await axios.get(NOMINATIM_URL, {
        params,
        headers: { 'User-Agent': 'TrafficForecastApp/1.0' },
        timeout: 8000,
      });
      setResults(resp.data || []);
      setIsOpen(true);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [defaultBias]);

  function handleInputChange(e) {
    const val = e.target.value;
    setQuery(val);
    onChange(''); // Clear previous selection

    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => searchLocations(val), DEBOUNCE_MS);
  }

  function handleSelect(result) {
    setQuery(result.display_name);
    onChange(result.display_name, {
      lat: parseFloat(result.lat),
      lng: parseFloat(result.lon),
    });
    setIsOpen(false);
    setResults([]);
  }

  function handleClear() {
    setQuery('');
    onChange('');
    setResults([]);
    setIsOpen(false);
  }

  return (
    <div className="relative" ref={wrapperRef}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1.5">
          {label}
        </label>
      )}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          id={id}
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          placeholder={placeholder}
          className="w-full pl-9 pr-9 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-400 text-sm transition-all bg-white"
          autoComplete="off"
        />
        {query && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        {loading && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />
          </div>
        )}
      </div>

      {/* Dropdown results */}
      {isOpen && results.length > 0 && (
        <div className="autocomplete-list animate-fade-in">
          {results.map((result, idx) => (
            <div
              key={result.place_id || idx}
              className="autocomplete-item flex items-start gap-2"
              onClick={() => handleSelect(result)}
            >
              <MapPin className="w-3.5 h-3.5 text-gray-400 mt-0.5 flex-shrink-0" />
              <span className="line-clamp-2">{result.display_name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
