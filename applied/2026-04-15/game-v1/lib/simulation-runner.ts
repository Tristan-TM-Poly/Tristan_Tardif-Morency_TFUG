import { simulateManyScenarios, summarizeSimulations, SimulationResult } from './simulation-engine';

export type LoreBranchCard = {
  branchLabel: string;
  seed: number;
  score: number;
  promotedCount: number;
  collapseEvents: number;
  theme: string;
};

function themeFromResult(result: SimulationResult): string {
  if (result.finalState.collapsePressure > 0.7) return 'age-of-collapse';
  if (result.finalState.promotedKnowledge > 0.7) return 'age-of-reactivation';
  if (result.finalState.symbolicCoherence > 0.7) return 'age-of-symbolic-unity';
  if (result.finalState.technicalCapacity > 0.7) return 'age-of-machines';
  return 'fractured-transition';
}

export function buildLoreBranchCards(count: number, steps: number): LoreBranchCard[] {
  return simulateManyScenarios(count, steps, 'lore').map((result) => ({
    branchLabel: result.branchLabel,
    seed: result.seed,
    score: result.score,
    promotedCount: result.promotedCount,
    collapseEvents: result.collapseEvents,
    theme: themeFromResult(result),
  }));
}

export function buildSimulationPack(count: number, steps: number) {
  const results = simulateManyScenarios(count, steps, 'lore');
  return {
    summary: summarizeSimulations(results),
    cards: buildLoreBranchCards(count, steps),
  };
}
