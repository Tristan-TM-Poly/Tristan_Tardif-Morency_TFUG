import React from 'react';
import { ActionCard, Society } from './HistoricalSocietiesExplorerPanel';

export type ComparativeCivilizationsMapProps = {
  societies: Society[];
  actionCards: ActionCard[];
};

export default function ComparativeCivilizationsMap({ societies, actionCards }: ComparativeCivilizationsMapProps) {
  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold">Comparative Civilizations Map</h2>
      <p className="mt-2 text-sm text-slate-700">Compare visible strengths, harms, and contradictions across societies without collapsing them into a single ladder of moral worth.</p>
      <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {societies.map((society) => {
          const cards = actionCards.filter((card) => card.society_id === society.id);
          const constructive = cards.filter((card) => card.action_type === 'constructive').length;
          const harmful = cards.filter((card) => card.action_type === 'harmful').length;
          const established = cards.filter((card) => card.confidence_label === 'established').length;

          return (
            <article key={society.id} className="rounded-xl border p-4">
              <h3 className="font-medium">{society.label}</h3>
              <p className="mt-1 text-sm text-slate-600">{society.time_range}</p>
              <p className="mt-2 text-sm text-slate-700">{society.summary}</p>
              <div className="mt-3 grid gap-2 grid-cols-3 text-center">
                <MiniMetric label="Constructive" value={constructive} />
                <MiniMetric label="Harmful" value={harmful} />
                <MiniMetric label="Established" value={established} />
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function MiniMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg border p-2">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}
