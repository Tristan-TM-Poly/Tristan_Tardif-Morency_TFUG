export type GateMetrics = {
  evidence: number;
  coherence: number;
  bridgeDensity: number;
  speculativeCost: number;
};

export function clamp01(value: number): number {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

export function scoreGate(metrics: GateMetrics): number {
  const score =
    0.30 * metrics.evidence +
    0.25 * metrics.coherence +
    0.20 * metrics.bridgeDensity -
    0.25 * metrics.speculativeCost;
  return clamp01(score);
}

export function resolveGateStatus(metrics: GateMetrics): 'passed' | 'open' | 'blocked' {
  const score = scoreGate(metrics);
  if (score >= 0.75) return 'passed';
  if (score >= 0.55) return 'open';
  return 'blocked';
}
