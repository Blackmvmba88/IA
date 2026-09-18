"""Generate the H2 reference hairspring geometry and metrics."""

from __future__ import annotations

import json
from pathlib import Path

from research.hairspring.geometry import SpiralSpec, centerline_points, write_ascii_dxf_polyline
from research.hairspring.h2_metrics import evaluate


def run(output_dir: str = "artifacts/hairspring-h2") -> dict:
    spec = SpiralSpec(
        inner_radius_mm=1.0,
        radial_pitch_mm_per_turn=0.30,
        turns=8.0,
        samples_per_turn=256,
    )
    width = 0.10
    metrics = evaluate(spec, width)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dxf = out/"reference-spiral.dxf"
    write_ascii_dxf_polyline(str(dxf), centerline_points(spec))

    payload = {
        "id": "h2-reference-spiral-001",
        "metrics": metrics.to_dict(),
        "artifact": str(dxf),
    }
    (out/"metrics.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
