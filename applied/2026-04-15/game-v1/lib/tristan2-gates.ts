import { GateMetrics, resolveGateStatus, scoreGate } from './scoring';

export type GateRow = GateMetrics & {
  id: string;
  objectId: string;
  status: 'open' | 'passed' | 'blocked' | 'downgraded';
  nextAction: string;
};

export function updateGate(row: GateRow, patch: Partial<GateMetrics>): GateRow {
  const metrics: GateMetrics = {
    evidence: patch.evidence ?? row.evidence,
    coherence: patch.coherence ?? row.coherence,
    bridgeDensity: patch.bridgeDensity ?? row.bridgeDensity,
    speculativeCost: patch.speculativeCost ?? row.speculativeCost,
  };

  const resolved = resolveGateStatus(metrics);
  const nextAction =
    resolved === 'passed'
      ? 'unlock next node'
      : resolved === 'open'
        ? 'collect more evidence or increase coherence'
        : 'reduce speculative cost and review contradictions';

  return {
    ...row,
    ...metrics,
    status: resolved,
    nextAction,
  };
}

export function explainGate(row: GateRow): string {
  const score = scoreGate(row).toFixed(2);
  return `Gate ${row.id} for ${row.objectId}: status=${row.status}, score=${score}, next=${row.nextAction}`;
}
