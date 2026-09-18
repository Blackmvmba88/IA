from research.hairspring.beam_bridge import (
    rectangular_second_moment_m4,
    rotational_stiffness_nm_per_rad,
    estimate_from_spiral,
)
from research.hairspring.geometry import SpiralSpec


def test_rectangular_section_scales_with_thickness_cubed():
    a = rectangular_second_moment_m4(1e-4, 2e-5)
    b = rectangular_second_moment_m4(1e-4, 4e-5)
    assert abs(b/a - 8.0) < 1e-12


def test_rotational_stiffness_scales_linearly_with_E():
    a = rotational_stiffness_nm_per_rad(100e9, 1e-4, 2e-5, 0.1)
    b = rotational_stiffness_nm_per_rad(200e9, 1e-4, 2e-5, 0.1)
    assert abs(b/a - 2.0) < 1e-12


def test_longer_spring_is_softer_in_first_order_model():
    short = rotational_stiffness_nm_per_rad(200e9, 1e-4, 2e-5, 0.05)
    long = rotational_stiffness_nm_per_rad(200e9, 1e-4, 2e-5, 0.10)
    assert long < short


def test_geometry_bridge_returns_positive_frequency():
    spec = SpiralSpec(1.0, 0.30, 8.0, 64)
    result = estimate_from_spiral(
        spec,
        spring_width_mm=0.10,
        spring_thickness_mm=0.03,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
    )
    assert result.active_length_m > 0
    assert result.stiffness_nm_per_rad > 0
    assert result.small_signal_frequency_hz > 0
    assert result.beats_per_hour > 0
