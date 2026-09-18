"""Coupled oscillator + escapement + rotating gravity perturbation."""

from __future__ import annotations

from dataclasses import dataclass

from research.escapement.lever import EscapementMemory, LeverEscapement, should_impulse
from research.oscillator.model import BalanceSpring, OscillatorState, step_semi_implicit
from research.oscillator.position import gravity_torque_nm
from research.oscillator.simulate import _apply_energy_impulse
from research.tourbillon.model import TourbillonTopology, Vector


@dataclass(frozen=True)
class CoupledResult:
    duration_s: float
    impulses: int
    zero_crossings: int
    mean_half_period_s: float | None
    estimated_frequency_hz: float | None
    estimated_rate_error_s_per_day: float | None
    max_abs_angle_rad: float


def simulate_coupled(
    oscillator: BalanceSpring,
    escapement: LeverEscapement,
    topology: TourbillonTopology,
    initial: OscillatorState,
    duration_s: float,
    dt_s: float,
    gravity_hat: Vector=(0.0, 0.0, -1.0),
    gravity_torque_scale_nm: float=0.0,
) -> CoupledResult:
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration_s and dt_s must be > 0")

    state = initial
    memory = EscapementMemory(previous_angle_rad=initial.angle_rad)
    crossing_times: list[float] = []
    impulses = 0
    max_abs_angle = abs(initial.angle_rad)

    for i in range(int(duration_s/dt_s) + 1):
        t = i*dt_s

        crossed = (
            (memory.previous_angle_rad < 0.0 <= state.angle_rad)
            or (memory.previous_angle_rad > 0.0 >= state.angle_rad)
        )
        if crossed and i > 0:
            crossing_times.append(t)

        if should_impulse(escapement, memory, state.angle_rad, t):
            state = _apply_energy_impulse(oscillator, state, escapement.impulse_energy_j)
            memory.last_impulse_s = t
            impulses += 1

        memory.previous_angle_rad = state.angle_rad

        tau_g = gravity_torque_nm(
            topology,
            t,
            state.angle_rad,
            gravity_hat,
            gravity_torque_scale_nm,
        )
        state = step_semi_implicit(
            oscillator,
            state,
            dt_s,
            external_torque_nm=tau_g,
        )
        max_abs_angle = max(max_abs_angle, abs(state.angle_rad))

    if len(crossing_times) < 2:
        return CoupledResult(
            duration_s, impulses, len(crossing_times),
            None, None, None, max_abs_angle
        )

    half_periods = [
        b-a for a, b in zip(crossing_times[:-1], crossing_times[1:])
    ]
    mean_half = sum(half_periods)/len(half_periods)
    measured_f = 1.0/(2.0*mean_half)
    target_f = oscillator.natural_frequency_hz

    # Rate error proxy: relative frequency error scaled to one mean solar day.
    rate_error = ((measured_f-target_f)/target_f)*86400.0

    return CoupledResult(
        duration_s=duration_s,
        impulses=impulses,
        zero_crossings=len(crossing_times),
        mean_half_period_s=mean_half,
        estimated_frequency_hz=measured_f,
        estimated_rate_error_s_per_day=rate_error,
        max_abs_angle_rad=max_abs_angle,
    )
