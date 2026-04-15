import React, { useMemo, useState } from 'react';

export type Society = {
  id: string;
  label: string;
  time_range: string;
  summary: string;
  visible_layer: string;
};

export type ActionCard = {
  id: string;
  society_id: string;
  domain: string;
  title: string;
  action_type: 'constructive' | 'harmful';
  short_term_effect: string;
  long_term_effect: string;
  confidence_label: string;
};

export type HistoricalSocietiesExplorerPanelProps = {
  societies: Society[];
  actionCards: ActionCard[];
};

export default function HistoricalSocietiesExplorerPanel({ societies, actionCards }: HistoricalSocietiesExplorerPanelProps) {
  const [selectedSocietyId, setSelectedSocietyId] = useState(societies[0]?.id ?? '');

  const selectedSociety = useMemo(
    () => societies.find((society) => society.id === selectedSocietyId) ?? societies[0],
    [selectedSocietyId, societies]
  );

  const visibleCards = useMemo(
    () => actionCards.filter((card) => card.society_id === selectedSociety?.id),
    [actionCards, selectedSociety]
  );

  const constructive = visibleCards.filter((card) => card.action_type === 'constructive');
  const harmful = visibleCards.filter((card) => card.action_type === 'harmful');

  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-xl font-semibold">Historical Societies Explorer</h2>
          <p className="mt-1 text-sm text-slate-700">Explore actions, institutions, consequences, and tradeoffs without flattening a society into a single moral label.</p>
        </div>
        <label className="text-sm">
          <span className="mb-1 block text-slate-600">Society</span>
          <select
            value={selectedSociety?.id}
            onChange={(event) => setSelectedSocietyId(event.target.value)}
            className="rounded-lg border px-3 py-2"
          >
            {societies.map((society) => (
              <option key={society.id} value={society.id}>
                {society.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {selectedSociety && (
        <div className="mt-4 rounded-xl border p-4">
          <h3 className="text-lg font-medium">{selectedSociety.label}</h3>
          <p className="mt-1 text-sm text-slate-600">{selectedSociety.time_range}</p>
          <p className="mt-2 text-sm text-slate-700">{selectedSociety.summary}</p>
          <p className="mt-2 text-xs text-slate-500">Layer: {selectedSociety.visible_layer}</p>
        </div>
      )}

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <CardColumn title="Constructive Actions" cards={constructive} />
        <CardColumn title="Harmful or Exclusionary Actions" cards={harmful} />
      </div>

      <div className="mt-6 rounded-xl border p-4 bg-slate-50">
        <h3 className="font-medium">Public Summary Rule</h3>
        <p className="mt-2 text-sm text-slate-700">State what is established, what remains under review, and what moral tradeoff or contradiction must remain visible.</p>
      </div>
    </section>
  );
}

function CardColumn({ title, cards }: { title: string; cards: ActionCard[] }) {
  return (
    <div className="rounded-xl border p-4">
      <h3 className="font-medium">{title}</h3>
      <div className="mt-3 space-y-3">
        {cards.map((card) => (
          <article key={card.id} className="rounded-xl border p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h4 className="font-medium">{card.title}</h4>
                <p className="mt-1 text-xs text-slate-500">{card.domain}</p>
              </div>
              <span className="text-xs rounded-full border px-2 py-1">{card.confidence_label}</span>
            </div>
            <p className="mt-2 text-sm text-slate-700">Short term: {card.short_term_effect}</p>
            <p className="mt-1 text-sm text-slate-700">Long term: {card.long_term_effect}</p>
          </article>
        ))}
        {!cards.length && <p className="text-sm text-slate-500">No cards available.</p>}
      </div>
    </div>
  );
}
