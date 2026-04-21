import matrixData from '../data/civilization-connection-matrix-v1.json';

type Rail = 'real-history' | 'hypothesis-review' | 'simulation-lore';

type Explanation = {
  title: string;
  summary: string;
  dominantEdges: Array<{ from: string; to: string; value: number }>;
  warnings: string[];
  opportunities: string[];
};

const labels = matrixData.labels as Record<string, string>;
const variables = matrixData.variables;

function strongestEdges(rail: Rail, threshold = 0.14) {
  const matrix = matrixData.rails[rail].matrix;
  const edges: Array<{ from: string; to: string; value: number }> = [];
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      const value = matrix[i][j];
      if (i !== j && Math.abs(value) >= threshold) {
        edges.push({ from: variables[j], to: variables[i], value });
      }
    }
  }
  return edges.sort((a, b) => Math.abs(b.value) - Math.abs(a.value));
}

export function explainCivilizationGraph(rail: Rail): Explanation {
  const edges = strongestEdges(rail);
  const warnings: string[] = [];
  const opportunities: string[] = [];

  const hasTechEcologyRisk = edges.some((e) => e.from === 'T' && e.to === 'E' && e.value < 0);
  const hasMemoryKnowledgeLoop = edges.some((e) => e.from === 'M' && e.to === 'K' && e.value > 0) && edges.some((e) => e.from === 'K' && e.to === 'M' && e.value > 0);
  const hasPressureGovernanceDamage = edges.some((e) => e.from === 'P' && e.to === 'G' && e.value < 0);
  const hasInclusionPressureRelief = edges.some((e) => e.from === 'I' && e.to === 'P' && e.value < 0);
  const hasEcologyPressureRelief = edges.some((e) => e.from === 'E' && e.to === 'P' && e.value < 0);

  if (hasTechEcologyRisk) warnings.push('Technical expansion can undermine ecological stability if not governed carefully.');
  if (hasPressureGovernanceDamage) warnings.push('Collapse pressure directly degrades governance quality, which can trigger destabilizing cascades.');
  if (hasMemoryKnowledgeLoop) opportunities.push('Knowledge and memory form a reinforcing stabilizing loop that supports long-range civilizational resilience.');
  if (hasInclusionPressureRelief) opportunities.push('Inclusion reduces collapse pressure and should be treated as a structural stabilizer, not a decorative value.');
  if (hasEcologyPressureRelief) opportunities.push('Ecological stability lowers collapse pressure and protects long-term flourishing.');

  const title = rail === 'real-history'
    ? 'AI Explainer: disciplined historical reading'
    : rail === 'hypothesis-review'
      ? 'AI Explainer: hypothesis tension map'
      : 'AI Explainer: simulation reading';

  const summary = `In the ${rail} rail, the graph suggests that civilizational trajectories depend strongly on how governance, memory, knowledge, inclusion, and ecology interact under pressure. The explainer highlights dominant stabilizing loops and destabilizing tradeoffs rather than pretending every link is equally important.`;

  return {
    title,
    summary,
    dominantEdges: edges.slice(0, 8).map((edge) => ({
      ...edge,
      from: labels[edge.from] ?? edge.from,
      to: labels[edge.to] ?? edge.to,
    })),
    warnings,
    opportunities,
  };
}
