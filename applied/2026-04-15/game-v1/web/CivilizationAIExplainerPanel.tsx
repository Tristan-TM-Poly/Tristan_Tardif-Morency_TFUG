import React, { useState } from 'react';
import { explainCivilizationGraph } from '../lib/civilization-ai-explainer';

type Rail = 'real-history' | 'hypothesis-review' | 'simulation-lore';

export default function CivilizationAIExplainerPanel() {
  const [rail, setRail] = useState<Rail>('real-history');

  const explanation = explainCivilizationGraph(rail);

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-xl font-semibold">AI Causal Explainer</h2>
          <p className="text-sm text-slate-700">Interpretation layer for the civilization graph.</p>
        </div>

        <select value={rail} onChange={(e) => setRail(e.target.value as Rail)} className="border p-2">
          <option value="real-history">Real History</option>
          <option value="hypothesis-review">Hypothesis</option>
          <option value="simulation-lore">Simulation</option>
        </select>
      </div>

      <div className="rounded-xl border p-3 bg-slate-50">
        <h3 className="font-medium">{explanation.title}</h3>
        <p className="mt-2 text-sm text-slate-700">{explanation.summary}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="rounded-xl border p-3">
          <h3 className="font-medium">Warnings</h3>
          <ul className="text-sm mt-2 list-disc pl-5">
            {explanation.warnings.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
            {!explanation.warnings.length && <li>No major warnings detected.</li>}
          </ul>
        </div>

        <div className="rounded-xl border p-3">
          <h3 className="font-medium">Opportunities</h3>
          <ul className="text-sm mt-2 list-disc pl-5">
            {explanation.opportunities.map((o, i) => (
              <li key={i}>{o}</li>
            ))}
            {!explanation.opportunities.length && <li>No major opportunities detected.</li>}
          </ul>
        </div>
      </div>

      <div className="rounded-xl border p-3">
        <h3 className="font-medium">Dominant Connections</h3>
        <ul className="text-sm mt-2 list-disc pl-5">
          {explanation.dominantEdges.map((edge, i) => (
            <li key={i}>
              {edge.from} → {edge.to} ({edge.value.toFixed(2)})
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
