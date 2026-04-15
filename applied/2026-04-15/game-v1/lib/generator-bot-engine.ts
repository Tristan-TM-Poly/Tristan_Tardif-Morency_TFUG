import { AgentMessage, createAgentMessage } from './message-protocol';

export type GeneratorBot = {
  id: string;
  name: string;
  generatorType: string;
  domain: string;
  outputKinds: string[];
  creativityWeight: number;
  coherenceBias: number;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
  linkedTripletIds: string[];
};

export type GeneratedSeed = {
  id: string;
  sourceBotId: string;
  kind: string;
  title: string;
  coherence: number;
  creativity: number;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
};

export function generateSeed(bot: GeneratorBot, missionId: string, index: number): GeneratedSeed {
  return {
    id: `${bot.id}-seed-${index}`,
    sourceBotId: bot.id,
    kind: bot.outputKinds[index % bot.outputKinds.length] ?? 'seed',
    title: `${bot.name} seed ${index}`,
    coherence: Math.min(0.99, bot.coherenceBias),
    creativity: Math.min(0.99, bot.creativityWeight),
    linkedMissionIds: [missionId],
    linkedNodeIds: bot.linkedNodeIds,
  };
}

export function generateGeneratorMessage(bot: GeneratorBot, missionId: string, index: number): AgentMessage {
  const seed = generateSeed(bot, missionId, index);
  return createAgentMessage({
    fromId: bot.id,
    toId: missionId,
    channel: 'aibot',
    payloadType: 'hypothesis',
    confidence: Math.min(0.97, 0.45 + 0.3 * bot.coherenceBias),
    speculativeCost: Math.max(0.05, 0.45 - 0.2 * bot.coherenceBias),
    content: `${bot.name} generates ${seed.kind} titled ${seed.title}.`,
    linkedMissionIds: seed.linkedMissionIds,
    linkedNodeIds: seed.linkedNodeIds,
  });
}
