import { scoreGate } from './scoring';

export type PyramidVector = {
  theta: number;
  heightBaseRatio: number;
  materialStrength: number;
  structuralRedundancy: number;
  thermalInertia: number;
  ventilation: number;
  solarUtility: number;
  thermalControl: number;
  capture: number;
  storage: number;
  filtration: number;
  redistribution: number;
  orientation: number;
  guidance: number;
  distribution: number;
  capacity: number;
  redundancy: number;
  transmissibility: number;
  accessibility: number;
  reviewQuality: number;
  decisionVisibility: number;
  powerDistribution: number;
  institutionalStability: number;
};

export type PyramidScores = {
  structure: number;
  thermal: number;
  water: number;
  light: number;
  memory: number;
  governance: number;
  penalty: number;
  totalScore: number;
  gateScore: number;
};

export type PyramidSimulationResult = {
  seed: number;
  vector: PyramidVector;
  scores: PyramidScores;
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

export function randomPyramidVector(seed: number): PyramidVector {
  const rand = mulberry32(seed);
  return {
    theta: 0.2 + rand(),
    heightBaseRatio: 0.1 + 1.4 * rand(),
    materialStrength: rand(),
    structuralRedundancy: rand(),
    thermalInertia: rand(),
    ventilation: rand(),
    solarUtility: rand(),
    thermalControl: rand(),
    capture: rand(),
    storage: rand(),
    filtration: rand(),
    redistribution: rand(),
    orientation: rand(),
    guidance: rand(),
    distribution: rand(),
    capacity: rand(),
    redundancy: rand(),
    transmissibility: rand(),
    accessibility: rand(),
    reviewQuality: rand(),
    decisionVisibility: rand(),
    powerDistribution: rand(),
    institutionalStability: rand(),
  };
}

export function evaluatePyramidVector(v: PyramidVector): PyramidScores {
  const structure = clamp01((v.materialStrength + v.structuralRedundancy + (1 - Math.abs(v.heightBaseRatio - 0.7))) / 3);
  const thermal = clamp01((v.thermalInertia + v.ventilation + v.solarUtility + v.thermalControl) / 4);
  const water = clamp01((v.capture + v.storage + v.filtration + v.redistribution) / 4);
  const light = clamp01((v.orientation + v.guidance + v.distribution) / 3);
  const memory = clamp01((v.capacity + v.redundancy + v.transmissibility + v.accessibility) / 4);
  const governance = clamp01((v.reviewQuality + v.decisionVisibility + v.powerDistribution + v.institutionalStability) / 4);

  const couplingSW = (structure + water) / 2;
  const couplingTM = (thermal + memory) / 2;
  const couplingMG = (memory + governance) / 2;
  const ornamentVoid = clamp01(1 - Math.min(structure, governance));
  const penalty = clamp01(0.25 * (1 - couplingSW) + 0.25 * (1 - couplingTM) + 0.25 * (1 - couplingMG) + 0.25 * ornamentVoid);

  const totalScore = clamp01(
    0.22 * structure +
    0.16 * thermal +
    0.16 * water +
    0.12 * light +
    0.16 * memory +
    0.18 * governance -
    0.20 * penalty
  );

  const gateScore = scoreGate({
    evidence: structure,
    coherence: clamp01((thermal + water + light) / 3),
    bridgeDensity: clamp01((memory + governance) / 2),
    speculativeCost: penalty,
  });

  return { structure, thermal, water, light, memory, governance, penalty, totalScore, gateScore };
}

export function simulatePyramid(seed: number): PyramidSimulationResult {
  const vector = randomPyramidVector(seed);
  const scores = evaluatePyramidVector(vector);
  return { seed, vector, scores };
}

export function simulateManyPyramids(count: number): PyramidSimulationResult[] {
  const results: PyramidSimulationResult[] = [];
  for (let i = 0; i < count; i++) {
    results.push(simulatePyramid(i + 1));
  }
  return results;
}

export function summarizePyramidSimulations(results: PyramidSimulationResult[]) {
  const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / Math.max(1, arr.length);
  return {
    total: results.length,
    averageTotalScore: avg(results.map((r) => r.scores.totalScore)),
    averageGateScore: avg(results.map((r) => r.scores.gateScore)),
    topDesigns: [...results]
      .sort((a, b) => b.scores.totalScore - a.scores.totalScore)
      .slice(0, 10)
      .map((r) => ({ seed: r.seed, totalScore: r.scores.totalScore, gateScore: r.scores.gateScore })),
  };
}
