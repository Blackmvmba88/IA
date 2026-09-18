from __future__ import annotations

import json

from .model import sweep_statistics
from .presets import (
    BIAXIAL_60_120,
    CLASSICAL_60S,
    INCLINED_25DEG_24S,
    TRIAXIAL_60_120_300,
)


def main() -> None:
    topologies = [
        CLASSICAL_60S,
        INCLINED_25DEG_24S,
        BIAXIAL_60_120,
        TRIAXIAL_60_120_300,
    ]
    report = {
        t.name: sweep_statistics(t, duration_s=600.0, samples=1200)
        for t in topologies
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
