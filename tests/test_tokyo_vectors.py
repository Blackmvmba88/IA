from math import pi

from research.time_synthesis.frames import rotation_z,translation
from tokyo.gear_vector import resolve_stage_geometry
from tokyo.machining_vectors import to_machine_pose
from tokyo.vector_field import display_pose


def test_display_pose_quarter_cycle():
    p=display_pose("x",15.0,60.0,10.0,2.0)
    assert abs(p.position_mm[0])<1e-12
    assert abs(p.position_mm[1]-10.0)<1e-12
    assert p.position_mm[2]==2.0
    assert abs(p.tangent_unit[0]+1.0)<1e-12


def test_machine_pose_translation_and_rotation():
    p=to_machine_pose(
        point_part_mm=(1.0,0.0,0.0),
        radial_part=(1.0,0.0,0.0),
        tangent_part=(0.0,1.0,0.0),
        tool_axis_part=(0.0,0.0,1.0),
        T_machine_setup=translation(10.0,0.0,0.0),
        T_setup_part=rotation_z(pi/2),
    )
    assert abs(p.point_mm[0]-10.0)<1e-12
    assert abs(p.point_mm[1]-1.0)<1e-12
    assert abs(p.radial_unit[1]-1.0)<1e-12
    assert abs(p.tool_axis_unit[2]-1.0)<1e-12


def test_stage_geometry_is_derived_from_teeth_and_module():
    g=resolve_stage_geometry(20,80,0.2)
    assert abs(g.driver_pitch_diameter_mm-4.0)<1e-12
    assert abs(g.driven_pitch_diameter_mm-16.0)<1e-12
    assert abs(g.center_distance_mm-10.0)<1e-12
