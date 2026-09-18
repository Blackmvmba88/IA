# BPME Research — Balance, hairspring and escapement

The regulating organ is treated as a dynamical system, not a decorative subassembly.

## Model 0

The first BPME oscillator is a damped rotational harmonic oscillator:

```
I θ¨ + c θ˙ + k θ = τ
```

where:

- `I` = balance moment of inertia
- `c` = loss coefficient
- `k` = effective hairspring torsional stiffness
- `τ` = external/escapement torque

For the ideal linear system:

```
f0 = (1 / 2π) sqrt(k / I)
```

This expresses an important design relationship: changing balance inertia or spring stiffness changes the natural frequency.

## Escapement abstraction

The first escapement model is event-based. When the oscillator crosses its central unlocking region, a small energy packet can be transferred to the balance.

This intentionally mirrors the physical role of an escapement without pretending to reproduce pallet/tooth contact geometry yet.

## What we measure

- natural frequency
- beats per hour
- amplitude envelope
- oscillator energy
- impulse count
- energy injected per unit time
- decay without escapement
- maintained amplitude with escapement

## Next levels

1. Coulomb + pivot friction
2. nonlinear hairspring torque
3. center-of-gravity offset
4. positional gravity torque
5. escapement lock/drop/impulse geometry
6. tooth/pallet contact efficiency
7. beat error
8. hairspring breathing and attachment geometry
9. temperature/material coefficient
10. shock and recovery
11. coupling to rotating tourbillon coordinate frame

## Research rule

A target frequency is a constraint. Stable amplitude and low positional rate variation are separate objectives.
