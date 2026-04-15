import React from 'react';
import { ActionCard, Society } from './HistoricalSocietiesExplorerPanel';

export type SocietyReviewGateProps = {
  society: Society;
  actionCards: ActionCard[];
};

export default function SocietyReviewGate({ society, actionCards }: SocietyReviewGateProps) {
  const establishedCount = actionCards.filter((card) => card.confidence_label === 'established').length;
  const constructiveCount = actionCards.filter((card) => card.action_type === 'constructive').length;
  const harmfulCount = actionCards.filter((card) => card.action_type === 'harmful').length;
  const verdict = establishedCount >= 2 ? 'open for disciplined public summary' : 'needs more evidence before strong public framing';

  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold">Society Review Gate</h2>
      <p className="mt-2 text-sm text-slate-700">Society: {society.label}</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <Metric label="Established Cards" value={String(establishedCount)} />
        <Metric label="Constructive" value={String(constructiveCount)} />
        <Metric label="Harmful" value={String(harmfulCount)} />
      </div>
      <div className="mt-4 rounded-xl border p-3 bg-slate-50">
        <p className="text-sm text-slate-700">Verdict: {verdict}</p>
        <p className="mt-2 text-sm text-slate-700">Rule: a public conclusion must preserve evidence level, contradiction, and tradeoff visibility.</p>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border p-3">
      <div className="text-sm text-slate-500">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}
