from math import pi

from research.oscillator.model import BalanceSpring, OscillatorState, step_semi_implicit
from research.oscillator.simulate import simulate
from research.escapement.lever import LeverEscapement


def test_frequency_relation_hits_4hz():
    inertia = 1e-9
    stiffness = (2 * pi * 4.0) ** 2 * inertia
    osc = BalanceSpring(inertia, stiffness)
    assert abs(osc.natural_frequency_hz - 4.0) < 1e-12
    assert abs(osc.beats_per_hour - 28800.0) < 1e-8


def test_damped_oscillator_loses_energy_without_impulses():
    inertia = 1e-9
    stiffness = (2 * pi * 4.0) ** 2 * inertia
    osc = BalanceSpring(inertia, stiffness, damping_nms_per_rad=2e-9)
    state = OscillatorState(angle_rad=0.4, angular_velocity_rad_s=0.0)
    e0 = osc.energy_j(state.angle_rad, state.angular_velocity_rad_s)
    for _ in range(4000):
        state = step_semi_implicit(osc, state, 0.0005)
    e1 = osc.energy_j(state.angle_rad, state.angular_velocity_rad_s)
    assert e1 < e0


def test_escapement_delivers_impulses():
    inertia = 1e-9
    stiffness = (2 * pi * 4.0) ** 2 * inertia
    osc = BalanceSpring(inertia, stiffness, damping_nms_per_rad=3e-10)
    esc = LeverEscapement(
        impulse_energy_j=1e-10,
        unlock_angle_rad=0.08,
        dead_time_s=0.02,
    )
    result = simulate(
        osc,
        esc,
        OscillatorState(angle_rad=0.4, angular_velocity_rad_s=0.0),
        duration_s=2.0,
        dt_s=0.0005,
    )
    assert result.impulses > 4
    assert max(abs(a) for a in result.angles_rad) > 0.1
