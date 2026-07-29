import { Polyline, Popup } from 'react-leaflet';

/**
 * Renders route segments as coloured polylines on the map.
 *
 * Phase 1: single segment with one colour.
 * Future phases: multiple segments, each independently coloured.
 *
 * Segment shape: { coordinates: [[lng,lat],…], color, congestion_score, label }
 */
export default function RouteLayer({ segments }) {
  if (!segments || segments.length === 0) return null;

  return (
    <>
      {segments.map((segment, idx) => {
        // Convert [lng, lat] → [lat, lng] for Leaflet
        const positions = segment.coordinates.map(([lng, lat]) => [lat, lng]);

        return (
          <Polyline
            key={idx}
            positions={positions}
            pathOptions={{
              color: segment.color,
              weight: 7,
              opacity: 0.9,
              lineJoin: 'round',
              lineCap: 'round',
            }}
          >
            <Popup>
              <div className="text-sm min-w-[140px]">
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className="w-3 h-3 rounded-full inline-block"
                    style={{ backgroundColor: segment.color }}
                  />
                  <strong>{segment.label || 'Traffic Forecast'}</strong>
                </div>
                {segment.congestion_score !== null && segment.congestion_score !== undefined && (
                  <div className="text-gray-600 text-xs">
                    Congestion Score: <strong>{segment.congestion_score}</strong> / 100
                  </div>
                )}
              </div>
            </Popup>
          </Polyline>
        );
      })}
    </>
  );
}
