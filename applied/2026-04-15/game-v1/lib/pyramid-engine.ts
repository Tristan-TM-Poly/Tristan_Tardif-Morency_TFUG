import { scoreGate } from './scoring';

export type PyramidSystemState = {
  structuralIntegrity: number;
  thermalStability: number;
  waterStability: number;
  lightAlignment: number;
  memoryCapacity: number;
  governanceClarity: number;
};

export type PyramidEvaluation = PyramidSystemState & {
  systemScore: number;
  recommendation: string;
};

function clamp01(value: number): number {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

export function evaluatePyramidSystem(state: PyramidSystemState): PyramidEvaluation {
  const coherence = clamp01((state.structuralIntegrity + state.thermalStability + state.waterStability + state.lightAlignment) / 4);
  const bridgeDensity = clamp01((state.memoryCapacity + state.governanceClarity) / 2);
  const speculativeCost = clamp01(1 - Math.min(state.structuralIntegrity, state.governanceClarity));
  const systemScore = scoreGate({
    evidence: state.structuralIntegrity,
    coherence,
    bridgeDensity,
    speculativeCost,
  });

  const recommendation =
    systemScore >= 0.75
      ? 'promote pyramid branch'
      : systemScore >= 0.55
        ? 'stabilize thermal, water, or governance subsystems'
        : 'rebuild from stronger structural and review foundations';

  return {
    ...state,
    systemScore,
    recommendation,
  };
}
