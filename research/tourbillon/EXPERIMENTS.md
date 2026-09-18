# Experiment matrix

The purpose of this matrix is to compare architecture families without pretending that a reduced-order model predicts real watch rate.

## Sweep A — cage period
Topology: single axis  
Periods: 15, 24, 30, 45, 60, 90 s

Observe:
- angular speed
- rotational kinetic energy
- estimated friction power
- orientation coverage

## Sweep B — inclination
Topology: single axis  
Tilt: 0, 10, 20, 25, 30, 35, 45 deg

Observe:
- gravity-projection coverage
- envelope growth
- inclined gearing requirements
- bearing-load direction

## Sweep C — number of axes
Compare:
- classical 1-axis
- biaxial
- triaxial

Observe:
- orientation coverage
- added energy cost
- bearing count
- assembly depth
- sensitivity to cage imbalance

## Sweep D — period ratios
For nested cages test rational and non-identical periods:
- 60/120
- 60/150
- 60/180
- 45/120
- 24/60

Question:
Does the orientation trajectory repeat too quickly, or does it cover the sphere efficiently?

## Sweep E — constant force interaction
Add a remontoire cadence parameter and compare it with cage periods.

Avoid cadences that repeatedly phase-lock with cage orientation until the coupled model proves this harmless.

## Next model upgrades
1. Explicit mass properties per cage
2. Separate bearing friction per pivot
3. Gear-mesh efficiency and tooth forces
4. Balance/hairspring oscillator
5. Escapement impulse model
6. Gravity-sensitive rate-error surface fitted from measured positions
7. Monte Carlo manufacturing tolerance model
8. CAD-derived inertia tensor
