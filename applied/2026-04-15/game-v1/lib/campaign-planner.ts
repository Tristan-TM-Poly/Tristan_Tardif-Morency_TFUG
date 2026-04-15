import { LoreFragment } from './lore-composer';

export type CampaignChapter = {
  id: string;
  title: string;
  objective: string;
  loreTitles: string[];
};

export function planCampaignFromLore(fragments: LoreFragment[]): CampaignChapter[] {
  const selected = [...fragments].sort((a, b) => b.score - a.score).slice(0, 5);
  return selected.map((fragment, index) => ({
    id: `chapter-${index + 1}`,
    title: fragment.title,
    objective: `Investigate and stabilize the branch ${fragment.title}.`,
    loreTitles: [fragment.title],
  }));
}
