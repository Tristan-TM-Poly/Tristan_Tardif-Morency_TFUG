import { AgentMessage, createAgentMessage, isHighRiskMessage } from './message-protocol';

export type AIBot = {
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

export function generateBotHypothesis(bot: AIBot, missionId: string, artifactIds: string[]): AgentMessage {
  const content = `${bot.name} proposes a bounded hypothesis for ${missionId} using ${artifactIds.length} linked artifacts.`;
  return createAgentMessage({
    fromId: bot.id,
    toId: missionId,
    channel: 'aibot',
    payloadType: 'hypothesis',
    confidence: Math.min(0.95, 0.45 + bot.scoreWeight * 0.4),
    speculativeCost: bot.domain === 'review' ? 0.1 : 0.4,
    content,
    linkedArtifactIds: artifactIds,
    linkedMissionIds: [missionId]
  });
}

export function shouldEscalateToReview(message: AgentMessage): boolean {
  return message.payloadType === 'hypothesis' || isHighRiskMessage(message);
}
