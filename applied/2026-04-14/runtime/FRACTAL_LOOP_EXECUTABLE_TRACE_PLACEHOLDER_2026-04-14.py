from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, List, Dict, Any


@dataclass
class ReducedState:
    value: float
    step: int = 0


@dataclass
class TracePoint:
    step: int
    state_value: float
    observable: float
    boundedness_witness: float


@dataclass
class TraceResult:
    trace: List[TracePoint]
    bounded: bool
    stop_reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace": [asdict(p) for p in self.trace],
            "bounded": self.bounded,
            "stop_reason": self.stop_reason,
        }


def reduced_update(state: ReducedState) -> ReducedState:
    """Minimal bounded placeholder update law for the staged Fractal-Loop pilot."""
    next_value = 0.8 * state.value + 0.1
    return ReducedState(value=next_value, step=state.step + 1)


def observable(state: ReducedState) -> float:
    return state.value


def boundedness_witness(state: ReducedState) -> float:
    return abs(state.value)


def run_reduced_trace(
    initial_state: ReducedState | None = None,
    max_steps: int = 8,
    witness_bound: float = 10.0,
    update_fn: Callable[[ReducedState], ReducedState] = reduced_update,
) -> TraceResult:
    state = initial_state or ReducedState(value=1.0, step=0)
    trace: List[TracePoint] = []

    for _ in range(max_steps):
        obs = observable(state)
        wit = boundedness_witness(state)
        trace.append(
            TracePoint(
                step=state.step,
                state_value=state.value,
                observable=obs,
                boundedness_witness=wit,
            )
        )
        if wit > witness_bound:
            return TraceResult(trace=trace, bounded=False, stop_reason="witness_bound_exceeded")
        state = update_fn(state)

    return TraceResult(trace=trace, bounded=True, stop_reason="max_steps_reached")


if __name__ == "__main__":
    result = run_reduced_trace()
    print(result.to_dict())
