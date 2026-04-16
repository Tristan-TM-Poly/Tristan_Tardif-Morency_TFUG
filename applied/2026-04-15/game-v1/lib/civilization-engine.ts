export type CivilizationState = {
  G: number;
  K: number;
  T: number;
  M: number;
  I: number;
  E: number;
  P: number;
};

export type CivilizationStepResult = {
  next: CivilizationState;
  resilience: number;
  flourishing: number;
  collapseRisk: number;
  recommendation: string;
};

function clamp01(value: number): number {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

export function evaluateCivilization(state: CivilizationState) {
  const resilience = clamp01((state.G + state.K + state.M + state.E) / 4 - 0.35 * state.P);
  const flourishing = clamp01((state.G + state.K + state.T + state.M + state.I + state.E) / 6 - 0.2 * state.P);
  const collapseRisk = clamp01(state.P + 0.25 * (1 - state.I) + 0.2 * (1 - state.E) + 0.15 * (1 - state.G));

  const recommendation =
    collapseRisk >= 0.7
      ? 'reduce collapse pressure and repair governance, ecology, or inclusion'
      : resilience >= 0.7 && flourishing >= 0.7
        ? 'promote this branch as a strong long-range civilizational pattern'
        : 'stabilize memory, inclusion, and ecology before stronger promotion';

  return { resilience, flourishing, collapseRisk, recommendation };
}

export function stepCivilization(state: CivilizationState): CivilizationStepResult {
  const next: CivilizationState = {
    G: clamp01(state.G + 0.04 * state.K - 0.03 * state.P),
    K: clamp01(state.K + 0.03 * state.M + 0.02 * state.T - 0.03 * state.P),
    T: clamp01(state.T + 0.03 * state.K - 0.02 * state.E + 0.01 * state.G),
    M: clamp01(state.M + 0.03 * state.K - 0.02 * state.P),
    I: clamp01(state.I + 0.02 * state.G - 0.03 * state.P),
    E: clamp01(state.E - 0.02 * state.T + 0.02 * state.G - 0.02 * state.P),
    P: clamp01(state.P + 0.03 * (1 - state.I) + 0.03 * (1 - state.E) - 0.03 * state.G - 0.02 * state.M),
  };

  const evaluation = evaluateCivilization(next);
  return { next, ...evaluation };
}

export function simulateCivilization(state: CivilizationState, steps: number) {
  const history: Array<{ step: number; state: CivilizationState; resilience: number; flourishing: number; collapseRisk: number }> = [];
  let current = state;
  for (let i = 0; i < steps; i++) {
    const result = stepCivilization(current);
    current = result.next;
    history.push({
      step: i + 1,
      state: current,
      resilience: result.resilience,
      flourishing: result.flourishing,
      collapseRisk: result.collapseRisk,
    });
  }
  return history;
}
