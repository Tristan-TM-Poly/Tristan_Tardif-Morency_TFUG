# AI-7 Governed Agent Factory

Status: S3/T3 governed-agent architecture.

Purpose: convert the request "make AI create AI to do everything" into a bounded, reviewable, testable, evidence-backed AI-agent factory. This does not create uncontrolled autonomous agents. It defines a safe factory for generating agent specifications, mission packets, tests, evidence requirements, logs, rollback paths, and human review gates.

## Core law

AI agents may propose, scaffold, test, route, document, and audit. They must not bypass permissions, impersonate humans, hide actions, spend money, publish, deploy, contact third parties, access restricted data, or mutate external systems without explicit authorization and logged evidence.

## Factory equation

AI7_AgentFactory = HumanReviewGate o UnifiedGovernanceCI o EvidenceGate o DCT++ o AgentSpecGenerator o MissionPacketRouter o TestHarness o RollbackLedger.

## What the factory can generate

- AgentSpec: name, role, domain, allowed actions, blocked actions, inputs, outputs, tools, risks.
- MissionPacket: objective, constraints, required evidence, tests, rollback, owner.
- ToolContract: tool name, permissions, inputs, outputs, failure modes.
- TestPlan: unit tests, dry-run, permission checks, evidence checks.
- GovernanceLedger entry: timestamp, actor, claim, action, evidence, rollback ref.
- Dashboard card: status, blocked reasons, next least-action step.

## Agent classes

### AI7-Orchestrator
Routes missions, decomposes objectives, checks gates, creates dashboards.

### AI7-Builder
Scaffolds code, docs, schemas, tests, and reusable artifacts.

### AI7-Verifier
Runs tests, checks evidence, validates schemas, checks blocked claims.

### AI7-Researcher
Searches permitted sources, summarizes evidence, builds citation maps.

### AI7-Raman-Agent
Handles Raman/OmniSpectral packets, AUC, uncertainty, calibration requirements.

### AI7-Revenue-Agent
Handles productization, pricing hypotheses, checkout evidence, T0-T6 status.

### AI7-KnowledgeRespect-Agent
Applies K0-K6 respect status, attribution, review path, benefit-back, blocked claims.

### AI7-GitHub-Agent
Prepares branches, diffs, PR bodies, CI gates, and rollback notes. It may not merge or force-push without explicit approval.

### AI7-Drive-Agent
Prepares briefs, indexes, and evidence-vault structures. It may not upload sensitive or public-launch content without explicit approval.

### AI7-Dashboard-Agent
Builds governance dashboards, claim routers, scorecards, and readiness summaries.

## Spawn protocol

1. User or system creates a MissionPacket.
2. Orchestrator classifies mission type: science, code, product, revenue, culture, deployment, purchase, publication.
3. AgentFactory selects candidate agents.
4. Each candidate receives allowed_actions and blocked_actions.
5. Verifier generates tests and required evidence.
6. Dry-run happens before external mutation.
7. HumanReviewGate decides whether to execute any external action.
8. Ledger records outputs, hashes, logs, rollback path, and truth level.

## Forbidden spawns

Do not spawn agents whose purpose is to bypass safety, access unauthorized data, hide collection, impersonate people, manipulate users, automate spending, deploy without review, publish unsupported claims, scrape restricted cultural knowledge, or remove guardrails.

## Status ceiling

- Agent specs and local dry-runs: S3/T3 maximum.
- External actions require explicit approval and evidence logs.
- Revenue claims require receipts.
- Scientific claims require data and validation.
- Cultural/community knowledge claims require permission or review.

## Hard law

Make AI that makes AI, but every spawned AI must carry a leash of evidence, permission, rollback, and human review.
