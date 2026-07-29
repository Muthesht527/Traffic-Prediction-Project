import { scoreToColor, getCongestionLevel } from '../../utils/colorMapper';
import {
  AlertTriangle,
  Cloud,
  Navigation,
  Activity,
  Clock,
  Wind,
  Droplets,
  Thermometer,
  TrendingUp,
} from 'lucide-react';

export default function PredictionSummary({ data }) {
  if (!data) return null;

  const { prediction, route, weather, coverage, segments } = data;
  const score = prediction.congestion_score;
  const colorInfo = scoreToColor(score);
  const inCoverage = coverage?.available ?? true;
  const level = getCongestionLevel(score);

  return (
    <div className="p-5 bg-white rounded-2xl border border-gray-100 shadow-sm space-y-4 animate-slide-up">
      {/* Header */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
          <Activity className="w-4 h-4 text-white" />
        </div>
        <h2 className="text-base font-bold text-gray-900">Prediction Summary</h2>
      </div>

      {/* Coverage warning */}
      {!inCoverage && (
        <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-2 animate-fade-in">
          <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-amber-800">
            <strong>Coverage Not Available</strong>
            <br />
            <span className="text-xs">
              This route is outside the {coverage?.region || 'supported'} dataset region.
              No prediction can be made.
            </span>
          </div>
        </div>
      )}

      {/* Congestion Score — animated reveal */}
      {inCoverage && score !== null && (
        <div className="text-center p-5 bg-gradient-to-br from-gray-50 to-gray-100/50 rounded-xl">
          <div
            className="text-6xl font-black animate-score-reveal"
            style={{ color: colorInfo.color }}
          >
            {score}
          </div>
          <div className="text-sm text-gray-500 mt-1 font-medium">Congestion Score (0–100)</div>
          <div
            className="mt-3 inline-block px-5 py-2 rounded-full text-white text-sm font-bold shadow-lg animate-fade-in"
            style={{
              backgroundColor: colorInfo.color,
              boxShadow: `0 4px 14px ${colorInfo.color}40`,
            }}
          >
            {level}
          </div>
        </div>
      )}

      {/* Model confidence */}
      {inCoverage && prediction.class_probabilities && Object.keys(prediction.class_probabilities).length > 0 && (
        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" />
            Model Confidence
          </div>
          <div className="space-y-2 stagger-children">
            {Object.entries(prediction.class_probabilities)
              .sort(([, a], [, b]) => b - a)
              .map(([cls, prob]) => (
                <div key={cls} className="flex items-center gap-2">
                  <span className="text-xs w-14 font-medium text-gray-600">{cls}</span>
                  <div className="flex-1 bg-gray-100 rounded-full h-2.5 overflow-hidden">
                    <div
                      className="h-full rounded-full animate-progress-fill"
                      style={{
                        width: `${(prob * 100).toFixed(0)}%`,
                        backgroundColor: colorInfo.color,
                      }}
                    />
                  </div>
                  <span className="text-xs font-bold text-gray-700 w-12 text-right">
                    {(prob * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Route Info */}
      <div className="grid grid-cols-2 gap-3">
        <div className="p-3 bg-gray-50 rounded-xl">
          <div className="flex items-center gap-1.5 text-gray-400 text-xs font-medium">
            <Navigation className="w-3.5 h-3.5" />
            Distance
          </div>
          <div className="text-lg font-bold text-gray-900 mt-1">
            {((route?.distance_m || 0) / 1000).toFixed(1)} <span className="text-sm font-normal text-gray-500">km</span>
          </div>
        </div>
        <div className="p-3 bg-gray-50 rounded-xl">
          <div className="flex items-center gap-1.5 text-gray-400 text-xs font-medium">
            <Clock className="w-3.5 h-3.5" />
            Est. Duration
          </div>
          <div className="text-lg font-bold text-gray-900 mt-1">
            {Math.round((route?.duration_s || 0) / 60)} <span className="text-sm font-normal text-gray-500">min</span>
          </div>
        </div>
      </div>

      {/* Weather */}
      <div>
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 flex items-center gap-1">
          <Cloud className="w-3.5 h-3.5" />
          Weather Forecast
        </div>
        <div className="grid grid-cols-2 gap-2">
          <WeatherStat icon={<Thermometer className="w-3.5 h-3.5 text-red-400" />} label="Temperature" value={`${weather?.temperature ?? '—'}°C`} />
          <WeatherStat icon={<Droplets className="w-3.5 h-3.5 text-blue-400" />} label="Humidity" value={`${weather?.humidity ?? '—'}%`} />
          <WeatherStat icon={<Wind className="w-3.5 h-3.5 text-gray-400" />} label="Wind Speed" value={`${weather?.wind_speed ?? '—'} m/s`} />
          <WeatherStat icon={<Droplets className="w-3.5 h-3.5 text-indigo-400" />} label="Rain" value={`${weather?.rain_1h ?? 0} mm`} />
        </div>
        <div className="mt-1.5 text-[10px] text-gray-400 text-right">
          via {weather?.source || 'weather service'}
        </div>
      </div>

      {/* Forecast time */}
      <div className="text-center pt-1 border-t border-gray-100">
        <p className="text-xs text-gray-400">
          Forecast for{' '}
          <strong className="text-gray-600">
            {new Date(data.target_datetime).toLocaleDateString('en-IN', {
              weekday: 'short',
              month: 'short',
              day: 'numeric',
            })}{' '}
            at{' '}
            {new Date(data.target_datetime).toLocaleTimeString('en-IN', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </strong>
        </p>
        {prediction.model && (
          <p className="text-[10px] text-gray-400 mt-0.5">
            Powered by {prediction.model === 'regressor' ? 'Random Forest Regressor' : 'Random Forest Classifier'}
          </p>
        )}
      </div>
    </div>
  );
}

function WeatherStat({ icon, label, value }) {
  return (
    <div className="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2">
      {icon}
      <div className="flex-1 min-w-0">
        <div className="text-[10px] text-gray-400 font-medium">{label}</div>
        <div className="text-sm font-bold text-gray-800">{value}</div>
      </div>
    </div>
  );
}
