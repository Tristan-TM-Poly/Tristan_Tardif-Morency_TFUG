def evaluate_for_merge(score, tests_passed, contradictions):
    if not tests_passed:
        return "reject"
    if contradictions > 0:
        return "review"
    if score >= 2.0:
        return "eligible"
    return "review"
