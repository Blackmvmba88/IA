"""Deterministic H2 hairspring candidate packaging."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from research.hairspring.design import required_thickness_for_spiral_mm
from research.hairspring.geometry import SpiralSpec, centerline_points, write_ascii_dxf_polyline
from research.hairspring.h2_metrics import evaluate


@dataclass(frozen=True)
class HairspringCandidate:
    id: str
    target_frequency_hz: float
    balance_inertia_kg_m2: float
    spring_width_mm: float
    spring_thickness_mm: float
    youngs_modulus_gpa: float
    spiral: SpiralSpec

    def canonical_payload(self) -> dict:
        return {
            "id": self.id,
            "target_frequency_hz": self.target_frequency_hz,
            "balance_inertia_kg_m2": self.balance_inertia_kg_m2,
            "spring_width_mm": self.spring_width_mm,
            "spring_thickness_mm": self.spring_thickness_mm,
            "youngs_modulus_gpa": self.youngs_modulus_gpa,
            "spiral": asdict(self.spiral),
            "model": "H2-first-order-K=EI/L",
        }

    def design_hash(self) -> str:
        encoded = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


def solve_candidate(
    candidate_id: str,
    spec: SpiralSpec,
    spring_width_mm: float,
    youngs_modulus_gpa: float,
    balance_inertia_kg_m2: float,
    target_frequency_hz: float,
) -> HairspringCandidate:
    thickness = required_thickness_for_spiral_mm(
        spec=spec,
        spring_width_mm=spring_width_mm,
        youngs_modulus_gpa=youngs_modulus_gpa,
        balance_inertia_kg_m2=balance_inertia_kg_m2,
        target_frequency_hz=target_frequency_hz,
    )
    return HairspringCandidate(
        id=candidate_id,
        target_frequency_hz=target_frequency_hz,
        balance_inertia_kg_m2=balance_inertia_kg_m2,
        spring_width_mm=spring_width_mm,
        spring_thickness_mm=thickness,
        youngs_modulus_gpa=youngs_modulus_gpa,
        spiral=spec,
    )


def export_candidate(candidate: HairspringCandidate, output_dir: str) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    points = centerline_points(candidate.spiral)
    dxf_path = out/"centerline.dxf"
    write_ascii_dxf_polyline(str(dxf_path), points)

    metrics = evaluate(candidate.spiral, candidate.spring_width_mm)
    manifest = {
        "candidate": candidate.canonical_payload(),
        "design_hash_sha256": candidate.design_hash(),
        "geometry_metrics": metrics.to_dict(),
        "artifacts": {
            "centerline_dxf": dxf_path.name
        },
        "release_state": "geometry-only",
        "manufacturing_authorized": False,
    }
    manifest_path = out/"manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest
