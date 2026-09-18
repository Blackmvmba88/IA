"""Parametric spur-gear geometry for BPME.

Standard reference geometry:
    pitch_radius = m*z/2
    base_radius  = pitch_radius*cos(alpha)
    addendum     = m
    dedendum     = 1.25*m   (reference full-depth system)

The involute of the base circle is:
    x(u) = rb*(cos(u) + u*sin(u))
    y(u) = rb*(sin(u) - u*cos(u))

This module generates geometry only; manufacturing allowances belong elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin, sqrt


@dataclass(frozen=True)
class SpurGearSpec:
    teeth: int
    module_mm: float
    pressure_angle_deg: float = 20.0
    face_width_mm: float = 2.0

    def __post_init__(self) -> None:
        if self.teeth < 6:
            raise ValueError("teeth must be >= 6")
        if self.module_mm <= 0 or self.face_width_mm <= 0:
            raise ValueError("module and face width must be > 0")
        if not (10.0 <= self.pressure_angle_deg <= 35.0):
            raise ValueError("pressure angle outside research bounds")

    @property
    def pitch_radius_mm(self) -> float:
        return self.module_mm*self.teeth/2.0

    @property
    def pressure_angle_rad(self) -> float:
        return self.pressure_angle_deg*pi/180.0

    @property
    def base_radius_mm(self) -> float:
        return self.pitch_radius_mm*cos(self.pressure_angle_rad)

    @property
    def addendum_radius_mm(self) -> float:
        return self.pitch_radius_mm+self.module_mm

    @property
    def root_radius_mm(self) -> float:
        return max(
            0.0,
            self.pitch_radius_mm-1.25*self.module_mm,
        )

    @property
    def circular_pitch_mm(self) -> float:
        return pi*self.module_mm

    @property
    def nominal_tooth_thickness_mm(self) -> float:
        return self.circular_pitch_mm/2.0


def center_distance_mm(a: SpurGearSpec, b: SpurGearSpec) -> float:
    if abs(a.module_mm-b.module_mm)>1e-12:
        raise ValueError("meshing gears must use the same module")
    if abs(a.pressure_angle_deg-b.pressure_angle_deg)>1e-12:
        raise ValueError("meshing gears must use the same pressure angle")
    return a.pitch_radius_mm+b.pitch_radius_mm


def involute_parameter_for_radius(base_radius_mm: float, radius_mm: float) -> float:
    if radius_mm < base_radius_mm:
        raise ValueError("involute does not exist below the base circle")
    return sqrt((radius_mm/base_radius_mm)**2-1.0)


def involute_xy(base_radius_mm: float, u: float) -> tuple[float,float]:
    return (
        base_radius_mm*(cos(u)+u*sin(u)),
        base_radius_mm*(sin(u)-u*cos(u)),
    )


def involute_flank_points(
    gear: SpurGearSpec,
    samples: int = 32,
) -> list[tuple[float,float]]:
    if samples < 2:
        raise ValueError("samples must be >= 2")
    rb=gear.base_radius_mm
    ra=gear.addendum_radius_mm
    u_max=involute_parameter_for_radius(rb,ra)
    return [
        involute_xy(rb,u_max*i/(samples-1))
        for i in range(samples)
    ]
