export type WorldNode = {
  id: string;
  label: string;
  type: string;
  zoneId?: string;
};

export type WorldEdge = {
  id: string;
  source: string;
  target: string;
  type: string;
  weight: number;
};

export type WorldGraph = {
  zones: Array<{ id: string; label: string; description: string; unlockLevel: number }>;
  nodes: WorldNode[];
  edges: WorldEdge[];
};

export function getNodeById(graph: WorldGraph, nodeId: string): WorldNode | undefined {
  return graph.nodes.find((node) => node.id === nodeId);
}

export function getEdgesForNode(graph: WorldGraph, nodeId: string): WorldEdge[] {
  return graph.edges.filter((edge) => edge.source === nodeId || edge.target === nodeId);
}

export function getNeighbors(graph: WorldGraph, nodeId: string): WorldNode[] {
  const neighborIds = new Set<string>();
  for (const edge of getEdgesForNode(graph, nodeId)) {
    if (edge.source === nodeId) neighborIds.add(edge.target);
    if (edge.target === nodeId) neighborIds.add(edge.source);
  }
  return graph.nodes.filter((node) => neighborIds.has(node.id));
}

export function getUnlockedZoneIds(playerLevel: number, graph: WorldGraph): string[] {
  return graph.zones.filter((zone) => zone.unlockLevel <= playerLevel).map((zone) => zone.id);
}
