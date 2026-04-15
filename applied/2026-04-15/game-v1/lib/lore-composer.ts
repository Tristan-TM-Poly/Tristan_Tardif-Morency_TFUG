import { SimulationResult } from './simulation-engine';

export type LoreFragment = {
  title: string;
  summary: string;
  tags: string[];
  score: number;
};

export function composeLoreFragment(result: SimulationResult): LoreFragment {
  const final = result.finalState;
  const title = `${result.branchLabel} - Seed ${result.seed}`;
  const summary = `This branch evolves through ${result.steps.length} steps, with promoted knowledge ${final.promotedKnowledge.toFixed(2)}, memory integrity ${final.memoryIntegrity.toFixed(2)}, technical capacity ${final.technicalCapacity.toFixed(2)}, symbolic coherence ${final.symbolicCoherence.toFixed(2)}, governance strength ${final.governanceStrength.toFixed(2)}, and collapse pressure ${final.collapsePressure.toFixed(2)}.`;
  const tags = [
    final.promotedKnowledge > 0.7 ? 'reactivation' : 'struggle',
    final.collapsePressure > 0.65 ? 'collapse-risk' : 'stability',
    final.technicalCapacity > 0.7 ? 'technology' : 'fragmentation',
    final.symbolicCoherence > 0.7 ? 'symbolic-unity' : 'plurality'
  ];
  return { title, summary, tags, score: result.score };
}

export function composeLoreFragments(results: SimulationResult[]): LoreFragment[] {
  return results.map(composeLoreFragment);
}
