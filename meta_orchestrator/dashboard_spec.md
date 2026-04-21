# Dashboard Spec

## Role
Interactive command and visibility layer over the sovereign control plane.
It must read from boards, queues, waves, and ledgers without becoming a competing source of truth.

## Required panels
1. Global power score
2. Command queue
3. Packet queue
4. Active campaigns
5. Wave states
6. Risk budget meters
7. Promotion readiness
8. Pilot scoreboard
9. Latest events
10. Rollback alerts
11. Adapter health
12. Return routes

## Required filters
- domain
- trust tier
- risk level
- campaign
- wave
- gate status
- adapter
- pilot state

## Actions allowed
- request review
- open packet detail
- open campaign detail
- open wave detail
- open rollback detail
- open linked Drive/GitHub artifact

## Actions forbidden without governance
- direct canon write
- direct promotion
- direct rollback execution
- direct trunk rewrite

## Main view law
The site is a projection and interaction surface.
The source of truth remains the orchestrator console, boards, ledgers, and governed artifacts.
