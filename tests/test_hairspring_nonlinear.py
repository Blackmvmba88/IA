from math import pi

from research.hairspring.nonlinear import amplitude_sweep, estimate_free_frequency_hz
from research.oscillator.model import BalanceSpring


def build(k3_ratio: float) -> BalanceSpring:
    inertia = 1e-9
    k1 = (2*pi*4.0)**2 * inertia
    return BalanceSpring(
        inertia_kg_m2=inertia,
        stiffness_nm_per_rad=k1,
        cubic_stiffness_nm_per_rad3=k3_ratio*k1,
    )


def test_linear_model_is_amplitude_independent_to_numerical_resolution():
    osc = build(0.0)
    low = estimate_free_frequency_hz(osc, 0.1)
    high = estimate_free_frequency_hz(osc, 0.8)
    assert abs(low-high) < 1e-6


def test_positive_cubic_stiffness_hardens_with_amplitude():
    osc = build(0.05)
    low = estimate_free_frequency_hz(osc, 0.1)
    high = estimate_free_frequency_hz(osc, 0.8)
    assert high > low + 0.03


def test_negative_cubic_stiffness_softens_with_amplitude():
    osc = build(-0.05)
    low = estimate_free_frequency_hz(osc, 0.1)
    high = estimate_free_frequency_hz(osc, 0.8)
    assert high < low - 0.03


def test_sweep_uses_first_amplitude_as_relative_rate_baseline():
    pts = amplitude_sweep(build(0.05), [0.1, 0.4, 0.8])
    assert pts[0].relative_rate_s_per_day == 0.0
    assert pts[-1].relative_rate_s_per_day > 0.0
