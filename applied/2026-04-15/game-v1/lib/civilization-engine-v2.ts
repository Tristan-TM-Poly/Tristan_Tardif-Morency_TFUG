import { CivilizationState } from './civilization-engine';

export type ShockEvent = {
  type: 'war' | 'climate' | 'resource' | 'institution' | 'memory' | 'breakthrough';
  intensity: number;
};

function clamp01(x: number) {
  return Math.max(0, Math.min(1, x));
}

export function applyShock(state: CivilizationState, shock: ShockEvent): CivilizationState {
  const s = { ...state };

  switch (shock.type) {
    case 'war':
      s.G -= 0.1 * shock.intensity;
      s.E -= 0.1 * shock.intensity;
      s.P += 0.15 * shock.intensity;
      break;
    case 'climate':
      s.E -= 0.15 * shock.intensity;
      s.P += 0.1 * shock.intensity;
      break;
    case 'resource':
      s.E -= 0.1 * shock.intensity;
      s.T -= 0.05 * shock.intensity;
      s.P += 0.1 * shock.intensity;
      break;
    case 'institution':
      s.G -= 0.15 * shock.intensity;
      s.I -= 0.1 * shock.intensity;
      break;
    case 'memory':
      s.M -= 0.2 * shock.intensity;
      s.K -= 0.1 * shock.intensity;
      break;
    case 'breakthrough':
      s.T += 0.15 * shock.intensity;
      s.K += 0.1 * shock.intensity;
      break;
  }

  return {
    G: clamp01(s.G),
    K: clamp01(s.K),
    T: clamp01(s.T),
    M: clamp01(s.M),
    I: clamp01(s.I),
    E: clamp01(s.E),
    P: clamp01(s.P),
  };
}

export function nonlinearStep(state: CivilizationState): CivilizationState {
  const s = { ...state };

  // nonlinear amplification
  const fragility = (1 - s.I) * (1 - s.E);
  const stabilization = s.G * s.M;

  return {
    G: clamp01(s.G + 0.05 * s.K - 0.04 * s.P),
    K: clamp01(s.K + 0.04 * s.M + 0.02 * s.T - 0.03 * s.P),
    T: clamp01(s.T + 0.04 * s.K - 0.03 * s.E),
    M: clamp01(s.M + 0.04 * s.K - 0.03 * s.P),
    I: clamp01(s.I + 0.03 * s.G - 0.05 * s.P),
    E: clamp01(s.E - 0.04 * s.T + 0.03 * s.G - 0.03 * s.P),
    P: clamp01(s.P + 0.05 * fragility - 0.04 * stabilization),
  };
}

export function simulateV2(initial: CivilizationState, steps: number, shocks: ShockEvent[] = []) {
  let current = initial;
  const history = [];

  for (let i = 0; i < steps; i++) {
    if (shocks[i]) {
      current = applyShock(current, shocks[i]);
    }

    current = nonlinearStep(current);

    history.push({ step: i + 1, state: current });
  }

  return history;
}
