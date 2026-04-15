import React from 'react';

export type CampaignChapter = {
  id: string;
  title: string;
  objective: string;
  loreTitles: string[];
};

export type CampaignMapProps = {
  chapters: CampaignChapter[];
};

export default function CampaignMap({ chapters }: CampaignMapProps) {
  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold mb-3">Campaign Map</h2>
      <div className="space-y-3">
        {chapters.map((chapter, index) => (
          <div key={chapter.id} className="rounded-xl border p-3">
            <div className="text-sm text-slate-500">Chapter {index + 1}</div>
            <h3 className="font-medium">{chapter.title}</h3>
            <p className="mt-1 text-sm text-slate-700">{chapter.objective}</p>
            <div className="mt-2 text-xs text-slate-600">Lore: {chapter.loreTitles.join(', ')}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
