"""Generate a first-order hairspring candidate from a target frequency."""

from __future__ import annotations

import json

from research.hairspring.design import required_thickness_for_spiral_mm
from research.hairspring.geometry import SpiralSpec


def run() -> dict:
    spec = SpiralSpec(
        inner_radius_mm=1.0,
        radial_pitch_mm_per_turn=0.30,
        turns=8.0,
        samples_per_turn=256,
    )

    thickness_mm = required_thickness_for_spiral_mm(
        spec=spec,
        spring_width_mm=0.10,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
        target_frequency_hz=4.0,
    )

    return {
        "id": "h2-inverse-design-4hz",
        "model": "first-order-K=EI/L",
        "target_frequency_hz": 4.0,
        "balance_inertia_kg_m2": 1e-9,
        "spring_width_mm": 0.10,
        "youngs_modulus_gpa": 200.0,
        "required_thickness_mm": thickness_mm,
        "warning": "starting candidate only; requires H3/H4 refinement"
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
