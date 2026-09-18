"""Evaluate the H2 spiral geometry through the first-order beam bridge."""

from __future__ import annotations

import json
from dataclasses import asdict

from research.hairspring.beam_bridge import estimate_from_spiral
from research.hairspring.geometry import SpiralSpec


def run() -> dict:
    spec = SpiralSpec(
        inner_radius_mm=1.0,
        radial_pitch_mm_per_turn=0.30,
        turns=8.0,
        samples_per_turn=256,
    )
    result = estimate_from_spiral(
        spec=spec,
        spring_width_mm=0.10,
        spring_thickness_mm=0.03,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
    )
    return {
        "id": "h2-beam-bridge-001",
        "warning": "first-order estimate; not a production hairspring prediction",
        "result": asdict(result),
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
