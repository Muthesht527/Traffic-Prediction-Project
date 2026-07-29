import { scoreToColor } from '../../utils/colorMapper';
import { AlertTriangle, Cloud, Navigation, Activity } from 'lucide-react';

export default function PredictionSummary({ data }) {
  const { prediction, route, weather, coverage, segments } = data;
  const score = prediction.congestion_score;
  const colorInfo = scoreToColor(score);
  const inCoverage = coverage?.available ?? true;

  return (
    <div className="p-5 bg-white rounded-2xl border border-gray-200 shadow-sm space-y-4">
      <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
        <Activity className="w-5 h-5 text-primary" />
        Prediction Summary
      </h2>

      {/* Coverage warning */}
      {!inCoverage && (
        <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-amber-800">
            <strong>Coverage Not Available</strong>
            <br />
            This route is outside our supported dataset region ({coverage?.region || 'Chennai'}).
            No prediction can be made.
          </div>
        </div>
      )}

      {/* Congestion Score */}
      <div className="text-center p-4 bg-gray-50 rounded-xl">
        <div
          className="text-5xl font-extrabold"
          style={{ color: colorInfo.color }}
        >
          {score !== null ? score : '—'}
        </div>
        <div className="text-sm text-gray-500 mt-1">Congestion Score (0–100)</div>
        <div
          className="mt-2 inline-block px-4 py-1.5 rounded-full text-white text-sm font-bold"
          style={{ backgroundColor: colorInfo.color }}
        >
          {colorInfo.label}
        </div>
      </div>

      {/* Class Probabilities */}
      {prediction.class_probabilities && Object.keys(prediction.class_probabilities).length > 0 && (
        <div>
          <div className="text-xs font-medium text-gray-500 uppercase mb-2">Model Confidence</div>
          <div className="space-y-2">
            {Object.entries(prediction.class_probabilities)
              .sort(([, a], [, b]) => b - a)
              .map(([cls, prob]) => (
                <div key={cls} className="flex items-center gap-2">
                  <span className="text-xs w-14 font-medium text-gray-700">{cls}</span>
                  <div className="flex-1 bg-gray-100 rounded-full h-2.5">
                    <div
                      className="h-2.5 rounded-full transition-all duration-500"
                      style={{
                        width: `${(prob * 100).toFixed(0)}%`,
                        backgroundColor: scoreToColor(score).color,
                      }}
                    />
                  </div>
                  <span className="text-xs font-medium text-gray-600 w-10 text-right">
                    {(prob * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Route Info */}
      <div className="grid grid-cols-2 gap-3">
        <InfoCard
          icon={<Navigation className="w-4 h-4 text-gray-500" />}
          label="Distance"
          value={`${(route?.distance_m / 1000).toFixed(1)} km`}
        />
        <InfoCard
          icon={<Navigation className="w-4 h-4 text-gray-500" />}
          label="Est. Duration"
          value={`${Math.round((route?.duration_s || 0) / 60)} min`}
        />
      </div>

      {/* Weather */}
      <div>
        <div className="text-xs font-medium text-gray-500 uppercase mb-2 flex items-center gap-1">
          <Cloud className="w-3.5 h-3.5" />
          Weather Forecast
        </div>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <WeatherStat label="Temp" value={`${weather?.temperature ?? '—'}°C`} />
          <WeatherStat label="Humidity" value={`${weather?.humidity ?? '—'}%`} />
          <WeatherStat label="Wind" value={`${weather?.wind_speed ?? '—'} m/s`} />
          <WeatherStat label="Rain" value={`${weather?.rain_1h ?? '0'} mm`} />
        </div>
        <div className="mt-1 text-xs text-gray-500">
          Source: {weather?.source || '—'}
        </div>
      </div>

      {/* Timestamp */}
      <div className="text-xs text-gray-400 text-center">
        Forecast for: {new Date(data.target_datetime).toLocaleString()}
      </div>
    </div>
  );
}

function InfoCard({ icon, label, value }) {
  return (
    <div className="p-3 bg-gray-50 rounded-xl">
      <div className="flex items-center gap-1 text-gray-500 text-xs">
        {icon}
        {label}
      </div>
      <div className="text-lg font-bold text-gray-900 mt-0.5">{value}</div>
    </div>
  );
}

function WeatherStat({ label, value }) {
  return (
    <div className="flex justify-between items-center bg-gray-50 rounded-lg px-2.5 py-1.5">
      <span className="text-gray-500 text-xs">{label}</span>
      <span className="font-semibold text-gray-800 text-xs">{value}</span>
    </div>
  );
}
