import { Link } from 'react-router-dom';
import { MapPin } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-[1600px] mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
            <MapPin className="w-4 h-4 text-white" />
          </div>
          <span className="text-lg font-bold text-gray-900">Traffic Forecast</span>
        </Link>
        <div className="flex items-center gap-4">
          <a
            href="/forecast"
            className="text-sm font-medium text-gray-700 hover:text-primary transition-colors"
          >
            Forecast
          </a>
          <div className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium">
            ● Live Demo
          </div>
        </div>
      </div>
    </nav>
  );
}
