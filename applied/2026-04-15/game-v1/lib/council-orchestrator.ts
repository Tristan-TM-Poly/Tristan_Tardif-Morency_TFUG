import { AgentMessage } from './message-protocol';
import { runGreatReview, GreatReviewResult } from './great-review-engine';

export type CouncilAdvice = {
  review: GreatReviewResult;
  dominantVoices: string[];
  recommendation: string;
};

export function buildCouncilAdvice(messages: AgentMessage[]): CouncilAdvice {
  const review = runGreatReview(messages);
  const voiceCount = new Map<string, number>();
  for (const message of messages) {
    voiceCount.set(message.fromId, (voiceCount.get(message.fromId) ?? 0) + 1);
  }
  const dominantVoices = [...voiceCount.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([id]) => id);

  const recommendation =
    review.verdict === 'passed'
      ? 'promote the branch and unlock the next civilizational layer'
      : review.verdict === 'open'
        ? 'collect more evidence and compare competing reconstructions'
        : 'downgrade the branch and reduce speculative inflation';

  return { review, dominantVoices, recommendation };
}
