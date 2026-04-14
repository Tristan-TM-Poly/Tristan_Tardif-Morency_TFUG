import React from 'react';

const npcModes = [
  'Concept Guide',
  'System Guide',
  'Experiment Guide',
  'Review Guide',
  'Collaboration Guide',
];

export default function AIBotNPCGuidePanelGenerated() {
  return (
    <section>
      <h2>AI-BOT NPC Guide Panel</h2>
      <p>
        Bounded AI-BOT guides help members and players understand TFUGA objects,
        system paths, experiments, review gates, and collaboration next steps.
      </p>
      <ul>
        {npcModes.map((mode) => (
          <li key={mode}>{mode}</li>
        ))}
      </ul>
      <div>
        <button>Ask for bounded hint</button>
        <button>Inspect linked artifact</button>
        <button>See next governed step</button>
      </div>
    </section>
  );
}
