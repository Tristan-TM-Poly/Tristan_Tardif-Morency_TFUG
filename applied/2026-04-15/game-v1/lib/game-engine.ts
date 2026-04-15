import { WorldGraph, getUnlockedZoneIds } from './graph-engine';
import { Mission, PlayerProgression, canStartMission, missionCompletionProgress, applyMissionRewards } from './mission-engine';
import { GateRow, updateGate } from './tristan2-gates';
import { AgentMessage } from './message-protocol';

export type Artifact = {
  id: string;
  type: string;
  label: string;
  zoneId: string;
  description: string;
  evidenceLevel: number;
  linkedNodeIds: string[];
  linkedMissionIds: string[];
};

export type NPCRecord = {
  id: string;
  name: string;
  role: 'concept' | 'system' | 'experiment' | 'review' | 'collaboration';
  memoryIds: string[];
  trustLevel: number;
  bias: string;
  linkedNPCIds: string[];
  linkedAIBotIds: string[];
  linkedTripletIds: string[];
  unlockedByMissionIds: string[];
};

export type AIBotRecord = {
  id: string;
  name: string;
  domain: string;
  operators: string[];
  scoreWeight: number;
  representationMode: string;
  policy: string;
  linkedBotIds: string[];
  linkedNPCIds: string[];
  linkedTripletIds: string[];
};

export type TrinityRecord = {
  id: string;
  tfugaRole: string;
  ai7Role: string;
  tristan2Role: string;
  linkedAgentIds: string[];
  gatePolicy: string;
  reviewLevel: 'light' | 'standard' | 'strict';
};

export type GameDataBundle = {
  graph: WorldGraph;
  missions: Mission[];
  gates: GateRow[];
  artifacts: Artifact[];
  npcs: NPCRecord[];
  aibots: AIBotRecord[];
  triplets: TrinityRecord[];
};

export type RuntimeIndexes = {
  missionById: Map<string, Mission>;
  gateById: Map<string, GateRow>;
  artifactById: Map<string, Artifact>;
  npcById: Map<string, NPCRecord>;
  aibotById: Map<string, AIBotRecord>;
  tripletById: Map<string, TrinityRecord>;
};

export type DerivedView = {
  unlockedZoneIds: string[];
  activeMission: Mission | null;
  activeGate: GateRow | null;
  missionProgress: number;
  activeArtifacts: Artifact[];
  npcIdsForActiveMission: string[];
  nodeIdsForActiveMission: string[];
};

export type GameRuntime = {
  data: GameDataBundle;
  indexes: RuntimeIndexes;
  player: PlayerProgression;
  messages: AgentMessage[];
  view: DerivedView;
};

export function createIndexes(data: GameDataBundle): RuntimeIndexes {
  return {
    missionById: new Map(data.missions.map((m) => [m.id, m])),
    gateById: new Map(data.gates.map((g) => [g.id, g])),
    artifactById: new Map(data.artifacts.map((a) => [a.id, a])),
    npcById: new Map(data.npcs.map((n) => [n.id, n])),
    aibotById: new Map(data.aibots.map((b) => [b.id, b])),
    tripletById: new Map(data.triplets.map((t) => [t.id, t])),
  };
}

export function deriveView(data: GameDataBundle, indexes: RuntimeIndexes, player: PlayerProgression): DerivedView {
  const unlockedZoneIds = getUnlockedZoneIds(player.playerLevel, data.graph);
  const activeMission = player.activeMissionId ? indexes.missionById.get(player.activeMissionId) ?? null : null;
  const activeGate = activeMission ? indexes.gateById.get(activeMission.reviewGateId) ?? null : null;
  const missionProgress = activeMission ? missionCompletionProgress(activeMission, player) : 0;
  const activeArtifacts = activeMission
    ? activeMission.requiredArtifacts.map((id) => indexes.artifactById.get(id)).filter(Boolean) as Artifact[]
    : [];
  const npcIdsForActiveMission = activeMission ? activeMission.requiredNPCs : [];
  const nodeIdsForActiveMission = activeMission ? activeMission.requiredNodes : [];

  return {
    unlockedZoneIds,
    activeMission,
    activeGate,
    missionProgress,
    activeArtifacts,
    npcIdsForActiveMission,
    nodeIdsForActiveMission,
  };
}

export function createGameRuntime(data: GameDataBundle, player: PlayerProgression, messages: AgentMessage[] = []): GameRuntime {
  const indexes = createIndexes(data);
  const view = deriveView(data, indexes, player);
  return { data, indexes, player, messages, view };
}

export function startMission(runtime: GameRuntime, missionId: string): GameRuntime {
  const mission = runtime.indexes.missionById.get(missionId);
  if (!mission) return runtime;
  if (!canStartMission(mission, runtime.player)) return runtime;

  const player: PlayerProgression = {
    ...runtime.player,
    activeMissionId: mission.id,
  };
  return createGameRuntime(runtime.data, player, runtime.messages);
}

export function discoverArtifact(runtime: GameRuntime, artifactId: string): GameRuntime {
  if (runtime.player.discoveredArtifacts.includes(artifactId)) return runtime;
  const player: PlayerProgression = {
    ...runtime.player,
    discoveredArtifacts: [...runtime.player.discoveredArtifacts, artifactId],
  };
  return createGameRuntime(runtime.data, player, runtime.messages);
}

export function unlockNode(runtime: GameRuntime, nodeId: string): GameRuntime {
  if (runtime.player.unlockedNodes.includes(nodeId)) return runtime;
  const player: PlayerProgression = {
    ...runtime.player,
    unlockedNodes: [...runtime.player.unlockedNodes, nodeId],
  };
  return createGameRuntime(runtime.data, player, runtime.messages);
}

export function submitGateMetrics(runtime: GameRuntime, gateId: string, patch: Partial<Pick<GateRow, 'evidence' | 'coherence' | 'bridgeDensity' | 'speculativeCost'>>): GameRuntime {
  const current = runtime.indexes.gateById.get(gateId);
  if (!current) return runtime;
  const updated = updateGate(current, patch);
  const gates = runtime.data.gates.map((gate) => (gate.id === gateId ? updated : gate));
  const data = { ...runtime.data, gates };
  return createGameRuntime(data, runtime.player, runtime.messages);
}

export function tryCompleteActiveMission(runtime: GameRuntime): GameRuntime {
  const mission = runtime.view.activeMission;
  const gate = runtime.view.activeGate;
  if (!mission || !gate) return runtime;
  if (gate.status !== 'passed') return runtime;
  if (missionCompletionProgress(mission, runtime.player) < 1) return runtime;

  const player = applyMissionRewards(mission, runtime.player);
  const mergedUnlockedZones = Array.from(new Set([...player.unlockedZones, ...getUnlockedZoneIds(player.playerLevel + 1, runtime.data.graph)]));
  const finalPlayer: PlayerProgression = {
    ...player,
    unlockedZones: mergedUnlockedZones,
    playerLevel: player.playerLevel + 1,
    reviewStatus: 'passed',
  };
  return createGameRuntime(runtime.data, finalPlayer, runtime.messages);
}

export function pushMessage(runtime: GameRuntime, message: AgentMessage): GameRuntime {
  return createGameRuntime(runtime.data, runtime.player, [...runtime.messages, message]);
}
