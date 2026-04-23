def summarize_profiles(profiles):
    summary = {}
    for org_id, profile in profiles.items():
        summary[org_id] = {
            "total_score": profile.total_score,
            "state": profile.profile_state
        }
    return summary
