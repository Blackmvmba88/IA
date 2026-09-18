"""Run the same oscillator through multiple regulator topologies and gravity poses.

Output is JSON so later optimization and plotting layers can consume it.
No topology is declared a winner: the current perturbation parameters are
synthetic research values, not calibrated chronometry data.
"""

from __future__ import annotations

import json
from math import pi

from research.escapement.lever import LeverEscapement
from research.oscillator.coupled import simulate_coupled
from research.oscillator.model import BalanceSpring, OscillatorState
from research.tourbillon.model import CageAxis, TourbillonTopology
from research.tourbillon.presets import (
    CLASSICAL_60S,
    INCLINED_25DEG_24S,
)


POSES = {
    "x+": (1.0, 0.0, 0.0),
    "x-": (-1.0, 0.0, 0.0),
    "y+": (0.0, 1.0, 0.0),
    "y-": (0.0, -1.0, 0.0),
    "z+": (0.0, 0.0, 1.0),
    "z-": (0.0, 0.0, -1.0),
}

STATIC = TourbillonTopology(
    name="static",
    axes=(),
    cage_inertia_kg_m2=0.0,
    friction_torque_nm=0.0,
)

BIAXIAL_60_137 = TourbillonTopology(
    name="biaxial-60-137",
    axes=(
        CageAxis((1.0, 0.0, 0.0), 60.0),
        CageAxis((0.0, 1.0, 0.0), 137.0),
    ),
    cage_inertia_kg_m2=1e-9,
    friction_torque_nm=2e-8,
)


def build_reference_oscillator() -> BalanceSpring:
    inertia = 1e-9
    stiffness = (2*pi*4.0)**2 * inertia
    return BalanceSpring(
        inertia_kg_m2=inertia,
        stiffness_nm_per_rad=stiffness,
        damping_nms_per_rad=3e-10,
    )


def run() -> dict:
    oscillator = build_reference_oscillator()
    escapement = LeverEscapement(
        impulse_energy_j=1e-10,
        unlock_angle_rad=0.08,
        dead_time_s=0.02,
    )
    topologies = [
        STATIC,
        CLASSICAL_60S,
        INCLINED_25DEG_24S,
        BIAXIAL_60_137,
    ]

    out = {
        "model": "bpme-reduced-order-position-coupling-v0",
        "target_frequency_hz": oscillator.natural_frequency_hz,
        "gravity_torque_scale_nm": 1e-10,
        "duration_s": 12.0,
        "dt_s": 0.0005,
        "results": {},
    }

    for topology in topologies:
        rows = {}
        for pose_name, gravity in POSES.items():
            r = simulate_coupled(
                oscillator=oscillator,
                escapement=escapement,
                topology=topology,
                initial=OscillatorState(0.4, 0.0),
                duration_s=out["duration_s"],
                dt_s=out["dt_s"],
                gravity_hat=gravity,
                gravity_torque_scale_nm=out["gravity_torque_scale_nm"],
            )
            rows[pose_name] = {
                "frequency_hz": r.estimated_frequency_hz,
                "rate_error_proxy_s_per_day": r.estimated_rate_error_s_per_day,
                "max_abs_angle_rad": r.max_abs_angle_rad,
                "impulses": r.impulses,
            }
        out["results"][topology.name] = rows

    return out


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
