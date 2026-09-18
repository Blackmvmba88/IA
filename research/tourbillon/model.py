"""Reduced-order research model for rotating watch regulators.

The model separates two different questions:

1. axis/orientation coverage — important for multi-axis mechanisms;
2. first-order averaging of a carried asymmetry vector — relevant to why a
   classical cage can average a gravity-sensitive error even when the balance
   axis itself does not sweep the sphere.

It is a topology-comparison harness, not a chronometer prediction engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, atan2, cos, pi, sin, sqrt


Vector = tuple[float, float, float]


def _dot(a: Vector, b: Vector) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def _norm(v: Vector) -> float:
    return sqrt(_dot(v, v))


def _unit(v: Vector) -> Vector:
    n = _norm(v)
    if n == 0:
        raise ValueError("vector must be non-zero")
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
    # Axes are listed inner -> outer and expressed in their parent frames.
    axis: Vector
    period_s: float

    def __post_init__(self) -> None:
        _unit(self.axis)
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
        # First-order estimate: one equivalent inertia per rotating cage.
        return sum(
            0.5*self.cage_inertia_kg_m2*self.angular_speed_rad_s(i)**2
            for i in range(len(self.axes))
        )

    def friction_power_w(self) -> float:
        # Coulomb-like friction estimate P = tau * omega for each cage.
        return sum(
            self.friction_torque_nm*self.angular_speed_rad_s(i)
            for i in range(len(self.axes))
        )

    def carry_vector(self, t_s: float, initial: Vector) -> Vector:
        """Carry a local vector through nested cage rotations.

        Axes are applied inner -> outer. This is a kinematic approximation
        suitable for topology sweeps; CAD-derived transforms will replace it
        when real cage geometry exists.
        """
        v = initial
        for axis in self.axes:
            v = rotate(v, axis.axis, 2*pi*(t_s/axis.period_s))
        return _unit(v)

    def regulator_normal(self, t_s: float) -> Vector:
        return self.carry_vector(t_s, (0.0, 0.0, 1.0))

    def asymmetry_vector(self, t_s: float) -> Vector:
        # Represents a small fixed eccentricity/error vector carried by cages.
        return self.carry_vector(t_s, (1.0, 0.0, 0.0))


def gravity_projection(
    topology: TourbillonTopology,
    t_s: float,
    gravity_hat: Vector=(0.0, 0.0, -1.0),
) -> float:
    """Projection of regulator normal onto gravity.

    Geometry-only orientation metric. It is not a rate-error equation.
    """
    return _dot(topology.regulator_normal(t_s), _unit(gravity_hat))


def first_order_bias_proxy(
    topology: TourbillonTopology,
    duration_s: float,
    gravity_hat: Vector,
    samples: int=720,
) -> float:
    """Mean linear gravity coupling of a carried asymmetry vector.

    Lower absolute magnitude means better averaging *under this deliberately
    simple linear-error assumption*. Real watches require measured rate maps,
    hairspring/escapement models and friction data.
    """
    if duration_s <= 0 or samples < 2:
        raise ValueError("duration_s must be > 0 and samples >= 2")
    g = _unit(gravity_hat)
    vals = [
        _dot(
            topology.asymmetry_vector(duration_s*i/(samples-1)),
            g,
        )
        for i in range(samples)
    ]
    return sum(vals)/len(vals)


def sphere_coverage_fraction(
    topology: TourbillonTopology,
    duration_s: float,
    samples: int=1440,
    polar_bins: int=18,
    azimuth_bins: int=36,
) -> float:
    """Fraction of coarse spherical bins visited by the regulator normal."""
    if duration_s <= 0 or samples < 2:
        raise ValueError("duration_s must be > 0 and samples >= 2")
    if polar_bins < 2 or azimuth_bins < 4:
        raise ValueError("insufficient sphere resolution")

    occupied: set[tuple[int, int]] = set()
    for i in range(samples):
        x, y, z = topology.regulator_normal(duration_s*i/(samples-1))
        theta = acos(max(-1.0, min(1.0, z)))
        phi = (atan2(y, x) + 2*pi) % (2*pi)
        p = min(polar_bins-1, int(theta/pi*polar_bins))
        a = min(azimuth_bins-1, int(phi/(2*pi)*azimuth_bins))
        occupied.add((p, a))

    return len(occupied)/(polar_bins*azimuth_bins)


def sweep_statistics(
    topology: TourbillonTopology,
    duration_s: float,
    samples: int=720,
) -> dict[str, float]:
    if duration_s <= 0 or samples < 2:
        raise ValueError("duration_s must be > 0 and samples >= 2")

    projections = [
        gravity_projection(topology, duration_s*i/(samples-1))
        for i in range(samples)
    ]
    mean = sum(projections)/len(projections)
    rms = sqrt(sum(v*v for v in projections)/len(projections))

    poses = (
        (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0), (0.0, -1.0, 0.0),
        (0.0, 0.0, 1.0), (0.0, 0.0, -1.0),
    )
    bias = [
        abs(first_order_bias_proxy(topology, duration_s, g, samples))
        for g in poses
    ]

    return {
        "normal_mean_projection": mean,
        "normal_rms_projection": rms,
        "normal_projection_span": max(projections)-min(projections),
        "sphere_coverage_fraction": sphere_coverage_fraction(
            topology, duration_s, max(samples, 720)
        ),
        "mean_abs_first_order_bias_proxy": sum(bias)/len(bias),
        "rotational_energy_j": topology.rotational_energy_j(),
        "friction_power_w": topology.friction_power_w(),
    }
