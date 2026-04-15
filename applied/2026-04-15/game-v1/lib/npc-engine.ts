import { AgentMessage, createAgentMessage } from './message-protocol';

export type NPC = {
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

export function canTalkToNPC(npc: NPC, completedMissionIds: string[]): boolean {
  if (!npc.unlockedByMissionIds.length) return true;
  return npc.unlockedByMissionIds.some((id) => completedMissionIds.includes(id));
}

export function generateNPCHint(npc: NPC, missionId: string): AgentMessage {
  let content = 'Bounded clue available.';
  if (npc.role === 'review') content = 'Review first. Stronger evidence is needed.';
  if (npc.role === 'system') content = 'Inspect linked mechanisms before proposing a function.';
  if (npc.role === 'concept') content = 'Compare symbolic and structural clues before escalating.';

  return createAgentMessage({
    fromId: npc.id,
    toId: missionId,
    channel: 'pnj',
    payloadType: 'hint',
    confidence: npc.trustLevel,
    speculativeCost: npc.role === 'review' ? 0.15 : 0.35,
    content,
    linkedMissionIds: [missionId]
  });
}

export function adjustNPCTrust(current: number, delta: number): number {
  const next = current + delta;
  if (next < 0) return 0;
  if (next > 1) return 1;
  return next;
}
