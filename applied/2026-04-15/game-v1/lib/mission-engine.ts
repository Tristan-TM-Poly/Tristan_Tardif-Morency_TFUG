export type Mission = {
  id: string;
  title: string;
  zoneId: string;
  objective: string;
  requiredArtifacts: string[];
  requiredNPCs: string[];
  requiredNodes: string[];
  successCondition: string;
  rewardNodeIds: string[];
  reviewGateId: string;
};

export type PlayerProgression = {
  playerLevel: number;
  unlockedZones: string[];
  discoveredArtifacts: string[];
  unlockedNodes: string[];
  activeMissionId: string | null;
  completedMissionIds: string[];
  npcTrust: Record<string, number>;
  hypothesisScore: number;
  reviewStatus: 'open' | 'passed' | 'blocked';
};

export function canStartMission(mission: Mission, state: PlayerProgression): boolean {
  return state.unlockedZones.includes(mission.zoneId) && !state.completedMissionIds.includes(mission.id);
}

export function missionCompletionProgress(mission: Mission, state: PlayerProgression): number {
  const artifactHits = mission.requiredArtifacts.filter((id) => state.discoveredArtifacts.includes(id)).length;
  const nodeHits = mission.requiredNodes.filter((id) => state.unlockedNodes.includes(id)).length;
  const artifactRatio = mission.requiredArtifacts.length ? artifactHits / mission.requiredArtifacts.length : 1;
  const nodeRatio = mission.requiredNodes.length ? nodeHits / mission.requiredNodes.length : 1;
  return (artifactRatio + nodeRatio) / 2;
}

export function applyMissionRewards(mission: Mission, state: PlayerProgression): PlayerProgression {
  return {
    ...state,
    unlockedNodes: Array.from(new Set([...state.unlockedNodes, ...mission.rewardNodeIds])),
    completedMissionIds: Array.from(new Set([...state.completedMissionIds, mission.id])),
    activeMissionId: state.activeMissionId === mission.id ? null : state.activeMissionId,
  };
}
