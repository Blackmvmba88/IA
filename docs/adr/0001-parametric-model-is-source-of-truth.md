# ADR-0001 — Parametric model is the source of truth

## Decision
The nominal parametric model is immutable design intent for a released revision.

Measured manufacturing deviation is stored as evidence. Compensation is stored separately as process state. No inspection or CAM stage may silently rewrite nominal geometry.

## Why
Without this separation, the system cannot distinguish a design revision from a machine correction. That destroys traceability and makes autonomous iteration unsafe and non-reproducible.
