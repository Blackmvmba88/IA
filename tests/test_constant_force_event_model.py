from research.constant_force.event_model import phase_lock_score, phase_samples


def test_equal_periods_phase_lock_strongly():
    phases = phase_samples(60.0, 60.0, 600.0)
    assert phase_lock_score(phases) == 1.0


def test_mismatched_periods_spread_events():
    phases = phase_samples(7.0, 60.0, 600.0)
    assert phase_lock_score(phases) < 0.25
