import { Link, useLocation } from 'react-router-dom';
import { MapPin, Home } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const isForecast = location.pathname === '/forecast';

  return (
    <nav className="bg-white/90 backdrop-blur-md border-b border-gray-100 px-6 py-3 sticky top-0 z-50">
      <div className="max-w-[1600px] mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center shadow-md shadow-orange-500/15 group-hover:shadow-orange-500/25 transition-shadow">
            <MapPin className="w-4 h-4 text-white" />
          </div>
          <div>
            <span className="text-base font-bold text-gray-900 block leading-tight">
              Traffic Forecast
            </span>
            <span className="text-[10px] text-gray-400 font-medium">
              AI-Powered Platform
            </span>
          </div>
        </Link>

        <div className="flex items-center gap-3">
          {!isForecast && (
            <Link
              to="/forecast"
              className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 bg-gray-50 hover:bg-orange-50 rounded-xl transition-colors"
            >
              <MapPin className="w-4 h-4" />
              Forecast
            </Link>
          )}
          {isForecast && (
            <Link
              to="/"
              className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-700 hover:text-orange-600 bg-gray-50 hover:bg-orange-50 rounded-xl transition-colors"
            >
              <Home className="w-4 h-4" />
              Home
            </Link>
          )}
          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-green-50 border border-green-100 rounded-full">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-[11px] font-semibold text-green-700">Live</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
