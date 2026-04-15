import { AgentMessage } from './message-protocol';
import { scoreGate } from './scoring';

export type GreatReviewResult = {
  evidence: number;
  coherence: number;
  bridgeDensity: number;
  speculativeCost: number;
  score: number;
  verdict: 'passed' | 'open' | 'blocked';
};

export function runGreatReview(messages: AgentMessage[]): GreatReviewResult {
  const evidence = Math.min(1, messages.filter((m) => m.payloadType === 'fact' || m.payloadType === 'artifact-link').length / 6);
  const coherence = Math.min(1, messages.filter((m) => m.payloadType === 'hint' || m.payloadType === 'review').length / 6);
  const bridgeDensity = Math.min(1, messages.reduce((acc, m) => acc + (m.linkedNodeIds?.length ?? 0), 0) / 12);
  const speculativeCost = Math.min(1, messages.reduce((acc, m) => acc + m.speculativeCost, 0) / Math.max(1, messages.length));
  const score = scoreGate({ evidence, coherence, bridgeDensity, speculativeCost });
  const verdict = score >= 0.75 ? 'passed' : score >= 0.55 ? 'open' : 'blocked';
  return { evidence, coherence, bridgeDensity, speculativeCost, score, verdict };
}
