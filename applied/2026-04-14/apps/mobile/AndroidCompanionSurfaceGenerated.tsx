import React from 'react';

const mobileModes = [
  'Member dashboard',
  'Guided demos',
  'AI-BOT NPC guidance',
  'Yggdrasil route snapshots',
  'Donations and subscriptions',
];

export default function AndroidCompanionSurfaceGenerated() {
  return (
    <main>
      <section>
        <h1>Android Companion Surface</h1>
        <p>
          A mobile companion for guided access to memberships, demos, AI-BOT guidance,
          Yggdrasil routes, and public or member-level progression.
        </p>
      </section>

      <section>
        <h2>Mobile modes</h2>
        <ul>
          {mobileModes.map((mode) => (
            <li key={mode}>{mode}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
