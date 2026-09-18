from inspection.compensate import Measurement, propose_process_offset


def test_process_offset_cancels_mean_bias():
    samples = [
        Measurement(nominal=10.0, measured=10.02),
        Measurement(nominal=10.0, measured=10.04),
    ]
    assert round(propose_process_offset(samples), 6) == -0.03
