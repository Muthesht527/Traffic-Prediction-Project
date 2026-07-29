import { Polyline, Popup } from 'react-leaflet';

/**
 * Renders route segments as coloured polylines on the map.
 *
 * Phase 1: the entire route is a single segment with one colour.
 * Future phases can return multiple segments (one per road section),
 * each coloured independently — this component already handles that.
 *
 * Each segment: { coordinates: [[lng,lat], …], color, congestion_score, label }
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
              weight: 6,
              opacity: 0.85,
              lineJoin: 'round',
            }}
          >
            <Popup>
              <div className="text-sm">
                <strong style={{ color: segment.color }}>
                  {segment.label || 'Traffic Forecast'}
                </strong>
                {segment.congestion_score !== null && segment.congestion_score !== undefined && (
                  <>
                    <br />
                    Score: {segment.congestion_score}/100
                  </>
                )}
              </div>
            </Popup>
          </Polyline>
        );
      })}
    </>
  );
}
