"""Reduced-order event model for constant-force research."""

from __future__ import annotations

from dataclasses import dataclass
from math import fmod


@dataclass(frozen=True)
class PeriodicStage:
    period_s: float

    def __post_init__(self) -> None:
        if self.period_s <= 0:
            raise ValueError("period_s must be > 0")

    def phase(self, t_s: float) -> float:
        return fmod(t_s, self.period_s) / self.period_s


def recharge_events(period_s: float, duration_s: float) -> list[float]:
    if period_s <= 0 or duration_s < 0:
        raise ValueError("invalid period/duration")
    count = int(duration_s // period_s)
    return [i*period_s for i in range(1, count+1)]


def phase_samples(
    recharge_period_s: float,
    cage_period_s: float,
    duration_s: float,
) -> list[float]:
    cage = PeriodicStage(cage_period_s)
    return [
        cage.phase(t)
        for t in recharge_events(recharge_period_s, duration_s)
    ]


def phase_lock_score(phases: list[float], bins: int=12) -> float:
    """Crude 0..1 concentration score; high means events cluster in cage phase."""
    if not phases:
        raise ValueError("phases required")
    if bins < 2:
        raise ValueError("bins must be >= 2")
    counts = [0]*bins
    for p in phases:
        i = min(bins-1, int((p % 1.0)*bins))
        counts[i] += 1
    return max(counts)/len(phases)
