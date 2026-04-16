import React, { useState } from 'react';
import { CivilizationState } from '../lib/civilization-engine';
import { simulateV2 } from '../lib/civilization-engine-v2';

export default function CivilizationGameplayLoop() {
  const [state] = useState<CivilizationState>({
    G: 0.6,
    K: 0.7,
    T: 0.6,
    M: 0.7,
    I: 0.5,
    E: 0.6,
    P: 0.5,
  });

  const history = simulateV2(state, 6, [
    { type: 'climate', intensity: 0.6 },
    { type: 'war', intensity: 0.4 },
    { type: 'breakthrough', intensity: 0.5 },
  ]);

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <h2 className="text-xl font-semibold">Civilization Gameplay Loop</h2>

      <p className="text-sm text-slate-700">
        Experience shocks, adaptation, and long-term consequences.
      </p>

      <div className="rounded-xl border p-3">
        <h3 className="font-medium">Simulation Timeline</h3>
        <ul className="text-sm mt-2 space-y-1">
          {history.map((h) => (
            <li key={h.step}>
              Step {h.step} → G:{h.state.G.toFixed(2)} K:{h.state.K.toFixed(2)} T:{h.state.T.toFixed(2)} P:{h.state.P.toFixed(2)}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
