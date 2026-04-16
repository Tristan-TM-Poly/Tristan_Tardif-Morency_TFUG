import React, { useState } from 'react';
import matrixData from '../data/civilization-connection-matrix-v1.json';

export default function CivilizationMatrixPanel() {
  const [rail, setRail] = useState<'real-history' | 'hypothesis-review' | 'simulation-lore'>('real-history');

  const matrix = matrixData.rails[rail].matrix;
  const variables = matrixData.variables;

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <h2 className="text-xl font-semibold">Civilization Connection Matrix</h2>

      <select value={rail} onChange={(e) => setRail(e.target.value as any)} className="border p-2">
        <option value="real-history">Real History</option>
        <option value="hypothesis-review">Hypothesis</option>
        <option value="simulation-lore">Simulation</option>
      </select>

      <div className="overflow-auto">
        <table className="text-xs border-collapse">
          <thead>
            <tr>
              <th></th>
              {variables.map((v) => (
                <th key={v} className="border px-2">{v}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                <th className="border px-2">{variables[i]}</th>
                {row.map((val, j) => (
                  <td key={j} className="border px-2">
                    {val.toFixed(2)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-sm text-slate-700">
        This matrix shows how each variable influences others. Values change depending on epistemic rail.
      </p>
    </section>
  );
}
