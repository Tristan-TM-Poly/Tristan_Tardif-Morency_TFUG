# GameShell Historical Societies Integration v1

## Purpose
Provide the exact integration path for the Historical Societies runtime section inside `web/GameShell.tsx`.

## Existing file
`web/GameShell.tsx`

## New import to add
```ts
import HistoricalSocietiesRuntimeSection from './HistoricalSocietiesRuntimeSection';
```

## Recommended placement
Insert the Historical Societies runtime section after the current Pyramid and Great Review section.

## Exact JSX insertion
```tsx
      <HistoricalSocietiesRuntimeSection />
```

## Resulting high-level section order
1. Header
2. Active Mission / Active Gate
3. Pyramid Dashboard / Great Review Panel
4. Historical Societies Runtime Section

## Reference layout sketch
```tsx
import React from 'react';
import { GameRuntime } from '../lib/game-engine';
import PyramidDashboard from './PyramidDashboard';
import GreatReviewPanel from './GreatReviewPanel';
import HistoricalSocietiesRuntimeSection from './HistoricalSocietiesRuntimeSection';
import { evaluatePyramidSystem } from '../lib/pyramid-engine';
import { runGreatReview } from '../lib/great-review-engine';

export type GameShellProps = {
  runtime: GameRuntime;
};

export default function GameShell({ runtime }: GameShellProps) {
  const pyramid = evaluatePyramidSystem({
    structuralIntegrity: 0.72,
    thermalStability: 0.61,
    waterStability: 0.64,
    lightAlignment: 0.77,
    memoryCapacity: 0.68,
    governanceClarity: 0.71,
  });

  const review = runGreatReview(runtime.messages);

  return (
    <main className="p-6 space-y-6 bg-slate-50 min-h-screen">
      <header className="rounded-2xl border p-5 bg-white shadow-sm">
        <h1 className="text-3xl font-semibold">Alexandrie Fractale</h1>
        <p className="mt-2 text-slate-700">A playable civilization of governed reconstruction of knowledge.</p>
      </header>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border p-4 bg-white shadow-sm">
          <h2 className="text-xl font-semibold mb-2">Active Mission</h2>
          <p className="text-sm text-slate-700">{runtime.view.activeMission?.title ?? 'No active mission'}</p>
          <p className="mt-2 text-sm text-slate-700">Progress: {runtime.view.missionProgress.toFixed(2)}</p>
          <p className="mt-2 text-sm text-slate-700">Unlocked zones: {runtime.view.unlockedZoneIds.join(', ') || 'none'}</p>
        </div>

        <div className="rounded-2xl border p-4 bg-white shadow-sm">
          <h2 className="text-xl font-semibold mb-2">Active Gate</h2>
          <p className="text-sm text-slate-700">{runtime.view.activeGate?.id ?? 'No active gate'}</p>
          <p className="mt-2 text-sm text-slate-700">Next action: {runtime.view.activeGate?.nextAction ?? 'N/A'}</p>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <PyramidDashboard evaluation={pyramid} />
        <GreatReviewPanel result={review} />
      </section>

      <HistoricalSocietiesRuntimeSection />
    </main>
  );
}
```

## Why this order is best
- keeps the current runtime identity intact
- places historical pedagogy after the core reconstruction dashboards
- makes society analysis feel like an extension of governed knowledge, not a disconnected minigame
- preserves a clean route for later connection to ledgers and global gates

## Next integration steps
1. bind Historical Societies cards to the Real History Ledger
2. bind public summaries to Global Promotion Gate Table
3. expose society rail labels in the Public Explorer
4. allow mission generation from society contradiction clusters

## Final law
The Historical Societies section should not sit outside the runtime. It should appear as a governed pedagogical extension of the same truth architecture.
