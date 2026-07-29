import { getLegendEntries } from '../../utils/colorMapper';

export default function Legend() {
  const entries = getLegendEntries();

  return (
    <div className="absolute bottom-5 left-5 z-[1000] bg-white/95 backdrop-blur-sm rounded-xl border border-gray-100 shadow-lg p-3 animate-fade-in">
      <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">
        Congestion Level
      </h4>
      <div className="space-y-1.5 stagger-children">
        {entries.map((entry) => (
          <div key={entry.label} className="flex items-center gap-2">
            <span
              className="w-5 h-2.5 rounded-full inline-block shadow-sm"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-[11px] text-gray-600 font-medium">{entry.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
