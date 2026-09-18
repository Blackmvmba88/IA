from math import isclose

from research.tourbillon.model import CageAxis, TourbillonTopology, rotate, sweep_statistics


def test_rodrigues_quarter_turn():
    v = rotate((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.5707963267948966)
    assert isclose(v[0], 0.0, abs_tol=1e-9)
    assert isclose(v[1], 1.0, abs_tol=1e-9)


def test_energy_and_friction_are_positive():
    t = TourbillonTopology(
        name="test",
        axes=(CageAxis((1.0, 0.0, 0.0), 60.0),),
        cage_inertia_kg_m2=1e-9,
        friction_torque_nm=1e-8,
    )
    stats = sweep_statistics(t, 60.0, 100)
    assert stats["rotational_energy_j"] > 0
    assert stats["friction_power_w"] > 0
    assert stats["projection_span"] > 1.9
