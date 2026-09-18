import json
from pathlib import Path


def test_example_cam_plan_does_not_authorize_gcode():
    data = json.loads(Path("cam/operation-plan.example.json").read_text())
    assert data["gcode_authorized"] is False
    assert data["release_state"] == "plan-only"
