from scoring_engine import build_organization_profile, EventDimensionScore


def build_profiles(events_by_org):
    profiles = {}
    for org_id, rows in events_by_org.items():
        scores = [EventDimensionScore(**r) for r in rows]
        profiles[org_id] = build_organization_profile(org_id, scores)
    return profiles
