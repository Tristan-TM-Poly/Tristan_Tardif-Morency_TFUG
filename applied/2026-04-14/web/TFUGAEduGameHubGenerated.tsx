import React from 'react';

const npcRoles = [
  'Concept Guide',
  'System Guide',
  'Experiment Guide',
  'Review Guide',
  'Collaboration Guide',
];

export default function TFUGAEduGameHubGenerated() {
  return (
    <main>
      <section>
        <h1>TFUGA Educational Game Hub</h1>
        <p>
          Learn, test, and develop theories and systems through bounded gameplay
          loops coupled to TFUGA, AI-7, and TRISTAN2.
        </p>
      </section>

      <section>
        <h2>AI-BOT NPC Guides</h2>
        <ul>
          {npcRoles.map((role) => (
            <li key={role}>{role}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Core paths</h2>
        <ul>
          <li>Fractal-Loop challenge path</li>
          <li>bounded LDK mastery path</li>
          <li>Raman observability path</li>
          <li>TFUGA Trinity progression path</li>
        </ul>
      </section>
    </main>
  );
}
