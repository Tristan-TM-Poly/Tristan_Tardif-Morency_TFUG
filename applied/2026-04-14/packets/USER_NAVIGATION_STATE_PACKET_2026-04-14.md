# USER_NAVIGATION_STATE_PACKET — Applied Snapshot (2026-04-14)

## Purpose
Define the first bounded navigation state packet for the unified public application layer.

## State fields
- current_route
- previous_route
- visible_nav_items
- user_role_hint
- access_scope_hint
- progression_hint
- release_layer_hint
- next_recommended_route

## State transitions
- public discovery -> deeper exploration
- exploration -> membership interest
- membership -> account entry
- account entry -> dashboard
- dashboard -> guided routes

## Law
Navigation state is valid only if route progression remains interpretable, role-aware, and compatible with public maturity distinctions.
