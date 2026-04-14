import React from 'react';

export default function SignUpPageGenerated() {
  return (
    <main>
      <section>
        <h1>Create Account</h1>
        <p>
          Join the TFUGA platform to access guided demos, member routes,
          life-project surfaces, and future research or institutional layers.
        </p>
      </section>

      <section>
        <div>
          <label>Name</label>
          <input type="text" placeholder="Your name" />
        </div>
        <div>
          <label>Email</label>
          <input type="email" placeholder="you@example.com" />
        </div>
        <div>
          <label>Password</label>
          <input type="password" placeholder="••••••••" />
        </div>
        <div>
          <button>Create account</button>
          <button>See membership options</button>
        </div>
      </section>
    </main>
  );
}
