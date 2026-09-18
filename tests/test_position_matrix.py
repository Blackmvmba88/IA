from research.oscillator.run_position_matrix import POSES, STATIC, build_reference_oscillator


def test_matrix_has_six_canonical_poses():
    assert set(POSES) == {"x+", "x-", "y+", "y-", "z+", "z-"}


def test_static_reference_is_zero_energy_cage():
    assert STATIC.rotational_energy_j() == 0.0
    assert STATIC.friction_power_w() == 0.0


def test_reference_oscillator_is_4hz():
    assert abs(build_reference_oscillator().natural_frequency_hz - 4.0) < 1e-12
