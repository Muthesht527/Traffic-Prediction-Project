/**
 * Congestion score → colour and label mapper.
 * Mirrors the backend color_mapper for consistent rendering.
 */

const COLOR_RANGES = [
  { min: 0, max: 20, color: '#22c55e', label: 'Low Congestion', gradient: 'from-green-400 to-green-600' },
  { min: 21, max: 40, color: '#eab308', label: 'Light Congestion', gradient: 'from-yellow-400 to-yellow-600' },
  { min: 41, max: 70, color: '#f97316', label: 'Moderate Congestion', gradient: 'from-orange-400 to-orange-600' },
  { min: 71, max: 100, color: '#ef4444', label: 'Heavy Congestion', gradient: 'from-red-500 to-red-700' },
];

const NO_COVERAGE = {
  color: '#9ca3af',
  label: 'Coverage Not Available',
  gradient: 'from-gray-300 to-gray-500',
};

/**
 * Map a congestion score (0-100) to a colour + label.
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

/**
 * Get a human-readable congestion level from score.
 */
export function getCongestionLevel(score) {
  if (score === null || score === undefined) return 'Unknown';
  if (score <= 20) return 'Free Flow';
  if (score <= 40) return 'Light Traffic';
  if (score <= 70) return 'Moderate Traffic';
  return 'Heavy Traffic';
}

export default { scoreToColor, getLegendEntries, getCongestionLevel };
