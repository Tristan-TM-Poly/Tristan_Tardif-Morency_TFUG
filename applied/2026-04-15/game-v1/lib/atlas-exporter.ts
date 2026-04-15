import { WorldGraph } from './graph-engine';

export type AtlasCard = {
  id: string;
  label: string;
  type: string;
  zoneId?: string;
  neighborCount: number;
};

export function exportAtlasCards(graph: WorldGraph): AtlasCard[] {
  return graph.nodes.map((node) => ({
    id: node.id,
    label: node.label,
    type: node.type,
    zoneId: node.zoneId,
    neighborCount: graph.edges.filter((edge) => edge.source === node.id || edge.target === node.id).length,
  }));
}

export function exportZoneSummaries(graph: WorldGraph) {
  return graph.zones.map((zone) => ({
    id: zone.id,
    label: zone.label,
    description: zone.description,
    nodeCount: graph.nodes.filter((node) => node.zoneId === zone.id).length,
  }));
}
