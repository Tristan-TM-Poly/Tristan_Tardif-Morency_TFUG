import { SimulationResult } from './simulation-engine';

export type BranchSelectionRule = {
  minScore?: number;
  maxCollapseEvents?: number;
  minPromotedCount?: number;
  preferredThemes?: string[];
};

export function selectTopSimulationBranches(results: SimulationResult[], rule: BranchSelectionRule = {}): SimulationResult[] {
  const filtered = results.filter((result) => {
    if (rule.minScore !== undefined && result.score < rule.minScore) return false;
    if (rule.maxCollapseEvents !== undefined && result.collapseEvents > rule.maxCollapseEvents) return false;
    if (rule.minPromotedCount !== undefined && result.promotedCount < rule.minPromotedCount) return false;
    return true;
  });

  return [...filtered].sort((a, b) => b.score - a.score || b.promotedCount - a.promotedCount);
}

export function pickCampaignSeed(results: SimulationResult[]): SimulationResult | null {
  if (!results.length) return null;
  return [...results].sort((a, b) => b.score - a.score || a.collapseEvents - b.collapseEvents)[0] ?? null;
}
