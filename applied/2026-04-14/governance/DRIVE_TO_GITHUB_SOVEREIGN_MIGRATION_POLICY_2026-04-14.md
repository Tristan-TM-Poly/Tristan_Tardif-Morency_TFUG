# DRIVE_TO_GITHUB_SOVEREIGN_MIGRATION_POLICY — Applied Snapshot (2026-04-14)

## Core rule
The best Drive artifacts must not remain Drive-only when they are trunk-facing, code-facing, reproducible, reviewable, benchmarkable, or publication-prep-ready.
They must be staged into GitHub as governed repo-side artifacts.

## Interpretation
- Drive remains the broad canon, cockpit, planning, scorecard, and archival layer.
- GitHub becomes the sovereign executable and reproducible layer for the best artifacts.
- The migration target is not "everything in Drive" but "the best governed, reusable, trunk-facing things from Drive".

## Promotion criteria from Drive to GitHub
An artifact should move from Drive to GitHub when it has one or more of the following properties:
1. It defines runtime, schema, queue, packet, review, promotion, rollback, or benchmark logic.
2. It is a trunk-facing theory-to-code bridge.
3. It is needed for reproducible automation, reporting, writing, or publication preparation.
4. It is a stable reference object that downstream code or documentation should cite.
5. It improves closure depth more than it increases archive mass.

## Do not keep Drive-only if
- the object is repeatedly reused in repo-side automation
- the object defines current source-of-truth execution doctrine
- the object is required for CI-visible generated outputs
- the object anchors active pilot governance

## Keep primarily in Drive if
- the object is broad exploratory archive mass
- the object is a large historical bundle with low current closure value
- the object is useful as memory but not yet code-facing or trunk-facing

## Immediate migration doctrine
1. identify best Drive artifacts
2. classify them as trunk-facing / crystallizable / exploratory / archive
3. convert trunk-facing and crystallizable best-of artifacts into repo-side governed files
4. attach CI, runner, or documentation linkage when useful
5. leave archive-heavy bulk in Drive unless a bounded extraction is justified

## Law
Drive is not demoted. It remains the wide sovereign memory.
But GitHub must become the concentrated sovereign executable memory for the best current artifacts.
