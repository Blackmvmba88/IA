"""Simple epicyclic/planetary kinematics using Willis' relation.

For a simple sun-ring-carrier set:

    (omega_s - omega_c) / (omega_r - omega_c) = -N_r / N_s

Equivalent linear form:

    N_s*omega_s + N_r*omega_r = (N_s+N_r)*omega_c

This is a foundational relation for differentials, astronomical indications
and rotating-carrier mechanisms. It does not imply that every tourbillon is a
simple planetary train.
"""

from __future__ import annotations


def carrier_speed(
    teeth_sun:int,
    teeth_ring:int,
    omega_sun:float,
    omega_ring:float,
)->float:
    if teeth_sun<=0 or teeth_ring<=0:
        raise ValueError("tooth counts must be positive")
    return (
        teeth_sun*omega_sun + teeth_ring*omega_ring
    )/(teeth_sun+teeth_ring)


def ring_speed(
    teeth_sun:int,
    teeth_ring:int,
    omega_sun:float,
    omega_carrier:float,
)->float:
    if teeth_sun<=0 or teeth_ring<=0:
        raise ValueError("tooth counts must be positive")
    return (
        (teeth_sun+teeth_ring)*omega_carrier
        - teeth_sun*omega_sun
    )/teeth_ring


def sun_speed(
    teeth_sun:int,
    teeth_ring:int,
    omega_ring:float,
    omega_carrier:float,
)->float:
    if teeth_sun<=0 or teeth_ring<=0:
        raise ValueError("tooth counts must be positive")
    return (
        (teeth_sun+teeth_ring)*omega_carrier
        - teeth_ring*omega_ring
    )/teeth_sun


def willis_residual(
    teeth_sun:int,
    teeth_ring:int,
    omega_sun:float,
    omega_ring:float,
    omega_carrier:float,
)->float:
    return (
        teeth_sun*omega_sun
        + teeth_ring*omega_ring
        - (teeth_sun+teeth_ring)*omega_carrier
    )
