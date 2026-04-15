export type AgentChannel = 'pnj' | 'aibot' | 'triplet';

export type AgentPayloadType =
  | 'fact'
  | 'hint'
  | 'hypothesis'
  | 'review'
  | 'warning'
  | 'artifact-link'
  | 'unlock'
  | 'contradiction';

export type AgentMessage = {
  id: string;
  fromId: string;
  toId: string;
  channel: AgentChannel;
  payloadType: AgentPayloadType;
  confidence: number;
  speculativeCost: number;
  content: string;
  linkedArtifactIds?: string[];
  linkedNodeIds?: string[];
  linkedMissionIds?: string[];
  timestamp: number;
};

export function createAgentMessage(input: Omit<AgentMessage, 'id' | 'timestamp'> & { id?: string; timestamp?: number }): AgentMessage {
  return {
    ...input,
    id: input.id ?? `msg-${Math.random().toString(36).slice(2, 10)}`,
    timestamp: input.timestamp ?? Date.now(),
  };
}

export function isHighRiskMessage(message: AgentMessage): boolean {
  return message.speculativeCost >= 0.7 && message.confidence < 0.6;
}
