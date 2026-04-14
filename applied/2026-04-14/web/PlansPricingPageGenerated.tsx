import React from 'react';

const tiers = [
  {
    name: 'Public',
    description: 'Open bounded access to core public pages, selected demos, and educational discovery routes.',
  },
  {
    name: 'Member',
    description: 'Extended guided access to demos, routes, life-project surfaces, and member progression.',
  },
  {
    name: 'Research Pro',
    description: 'Deeper workbench, packets, advanced routes, and research-facing interactive layers.',
  },
  {
    name: 'Institutional',
    description: 'Partner and organization access with broader governance, collaboration, and deployment-facing pathways.',
  },
];

export default function PlansPricingPageGenerated() {
  return (
    <main>
      <section>
        <h1>Plans and Access</h1>
        <p>
          Choose a governed access level aligned with public exploration, guided membership,
          research work, or institutional collaboration.
        </p>
      </section>

      <section>
        <h2>Tiers</h2>
        <ul>
          {tiers.map((tier) => (
            <li key={tier.name}>
              <strong>{tier.name}</strong>: {tier.description}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <div>
          <button>Start free</button>
          <button>Become member</button>
          <button>Explore institutional access</button>
        </div>
      </section>
    </main>
  );
}
