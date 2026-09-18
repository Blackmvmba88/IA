"""Run the H1 nonlinear hairspring amplitude sweep and emit JSON."""

from __future__ import annotations

import json
from math import pi

from research.hairspring.nonlinear import amplitude_sweep
from research.oscillator.model import BalanceSpring


def run() -> dict:
    inertia = 1e-9
    k1 = (2*pi*4.0)**2 * inertia
    amplitudes = [0.1, 0.2, 0.4, 0.6, 0.8]

    cases = {}
    for ratio in (-0.05, 0.0, 0.05):
        osc = BalanceSpring(
            inertia_kg_m2=inertia,
            stiffness_nm_per_rad=k1,
            cubic_stiffness_nm_per_rad3=ratio*k1,
        )
        points = amplitude_sweep(
            osc,
            amplitudes_rad=amplitudes,
            duration_s=5.0,
            dt_s=0.00025,
        )
        rates = [p.relative_rate_s_per_day for p in points]
        cases[f"k3_over_k1={ratio:+.3f}"] = {
            "points": [
                {
                    "amplitude_rad": p.amplitude_rad,
                    "frequency_hz": p.frequency_hz,
                    "relative_rate_s_per_day": p.relative_rate_s_per_day,
                }
                for p in points
            ],
            "rate_spread_s_per_day": max(rates)-min(rates),
        }

    return {
        "model": "BPME-H1-Duffing-like-hairspring",
        "small_signal_frequency_hz": 4.0,
        "cases": cases,
    }


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
