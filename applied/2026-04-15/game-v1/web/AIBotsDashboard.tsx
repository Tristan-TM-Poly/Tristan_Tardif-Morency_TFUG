import React from 'react';
import bots from '../data/ai-bots-manifest.json';

export default function AIBotsDashboard() {
  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-3">AI Bots Dashboard</h2>
      <ul className="space-y-2 text-sm">
        {bots.bots.map((bot) => (
          <li key={bot.id} className="border p-2 rounded">
            <strong>{bot.id}</strong> — role: {bot.role}
            <div className="text-xs text-slate-600">commands: {bot.commands.join(', ')}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
