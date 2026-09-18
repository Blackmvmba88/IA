# BPME-NEXT Roadmap

## Phase 0 — Deterministic kernel
- [x] Canonical project structure
- [x] Mechanism genome contract
- [x] Separate nominal/process/compensation state
- [x] Genesis-300 starter genome
- [ ] Deterministic gear geometry reference implementation
- [ ] Golden fixtures and hash certification

## Phase 1 — CAD
- [ ] CadQuery adapter for gears, shafts, spacers and plates
- [ ] STEP/DXF artifact manifest
- [ ] Assembly constraints and interference checks

## Phase 2 — Manufacturing planning
- [ ] Operation graph: stock → setup → operation → inspection gate
- [ ] Machine profile schema
- [ ] Tool inventory schema
- [ ] Lathe/mill/router capability matching
- [ ] Explicit authorization gate before machine-specific G-code

## Phase 3 — Metrology loop
- [ ] Inspection point schema
- [ ] Nominal vs measured comparison
- [ ] Bias/runout/backlash evidence model
- [ ] Compensation proposal engine
- [ ] Reject/accept/rework state machine

## Phase 4 — Autonomous horology
- [ ] Assembly graph knows missing parts
- [ ] Planner chooses next manufacturable part
- [ ] Vision/probe measurements update evidence
- [ ] Digital twin tracks every physical part revision
- [ ] Closed-loop iteration with human approval at machine boundary

## Phase 5 — Wristwatch scale
- [ ] Escapement contracts
- [ ] Balance train
- [ ] Jewel/bearing interfaces
- [ ] Tourbillon carrier experiments
- [ ] Ouroboros collection lineage
