import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';
import RouteLayer from './RouteLayer';

const CHENNAI_CENTER = [13.0827, 80.2707];
const DEFAULT_ZOOM = 12;

// Fix Leaflet default icon issue with bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Custom icons
const createIcon = (color) =>
  L.divIcon({
    className: 'custom-marker',
    html: `<div style="width:24px;height:24px;border-radius:50%;background:${color};border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -14],
  });

const SOURCE_ICON = createIcon('#22c55e');
const DEST_ICON = createIcon('#ef4444');

function FitBounds({ forecastData }) {
  const map = useMap();

  useEffect(() => {
    if (!forecastData) return;
    const { source, destination, segments } = forecastData;

    // If we have route segments, use their bounds
    if (segments && segments.length > 0) {
      const allCoords = segments.flatMap((seg) =>
        seg.coordinates.map(([lng, lat]) => [lat, lng])
      );
      if (allCoords.length > 1) {
        const bounds = L.latLngBounds(allCoords);
        map.fitBounds(bounds, { padding: [60, 60] });
        return;
      }
    }

    // Fallback to source/destination markers
    if (source?.lat && destination?.lat) {
      const bounds = L.latLngBounds(
        [source.lat, source.lng],
        [destination.lat, destination.lng]
      );
      map.fitBounds(bounds, { padding: [60, 60] });
    }
  }, [forecastData, map]);

  return null;
}

export default function TrafficMap({ forecastData, loading }) {
  const centerLat = forecastData?.source?.lat ?? CHENNAI_CENTER[0];
  const centerLng = forecastData?.source?.lng ?? CHENNAI_CENTER[1];

  return (
    <div className="flex-1 rounded-2xl overflow-hidden border border-gray-100 shadow-sm relative bg-gray-100">
      <MapContainer
        center={[centerLat, centerLng]}
        zoom={DEFAULT_ZOOM}
        className="w-full h-full"
        style={{ minHeight: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Source marker */}
        {forecastData?.source?.lat && (
          <Marker position={[forecastData.source.lat, forecastData.source.lng]} icon={SOURCE_ICON}>
            <Popup>
              <div className="font-medium text-sm">
                <span className="text-green-600">● </span>Source
                <br />
                <span className="text-gray-500 text-xs">{forecastData.source.query}</span>
              </div>
            </Popup>
          </Marker>
        )}

        {/* Destination marker */}
        {forecastData?.destination?.lat && (
          <Marker position={[forecastData.destination.lat, forecastData.destination.lng]} icon={DEST_ICON}>
            <Popup>
              <div className="font-medium text-sm">
                <span className="text-red-500">● </span>Destination
                <br />
                <span className="text-gray-500 text-xs">{forecastData.destination.query}</span>
              </div>
            </Popup>
          </Marker>
        )}

        {/* Route with congestion colours */}
        {forecastData?.segments && !loading && (
          <RouteLayer segments={forecastData.segments} />
        )}

        <FitBounds forecastData={forecastData} />
      </MapContainer>

      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 z-[1000] bg-white/70 backdrop-blur-sm flex flex-col items-center justify-center gap-3 animate-fade-in">
          <div className="w-12 h-12 border-4 border-orange-200 border-t-orange-500 rounded-full animate-spin" />
          <p className="text-sm font-medium text-gray-600">Forecasting traffic…</p>
          <p className="text-xs text-gray-400">Fetching route, weather, and running ML model</p>
        </div>
      )}
    </div>
  );
}
