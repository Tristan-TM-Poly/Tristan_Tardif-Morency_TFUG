def compute_priority(fertility_gain, synergy_gain, connectivity_gain, friction_cost, redundancy_cost):
    return fertility_gain + synergy_gain + connectivity_gain - friction_cost - redundancy_cost


def select_best_action(actions):
    scored = [(a, compute_priority(**a)) for a in actions]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0] if scored else None
