export type RosettaInput = {
  source: string;
  transliteration?: string;
  translations: string[];
  symbols?: string[];
};

export type RosettaOutput = {
  invariants: string[];
  ambiguities: string[];
  stabilityScore: number;
};

function normalize(text: string): string[] {
  return text.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(Boolean);
}

export function alignRosetta(input: RosettaInput): RosettaOutput {
  const tokenLists = [input.source, input.transliteration ?? '', ...input.translations]
    .filter(Boolean)
    .map(normalize);

  if (!tokenLists.length) {
    return { invariants: [], ambiguities: [], stabilityScore: 0 };
  }

  const counts = new Map<string, number>();
  for (const list of tokenLists) {
    const unique = new Set(list);
    for (const token of unique) {
      counts.set(token, (counts.get(token) ?? 0) + 1);
    }
  }

  const threshold = Math.max(2, Math.ceil(tokenLists.length * 0.6));
  const invariants = [...counts.entries()].filter(([, n]) => n >= threshold).map(([t]) => t);
  const ambiguities = [...counts.entries()].filter(([, n]) => n > 0 && n < threshold).map(([t]) => t).slice(0, 20);
  const stabilityScore = invariants.length / Math.max(1, invariants.length + ambiguities.length);

  return { invariants, ambiguities, stabilityScore };
}
