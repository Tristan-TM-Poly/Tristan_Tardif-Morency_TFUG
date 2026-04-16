import React, { useMemo, useState } from 'react';
import matrixData from '../data/civilization-connection-matrix-v1.json';

type Rail = 'real-history' | 'hypothesis-review' | 'simulation-lore';

type NodePos = { x: number; y: number };

const positions: Record<string, NodePos> = {
  G: { x: 330, y: 70 },
  K: { x: 530, y: 150 },
  T: { x: 560, y: 340 },
  M: { x: 330, y: 430 },
  I: { x: 120, y: 340 },
  E: { x: 90, y: 150 },
  P: { x: 330, y: 250 },
};

function edgeStyle(value: number) {
  const magnitude = Math.abs(value);
  const width = 1 + magnitude * 8;
  const color = value >= 0 ? '#0f766e' : '#b91c1c';
  const opacity = 0.18 + magnitude * 0.82;
  return { width, color, opacity };
}

export default function CivilizationCausalGraph() {
  const [rail, setRail] = useState<Rail>('real-history');
  const [threshold, setThreshold] = useState(0.1);

  const variables = matrixData.variables;
  const labels = matrixData.labels as Record<string, string>;
  const matrix = matrixData.rails[rail].matrix;

  const edges = useMemo(() => {
    const output: Array<{ from: string; to: string; value: number }> = [];
    for (let i = 0; i < matrix.length; i++) {
      for (let j = 0; j < matrix[i].length; j++) {
        const value = matrix[i][j];
        if (i !== j && Math.abs(value) >= threshold) {
          output.push({ from: variables[j], to: variables[i], value });
        }
      }
    }
    return output;
  }, [matrix, threshold, variables]);

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-xl font-semibold">Civilization Causal Graph</h2>
          <p className="mt-1 text-sm text-slate-700">Green edges reinforce, red edges destabilize. Edge thickness tracks connection magnitude. Rail switching changes the epistemic weight of the graph.</p>
        </div>
        <div className="flex gap-3 flex-wrap">
          <label className="text-sm">
            <span className="mb-1 block text-slate-600">Rail</span>
            <select value={rail} onChange={(e) => setRail(e.target.value as Rail)} className="rounded-lg border px-3 py-2">
              <option value="real-history">Real History</option>
              <option value="hypothesis-review">Hypothesis Review</option>
              <option value="simulation-lore">Simulation Lore</option>
            </select>
          </label>
          <label className="text-sm min-w-[180px]">
            <span className="mb-1 block text-slate-600">Edge threshold: {threshold.toFixed(2)}</span>
            <input type="range" min="0.02" max="0.26" step="0.01" value={threshold} onChange={(e) => setThreshold(parseFloat(e.target.value))} className="w-full" />
          </label>
        </div>
      </div>

      <div className="overflow-auto rounded-xl border bg-slate-50">
        <svg viewBox="0 0 650 500" className="w-full h-auto">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#475569" />
            </marker>
          </defs>

          {edges.map((edge) => {
            const from = positions[edge.from];
            const to = positions[edge.to];
            const style = edgeStyle(edge.value);
            return (
              <g key={`${edge.from}-${edge.to}-${rail}`}>
                <line
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke={style.color}
                  strokeWidth={style.width}
                  strokeOpacity={style.opacity}
                  markerEnd="url(#arrowhead)"
                />
                <text
                  x={(from.x + to.x) / 2}
                  y={(from.y + to.y) / 2}
                  fontSize="11"
                  fill="#334155"
                  textAnchor="middle"
                >
                  {edge.value.toFixed(2)}
                </text>
              </g>
            );
          })}

          {variables.map((variable) => {
            const pos = positions[variable];
            return (
              <g key={variable}>
                <circle cx={pos.x} cy={pos.y} r="34" fill="#ffffff" stroke="#334155" strokeWidth="2" />
                <text x={pos.x} y={pos.y - 2} textAnchor="middle" fontSize="16" fontWeight="700" fill="#0f172a">
                  {variable}
                </text>
                <text x={pos.x} y={pos.y + 16} textAnchor="middle" fontSize="10" fill="#475569">
                  {labels[variable]}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="grid gap-4 md:grid-cols-3 text-sm">
        <div className="rounded-xl border p-3">
          <div className="font-medium">Positive edges</div>
          <p className="mt-1 text-slate-700">Reinforcing or stabilizing influences.</p>
        </div>
        <div className="rounded-xl border p-3">
          <div className="font-medium">Negative edges</div>
          <p className="mt-1 text-slate-700">Destabilizing or pressure-increasing influences.</p>
        </div>
        <div className="rounded-xl border p-3">
          <div className="font-medium">Threshold control</div>
          <p className="mt-1 text-slate-700">Filters weak links to reveal dominant causal structure.</p>
        </div>
      </div>
    </section>
  );
}
