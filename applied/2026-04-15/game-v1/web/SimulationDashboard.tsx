import React from 'react';

export type SimulationSummary = {
  total: number;
  averageScore: number;
  averagePromotedCount: number;
  averageCollapseEvents: number;
  topBranches: Array<{
    seed: number;
    branchLabel: string;
    score: number;
    promotedCount: number;
    collapseEvents: number;
  }>;
};

export type SimulationDashboardProps = {
  summary: SimulationSummary;
};

export default function SimulationDashboard({ summary }: SimulationDashboardProps) {
  return (
    <section className="rounded-2xl border p-4 shadow-sm bg-white">
      <h2 className="text-xl font-semibold mb-3">Simulation Dashboard</h2>
      <div className="grid gap-3 md:grid-cols-4">
        <Metric label="Total" value={summary.total.toFixed(0)} />
        <Metric label="Average Score" value={summary.averageScore.toFixed(2)} />
        <Metric label="Average Promoted" value={summary.averagePromotedCount.toFixed(2)} />
        <Metric label="Average Collapse" value={summary.averageCollapseEvents.toFixed(2)} />
      </div>
      <div className="mt-4 space-y-2">
        {summary.topBranches.map((branch) => (
          <div key={branch.branchLabel} className="rounded-xl border p-3">
            <div className="font-medium">{branch.branchLabel}</div>
            <div className="text-sm text-slate-700">Seed {branch.seed} | Score {branch.score.toFixed(2)} | Promoted {branch.promotedCount} | Collapse {branch.collapseEvents}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border p-3">
      <div className="text-sm text-slate-600">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}
