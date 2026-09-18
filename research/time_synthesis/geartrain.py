"""Kinematic primitives for mechanical time synthesis.

A watch train is an angular-frequency transformer.

For one external spur-gear mesh:
    omega_out = -omega_in * z_in / z_out

The sign changes because external gears rotate in opposite directions.
Magnitude controls the time scale.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import pi


TAU = 2.0*pi


def angular_velocity_from_period(period_s: float) -> float:
    if period_s <= 0:
        raise ValueError("period_s must be > 0")
    return TAU/period_s


def period_from_angular_velocity(omega_rad_s: float) -> float:
    if omega_rad_s == 0:
        raise ValueError("omega_rad_s must be non-zero")
    return TAU/abs(omega_rad_s)


def external_mesh_omega(
    omega_in_rad_s: float,
    teeth_in: int,
    teeth_out: int,
) -> float:
    if teeth_in <= 0 or teeth_out <= 0:
        raise ValueError("tooth counts must be positive")
    return -omega_in_rad_s*(teeth_in/teeth_out)


def required_single_mesh_ratio(period_in_s: float, period_out_s: float) -> float:
    """Return z_out/z_in required for one external mesh by magnitude."""
    if period_in_s <= 0 or period_out_s <= 0:
        raise ValueError("periods must be > 0")
    return period_out_s/period_in_s


@dataclass(frozen=True)
class GearPair:
    teeth_in: int
    teeth_out: int

    @property
    def ratio_out_over_in(self) -> float:
        return self.teeth_out/self.teeth_in

    @property
    def signed_speed_ratio(self) -> float:
        return -self.teeth_in/self.teeth_out


def best_single_mesh_pair(
    target_period_ratio: float,
    min_teeth: int = 12,
    max_teeth: int = 120,
) -> GearPair:
    """Find integer teeth minimizing |z_out/z_in - target_period_ratio|."""
    if target_period_ratio <= 0:
        raise ValueError("target_period_ratio must be > 0")
    if min_teeth < 6 or max_teeth < min_teeth:
        raise ValueError("invalid tooth bounds")

    best: tuple[float, GearPair] | None = None
    for zin in range(min_teeth, max_teeth+1):
        for zout in range(min_teeth, max_teeth+1):
            pair=GearPair(zin,zout)
            err=abs(pair.ratio_out_over_in-target_period_ratio)
            if best is None or err<best[0]:
                best=(err,pair)
    assert best is not None
    return best[1]


def rational_ratio(target: float, max_denominator: int = 1000) -> Fraction:
    if target <= 0:
        raise ValueError("target must be > 0")
    return Fraction(target).limit_denominator(max_denominator)


@dataclass(frozen=True)
class CompoundStage:
    """One input gear drives one output gear; next stage may share the output shaft."""
    teeth_driver: int
    teeth_driven: int

    @property
    def signed_speed_ratio(self) -> float:
        return -self.teeth_driver/self.teeth_driven


def compound_speed_ratio(stages: tuple[CompoundStage, ...]) -> float:
    ratio=1.0
    for s in stages:
        ratio*=s.signed_speed_ratio
    return ratio
