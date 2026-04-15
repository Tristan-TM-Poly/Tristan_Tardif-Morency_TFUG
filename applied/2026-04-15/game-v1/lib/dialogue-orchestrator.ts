import { AgentMessage } from './message-protocol';

export type DialogueTurn = {
  speakerId: string;
  text: string;
  tone: 'neutral' | 'guiding' | 'critical' | 'visionary';
  linkedMissionIds?: string[];
  linkedNodeIds?: string[];
};

export type DialogueScene = {
  id: string;
  title: string;
  turns: DialogueTurn[];
  recommendedNextAction: string;
};

export function buildDialogueScene(id: string, title: string, messages: AgentMessage[]): DialogueScene {
  const turns: DialogueTurn[] = messages.map((message) => ({
    speakerId: message.fromId,
    text: message.content,
    tone:
      message.payloadType === 'warning'
        ? 'critical'
        : message.payloadType === 'review'
          ? 'critical'
          : message.payloadType === 'hint'
            ? 'guiding'
            : message.payloadType === 'hypothesis'
              ? 'visionary'
              : 'neutral',
    linkedMissionIds: message.linkedMissionIds,
    linkedNodeIds: message.linkedNodeIds,
  }));

  const recommendedNextAction = messages.some((m) => m.payloadType === 'warning' || m.payloadType === 'review')
    ? 'strengthen evidence before promotion'
    : messages.some((m) => m.payloadType === 'hypothesis')
      ? 'compare and submit bounded hypothesis'
      : 'inspect linked artifacts and continue inquiry';

  return { id, title, turns, recommendedNextAction };
}
