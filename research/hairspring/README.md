# BPME Research — Hairspring

The current oscillator uses one effective torsional stiffness `k`.

That is only Level 0.

Real hairspring behavior depends on geometry, attachment, material, temperature,
concentric breathing, center-of-gravity motion and interaction with the balance.

## Planned levels

### H0 — effective linear spring
`tau = -k * theta`

Purpose:
- validate oscillator/escapement integration
- frequency and energy bookkeeping

### H1 — amplitude-dependent stiffness
Add a small nonlinear term:

`tau = -(k1*theta + k3*theta^3)`

Purpose:
- study amplitude-dependent rate behavior
- expose non-isochronism in a controlled model

### H2 — breathing geometry
Represent spring coils and attachment points.

Measure:
- center-of-mass displacement during breathing
- lateral force at collet/stud
- effective stiffness across amplitude
- sensitivity to attachment geometry

### H3 — CAD/FEA-informed reduced model
Fit reduced-order coefficients from a real spring geometry.

### H4 — manufactured spring calibration
Fit the model from measured oscillator data rather than assuming ideal geometry.

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

BPME should eventually be able to change a hairspring parameter and predict how
that change propagates through frequency, amplitude, positional sensitivity,
manufacturability and the tourbillon's behavior.

No proprietary production hairspring geometry is assumed here.
