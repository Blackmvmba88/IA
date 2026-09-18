"""Reduced-order balance + hairspring model for BPME research.

This module models a rotational oscillator:

    I * theta_ddot + c * theta_dot + k * theta = tau_ext

where I is balance inertia, c is viscous-loss coefficient and k is the
effective hairspring torsional stiffness.

It is intentionally simple enough to inspect and test. Real chronometry
requires nonlinear hairspring geometry, escapement contact, pivot friction,
temperature, shock and measured positional error maps.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt


@dataclass(frozen=True)
class BalanceSpring:
    inertia_kg_m2: float
    stiffness_nm_per_rad: float
    damping_nms_per_rad: float = 0.0

    def __post_init__(self) -> None:
        if self.inertia_kg_m2 <= 0:
            raise ValueError("inertia_kg_m2 must be > 0")
        if self.stiffness_nm_per_rad <= 0:
            raise ValueError("stiffness_nm_per_rad must be > 0")
        if self.damping_nms_per_rad < 0:
            raise ValueError("damping must be >= 0")

    @property
    def natural_frequency_hz(self) -> float:
        return sqrt(self.stiffness_nm_per_rad / self.inertia_kg_m2) / (2 * pi)

    @property
    def beats_per_hour(self) -> float:
        # One full oscillation contains two beats.
        return 2.0 * self.natural_frequency_hz * 3600.0

    @property
    def damping_ratio(self) -> float:
        return self.damping_nms_per_rad / (
            2 * sqrt(self.stiffness_nm_per_rad * self.inertia_kg_m2)
        )

    def energy_j(self, angle_rad: float, angular_velocity_rad_s: float) -> float:
        potential = 0.5 * self.stiffness_nm_per_rad * angle_rad**2
        kinetic = 0.5 * self.inertia_kg_m2 * angular_velocity_rad_s**2
        return potential + kinetic


@dataclass(frozen=True)
class OscillatorState:
    angle_rad: float
    angular_velocity_rad_s: float


def step_semi_implicit(
    oscillator: BalanceSpring,
    state: OscillatorState,
    dt_s: float,
    external_torque_nm: float = 0.0,
) -> OscillatorState:
    """Semi-implicit Euler step; stable enough for coarse research sweeps."""
    if dt_s <= 0:
        raise ValueError("dt_s must be > 0")

    accel = (
        external_torque_nm
        - oscillator.damping_nms_per_rad * state.angular_velocity_rad_s
        - oscillator.stiffness_nm_per_rad * state.angle_rad
    ) / oscillator.inertia_kg_m2

    omega = state.angular_velocity_rad_s + accel * dt_s
    angle = state.angle_rad + omega * dt_s
    return OscillatorState(angle, omega)
