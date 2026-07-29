import { getLegendEntries } from '../../utils/colorMapper';

export default function Legend() {
  const entries = getLegendEntries();

  return (
    <div className="absolute bottom-6 left-6 z-[1000] bg-white/95 backdrop-blur-sm rounded-xl border border-gray-200 shadow-lg p-3">
      <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wide mb-2">
        Congestion Level
      </h4>
      <div className="space-y-1.5">
        {entries.map((entry) => (
          <div key={entry.label} className="flex items-center gap-2">
            <span
              className="w-5 h-2.5 rounded-full inline-block"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-xs text-gray-700">{entry.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
