"""Inverse first-order hairspring design helpers.

These functions invert the H2 beam approximation. They are useful for creating
starting candidates that later must be refined by H3/H4 analysis and measurement.
"""

from __future__ import annotations

from math import pi

from research.hairspring.geometry import SpiralSpec, centerline_points, polyline_length_mm


def target_rotational_stiffness_nm_per_rad(
    balance_inertia_kg_m2: float,
    target_frequency_hz: float,
) -> float:
    if balance_inertia_kg_m2 <= 0 or target_frequency_hz <= 0:
        raise ValueError("balance inertia and target frequency must be > 0")
    return balance_inertia_kg_m2 * (2*pi*target_frequency_hz)**2


def required_thickness_m(
    target_stiffness_nm_per_rad: float,
    youngs_modulus_pa: float,
    width_m: float,
    active_length_m: float,
) -> float:
    """Solve h from K=(E*b*h^3/12)/L."""
    if min(
        target_stiffness_nm_per_rad,
        youngs_modulus_pa,
        width_m,
        active_length_m,
    ) <= 0:
        raise ValueError("all inputs must be > 0")

    return (
        12.0
        * target_stiffness_nm_per_rad
        * active_length_m
        / (youngs_modulus_pa * width_m)
    ) ** (1.0/3.0)


def required_thickness_for_spiral_mm(
    spec: SpiralSpec,
    spring_width_mm: float,
    youngs_modulus_gpa: float,
    balance_inertia_kg_m2: float,
    target_frequency_hz: float,
) -> float:
    if spring_width_mm <= 0 or youngs_modulus_gpa <= 0:
        raise ValueError("width and Young modulus must be > 0")

    length_m = polyline_length_mm(centerline_points(spec))/1000.0
    k_target = target_rotational_stiffness_nm_per_rad(
        balance_inertia_kg_m2,
        target_frequency_hz,
    )
    thickness_m = required_thickness_m(
        target_stiffness_nm_per_rad=k_target,
        youngs_modulus_pa=youngs_modulus_gpa*1e9,
        width_m=spring_width_mm/1000.0,
        active_length_m=length_m,
    )
    return thickness_m*1000.0
