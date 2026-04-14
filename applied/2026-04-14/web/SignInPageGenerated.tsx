import React from 'react';

export default function SignInPageGenerated() {
  return (
    <main>
      <section>
        <h1>Sign In</h1>
        <p>
          Access member, research, institutional, and guided interactive surfaces
          across the TFUGA platform.
        </p>
      </section>

      <section>
        <div>
          <label>Email</label>
          <input type="email" placeholder="you@example.com" />
        </div>
        <div>
          <label>Password</label>
          <input type="password" placeholder="••••••••" />
        </div>
        <div>
          <button>Sign in</button>
          <button>Request guided access</button>
        </div>
      </section>
    </main>
  );
}
