from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
    nominal: float
    measured: float

    @property
    def error(self) -> float:
        return self.measured - self.nominal


def propose_process_offset(samples: list[Measurement]) -> float:
    """Return a simple bias-canceling process offset.

    Positive measured bias produces a negative proposed process offset.
    This changes process compensation only; it never mutates nominal geometry.
    """
    if not samples:
        raise ValueError("at least one measurement is required")
    mean_error = sum(s.error for s in samples) / len(samples)
    return -mean_error
