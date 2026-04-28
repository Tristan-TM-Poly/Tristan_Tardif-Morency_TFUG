# AI-7 QC-CA Top 64^4 Tensor

Compressed Top 64×64×64×64 generator for the Québec–Canada Institutional HyperAtlas.

It contains:
- 64 institutions/sources
- 64 challenges/sectors
- 64 AI-7 capabilities
- 64 governance actions

Total generated opportunity hyperedges:

    16,777,216

Files:
- axes/top_64_axes.json
- generator/generate_top_tensor.py
- examples/top_256_beam_candidates.json
- reports/top_64x64x64x64_report.md

Use:
    python generator/generate_top_tensor.py --limit 1000 --out reports/generated_top_1000.json
