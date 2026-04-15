import React from 'react';
import { GameRuntime } from '../lib/game-engine';
import PyramidDashboard from './PyramidDashboard';
import GreatReviewPanel from './GreatReviewPanel';
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
    </main>
  );
}
