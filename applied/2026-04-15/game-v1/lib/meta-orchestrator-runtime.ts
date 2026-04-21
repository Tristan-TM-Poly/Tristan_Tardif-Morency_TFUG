import orchestrationData from '../data/meta-orchestration-sample.json';

export type OrchestrationRow = typeof orchestrationData.rows[number];

export function routeRow(row: OrchestrationRow) {
  return {
    ...row,
    routed: true,
    timestamp: Date.now(),
  };
}

export function executeCommand(row: OrchestrationRow, command: string) {
  return {
    object_id: row.object_id,
    command,
    status: 'executed',
    next_state: computeNextState(row, command),
  };
}

function computeNextState(row: OrchestrationRow, command: string) {
  switch (command) {
    case 'RUN_PILOT':
      return 'running';
    case 'REVIEW':
      return 'under_review';
    case 'PROMOTE':
      return 'promoted';
    case 'DOWNGRADE':
      return 'downgraded';
    default:
      return row.status;
  }
}

export function dispatchAll() {
  return orchestrationData.rows.map((row) => routeRow(row));
}
