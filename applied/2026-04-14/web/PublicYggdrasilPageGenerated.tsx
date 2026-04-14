import React from 'react';
import YggdrasilNodeExplorerGenerated from './YggdrasilNodeExplorerGenerated';

const publicRoutes = [
  'Theory roots',
  'AI-7 metabolism routes',
  'TRISTAN2 governance routes',
  'Life-project branches',
  'Educational game routes',
  'Collaboration corridors',
];

export default function PublicYggdrasilPageGenerated() {
  return (
    <main>
      <section>
        <h1>Public Yggdrasil</h1>
        <p>
          Navigate a bounded public surface of roots, branches, routes,
          governance links, and collaboration corridors across the sovereign stack.
        </p>
      </section>

      <section>
        <h2>Public routes</h2>
        <ul>
          {publicRoutes.map((route) => (
            <li key={route}>{route}</li>
          ))}
        </ul>
      </section>

      <YggdrasilNodeExplorerGenerated />
    </main>
  );
}
