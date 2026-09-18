"""Research-only tourbillon comparison model.

This is deliberately a reduced-order model. It is useful for comparing
topologies and parameter sweeps; it is not a chronometer prediction engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin, sqrt


Vector = tuple[float, float, float]


def _dot(a: Vector, b: Vector) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def _norm(v: Vector) -> float:
    return sqrt(_dot(v, v))


def _unit(v: Vector) -> Vector:
    n = _norm(v)
    if n == 0:
        raise ValueError("axis must be non-zero")
    return (v[0]/n, v[1]/n, v[2]/n)


def rotate(v: Vector, axis: Vector, angle_rad: float) -> Vector:
    """Rotate v around axis using Rodrigues' rotation formula."""
    k = _unit(axis)
    c, s = cos(angle_rad), sin(angle_rad)
    cross = (
        k[1]*v[2] - k[2]*v[1],
        k[2]*v[0] - k[0]*v[2],
        k[0]*v[1] - k[1]*v[0],
    )
    kv = _dot(k, v)
    return (
        v[0]*c + cross[0]*s + k[0]*kv*(1-c),
        v[1]*c + cross[1]*s + k[1]*kv*(1-c),
        v[2]*c + cross[2]*s + k[2]*kv*(1-c),
    )


@dataclass(frozen=True)
class CageAxis:
    axis: Vector
    period_s: float

    def __post_init__(self) -> None:
        if self.period_s <= 0:
            raise ValueError("period_s must be > 0")


@dataclass(frozen=True)
class TourbillonTopology:
    name: str
    axes: tuple[CageAxis, ...]
    cage_inertia_kg_m2: float
    friction_torque_nm: float

    def angular_speed_rad_s(self, i: int) -> float:
        return 2*pi / self.axes[i].period_s

    def rotational_energy_j(self) -> float:
        # Reduced-order estimate: same equivalent inertia assigned to each cage axis.
        return sum(
            0.5*self.cage_inertia_kg_m2*self.angular_speed_rad_s(i)**2
            for i in range(len(self.axes))
        )

    def friction_power_w(self) -> float:
        return sum(
            self.friction_torque_nm*self.angular_speed_rad_s(i)
            for i in range(len(self.axes))
        )

    def regulator_normal(self, t_s: float, initial: Vector=(0.0, 0.0, 1.0)) -> Vector:
        v = initial
        for axis in self.axes:
            angle = 2*pi*(t_s/axis.period_s)
            v = rotate(v, axis.axis, angle)
        return _unit(v)


def gravity_projection(topology: TourbillonTopology, t_s: float) -> float:
    """Projection of regulator normal onto gravity direction.

    Useful as a geometry-only proxy for how orientation is swept.
    It is not a direct rate-error equation.
    """
    g_hat: Vector = (0.0, 0.0, -1.0)
    return _dot(topology.regulator_normal(t_s), g_hat)


def sweep_statistics(topology: TourbillonTopology, duration_s: float, samples: int=720) -> dict[str, float]:
    if duration_s <= 0 or samples < 2:
        raise ValueError("duration_s must be > 0 and samples >= 2")

    vals = [
        gravity_projection(topology, duration_s*i/(samples-1))
        for i in range(samples)
    ]
    mean = sum(vals)/len(vals)
    rms = sqrt(sum(v*v for v in vals)/len(vals))
    span = max(vals) - min(vals)
    return {
        "mean_projection": mean,
        "rms_projection": rms,
        "projection_span": span,
        "rotational_energy_j": topology.rotational_energy_j(),
        "friction_power_w": topology.friction_power_w(),
    }
