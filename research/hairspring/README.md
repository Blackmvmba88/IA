# BPME Research — Hairspring

BPME treats the hairspring as a progressively refined model rather than one fixed equation.

Real behavior depends on geometry, attachment, material, temperature,
concentric breathing, center-of-gravity motion and interaction with the balance.

## H0 — effective linear spring ✅

`tau = -k1*theta`

Implemented in `research/oscillator/model.py`.

Purpose:
- oscillator/escapement integration
- small-signal frequency
- energy bookkeeping

## H1 — amplitude-dependent stiffness ✅

`tau = -(k1*theta + k3*theta^3)`

Implemented in:
- `research/hairspring/nonlinear.py`
- `research/hairspring/run_h1_sweep.py`

Purpose:
- expose amplitude-dependent rate behavior
- represent hardening/softening non-isocronism
- measure relative rate spread across amplitudes

The cubic coefficient is currently a research parameter; it is not yet derived from physical spring geometry.

## H2 — deterministic geometry + first-order stiffness bridge ✅

Implemented in:
- `research/hairspring/geometry.py`
- `research/hairspring/h2_metrics.py`
- `research/hairspring/beam_bridge.py`
- `research/hairspring/design.py`
- `research/hairspring/candidate.py`

Capabilities:
- deterministic Archimedean centerline
- active-length calculation
- inner/outer radius and edge-gap metrics
- DXF centerline export
- first-order `K ≈ E*I/L` bridge
- inverse solve: target frequency → candidate spring thickness
- deterministic candidate manifest + SHA-256
- explicit geometry-only / non-authorized manufacturing state

The first-order beam bridge is a candidate generator, not watch-grade prediction.

## H3 — CAD/FEA-informed reduced model ⏭️

Goal:
- convert real spring geometry into effective `k1`, `k3` and parasitic terms
- quantify stress and attachment effects
- fit a reduced model that is fast enough for optimization

Planned outputs:
- stiffness curve `tau(theta)`
- strain/stress envelope
- lateral reaction forces
- center-of-mass breathing trajectory
- fitted `k1` / `k3`
- geometry hash linked to solver result

## H4 — manufactured spring calibration

Fit H3 coefficients from physical measurements rather than assuming the CAD model is perfect.

Planned evidence:
- measured frequency vs amplitude
- positional rate map
- temperature sweep
- repeatability between nominally identical springs
- manufacturing compensation record

## Design variables

- active length
- thickness
- width
- coil count
- mean radius
- inner attachment
- outer attachment
- terminal curve
- material elastic modulus
- thermal coefficient

## Objective

A future BPME loop should be able to accept:

**target frequency + balance inertia + envelope + material + manufacturability constraints**

and return:

**candidate geometry → predicted dynamics → CAD artifact → measurement plan → compensation update**

No proprietary production hairspring geometry is assumed here.
