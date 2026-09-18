from math import pi

from research.time_synthesis.astronomy import MOON_PHASE,phase_angle_rad
from research.time_synthesis.frames import apply,compose,rotation_z,translation
from research.time_synthesis.gear_geometry import SpurGearSpec,center_distance_mm
from research.time_synthesis.geartrain import (
    angular_velocity_from_period,
    external_mesh_omega,
    required_single_mesh_ratio,
)
from research.time_synthesis.synthesize import canonical_time_state


def test_seconds_minutes_hours_periods():
    state=canonical_time_state(60.0)
    assert abs(state.seconds_angle_rad-0.0)<1e-12
    assert abs(state.minutes_angle_rad-(2*pi/60.0))<1e-12
    assert abs(state.hours_angle_rad-(2*pi/720.0))<1e-12


def test_external_mesh_reverses_and_scales_speed():
    w=angular_velocity_from_period(60.0)
    out=external_mesh_omega(w,20,60)
    assert out<0
    assert abs(abs(out)-w/3.0)<1e-12


def test_period_ratio_is_tooth_ratio_for_one_mesh():
    assert required_single_mesh_ratio(60.0,3600.0)==60.0


def test_standard_center_distance():
    a=SpurGearSpec(20,0.2)
    b=SpurGearSpec(60,0.2)
    assert abs(center_distance_mm(a,b)-8.0)<1e-12


def test_frame_composition_translates_rotated_point():
    T=compose(translation(10,0,0),rotation_z(pi/2))
    x,y,z=apply(T,(1,0,0))
    assert abs(x-10.0)<1e-12
    assert abs(y-1.0)<1e-12
    assert abs(z)<1e-12


def test_moon_phase_repeats_after_one_mean_cycle():
    assert abs(MOON_PHASE.angle_rad(MOON_PHASE.period_s))<1e-10
