from research.tourbillon.model import (
    CageAxis,
    TourbillonTopology,
    first_order_bias_proxy,
    sphere_coverage_fraction,
)


def _classic() -> TourbillonTopology:
    return TourbillonTopology(
        name="classic",
        axes=(CageAxis((0.0, 0.0, 1.0), 60.0),),
        cage_inertia_kg_m2=1e-9,
        friction_torque_nm=1e-8,
    )


def _biaxial() -> TourbillonTopology:
    return TourbillonTopology(
        name="biaxial",
        axes=(
            CageAxis((1.0, 0.0, 0.0), 60.0),
            CageAxis((0.0, 1.0, 0.0), 137.0),
        ),
        cage_inertia_kg_m2=1e-9,
        friction_torque_nm=1e-8,
    )


def test_classical_cage_averages_linear_radial_bias_over_full_turn():
    v = first_order_bias_proxy(_classic(), 60.0, (1.0, 0.0, 0.0), samples=721)
    assert abs(v) < 0.01


def test_biaxial_normal_explores_more_spherical_bins_than_classical():
    classical = sphere_coverage_fraction(_classic(), 600.0, samples=1440)
    biaxial = sphere_coverage_fraction(_biaxial(), 600.0, samples=1440)
    assert biaxial > classical
