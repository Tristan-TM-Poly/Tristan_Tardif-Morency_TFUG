import React from 'react';

const plans = [
  'Public / free access',
  'Member access',
  'Research / pro access',
  'Institutional / partner access',
];

export default function MembershipDonationPortalGenerated() {
  return (
    <main>
      <section>
        <h1>Memberships, Subscriptions, and Donations</h1>
        <p>
          Support TFUGA, AI-7, TRISTAN2, educational layers, life projects,
          and public-interactive development through governed memberships and donations.
        </p>
      </section>

      <section>
        <h2>Access levels</h2>
        <ul>
          {plans.map((plan) => (
            <li key={plan}>{plan}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Actions</h2>
        <div>
          <button>Create account</button>
          <button>Choose subscription</button>
          <button>Support with donation</button>
        </div>
      </section>
    </main>
  );
}
