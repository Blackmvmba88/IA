# BPME Research — Constant-force systems

Constant-force mechanisms are studied as energy-conditioning stages between the mainspring/barrel and the regulating system.

The purpose of this research track is not to assume that one architecture is superior. BPME will model the periodic transfer of energy and test interaction with rotating cages and escapement cadence.

## Families

### Remontoire
A secondary spring or energy store is periodically recharged by the train and then feeds a downstream stage over a shorter interval.

Research variables:
- recharge period
- stored energy window
- release torque curve
- recharge disturbance
- phase relationship to cage rotation
- effect on balance amplitude

### Constant-force escapement
An elastic element can be designed to deliver a more controlled impulse near the escapement itself.

Research variables:
- snap/buckling threshold
- elastic hysteresis
- fatigue
- impulse repeatability
- material/process sensitivity

## BPME coupling problem

A rotating regulator already creates periodic dynamics. A remontoire adds another periodic process.

Therefore BPME must track phase relationships:

barrel period/drift
→ train
→ remontoire recharge cadence
→ cage period(s)
→ escapement frequency

A visually elegant solution can still be dynamically poor if periodic events repeatedly align in an unfavorable phase.

## Next model

Build an event simulator that records:
- torque before recharge
- torque after recharge
- cage angle at recharge
- oscillator phase at recharge
- resulting amplitude perturbation proxy
