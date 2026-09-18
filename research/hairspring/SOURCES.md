# Hairspring research sources

## First-order spiral-spring stiffness

A published planar spiral-spring treatment derives a rotational stiffness of
the form:

    K = E*I/L

from elastic strain energy under bending.

BPME uses that relationship only as the H2 first-order bridge from deterministic
centerline geometry to an effective linear stiffness. It is not considered
sufficient for watch-grade chronometry.

Reference:
- Biomimetics 2026, "Design and Performance Evaluation of Unpowered Hip-Assisted Exoskeletons"
  https://www.mdpi.com/2313-7673/11/9/625

## Why BPME needs later levels

Watch oscillators are sensitive to nonlinear elasticity, attachment geometry,
gravity, friction and amplitude. H3 therefore replaces the first-order beam
bridge with CAD/FEA-informed reduced coefficients, while H4 calibrates those
coefficients from measurements.
