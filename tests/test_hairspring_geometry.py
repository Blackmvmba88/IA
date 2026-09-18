from pathlib import Path

from research.hairspring.geometry import (
    SpiralSpec,
    centerline_points,
    edge_gap_mm,
    polyline_length_mm,
    write_ascii_dxf_polyline,
)
from research.hairspring.h2_metrics import evaluate


def test_reference_spiral_hits_requested_outer_radius():
    spec = SpiralSpec(1.0, 0.30, 8.0, 64)
    assert abs(spec.outer_radius_mm - 3.4) < 1e-12
    points = centerline_points(spec)
    x, y = points[-1]
    assert abs((x*x+y*y)**0.5 - 3.4) < 1e-9


def test_more_turns_produce_longer_active_length():
    short = centerline_points(SpiralSpec(1.0, 0.30, 4.0, 64))
    long = centerline_points(SpiralSpec(1.0, 0.30, 8.0, 64))
    assert polyline_length_mm(long) > polyline_length_mm(short)


def test_edge_gap_is_pitch_minus_width():
    spec = SpiralSpec(1.0, 0.30, 8.0, 64)
    assert abs(edge_gap_mm(spec, 0.10) - 0.20) < 1e-12


def test_metrics_are_deterministic():
    spec = SpiralSpec(1.0, 0.30, 8.0, 64)
    a = evaluate(spec, 0.10)
    b = evaluate(spec, 0.10)
    assert a == b


def test_dxf_export_contains_polyline(tmp_path: Path):
    spec = SpiralSpec(1.0, 0.30, 1.0, 32)
    path = tmp_path/"spring.dxf"
    write_ascii_dxf_polyline(str(path), centerline_points(spec))
    text = path.read_text(encoding="ascii")
    assert "POLYLINE" in text
    assert "VERTEX" in text
    assert text.endswith("EOF\n")
