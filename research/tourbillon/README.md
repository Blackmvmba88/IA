# BPME Horology Research Lab — Tourbillon & Regulator Systems

This directory is a research track, not a production design.

## Why this exists

BPME should be able to represent, simulate, compare and eventually prototype regulating architectures rather than treating a watch as only a set of gears.

The research target is a machine-readable family of regulator topologies with measurable trade-offs:

- positional rate error
- balance amplitude
- cage inertia
- torque demand
- energy variation
- bearing friction
- cage rotational period
- number and orientation of axes
- shock sensitivity
- manufacturability
- inspection complexity
- assembly complexity

## Architecture families

### T01 — Classical one-axis tourbillon
Balance, hairspring, lever and escape wheel are carried by a rotating cage. Classical implementations commonly use a fixed wheel and a rotating cage, often with a one-minute revolution.

Research questions:
- What cage inertia is tolerable at a given torque budget?
- How strongly does cage period affect averaging of positional error?
- How does eccentric mass influence amplitude and rate?
- How should the fixed-wheel geometry be parameterized?

### T02 — Flying tourbillon
A one-sided cage support removes the upper bridge.

Research questions:
- bearing stiffness vs visual openness
- axial/radial runout sensitivity
- shock load at the single support
- cage tilt and endshake

### T03 — Inclined tourbillon
The regulator axis is tilted relative to the movement reference plane.

Reference direction: Greubel Forsey has demonstrated a 25-degree, 24-second architecture using a lightweight cage and special inclined gearing.

Research questions:
- angle sweep: 0–45 degrees
- cage period sweep: 15–60 seconds
- energy cost vs positional averaging
- inclined gear contact geometry

### T04 — Bi-axis / tri-axis / poly-axis tourbillon
Nested cages rotate the oscillator through multiple orientations.

Research questions:
- axis orientation optimization
- cage period ratios
- nested bearing losses
- resonance/coupling between cage frequencies
- mass distribution and dynamic balancing
- minimum practical envelope

### T05 — Carrousel
Alternative rotating regulator architecture using separate power paths for cage rotation and escapement drive.

Research questions:
- two-train torque distribution
- sensitivity to train efficiency mismatch
- cage speed stability
- comparison with fixed-wheel tourbillon

### T06 — Tourbillon + remontoire / constant force
A secondary energy store isolates the escapement from mainspring torque variation.

Research questions:
- recharge period
- remontoire spring energy window
- impulse disturbance during recharge
- interaction between remontoire cadence and cage period
- amplitude stability across power reserve

### T07 — High-frequency / experimental escapements
Research-only category for magnetic, high-frequency and other unconventional escapement architectures.

No production claims are made from published examples. Patent status and freedom-to-operate must be reviewed independently before any commercialization.

## Experimental hierarchy

1. Kinematic model
2. Torque-flow model
3. Rigid-body cage inertia model
4. Oscillator + escapement timing model
5. Positional gravity model
6. Bearing/friction model
7. CAD envelope
8. Prototype-scale manufacturing
9. Metrology
10. Chronometric bench testing

## Rule

A beautiful mechanism is not automatically a better regulator.

Every topology must earn its place with measured evidence.
