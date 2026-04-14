import React from 'react';

const botFamilies = [
  'Research and theory bots',
  'Guidance and NPC bots',
  'Monitoring and contradiction bots',
  'Packet and review bots',
  'Life-project and centrale bots',
  'Propagation and publication bots',
];

export default function AIBotsPageGenerated() {
  return (
    <main>
      <section>
        <h1>AI-BOTS</h1>
        <p>
          Explore bounded AI-BOT families distributed across theory, gameplay,
          monitoring, review, propagation, and life-project deployment.
        </p>
      </section>

      <section>
        <h2>Bot families</h2>
        <ul>
          {botFamilies.map((family) => (
            <li key={family}>{family}</li>
          ))}
        </ul>
      </section>

      <section>
        <div>
          <button>Inspect AI-BOT roles</button>
          <button>Inspect governance links</button>
          <button>Inspect deployment routes</button>
        </div>
      </section>
    </main>
  );
}
