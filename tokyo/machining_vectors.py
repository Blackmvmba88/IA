"""Translate design vectors into setup/machine coordinates.

TOKYO keeps the transform chain explicit:

    p_machine =
        T_machine_setup
        @ T_setup_part
        @ p_part

Vectors use rotation only; points use rotation + translation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from research.time_synthesis.frames import Matrix4,apply,compose


Vector3=tuple[float,float,float]


def transform_vector(T:Matrix4,v:Vector3)->Vector3:
    x,y,z=v
    return (
        T[0][0]*x+T[0][1]*y+T[0][2]*z,
        T[1][0]*x+T[1][1]*y+T[1][2]*z,
        T[2][0]*x+T[2][1]*y+T[2][2]*z,
    )


def unit(v:Vector3)->Vector3:
    n=sqrt(v[0]**2+v[1]**2+v[2]**2)
    if n==0:
        raise ValueError("zero vector")
    return (v[0]/n,v[1]/n,v[2]/n)


@dataclass(frozen=True)
class MachinePose:
    point_mm:Vector3
    radial_unit:Vector3
    tangent_unit:Vector3
    tool_axis_unit:Vector3


def to_machine_pose(
    point_part_mm:Vector3,
    radial_part:Vector3,
    tangent_part:Vector3,
    tool_axis_part:Vector3,
    T_machine_setup:Matrix4,
    T_setup_part:Matrix4,
)->MachinePose:
    T=compose(T_machine_setup,T_setup_part)
    return MachinePose(
        point_mm=apply(T,point_part_mm),
        radial_unit=unit(transform_vector(T,radial_part)),
        tangent_unit=unit(transform_vector(T,tangent_part)),
        tool_axis_unit=unit(transform_vector(T,tool_axis_part)),
    )
