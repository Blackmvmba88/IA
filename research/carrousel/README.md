# BPME Research — Carrousel

The carrousel is tracked as a separate architecture family, not as a tourbillon alias.

## Topological distinction

A classical tourbillon commonly couples cage rotation and escapement operation through the cage/fixed-wheel architecture.

A carrousel uses two complementary power paths:
1. a path feeding the escapement/regulating organ;
2. a path controlling cage rotation.

This makes the carrousel a valuable BPME research case because energy routing becomes an explicit graph.

## BPME questions

- Can cage period be adjusted without forcing the same change into escapement gearing?
- How do losses split between the two trains?
- How sensitive is cage speed to efficiency mismatch?
- Can one train be instrumented/controlled independently during prototyping?
- What is the minimum part-count topology that preserves the architectural distinction?
- How does tolerance accumulation compare with a classical tourbillon?

## Required measurements

Every carrousel experiment should eventually record:
- barrel/input torque
- escapement-path torque
- cage-path torque
- cage period
- balance frequency/amplitude
- train efficiencies
- backlash per branch
- bearing losses
- cage inertia
- positional rate map

## Research boundary

The initial BPME implementation models power routing only. It does not reproduce a proprietary production caliber.
