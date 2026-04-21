import React, { useMemo, useState } from 'react';
import orchestrationData from '../data/meta-orchestration-sample.json';
import { dispatchAll, executeCommand } from '../lib/meta-orchestrator-runtime';

const commands = orchestrationData.command_bus;

export default function OrchestratorConsolePanel() {
  const [selectedCommand, setSelectedCommand] = useState(commands[0] ?? 'INGEST');
  const rows = useMemo(() => dispatchAll(), []);
  const executions = useMemo(() => rows.map((row) => executeCommand(row as any, selectedCommand)), [rows, selectedCommand]);

  return (
    <section className="rounded-2xl border p-4 bg-white shadow-sm space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-xl font-semibold">Meta Orchestrator Console</h2>
          <p className="mt-1 text-sm text-slate-700">Unified control surface for lanes, packets, commands, and execution states.</p>
        </div>
        <label className="text-sm">
          <span className="mb-1 block text-slate-600">Command</span>
          <select value={selectedCommand} onChange={(e) => setSelectedCommand(e.target.value)} className="rounded-lg border px-3 py-2">
            {commands.map((command) => (
              <option key={command} value={command}>{command}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="overflow-auto rounded-xl border">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-3 py-2 text-left">Object</th>
              <th className="px-3 py-2 text-left">Lane</th>
              <th className="px-3 py-2 text-left">Status</th>
              <th className="px-3 py-2 text-left">Packet</th>
              <th className="px-3 py-2 text-left">Command</th>
              <th className="px-3 py-2 text-left">Next State</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={row.object_id} className="border-t">
                <td className="px-3 py-2">{row.object_id}</td>
                <td className="px-3 py-2">{row.lane}</td>
                <td className="px-3 py-2">{row.status}</td>
                <td className="px-3 py-2">{row.packet_family}</td>
                <td className="px-3 py-2">{selectedCommand}</td>
                <td className="px-3 py-2">{executions[index]?.next_state}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
