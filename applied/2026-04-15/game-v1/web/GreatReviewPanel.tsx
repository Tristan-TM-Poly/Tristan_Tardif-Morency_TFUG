import React from 'react';
import { GreatReviewResult } from '../lib/great-review-engine';

export type GreatReviewPanelProps = {
  result: GreatReviewResult;
};

export default function GreatReviewPanel({ result }: GreatReviewPanelProps) {
  const rows = [
    ['Evidence', result.evidence],
    ['Coherence', result.coherence],
    ['Bridge Density', result.bridgeDensity],
    ['Speculative Cost', result.speculativeCost],
    ['Score', result.score],
  ];

  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold mb-3">Great Review</h2>
      <div className="space-y-2">
        {rows.map(([label, value]) => (
          <div key={label} className="grid grid-cols-[160px_1fr_60px] items-center gap-3">
            <span className="text-sm">{label}</span>
            <div className="h-2 rounded-full bg-slate-200 overflow-hidden">
              <div className="h-full bg-slate-800" style={{ width: `${Number(value) * 100}%` }} />
            </div>
            <span className="text-sm text-right">{Number(value).toFixed(2)}</span>
          </div>
        ))}
      </div>
      <p className="mt-4 text-sm text-slate-700">Verdict: {result.verdict}</p>
    </section>
  );
}
