"""Reduced-order balance + hairspring model for BPME research.

The oscillator supports both the linear H0 model and the nonlinear H1 model:

    I * theta_ddot + c * theta_dot + k1*theta + k3*theta^3 = tau_ext

Set k3=0 to recover the original linear oscillator.

This is intentionally a reduced-order model. Real chronometry also depends on
hairspring geometry, escapement contact, pivot friction, temperature, shock and
measured positional error maps.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi, sqrt


@dataclass(frozen=True)
class BalanceSpring:
    inertia_kg_m2: float
    stiffness_nm_per_rad: float
    damping_nms_per_rad: float = 0.0
    cubic_stiffness_nm_per_rad3: float = 0.0

    def __post_init__(self) -> None:
        if self.inertia_kg_m2 <= 0 or not isfinite(self.inertia_kg_m2):
            raise ValueError("inertia_kg_m2 must be positive and finite")
        if self.stiffness_nm_per_rad <= 0 or not isfinite(self.stiffness_nm_per_rad):
            raise ValueError("stiffness_nm_per_rad must be positive and finite")
        if self.damping_nms_per_rad < 0 or not isfinite(self.damping_nms_per_rad):
            raise ValueError("damping must be finite and >= 0")
        if not isfinite(self.cubic_stiffness_nm_per_rad3):
            raise ValueError("cubic stiffness must be finite")

    @property
    def natural_frequency_hz(self) -> float:
        """Small-signal frequency around theta=0."""
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

    def restoring_torque_nm(self, angle_rad: float) -> float:
        """Return spring torque opposing displacement."""
        return -(
            self.stiffness_nm_per_rad * angle_rad
            + self.cubic_stiffness_nm_per_rad3 * angle_rad**3
        )

    def potential_energy_j(self, angle_rad: float) -> float:
        return (
            0.5 * self.stiffness_nm_per_rad * angle_rad**2
            + 0.25 * self.cubic_stiffness_nm_per_rad3 * angle_rad**4
        )

    def energy_j(self, angle_rad: float, angular_velocity_rad_s: float) -> float:
        kinetic = 0.5 * self.inertia_kg_m2 * angular_velocity_rad_s**2
        return self.potential_energy_j(angle_rad) + kinetic


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
        + oscillator.restoring_torque_nm(state.angle_rad)
    ) / oscillator.inertia_kg_m2

    omega = state.angular_velocity_rad_s + accel * dt_s
    angle = state.angle_rad + omega * dt_s
    return OscillatorState(angle, omega)
