# AI-7 Top 64 Schema Validation

This layer adds dependency-free schema-style validation for the `64^4` and `64^5` HyperAtlas axes.

## Files

- `institutional_hyperatlas/schemas/top64_axes_schema.json`
- `institutional_hyperatlas/schemas/top64_e_axis_schema.json`
- `institutional_hyperatlas/tests/validate_top64_schemas.py`

## Run

```bash
python institutional_hyperatlas/tests/validate_top64_schemas.py
```

## Checks

- A/B/C/D axes exist.
- E axis exists.
- Every axis has exactly 64 entries.
- Every axis has unique non-empty string entries.
- `64^4 = 16,777,216` is exact.
- `64^5 = 1,073,741,824` is exact.
- Schema constants match actual tensor counts.

## Why this matters

The HyperAtlas is allowed to generate huge candidate spaces only if its generators remain compact, exact, testable, and governed.
