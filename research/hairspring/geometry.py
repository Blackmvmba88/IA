"""Deterministic planar hairspring centerline geometry.

H2 starts from an Archimedean spiral centerline:

    r(phi) = r0 + b*phi

with b chosen from the requested radial pitch per turn.

This module is geometric only. It does not claim that a planar centerline is a
complete model of a manufactured hairspring.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, hypot, pi, sin


Point2 = tuple[float, float]


@dataclass(frozen=True)
class SpiralSpec:
    inner_radius_mm: float
    radial_pitch_mm_per_turn: float
    turns: float
    samples_per_turn: int = 256

    def __post_init__(self) -> None:
        if self.inner_radius_mm <= 0:
            raise ValueError("inner_radius_mm must be > 0")
        if self.radial_pitch_mm_per_turn <= 0:
            raise ValueError("radial_pitch_mm_per_turn must be > 0")
        if self.turns <= 0:
            raise ValueError("turns must be > 0")
        if self.samples_per_turn < 16:
            raise ValueError("samples_per_turn must be >= 16")

    @property
    def outer_radius_mm(self) -> float:
        return self.inner_radius_mm + self.radial_pitch_mm_per_turn*self.turns

    @property
    def b_mm_per_rad(self) -> float:
        return self.radial_pitch_mm_per_turn/(2*pi)


def centerline_points(spec: SpiralSpec) -> list[Point2]:
    count = max(2, int(round(spec.turns*spec.samples_per_turn)) + 1)
    end_phi = 2*pi*spec.turns
    pts: list[Point2] = []
    for i in range(count):
        phi = end_phi*i/(count-1)
        r = spec.inner_radius_mm + spec.b_mm_per_rad*phi
        pts.append((r*cos(phi), r*sin(phi)))
    return pts


def polyline_length_mm(points: list[Point2]) -> float:
    if len(points) < 2:
        raise ValueError("at least two points required")
    return sum(
        hypot(b[0]-a[0], b[1]-a[1])
        for a, b in zip(points[:-1], points[1:])
    )


def centerline_centroid_mm(points: list[Point2]) -> Point2:
    if not points:
        raise ValueError("points required")
    return (
        sum(p[0] for p in points)/len(points),
        sum(p[1] for p in points)/len(points),
    )


def radial_gap_mm(spec: SpiralSpec) -> float:
    """Nominal centerline-to-centerline radial separation between adjacent turns."""
    return spec.radial_pitch_mm_per_turn


def edge_gap_mm(spec: SpiralSpec, spring_width_mm: float) -> float:
    if spring_width_mm <= 0:
        raise ValueError("spring_width_mm must be > 0")
    return radial_gap_mm(spec)-spring_width_mm


def write_ascii_dxf_polyline(path: str, points: list[Point2]) -> None:
    """Write a minimal deterministic R12-style open POLYLINE in millimetres."""
    if len(points) < 2:
        raise ValueError("at least two points required")

    lines = [
        "0", "SECTION", "2", "HEADER",
        "9", "$INSUNITS", "70", "4",
        "0", "ENDSEC",
        "0", "SECTION", "2", "ENTITIES",
        "0", "POLYLINE", "8", "HAIRSPRING", "66", "1", "70", "0",
    ]
    for x, y in points:
        lines += [
            "0", "VERTEX", "8", "HAIRSPRING",
            "10", f"{x:.9f}",
            "20", f"{y:.9f}",
            "30", "0.000000000",
        ]
    lines += [
        "0", "SEQEND",
        "0", "ENDSEC",
        "0", "EOF",
    ]
    with open(path, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
