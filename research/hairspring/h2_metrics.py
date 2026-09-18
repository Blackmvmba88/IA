"""Geometry metrics for H2 hairspring experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from research.hairspring.geometry import (
    SpiralSpec,
    centerline_centroid_mm,
    centerline_points,
    edge_gap_mm,
    polyline_length_mm,
)


@dataclass(frozen=True)
class H2Metrics:
    inner_radius_mm: float
    outer_radius_mm: float
    turns: float
    active_length_mm: float
    centerline_centroid_x_mm: float
    centerline_centroid_y_mm: float
    edge_gap_mm: float
    point_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate(spec: SpiralSpec, spring_width_mm: float) -> H2Metrics:
    points = centerline_points(spec)
    cx, cy = centerline_centroid_mm(points)
    return H2Metrics(
        inner_radius_mm=spec.inner_radius_mm,
        outer_radius_mm=spec.outer_radius_mm,
        turns=spec.turns,
        active_length_mm=polyline_length_mm(points),
        centerline_centroid_x_mm=cx,
        centerline_centroid_y_mm=cy,
        edge_gap_mm=edge_gap_mm(spec, spring_width_mm),
        point_count=len(points),
    )
