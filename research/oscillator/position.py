"""Position/gravity coupling for balance-oscillator research.

The perturbation represents a small center-of-mass offset of the oscillator.
A radial offset vector is carried by the tourbillon cage(s), then rotated by
the instantaneous balance angle. Gravity acting on that offset produces a
torque about the current balance axis.

This remains a reduced-order model: torque_scale_nm bundles mass * g * offset.
"""

from __future__ import annotations

from research.tourbillon.model import TourbillonTopology, Vector, _dot, _unit, rotate


def _cross(a: Vector, b: Vector) -> Vector:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def gravity_torque_nm(
    topology: TourbillonTopology,
    t_s: float,
    balance_angle_rad: float,
    gravity_hat: Vector,
    torque_scale_nm: float,
) -> float:
    """Torque around balance axis from a carried radial CG-offset vector."""
    if torque_scale_nm < 0:
        raise ValueError("torque_scale_nm must be >= 0")

    g = _unit(gravity_hat)
    balance_axis = topology.regulator_normal(t_s)
    radial_zero = topology.asymmetry_vector(t_s)
    radial = rotate(radial_zero, balance_axis, balance_angle_rad)

    # Torque direction is r x F; project onto current balance axis.
    signed_geometry = _dot(_cross(radial, g), balance_axis)
    return torque_scale_nm * signed_geometry
