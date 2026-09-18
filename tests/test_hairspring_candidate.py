import json
from pathlib import Path

from research.hairspring.candidate import export_candidate, solve_candidate
from research.hairspring.geometry import SpiralSpec


def build():
    return solve_candidate(
        "candidate-test",
        SpiralSpec(1.0, 0.30, 8.0, 64),
        spring_width_mm=0.10,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
        target_frequency_hz=4.0,
    )


def test_design_hash_is_deterministic():
    assert build().design_hash() == build().design_hash()


def test_hash_changes_when_design_changes():
    a = build()
    b = solve_candidate(
        "candidate-test",
        SpiralSpec(1.0, 0.31, 8.0, 64),
        spring_width_mm=0.10,
        youngs_modulus_gpa=200.0,
        balance_inertia_kg_m2=1e-9,
        target_frequency_hz=4.0,
    )
    assert a.design_hash() != b.design_hash()


def test_export_contains_non_authorized_manifest(tmp_path: Path):
    manifest = export_candidate(build(), str(tmp_path))
    assert manifest["manufacturing_authorized"] is False
    assert manifest["release_state"] == "geometry-only"
    assert (tmp_path/"centerline.dxf").exists()
    saved = json.loads((tmp_path/"manifest.json").read_text())
    assert saved["design_hash_sha256"] == build().design_hash()
