# FRACTAL_LOOP_REDUCED_TRACE — Applied Snapshot (2026-04-14)

## Purpose
Provide the first explicit reduced trace placeholder for the bounded Fractal-Loop pilot.

## Reduced trace schema
- initial reduced state: `s0`
- reduced update law: `s_{n+1} = F_red(s_n)`
- observable: `o_n = Obs(s_n)`
- boundedness witness: `B(s_n) <= B_max`
- stop condition: bounded convergence, bounded oscillation, or bounded finite horizon

## Minimal staged trace
1. `s0` declared
2. `s1 = F_red(s0)`
3. `s2 = F_red(s1)`
4. `o0, o1, o2` recorded
5. boundedness witness checked at each step

## Acceptance condition
The reduced trace is acceptable when the same staged schema can be re-used for later executable closure without changing the conceptual object.
