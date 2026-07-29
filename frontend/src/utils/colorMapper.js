/**
 * Congestion score → colour and label mapper.
 * Mirrors the backend's color_mapper.py so the frontend can render
 * consistently even without an API round-trip.
 */

const COLOR_RANGES = [
  { min: 0, max: 20, color: '#22c55e', label: 'Low Congestion', bgClass: 'bg-green-500' },
  { min: 21, max: 40, color: '#eab308', label: 'Light Congestion', bgClass: 'bg-yellow-500' },
  { min: 41, max: 70, color: '#f97316', label: 'Moderate Congestion', bgClass: 'bg-orange-500' },
  { min: 71, max: 100, color: '#ef4444', label: 'Heavy Congestion', bgClass: 'bg-red-500' },
];

const NO_COVERAGE = { color: '#9ca3af', label: 'Coverage Not Available', bgClass: 'bg-gray-400' };

/**
 * Map a congestion score (0-100) to a colour + label.
 * @param {number|null} score
 * @returns {{ color: string, label: string, bgClass: string }}
 */
export function scoreToColor(score) {
  if (score === null || score === undefined) return NO_COVERAGE;
  for (const band of COLOR_RANGES) {
    if (score >= band.min && score <= band.max) return band;
  }
  return NO_COVERAGE;
}

/**
 * All colour legend entries.
 */
export function getLegendEntries() {
  return [...COLOR_RANGES, NO_COVERAGE];
}

export default { scoreToColor, getLegendEntries };
