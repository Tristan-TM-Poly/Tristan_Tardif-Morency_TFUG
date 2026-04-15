export type RecouplingId = {
  A: number;
  B: number;
  C: number;
  D: number;
};

export type RecouplingMetrics = {
  fertility: number;
  feasibility: number;
  depth: number;
  impact: number;
};

export type RankedRecoupling = RecouplingId & RecouplingMetrics & {
  id: string;
  score: number;
};

function clamp01(value: number): number {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

export function recouplingIdToString(id: RecouplingId): string {
  return `A${id.A} B${id.B} C${id.C} D${id.D}`;
}

export function scoreRecoupling(metrics: RecouplingMetrics): number {
  return clamp01(
    0.30 * metrics.fertility +
    0.25 * metrics.feasibility +
    0.20 * metrics.depth +
    0.25 * metrics.impact
  );
}

export function rankRecoupling(id: RecouplingId, metrics: RecouplingMetrics): RankedRecoupling {
  return {
    ...id,
    ...metrics,
    id: recouplingIdToString(id),
    score: scoreRecoupling(metrics),
  };
}

export function rankManyRecouplings(items: Array<{ id: RecouplingId; metrics: RecouplingMetrics }>): RankedRecoupling[] {
  return items.map((item) => rankRecoupling(item.id, item.metrics)).sort((a, b) => b.score - a.score);
}

export function buildCanonicalSeedRankings(): RankedRecoupling[] {
  const seeds: Array<{ id: RecouplingId; metrics: RecouplingMetrics }> = [
    { id: { A: 1, B: 1, C: 1, D: 5 }, metrics: { fertility: 0.98, feasibility: 0.82, depth: 0.95, impact: 0.99 } },
    { id: { A: 3, B: 4, C: 2, D: 2 }, metrics: { fertility: 0.93, feasibility: 0.88, depth: 0.86, impact: 0.94 } },
    { id: { A: 5, B: 2, C: 4, D: 4 }, metrics: { fertility: 0.9, feasibility: 0.9, depth: 0.9, impact: 0.96 } },
    { id: { A: 2, B: 5, C: 5, D: 3 }, metrics: { fertility: 0.95, feasibility: 0.8, depth: 0.87, impact: 0.93 } },
    { id: { A: 1, B: 3, C: 7, D: 5 }, metrics: { fertility: 0.92, feasibility: 0.78, depth: 0.94, impact: 0.97 } },
  ];
  return rankManyRecouplings(seeds);
}
