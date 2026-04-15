import React from 'react';
import { PyramidEvaluation } from '../lib/pyramid-engine';

export type PyramidDashboardProps = {
  evaluation: PyramidEvaluation;
};

export default function PyramidDashboard({ evaluation }: PyramidDashboardProps) {
  const rows = [
    ['Structural Integrity', evaluation.structuralIntegrity],
    ['Thermal Stability', evaluation.thermalStability],
    ['Water Stability', evaluation.waterStability],
    ['Light Alignment', evaluation.lightAlignment],
    ['Memory Capacity', evaluation.memoryCapacity],
    ['Governance Clarity', evaluation.governanceClarity],
    ['System Score', evaluation.systemScore],
  ];

  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold mb-3">Pyramid Dashboard</h2>
      <div className="space-y-2">
        {rows.map(([label, value]) => (
          <div key={label} className="grid grid-cols-[180px_1fr_60px] items-center gap-3">
            <span className="text-sm">{label}</span>
            <div className="h-2 rounded-full bg-slate-200 overflow-hidden">
              <div className="h-full bg-slate-700" style={{ width: `${Number(value) * 100}%` }} />
            </div>
            <span className="text-sm text-right">{Number(value).toFixed(2)}</span>
          </div>
        ))}
      </div>
      <p className="mt-4 text-sm text-slate-700">Recommendation: {evaluation.recommendation}</p>
    </section>
  );
}
