from research.time_synthesis.epicyclic import (
    carrier_speed,
    ring_speed,
    sun_speed,
    willis_residual,
)


def test_fixed_ring_carrier_speed():
    wc=carrier_speed(20,60,omega_sun=4.0,omega_ring=0.0)
    assert abs(wc-1.0)<1e-12


def test_round_trip_unknowns():
    ns,nr=20,60
    ws,wr=4.0,-1.0
    wc=carrier_speed(ns,nr,ws,wr)
    assert abs(ring_speed(ns,nr,ws,wc)-wr)<1e-12
    assert abs(sun_speed(ns,nr,wr,wc)-ws)<1e-12
    assert abs(willis_residual(ns,nr,ws,wr,wc))<1e-12
