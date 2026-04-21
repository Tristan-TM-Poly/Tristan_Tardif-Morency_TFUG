import bots from '../data/ai-bots-manifest.json';
import orchestrationData from '../data/meta-orchestration-sample.json';
import { executeCommand } from './meta-orchestrator-runtime';

export function runAutoLoop() {
  const results: any[] = [];

  for (const row of orchestrationData.rows) {
    const bot = bots.bots.find((b) => b.commands.includes('RUN_PILOT')) || bots.bots[0];
    const command = bot.commands[0];

    const execution = executeCommand(row as any, command);

    results.push({
      bot: bot.id,
      object: row.object_id,
      command,
      result: execution,
    });
  }

  return results;
}
