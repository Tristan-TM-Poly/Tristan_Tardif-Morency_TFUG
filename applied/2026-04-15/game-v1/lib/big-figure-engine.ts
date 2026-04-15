import { AgentMessage, createAgentMessage } from './message-protocol';

export type BigFigure = {
  id: string;
  name: string;
  domain: string;
  method: string;
  proofStyle: string;
  modelingPower: number;
  representationMode: string;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
  linkedTripletIds: string[];
};

export function generateBigFigureMethodMessage(figure: BigFigure, missionId: string): AgentMessage {
  return createAgentMessage({
    fromId: figure.id,
    toId: missionId,
    channel: 'aibot',
    payloadType: 'hint',
    confidence: Math.min(0.98, 0.55 + figure.modelingPower * 0.4),
    speculativeCost: 0.18,
    content: `${figure.name} recommends the method ${figure.method} with proof style ${figure.proofStyle}.`,
    linkedMissionIds: [missionId],
    linkedNodeIds: figure.linkedNodeIds,
  });
}

export function generateBigFigureModelingMessage(figure: BigFigure, missionId: string): AgentMessage {
  return createAgentMessage({
    fromId: figure.id,
    toId: missionId,
    channel: 'aibot',
    payloadType: 'hypothesis',
    confidence: Math.min(0.98, 0.5 + figure.modelingPower * 0.45),
    speculativeCost: 0.24,
    content: `${figure.name} proposes a bounded model using ${figure.representationMode}.`,
    linkedMissionIds: [missionId],
    linkedNodeIds: figure.linkedNodeIds,
  });
}
