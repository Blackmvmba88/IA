"""Minimal event-level Swiss-lever-like impulse model.

This does not model pallet geometry or tooth contact. It captures the key
research abstraction: the escapement periodically unlocks and delivers a
small impulse to sustain the balance oscillator.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeverEscapement:
    impulse_energy_j: float
    unlock_angle_rad: float
    dead_time_s: float = 0.0

    def __post_init__(self) -> None:
        if self.impulse_energy_j <= 0:
            raise ValueError("impulse_energy_j must be > 0")
        if self.unlock_angle_rad <= 0:
            raise ValueError("unlock_angle_rad must be > 0")
        if self.dead_time_s < 0:
            raise ValueError("dead_time_s must be >= 0")


@dataclass
class EscapementMemory:
    last_impulse_s: float = -1e30
    previous_angle_rad: float = 0.0


def should_impulse(
    escapement: LeverEscapement,
    memory: EscapementMemory,
    angle_rad: float,
    t_s: float,
) -> bool:
    """Trigger when crossing the central unlocking region in either direction."""
    crossed_center = (
        (memory.previous_angle_rad < 0.0 <= angle_rad)
        or (memory.previous_angle_rad > 0.0 >= angle_rad)
    )
    near_unlock = abs(angle_rad) <= escapement.unlock_angle_rad
    ready = (t_s - memory.last_impulse_s) >= escapement.dead_time_s
    return crossed_center and near_unlock and ready
