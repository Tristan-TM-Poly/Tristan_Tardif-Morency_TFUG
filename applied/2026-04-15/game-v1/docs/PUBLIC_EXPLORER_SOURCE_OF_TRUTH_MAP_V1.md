# Public Explorer Source-of-Truth Map v1

## Purpose
Define the public-facing knowledge map for the site and educational game while preserving separation between evidence, hypotheses, and simulated branches.

## Three visible layers
1. Established History
2. Hypotheses in Review
3. Simulations and Playable Branches

## Core explorer objects
- world zones
- knowledge branches
- historical objects
- symbol clusters
- mission gateways
- review gates
- Rosetta alignment nodes
- ledger entries

## Required map fields per object
- id
- label
- object_type
- visible_layer
- linked_ledger_ids
- linked_mission_ids
- linked_node_ids
- gate_dependency
- confidence_label
- user_facing_summary
- pedagogical_goal

## User-facing confidence labels
- established
- under review
- exploratory
- simulated

## Explorer doctrine
The Public Explorer must always show:
- what is known
- what is being tested
- what is simulated for learning

It must never visually collapse these three into one misleading category.

## Navigation flows
- history-first flow
- symbol-first flow
- temple-first flow
- myth-to-history flow
- evidence-to-simulation flow

## Output use
This map feeds:
- interactive site explorer
- game world navigation
- public pedagogy layer
- mission generation entry points

## Final law
The Public Explorer is the surface where complexity becomes legible without sacrificing epistemic honesty.
