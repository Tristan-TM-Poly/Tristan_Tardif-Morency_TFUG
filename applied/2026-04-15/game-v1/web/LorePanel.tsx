import React from 'react';

export type LoreFragment = {
  title: string;
  summary: string;
  tags: string[];
  score: number;
};

export type LorePanelProps = {
  fragments: LoreFragment[];
};

export default function LorePanel({ fragments }: LorePanelProps) {
  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold mb-3">Lore Fragments</h2>
      <div className="space-y-3">
        {fragments.map((fragment) => (
          <article key={fragment.title} className="rounded-xl border p-3">
            <div className="flex items-start justify-between gap-3">
              <h3 className="font-medium">{fragment.title}</h3>
              <span className="text-sm">{fragment.score.toFixed(2)}</span>
            </div>
            <p className="mt-2 text-sm text-slate-700">{fragment.summary}</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {fragment.tags.map((tag) => (
                <span key={tag} className="rounded-full border px-2 py-1 text-xs text-slate-700">{tag}</span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
