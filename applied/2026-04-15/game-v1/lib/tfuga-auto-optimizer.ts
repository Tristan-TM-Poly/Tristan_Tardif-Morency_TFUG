export type OptimizationObjectives = {
  fertility: number;
  feasibility: number;
  coherence: number;
  impact: number;
  reuse: number;
  automation: number;
  antiInflation: number;
};

export type OptimizationCandidate = {
  id: string;
  family: string;
  metrics: OptimizationObjectives;
};

export type RankedOptimizationCandidate = OptimizationCandidate & {
  score: number;
  recommendation: string;
};

function clamp01(x: number) {
  return Math.max(0, Math.min(1, x));
}

export function scoreOptimizationCandidate(candidate: OptimizationCandidate): RankedOptimizationCandidate {
  const m = candidate.metrics;
  const score = clamp01(
    0.18 * m.fertility +
    0.14 * m.feasibility +
    0.14 * m.coherence +
    0.16 * m.impact +
    0.14 * m.reuse +
    0.12 * m.automation +
    0.12 * m.antiInflation
  );

  const recommendation =
    score >= 0.82
      ? 'promote into active trunk'
      : score >= 0.65
        ? 'crystallize and benchmark before promotion'
        : 'keep exploratory or refactor for stronger coherence and reuse';

  return { ...candidate, score, recommendation };
}

export function rankOptimizationCandidates(candidates: OptimizationCandidate[]) {
  return candidates.map(scoreOptimizationCandidate).sort((a, b) => b.score - a.score);
}

export function selectBestReusableAutomation(candidates: OptimizationCandidate[]) {
  return rankOptimizationCandidates(candidates)[0] ?? null;
}
