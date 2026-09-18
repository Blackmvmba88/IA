"""Time-dependent vectors for resolved TOKYO displays."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos,pi,sin

TAU=2*pi


@dataclass(frozen=True)
class DisplayPose:
    id:str
    angle_rad:float
    position_mm:tuple[float,float,float]
    radial_unit:tuple[float,float,float]
    tangent_unit:tuple[float,float,float]


def phase_angle(t_s:float,period_s:float,phase0_rad:float=0.0)->float:
    if period_s<=0:
        raise ValueError("period_s must be > 0")
    return (phase0_rad+TAU*t_s/period_s)%TAU


def display_pose(
    id_:str,
    t_s:float,
    period_s:float,
    radius_mm:float,
    z_mm:float,
    phase0_rad:float=0.0,
)->DisplayPose:
    if radius_mm<0:
        raise ValueError("radius_mm must be >= 0")
    a=phase_angle(t_s,period_s,phase0_rad)
    c,s=cos(a),sin(a)
    return DisplayPose(
        id=id_,
        angle_rad=a,
        position_mm=(radius_mm*c,radius_mm*s,z_mm),
        radial_unit=(c,s,0.0),
        tangent_unit=(-s,c,0.0),
    )
