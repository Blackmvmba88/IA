from math import pi

from research.escapement.lever import LeverEscapement
from research.oscillator.coupled import simulate_coupled
from research.oscillator.model import BalanceSpring, OscillatorState
from research.oscillator.position import gravity_torque_nm
from research.tourbillon.model import CageAxis, TourbillonTopology


def static_topology() -> TourbillonTopology:
    return TourbillonTopology(
        name="static",
        axes=(),
        cage_inertia_kg_m2=0.0,
        friction_torque_nm=0.0,
    )


def classic_topology() -> TourbillonTopology:
    return TourbillonTopology(
        name="classic",
        axes=(CageAxis((0.0, 0.0, 1.0), 60.0),),
        cage_inertia_kg_m2=1e-9,
        friction_torque_nm=1e-8,
    )


def test_gravity_torque_zero_when_gravity_parallel_to_balance_axis():
    tau = gravity_torque_nm(
        static_topology(),
        t_s=0.0,
        balance_angle_rad=0.3,
        gravity_hat=(0.0, 0.0, -1.0),
        torque_scale_nm=1e-10,
    )
    assert abs(tau) < 1e-20


def test_coupled_simulation_reports_frequency():
    inertia = 1e-9
    stiffness = (2*pi*4.0)**2 * inertia
    osc = BalanceSpring(inertia, stiffness, damping_nms_per_rad=3e-10)
    esc = LeverEscapement(1e-10, 0.08, 0.02)
    result = simulate_coupled(
        oscillator=osc,
        escapement=esc,
        topology=classic_topology(),
        initial=OscillatorState(0.4, 0.0),
        duration_s=4.0,
        dt_s=0.0005,
        gravity_hat=(1.0, 0.0, 0.0),
        gravity_torque_scale_nm=1e-10,
    )
    assert result.estimated_frequency_hz is not None
    assert 3.5 < result.estimated_frequency_hz < 4.5
    assert result.zero_crossings > 20
