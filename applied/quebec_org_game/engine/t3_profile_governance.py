def evaluate_profile(profile):
    score = getattr(profile, "total_score", 0)

    if score >= 2.0:
        return "promote"
    if score <= -2.0:
        return "quarantine"
    return "review"


def apply_governance(profiles):
    decisions = {}
    for org_id, profile in profiles.items():
        decisions[org_id] = evaluate_profile(profile)
    return decisions
