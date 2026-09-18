"""Simple deterministic radial/axial layout model."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos,sin,pi


@dataclass(frozen=True)
class DisplayNode:
    id:str
    radius_mm:float
    z_mm:float
    phase_rad:float=0.0


def polar_position(node:DisplayNode)->tuple[float,float,float]:
    return (
        node.radius_mm*cos(node.phase_rad),
        node.radius_mm*sin(node.phase_rad),
        node.z_mm,
    )


def evenly_spaced_nodes(
    ids:list[str],
    radius_mm:float,
    z_mm:float,
)->list[DisplayNode]:
    if radius_mm<=0:
        raise ValueError("radius_mm must be > 0")
    n=len(ids)
    if n==0:
        return []
    return [
        DisplayNode(
            id=id_,
            radius_mm=radius_mm,
            z_mm=z_mm,
            phase_rad=2*pi*i/n,
        )
        for i,id_ in enumerate(ids)
    ]
