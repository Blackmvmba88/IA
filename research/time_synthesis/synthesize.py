"""A canonical time-synthesis state.

The mechanism does not 'know the time' directly.
It transports phase.

Oscillator:
    phi_osc(t)=2*pi*f*t

Escapement:
    quantizes oscillator motion into tooth-release events

Gear train:
    scales angular velocity

Displays:
    map shaft angles into visual coordinates
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi

from research.time_synthesis.astronomy import MOON_PHASE,TROPICAL_YEAR,phase_angle_rad


@dataclass(frozen=True)
class TimeState:
    seconds_angle_rad:float
    minutes_angle_rad:float
    hours_angle_rad:float
    moon_angle_rad:float
    year_angle_rad:float


def canonical_time_state(t_s:float)->TimeState:
    if t_s<0:
        raise ValueError("t_s must be >= 0")
    return TimeState(
        seconds_angle_rad=phase_angle_rad(t_s,60.0),
        minutes_angle_rad=phase_angle_rad(t_s,3600.0),
        hours_angle_rad=phase_angle_rad(t_s,43200.0),
        moon_angle_rad=MOON_PHASE.angle_rad(t_s),
        year_angle_rad=TROPICAL_YEAR.angle_rad(t_s),
    )


def hand_tip_xy(radius_mm:float,angle_rad:float)->tuple[float,float]:
    """12 o'clock is zero; clockwise is positive."""
    if radius_mm<=0:
        raise ValueError("radius_mm must be > 0")
    return (
        radius_mm*__import__("math").sin(angle_rad),
        radius_mm*__import__("math").cos(angle_rad),
    )
