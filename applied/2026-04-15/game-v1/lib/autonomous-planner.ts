import orchestrationData from '../data/meta-orchestration-sample.json';

export function planNextActions() {
  return orchestrationData.rows.map((row) => {
    let nextCommand = 'INGEST';

    if (row.status === 'queued') nextCommand = 'RUN_PILOT';
    if (row.review_status === 'open') nextCommand = 'REVIEW';
    if (row.gate_status === 'passed') nextCommand = 'PROMOTE';

    return {
      object_id: row.object_id,
      suggested_command: nextCommand,
      confidence: computeConfidence(row),
    };
  });
}

function computeConfidence(row: any) {
  let score = 0.5;
  if (row.status === 'ready') score += 0.2;
  if (row.review_status === 'passed') score += 0.2;
  if (row.gate_status === 'passed') score += 0.1;
  return Math.min(score, 1);
}
