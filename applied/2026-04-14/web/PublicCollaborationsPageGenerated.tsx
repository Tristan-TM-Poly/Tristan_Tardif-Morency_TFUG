import React from 'react';

const collaborationModes = [
  'Research collaboration',
  'Applied pilot',
  'Technical framing session',
  'Public demonstration partnership',
];

export default function PublicCollaborationsPageGenerated() {
  return (
    <main>
      <section>
        <h1>Collaborations</h1>
        <p>
          Engage with AT-1 through bounded research, applied pilots, technical framing,
          and public demonstration pathways.
        </p>
      </section>

      <section>
        <h2>Modes</h2>
        <ul>
          {collaborationModes.map((mode) => (
            <li key={mode}>{mode}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Entry conditions</h2>
        <ul>
          <li>bounded problem statement</li>
          <li>visible success criterion</li>
          <li>governed artifact or note family</li>
          <li>clear next collaboration step</li>
        </ul>
      </section>
    </main>
  );
}
