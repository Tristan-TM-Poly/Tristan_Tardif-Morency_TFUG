import { scoreGate } from './scoring';

export type CivilizationState = {
  memoryIntegrity: number;
  technicalCapacity: number;
  symbolicCoherence: number;
  governanceStrength: number;
  collapsePressure: number;
  reconstructionPower: number;
  promotedKnowledge: number;
};

export type SimulationConfig = {
  seed: number;
  steps: number;
  branchLabel: string;
};

export type SimulationStep = {
  step: number;
  eventType: 'discovery' | 'translation' | 'collapse' | 'review' | 'promotion' | 'recoding';
  deltaMemory: number;
  deltaTechnical: number;
  deltaSymbolic: number;
  deltaGovernance: number;
  deltaCollapse: number;
  deltaReconstruction: number;
  deltaPromotedKnowledge: number;
  gateScore: number;
};

export type SimulationResult = {
  seed: number;
  branchLabel: string;
  finalState: CivilizationState;
  steps: SimulationStep[];
  promotedCount: number;
  collapseEvents: number;
  score: number;
};

function clamp01(value: number): number {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

function mulberry32(seed: number): () => number {
  let t = seed >>> 0;
  return function () {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), t | 1);
    r ^= r + Math.imul(r ^ (r >>> 7), r | 61);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

export function initialCivilizationState(): CivilizationState {
  return {
    memoryIntegrity: 0.45,
    technicalCapacity: 0.35,
    symbolicCoherence: 0.4,
    governanceStrength: 0.5,
    collapsePressure: 0.3,
    reconstructionPower: 0.2,
    promotedKnowledge: 0.1,
  };
}

export function simulateScenario(config: SimulationConfig): SimulationResult {
  const rand = mulberry32(config.seed);
  let state = initialCivilizationState();
  const steps: SimulationStep[] = [];
  let promotedCount = 0;
  let collapseEvents = 0;

  for (let step = 1; step <= config.steps; step++) {
    const roll = rand();
    let eventType: SimulationStep['eventType'] = 'discovery';
    if (roll < 0.18) eventType = 'collapse';
    else if (roll < 0.34) eventType = 'translation';
    else if (roll < 0.5) eventType = 'recoding';
    else if (roll < 0.7) eventType = 'review';
    else if (roll < 0.86) eventType = 'promotion';

    const deltaMemory = eventType === 'collapse' ? -0.12 * rand() : 0.02 + 0.06 * rand();
    const deltaTechnical = eventType === 'discovery' || eventType === 'promotion' ? 0.03 + 0.08 * rand() : -0.02 + 0.03 * rand();
    const deltaSymbolic = eventType === 'translation' || eventType === 'recoding' ? 0.02 + 0.07 * rand() : -0.01 + 0.02 * rand();
    const deltaGovernance = eventType === 'review' || eventType === 'promotion' ? 0.02 + 0.05 * rand() : -0.015 + 0.02 * rand();
    const deltaCollapse = eventType === 'collapse' ? 0.08 + 0.1 * rand() : -0.01 - 0.03 * rand();
    const deltaReconstruction = eventType === 'translation' || eventType === 'discovery' || eventType === 'review' ? 0.02 + 0.06 * rand() : -0.01 + 0.02 * rand();

    const gateScore = scoreGate({
      evidence: clamp01(state.memoryIntegrity + deltaMemory),
      coherence: clamp01(state.symbolicCoherence + deltaSymbolic),
      bridgeDensity: clamp01(state.reconstructionPower + deltaReconstruction),
      speculativeCost: clamp01(state.collapsePressure + Math.max(0, -deltaGovernance)),
    });

    const promoted = eventType === 'promotion' && gateScore >= 0.75 ? 0.03 + 0.07 * rand() : 0;
    const deltaPromotedKnowledge = promoted;

    state = {
      memoryIntegrity: clamp01(state.memoryIntegrity + deltaMemory),
      technicalCapacity: clamp01(state.technicalCapacity + deltaTechnical),
      symbolicCoherence: clamp01(state.symbolicCoherence + deltaSymbolic),
      governanceStrength: clamp01(state.governanceStrength + deltaGovernance),
      collapsePressure: clamp01(state.collapsePressure + deltaCollapse),
      reconstructionPower: clamp01(state.reconstructionPower + deltaReconstruction),
      promotedKnowledge: clamp01(state.promotedKnowledge + deltaPromotedKnowledge),
    };

    if (deltaPromotedKnowledge > 0) promotedCount += 1;
    if (eventType === 'collapse') collapseEvents += 1;

    steps.push({
      step,
      eventType,
      deltaMemory,
      deltaTechnical,
      deltaSymbolic,
      deltaGovernance,
      deltaCollapse,
      deltaReconstruction,
      deltaPromotedKnowledge,
      gateScore,
    });
  }

  const score = clamp01(
    0.22 * state.memoryIntegrity +
    0.22 * state.technicalCapacity +
    0.16 * state.symbolicCoherence +
    0.16 * state.governanceStrength +
    0.16 * state.reconstructionPower +
    0.18 * state.promotedKnowledge -
    0.2 * state.collapsePressure
  );

  return {
    seed: config.seed,
    branchLabel: config.branchLabel,
    finalState: state,
    steps,
    promotedCount,
    collapseEvents,
    score,
  };
}

export function simulateManyScenarios(count: number, steps: number, branchPrefix = 'branch'): SimulationResult[] {
  const results: SimulationResult[] = [];
  for (let i = 0; i < count; i++) {
    results.push(simulateScenario({
      seed: i + 1,
      steps,
      branchLabel: `${branchPrefix}-${i + 1}`,
    }));
  }
  return results;
}

export function summarizeSimulations(results: SimulationResult[]) {
  const total = results.length;
  const avg = (values: number[]) => values.reduce((a, b) => a + b, 0) / Math.max(1, values.length);
  return {
    total,
    averageScore: avg(results.map((r) => r.score)),
    averagePromotedCount: avg(results.map((r) => r.promotedCount)),
    averageCollapseEvents: avg(results.map((r) => r.collapseEvents)),
    topBranches: [...results].sort((a, b) => b.score - a.score).slice(0, 10).map((r) => ({
      seed: r.seed,
      branchLabel: r.branchLabel,
      score: r.score,
      promotedCount: r.promotedCount,
      collapseEvents: r.collapseEvents,
    })),
  };
}
