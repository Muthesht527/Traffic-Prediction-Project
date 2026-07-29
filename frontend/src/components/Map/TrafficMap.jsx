import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';
import RouteLayer from './RouteLayer';

// Default Chennai center
const CHENNAI_CENTER = [13.0827, 80.2707];
const DEFAULT_ZOOM = 12;

// Fix Leaflet default icon issue with bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

/**
 * Fly to fit bounds whenever forecast data changes.
 */
function FitBounds({ forecastData }) {
  const map = useMap();

  useEffect(() => {
    if (!forecastData) return;
    const { source, destination } = forecastData;
    if (source?.lat && destination?.lat) {
      const bounds = L.latLngBounds(
        [source.lat, source.lng],
        [destination.lat, destination.lng]
      );
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [forecastData, map]);

  return null;
}

export default function TrafficMap({ forecastData }) {
  const sourceLat = forecastData?.source?.lat ?? CHENNAI_CENTER[0];
  const sourceLng = forecastData?.source?.lng ?? CHENNAI_CENTER[1];

  return (
    <div className="flex-1 rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
      <MapContainer
        center={[sourceLat, sourceLng]}
        zoom={DEFAULT_ZOOM}
        className="w-full h-full"
        style={{ minHeight: '500px' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Source marker */}
        {forecastData?.source?.lat && (
          <Marker position={[forecastData.source.lat, forecastData.source.lng]}>
            <Popup>
              <strong>Source</strong>
              <br />
              {forecastData.source.query}
            </Popup>
          </Marker>
        )}

        {/* Destination marker */}
        {forecastData?.destination?.lat && (
          <Marker position={[forecastData.destination.lat, forecastData.destination.lng]}>
            <Popup>
              <strong>Destination</strong>
              <br />
              {forecastData.destination.query}
            </Popup>
          </Marker>
        )}

        {/* Route with congestion colours */}
        {forecastData?.segments && (
          <RouteLayer segments={forecastData.segments} />
        )}

        <FitBounds forecastData={forecastData} />
      </MapContainer>
    </div>
  );
}
