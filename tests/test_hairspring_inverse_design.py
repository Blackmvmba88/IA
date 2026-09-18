from research.hairspring.beam_bridge import estimate_from_spiral
from research.hairspring.design import (
    required_thickness_for_spiral_mm,
    target_rotational_stiffness_nm_per_rad,
)
from research.hairspring.geometry import SpiralSpec


def test_target_stiffness_increases_with_frequency_squared():
    a = target_rotational_stiffness_nm_per_rad(1e-9, 2.0)
    b = target_rotational_stiffness_nm_per_rad(1e-9, 4.0)
    assert abs(b/a - 4.0) < 1e-12


def test_inverse_design_closes_the_first_order_loop():
    spec = SpiralSpec(1.0, 0.30, 8.0, 128)
    thickness_mm = required_thickness_for_spiral_mm(
        spec=spec,
        spring_width_mm=0.10,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
        target_frequency_hz=4.0,
    )
    forward = estimate_from_spiral(
        spec=spec,
        spring_width_mm=0.10,
        spring_thickness_mm=thickness_mm,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
    )
    assert abs(forward.small_signal_frequency_hz - 4.0) < 1e-9


def test_reference_solution_is_physically_positive():
    spec = SpiralSpec(1.0, 0.30, 8.0, 128)
    thickness_mm = required_thickness_for_spiral_mm(
        spec, 0.10, 200.0, 1e-9, 4.0
    )
    assert 0.0 < thickness_mm < 1.0
