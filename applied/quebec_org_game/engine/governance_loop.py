def governance_cycle(profiles, flags):
    updated = {}
    for org_id, profile in profiles.items():
        org_flags = [f for f in flags if f.get("org_id") == org_id]
        if any(f.get("flag_type") == "critical" for f in org_flags):
            profile.profile_state = "under_review"
        updated[org_id] = profile
    return updated
