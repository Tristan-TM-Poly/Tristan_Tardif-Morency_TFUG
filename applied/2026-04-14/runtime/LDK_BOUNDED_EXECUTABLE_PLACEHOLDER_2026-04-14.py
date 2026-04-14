from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class LDKState:
    amplitude: float
    admissible: bool = True


def ldk_step(state: LDKState) -> LDKState:
    next_amplitude = 0.9 * state.amplitude
    admissible = abs(next_amplitude) <= abs(state.amplitude) + 1e-12
    return LDKState(amplitude=next_amplitude, admissible=admissible)


def run_ldk_bounded_example(steps: int = 5) -> Dict[str, Any]:
    state = LDKState(amplitude=1.0, admissible=True)
    trace = [asdict(state)]
    for _ in range(steps):
        state = ldk_step(state)
        trace.append(asdict(state))
    return {
        "artifact_type": "ldk_bounded_example",
        "trace": trace,
        "admissible": all(point["admissible"] for point in trace),
    }


if __name__ == "__main__":
    print(run_ldk_bounded_example())
