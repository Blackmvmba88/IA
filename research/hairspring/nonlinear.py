"""Amplitude-dependent hairspring experiments.

H1 uses a Duffing-like torsional spring:
    tau = -(k1*theta + k3*theta^3)

The sweep measures frequency from simulated zero crossings. It is intended to
expose non-isochronism, not to reproduce a specific production hairspring.
"""

from __future__ import annotations

from dataclasses import dataclass

from research.oscillator.model import BalanceSpring, OscillatorState, step_semi_implicit


@dataclass(frozen=True)
class SweepPoint:
    amplitude_rad: float
    frequency_hz: float
    relative_rate_s_per_day: float


def estimate_free_frequency_hz(
    oscillator: BalanceSpring,
    amplitude_rad: float,
    duration_s: float = 5.0,
    dt_s: float = 0.00025,
) -> float:
    if amplitude_rad <= 0:
        raise ValueError("amplitude_rad must be > 0")
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration_s and dt_s must be > 0")

    state = OscillatorState(amplitude_rad, 0.0)
    previous = state.angle_rad
    crossings: list[float] = []

    for i in range(1, int(duration_s/dt_s) + 1):
        state = step_semi_implicit(oscillator, state, dt_s)
        t = i*dt_s
        if (previous < 0.0 <= state.angle_rad) or (previous > 0.0 >= state.angle_rad):
            crossings.append(t)
        previous = state.angle_rad

    if len(crossings) < 4:
        raise RuntimeError("not enough zero crossings to estimate frequency")

    half_periods = [b-a for a, b in zip(crossings[:-1], crossings[1:])]
    mean_half_period = sum(half_periods)/len(half_periods)
    return 1.0/(2.0*mean_half_period)


def amplitude_sweep(
    oscillator: BalanceSpring,
    amplitudes_rad: list[float],
    duration_s: float = 5.0,
    dt_s: float = 0.00025,
) -> list[SweepPoint]:
    if not amplitudes_rad:
        raise ValueError("at least one amplitude is required")

    frequencies = [
        estimate_free_frequency_hz(oscillator, amp, duration_s, dt_s)
        for amp in amplitudes_rad
    ]
    baseline = frequencies[0]

    return [
        SweepPoint(
            amplitude_rad=amp,
            frequency_hz=freq,
            relative_rate_s_per_day=((freq-baseline)/baseline)*86400.0,
        )
        for amp, freq in zip(amplitudes_rad, frequencies)
    ]
