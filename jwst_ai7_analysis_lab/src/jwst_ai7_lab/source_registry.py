#!/usr/bin/env python3
"""Source registry validation for JWST AI-7 workflows.

This module validates the manifest of existing web/GitHub/STScI resources without
performing network access. It is intentionally conservative: sources are allowed
into the planning registry only if they declare provenance, intended use, ingest
mode, and risk level.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_TOP_LEVEL = {"version", "purpose", "policy", "resources"}
REQUIRED_RESOURCE_FIELDS = {"id", "name", "kind", "url", "use_for", "ingest_mode", "risk_level"}
ALLOWED_INGEST_MODES = {
    "metadata_reference_only",
    "manifest_then_manual_download_review",
    "dependency_reference_only",
    "reference_and_adapt_with_citation",
    "reference_only_unless_explicit_download",
    "reference_only_optional_dependency",
    "optional_dependency_reference",
    "manifest_and_license_review",
}
ALLOWED_RISK_LEVEL_PREFIXES = {"low", "medium", "high"}


def load_registry(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def is_https_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_resource(resource: dict, index: int) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_RESOURCE_FIELDS - set(resource))
    if missing:
        errors.append(f"resource[{index}] missing fields: {', '.join(missing)}")
        return errors

    if not isinstance(resource["id"], str) or not resource["id"].strip():
        errors.append(f"resource[{index}] id must be a non-empty string")
    if not isinstance(resource["name"], str) or not resource["name"].strip():
        errors.append(f"resource[{index}] name must be a non-empty string")
    if not is_https_url(resource["url"]):
        errors.append(f"resource[{index}] url must be https")
    if not isinstance(resource["use_for"], list) or not resource["use_for"]:
        errors.append(f"resource[{index}] use_for must be a non-empty list")
    if resource["ingest_mode"] not in ALLOWED_INGEST_MODES:
        errors.append(f"resource[{index}] ingest_mode not allowed: {resource['ingest_mode']}")
    risk = str(resource["risk_level"]).lower()
    if not any(risk.startswith(prefix) for prefix in ALLOWED_RISK_LEVEL_PREFIXES):
        errors.append(f"resource[{index}] risk_level must start with low, medium, or high")
    return errors


def validate_registry(registry: dict) -> dict:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append(f"registry missing fields: {', '.join(missing)}")

    policy = registry.get("policy", {})
    if not policy.get("public_or_authorized_data_only", False):
        errors.append("policy.public_or_authorized_data_only must be true")
    if not policy.get("license_and_citation_check_required", False):
        errors.append("policy.license_and_citation_check_required must be true")
    if not policy.get("no_bulk_download_without_review", False):
        errors.append("policy.no_bulk_download_without_review must be true")
    if not policy.get("no_unverified_discovery_claims", False):
        errors.append("policy.no_unverified_discovery_claims must be true")

    resources = registry.get("resources", [])
    if not isinstance(resources, list) or not resources:
        errors.append("resources must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        for index, resource in enumerate(resources):
            errors.extend(validate_resource(resource, index))
            resource_id = resource.get("id")
            if resource_id in seen_ids:
                errors.append(f"duplicate resource id: {resource_id}")
            seen_ids.add(resource_id)

    return {"passed": not errors, "errors": errors, "resource_count": len(resources) if isinstance(resources, list) else 0}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("registry", help="Path to jwst_existing_resources_registry.json")
    args = parser.parse_args()
    result = validate_registry(load_registry(args.registry))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
