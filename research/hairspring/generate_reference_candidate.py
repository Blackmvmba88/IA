"""Generate a deterministic 4 Hz H2 reference candidate."""

from __future__ import annotations

import json

from research.hairspring.candidate import export_candidate, solve_candidate
from research.hairspring.geometry import SpiralSpec


def run(output_dir: str = "artifacts/hairspring-reference-4hz") -> dict:
    candidate = solve_candidate(
        candidate_id="mamba-hs-h2-4hz-001",
        spec=SpiralSpec(
            inner_radius_mm=1.0,
            radial_pitch_mm_per_turn=0.30,
            turns=8.0,
            samples_per_turn=256,
        ),
        spring_width_mm=0.10,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
        target_frequency_hz=4.0,
    )
    return export_candidate(candidate, output_dir)


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
