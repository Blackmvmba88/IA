# ADR-0002 — Machine execution is an explicit authorization boundary

## Decision
BPME may generate deterministic geometry and machine-neutral operation plans automatically. Machine-specific G-code is not considered released until the active machine profile, tooling, stock, workholding, material and authorization state are all present.

## Consequence
The autonomous planner can reason about manufacturing without silently causing physical motion.
