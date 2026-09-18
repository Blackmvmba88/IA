"""Coupled balance/hairspring + event escapement simulation."""

from __future__ import annotations

from dataclasses import dataclass
from math import copysign, sqrt

from research.escapement.lever import EscapementMemory, LeverEscapement, should_impulse
from research.oscillator.model import BalanceSpring, OscillatorState, step_semi_implicit


@dataclass(frozen=True)
class SimulationResult:
    times_s: tuple[float, ...]
    angles_rad: tuple[float, ...]
    energies_j: tuple[float, ...]
    impulses: int


def _apply_energy_impulse(
    oscillator: BalanceSpring,
    state: OscillatorState,
    energy_j: float,
) -> OscillatorState:
    """Increase kinetic energy by a fixed positive amount in current direction."""
    current_ke = 0.5 * oscillator.inertia_kg_m2 * state.angular_velocity_rad_s**2
    new_speed = sqrt(2.0 * (current_ke + energy_j) / oscillator.inertia_kg_m2)

    direction = state.angular_velocity_rad_s
    if direction == 0.0:
        direction = -state.angle_rad if state.angle_rad != 0.0 else 1.0

    return OscillatorState(
        angle_rad=state.angle_rad,
        angular_velocity_rad_s=copysign(new_speed, direction),
    )


def simulate(
    oscillator: BalanceSpring,
    escapement: LeverEscapement,
    initial: OscillatorState,
    duration_s: float,
    dt_s: float,
) -> SimulationResult:
    if duration_s <= 0:
        raise ValueError("duration_s must be > 0")

    state = initial
    memory = EscapementMemory(previous_angle_rad=initial.angle_rad)
    times: list[float] = []
    angles: list[float] = []
    energies: list[float] = []
    impulses = 0

    steps = int(duration_s / dt_s)
    for i in range(steps + 1):
        t = i * dt_s
        times.append(t)
        angles.append(state.angle_rad)
        energies.append(oscillator.energy_j(state.angle_rad, state.angular_velocity_rad_s))

        if should_impulse(escapement, memory, state.angle_rad, t):
            state = _apply_energy_impulse(oscillator, state, escapement.impulse_energy_j)
            memory.last_impulse_s = t
            impulses += 1

        memory.previous_angle_rad = state.angle_rad
        state = step_semi_implicit(oscillator, state, dt_s)

    return SimulationResult(tuple(times), tuple(angles), tuple(energies), impulses)
