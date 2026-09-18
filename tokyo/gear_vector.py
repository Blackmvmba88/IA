"""Convert a resolved gear stage into deterministic pitch geometry."""

from __future__ import annotations

from dataclasses import dataclass

from research.time_synthesis.gear_geometry import SpurGearSpec,center_distance_mm


@dataclass(frozen=True)
class GearStageGeometry:
    driver_teeth:int
    driven_teeth:int
    driver_pitch_diameter_mm:float
    driven_pitch_diameter_mm:float
    center_distance_mm:float


def resolve_stage_geometry(
    driver:int,
    driven:int,
    module_mm:float,
    pressure_angle_deg:float=20.0,
)->GearStageGeometry:
    a=SpurGearSpec(driver,module_mm,pressure_angle_deg)
    b=SpurGearSpec(driven,module_mm,pressure_angle_deg)
    return GearStageGeometry(
        driver_teeth=driver,
        driven_teeth=driven,
        driver_pitch_diameter_mm=2*a.pitch_radius_mm,
        driven_pitch_diameter_mm=2*b.pitch_radius_mm,
        center_distance_mm=center_distance_mm(a,b),
    )
