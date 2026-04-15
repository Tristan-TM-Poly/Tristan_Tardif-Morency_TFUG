import React from 'react';
import { ActionCard, Society } from './HistoricalSocietiesExplorerPanel';

export type PublicSummaryCardProps = {
  society: Society;
  actionCards: ActionCard[];
};

export default function PublicSummaryCard({ society, actionCards }: PublicSummaryCardProps) {
  const established = actionCards.filter((card) => card.confidence_label === 'established');
  const constructive = actionCards.filter((card) => card.action_type === 'constructive');
  const harmful = actionCards.filter((card) => card.action_type === 'harmful');

  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold">Public Summary Card</h2>
      <p className="mt-2 text-sm text-slate-700">{society.label} should be presented as a society with both constructive capacities and harmful contradictions, not as a single moral block.</p>
      <div className="mt-4 rounded-xl border p-3 bg-slate-50">
        <h3 className="font-medium">Established points to keep visible</h3>
        <ul className="mt-2 space-y-1 text-sm text-slate-700 list-disc pl-5">
          {established.slice(0, 3).map((card) => (
            <li key={card.id}>{card.title}</li>
          ))}
          {!established.length && <li>No established points available yet.</li>}
        </ul>
      </div>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <SummaryBlock title="Constructive side" items={constructive} />
        <SummaryBlock title="Harmful side" items={harmful} />
      </div>
    </section>
  );
}

function SummaryBlock({ title, items }: { title: string; items: ActionCard[] }) {
  return (
    <div className="rounded-xl border p-3">
      <h3 className="font-medium">{title}</h3>
      <ul className="mt-2 space-y-1 text-sm text-slate-700 list-disc pl-5">
        {items.slice(0, 3).map((item) => (
          <li key={item.id}>{item.title}</li>
        ))}
        {!items.length && <li>No items available.</li>}
      </ul>
    </div>
  );
}
