import { GameDataBundle } from './game-engine';
import { GateRow } from './tristan2-gates';
import { Mission } from './mission-engine';

export type ExpansionNode = { id: string; label: string; type: string; zoneId?: string };
export type ExpansionArtifact = {
  id: string;
  type: string;
  label: string;
  zoneId: string;
  description: string;
  evidenceLevel: number;
  linkedNodeIds: string[];
  linkedMissionIds: string[];
};
export type ExpansionMission = Mission;
export type ExpansionGate = GateRow;

export type ExpansionPack = {
  version: string;
  label: string;
  nodes: ExpansionNode[];
  artifacts: ExpansionArtifact[];
  missions: ExpansionMission[];
  gates: ExpansionGate[];
};

function dedupeById<T extends { id: string }>(items: T[]): T[] {
  const seen = new Map<string, T>();
  for (const item of items) seen.set(item.id, item);
  return [...seen.values()];
}

export function integrateExpansionPack(bundle: GameDataBundle, pack: ExpansionPack): GameDataBundle {
  return {
    ...bundle,
    graph: {
      ...bundle.graph,
      nodes: dedupeById([...bundle.graph.nodes, ...pack.nodes]),
      edges: bundle.graph.edges,
      zones: bundle.graph.zones,
    },
    artifacts: dedupeById([...bundle.artifacts, ...pack.artifacts]),
    missions: dedupeById([...bundle.missions, ...pack.missions]),
    gates: dedupeById([...bundle.gates, ...pack.gates]),
  };
}
