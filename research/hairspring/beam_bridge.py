"""First-order bridge from hairspring geometry to oscillator stiffness.

For a thin flat spiral strip under a nearly uniform bending moment, a useful
first approximation is:

    K_theta ~= E * I_section / L

with rectangular-section second moment:

    I_section = width * thickness^3 / 12

This is an engineering estimate, not a replacement for nonlinear beam analysis,
FEA, attachment effects or calibration from a manufactured spring.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt

from research.hairspring.geometry import SpiralSpec, centerline_points, polyline_length_mm


def rectangular_second_moment_m4(width_m: float, thickness_m: float) -> float:
    if width_m <= 0 or thickness_m <= 0:
        raise ValueError("width and thickness must be > 0")
    return width_m * thickness_m**3 / 12.0


def rotational_stiffness_nm_per_rad(
    youngs_modulus_pa: float,
    width_m: float,
    thickness_m: float,
    active_length_m: float,
) -> float:
    if youngs_modulus_pa <= 0 or active_length_m <= 0:
        raise ValueError("E and active length must be > 0")
    section_i = rectangular_second_moment_m4(width_m, thickness_m)
    return youngs_modulus_pa * section_i / active_length_m


@dataclass(frozen=True)
class GeometryFrequencyEstimate:
    active_length_m: float
    section_second_moment_m4: float
    stiffness_nm_per_rad: float
    small_signal_frequency_hz: float
    beats_per_hour: float


def estimate_from_spiral(
    spec: SpiralSpec,
    spring_width_mm: float,
    spring_thickness_mm: float,
    youngs_modulus_gpa: float,
    balance_inertia_kg_m2: float,
) -> GeometryFrequencyEstimate:
    if balance_inertia_kg_m2 <= 0:
        raise ValueError("balance inertia must be > 0")

    length_m = polyline_length_mm(centerline_points(spec)) / 1000.0
    width_m = spring_width_mm / 1000.0
    thickness_m = spring_thickness_mm / 1000.0
    e_pa = youngs_modulus_gpa * 1e9

    section_i = rectangular_second_moment_m4(width_m, thickness_m)
    stiffness = rotational_stiffness_nm_per_rad(
        e_pa, width_m, thickness_m, length_m
    )
    frequency = sqrt(stiffness / balance_inertia_kg_m2) / (2*pi)

    return GeometryFrequencyEstimate(
        active_length_m=length_m,
        section_second_moment_m4=section_i,
        stiffness_nm_per_rad=stiffness,
        small_signal_frequency_hz=frequency,
        beats_per_hour=2*frequency*3600.0,
    )
