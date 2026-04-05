# Access Policy

## Access intent
This library is intended only for:
- Tristan
- AI-7
- TRISTAN2
- ChatGPT-facing orchestration acting for Tristan
- Tristan's Drive-governed document layer

## Enforcement reality
Current enforcement is based on repository privacy and actor-intent checks in code.
This is **not** a substitute for full production authentication, secrets management, or cryptographic identity.

## Policy rules
1. Unknown actors are denied by default.
2. Every artifact should declare source, owner, and governance state.
3. Drive-facing payloads should be tagged as private by default.
4. Promotion to stable or canon-facing status requires governance review.
5. Quarantine must remain available for ambiguous or inflated objects.

## Recommended future hardening
- signed actor tokens
- encrypted secrets outside Git
- private runtime identity provider
- Drive app-folder scoping
- audit trails for write operations
