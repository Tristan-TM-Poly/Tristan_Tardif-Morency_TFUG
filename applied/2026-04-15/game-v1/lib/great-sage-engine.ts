import { AgentMessage, createAgentMessage } from './message-protocol';

export type GreatSage = {
  id: string;
  name: string;
  vision: string;
  synthesisPower: number;
  governanceWeight: number;
  limitsLens: string;
  questionQuality: number;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
  linkedTripletIds: string[];
};

export function generateGreatSageQuestionMessage(sage: GreatSage, missionId: string): AgentMessage {
  return createAgentMessage({
    fromId: sage.id,
    toId: missionId,
    channel: 'triplet',
    payloadType: 'review',
    confidence: Math.min(0.99, 0.6 + sage.questionQuality * 0.35),
    speculativeCost: 0.12,
    content: `${sage.name} asks whether the current branch honors the vision: ${sage.vision}`,
    linkedMissionIds: [missionId],
    linkedNodeIds: sage.linkedNodeIds,
  });
}

export function generateGreatSageWarningMessage(sage: GreatSage, missionId: string): AgentMessage {
  return createAgentMessage({
    fromId: sage.id,
    toId: missionId,
    channel: 'triplet',
    payloadType: 'warning',
    confidence: Math.min(0.99, 0.55 + sage.governanceWeight * 0.4),
    speculativeCost: 0.08,
    content: `${sage.name} warns about the limits lens: ${sage.limitsLens}`,
    linkedMissionIds: [missionId],
    linkedNodeIds: sage.linkedNodeIds,
  });
}
