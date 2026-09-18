# BlackMamba Parametric Mechanism Engine — NEXT

**BPME-NEXT** is a deterministic engineering pipeline for parametric mechanical watches and kinetic mechanisms.

The system is designed around one loop:

**Parameters → constraints → mechanism → CAD → simulation → CAM plan → machining → inspection → compensation → next revision**

The long-term target is autonomous horology: a watch design should carry enough machine-readable intent for the system to decide what part must exist, how it should be manufactured, how the result should be measured, and how the next manufacturing pass should compensate for measured deviation.

## First demonstrator: Genesis-300

Genesis-300 is the reference mechanism used to validate the pipeline before miniaturizing into wristwatch-scale mechanisms. It starts with deterministic gears, shafts, plates, tolerances, inspection evidence, and compensation records.

## Horology Research Lab

BPME also contains a research layer for high-watchmaking regulator and energy architectures.

Current tracks:

- `research/tourbillon/` — classical, inclined, flying and multi-axis rotating regulators
- `research/carrousel/` — dual-power-path rotating regulator architecture
- `research/constant-force/` — remontoire and constant-force energy conditioning
- `research/tourbillon/experiments/` — machine-readable candidate topologies

Research models are deliberately reduced-order. They compare topology, kinematics, energy and periodic coupling; they do not claim chronometer-grade prediction until calibrated with real measurement data.

## First research candidate

`mamba-t01-biaxial` is a simulation-only biaxial candidate used to exercise:
- nested-axis kinematics
- spherical orientation coverage
- cage-period interactions
- energy-cost proxies
- future CAD-derived inertia

It is not a production movement or a copy of an existing caliber.

## Safety boundary

This repository does **not** release production-ready G-code by default. CAM output starts as a machine-neutral operation plan. Machine-specific post-processing requires an explicit machine profile, material profile, tool inventory, stock definition, workholding declaration, and human authorization.

## Repository map

- `contracts/` — canonical machine-readable engineering contracts
- `crates/bpme-core/` — deterministic geometry/validation core
- `cad/` — CAD generator adapters
- `cam/` — machine-neutral manufacturing plans
- `inspection/` — measurement evidence and compensation logic
- `examples/genesis-300/` — first mechanism genome
- `research/` — horology research models and experiment contracts
- `docs/adr/` — architectural decisions
- `tests/` — contract and regression tests

## Core rules

> The nominal model is truth. Manufacturing is evidence. Compensation changes process parameters, never silently rewrites design intent.

> A beautiful complication is a hypothesis until measurement supports it.

BLACKMAMBA / Iyari Gomez
