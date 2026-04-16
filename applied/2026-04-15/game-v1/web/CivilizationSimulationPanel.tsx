import React, { useState } from 'react';
import { CivilizationState, evaluateCivilization, simulateCivilization } from '../lib/civilization-engine';

export default function CivilizationSimulationPanel() {
  const [state, setState] = useState<CivilizationState>({
    G: 0.6,
    K: 0.7,
    T: 0.6,
    M: 0.7,
    I: 0.5,
    E: 0.6,
    P: 0.5,
  });

  const evaluation = evaluateCivilization(state);
  const history = simulateCivilization(state, 5);

  function update(key: keyof CivilizationState, value: number) {
    setState({ ...state, [key]: value });
  }

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <h2 className="text-xl font-semibold">Civilization Simulation Panel</h2>

      <div className="grid grid-cols-2 gap-4">
        {Object.entries(state).map(([key, value]) => (
          <div key={key}>
            <label className="text-sm">{key}: {value.toFixed(2)}</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={value}
              onChange={(e) => update(key as keyof CivilizationState, parseFloat(e.target.value))}
              className="w-full"
            />
          </div>
        ))}
      </div>

      <div className="rounded-xl border p-3 bg-slate-50">
        <p>Resilience: {evaluation.resilience.toFixed(2)}</p>
        <p>Flourishing: {evaluation.flourishing.toFixed(2)}</p>
        <p>Collapse Risk: {evaluation.collapseRisk.toFixed(2)}</p>
        <p className="mt-2 text-sm">{evaluation.recommendation}</p>
      </div>

      <div className="rounded-xl border p-3">
        <h3 className="font-medium">Simulation (5 steps)</h3>
        <ul className="text-sm mt-2 space-y-1">
          {history.map((h) => (
            <li key={h.step}>
              Step {h.step}: R={h.resilience.toFixed(2)}, F={h.flourishing.toFixed(2)}, C={h.collapseRisk.toFixed(2)}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
