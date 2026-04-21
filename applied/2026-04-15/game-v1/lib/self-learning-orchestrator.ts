import orchestrationData from '../data/meta-orchestration-sample.json';

export type CommandScoreMap = Record<string, number>;
export type BotPreferenceMap = Record<string, Record<string, number>>;

export type ExecutionFeedback = {
  object_id: string;
  command: string;
  bot_id: string;
  success: boolean;
  latency_ms: number;
  review_delta: number;
  gate_delta: number;
};

export type LearningState = {
  commandScores: CommandScoreMap;
  botPreferences: BotPreferenceMap;
  historyCount: number;
};

const DEFAULT_COMMAND_SCORE = 0.5;

export function buildInitialLearningState(commands: string[], botIds: string[]): LearningState {
  const commandScores: CommandScoreMap = {};
  for (const command of commands) commandScores[command] = DEFAULT_COMMAND_SCORE;

  const botPreferences: BotPreferenceMap = {};
  for (const botId of botIds) {
    botPreferences[botId] = {};
    for (const command of commands) botPreferences[botId][command] = DEFAULT_COMMAND_SCORE;
  }

  return { commandScores, botPreferences, historyCount: 0 };
}

export function updateLearningState(state: LearningState, feedbackBatch: ExecutionFeedback[]): LearningState {
  const next: LearningState = JSON.parse(JSON.stringify(state));

  for (const feedback of feedbackBatch) {
    const successBoost = feedback.success ? 0.08 : -0.10;
    const latencyPenalty = Math.min(feedback.latency_ms / 10000, 0.08);
    const reviewBoost = 0.06 * feedback.review_delta;
    const gateBoost = 0.06 * feedback.gate_delta;
    const delta = successBoost - latencyPenalty + reviewBoost + gateBoost;

    next.commandScores[feedback.command] = clamp01((next.commandScores[feedback.command] ?? DEFAULT_COMMAND_SCORE) + delta);

    if (!next.botPreferences[feedback.bot_id]) next.botPreferences[feedback.bot_id] = {};
    next.botPreferences[feedback.bot_id][feedback.command] = clamp01(
      (next.botPreferences[feedback.bot_id][feedback.command] ?? DEFAULT_COMMAND_SCORE) + delta
    );
  }

  next.historyCount += feedbackBatch.length;
  return next;
}

export function suggestAdaptiveCommand(row: typeof orchestrationData.rows[number], state: LearningState) {
  const candidates = ['INGEST', 'REVIEW', 'RUN_PILOT', 'PROMOTE', 'DOWNGRADE', 'SYNC'];
  const scored = candidates.map((command) => ({
    command,
    score: computeAdaptiveScore(row, command, state),
  }));

  scored.sort((a, b) => b.score - a.score);
  return scored[0];
}

function computeAdaptiveScore(row: typeof orchestrationData.rows[number], command: string, state: LearningState) {
  let score = state.commandScores[command] ?? DEFAULT_COMMAND_SCORE;

  if (row.status === 'queued' && command === 'RUN_PILOT') score += 0.22;
  if (row.review_status === 'open' && command === 'REVIEW') score += 0.18;
  if (row.gate_status === 'passed' && command === 'PROMOTE') score += 0.25;
  if (row.gate_status === 'open' && command === 'SYNC') score += 0.04;
  if (row.review_status === 'prepared' && command === 'RUN_PILOT') score += 0.12;
  if (row.status === 'ready' && command === 'SYNC') score += 0.08;

  return clamp01(score);
}

function clamp01(x: number) {
  return Math.max(0, Math.min(1, x));
}
