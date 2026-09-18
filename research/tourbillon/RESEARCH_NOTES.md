# Research notes — regulator architecture

## Confirmed design facts used by BPME

### Classical tourbillon
The escapement and balance are carried in a mobile cage. In the common Breguet architecture, energy from the barrel must both sustain the oscillator/escapement and rotate the cage. This makes cage mass and rotational losses first-class design variables.

### Multi-axis
Published multi-axis architectures use nested cages rotating about different axes. This expands the orientation trajectory of the regulating organ, but adds bearings, inertia, gearing and assembly complexity.

### Research implication
BPME must never compare tourbillons only by axis count. At minimum a candidate must carry:
- orientation coverage
- cage mass/inertia
- bearing count
- rotational periods
- friction estimate
- oscillator frequency
- torque budget
- manufacturing tolerance burden

## Hypotheses to test

H1. Lower cage inertia can permit faster cage periods for a given energy budget.

H2. Additional axes can improve orientation coverage while simultaneously worsening energy loss and tolerance stack-up.

H3. Period ratios strongly influence how quickly a nested system revisits the same orientation trajectory.

H4. A constant-force stage may stabilize energy delivery, but its recharge cadence can couple to cage motion and must be studied as a coupled periodic system.

H5. The best architecture for a wristwatch may not be the architecture with the most axes; optimization should be multi-objective.

## Next experiment
Generate a grid over:
- 1–3 axes
- 15–180 s cage periods
- 0–45 deg inclination
- equivalent inertia
- bearing friction

Rank nothing yet. Produce a Pareto surface for:
- orientation coverage
- estimated energy cost
- mechanical complexity
