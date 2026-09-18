"""Mean-motion astronomical complication primitives.

These are mean-period mechanisms, not high-precision ephemerides.
For display synthesis:
    theta(t) = theta0 + 2*pi*t/P

A mechanical ratio approximates the period ratio with integer tooth counts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


DAY_S=86400.0
SYNODIC_MONTH_DAYS=29.530588853
TROPICAL_YEAR_DAYS=365.2421897


def phase_angle_rad(t_s:float,period_s:float,phase0_rad:float=0.0)->float:
    if period_s<=0:
        raise ValueError("period_s must be > 0")
    return (phase0_rad+2*pi*t_s/period_s)%(2*pi)


@dataclass(frozen=True)
class AstronomicalCycle:
    name:str
    period_days:float

    @property
    def period_s(self)->float:
        return self.period_days*DAY_S

    def angle_rad(self,t_s:float,phase0_rad:float=0.0)->float:
        return phase_angle_rad(t_s,self.period_s,phase0_rad)


MOON_PHASE=AstronomicalCycle("synodic-month",SYNODIC_MONTH_DAYS)
TROPICAL_YEAR=AstronomicalCycle("tropical-year",TROPICAL_YEAR_DAYS)


def cycle_error_days_after_elapsed(
    true_period_days:float,
    mechanical_period_days:float,
    elapsed_days:float,
)->float:
    """Equivalent phase error expressed as days of the true cycle."""
    if min(true_period_days,mechanical_period_days,elapsed_days)<=0:
        raise ValueError("all values must be > 0")
    true_cycles=elapsed_days/true_period_days
    mech_cycles=elapsed_days/mechanical_period_days
    phase_cycles=mech_cycles-true_cycles
    return phase_cycles*true_period_days
