# Deontological Firewall (DFW) v6.x — Deterministic Runtime Safety Kernel

**Author:** Damien Richard Elliot-Smith  
**Date:** December 2025  
**Contact:** damien.research.ai@gmail.com  

DFW is a **deterministic, auditable veto/guard kernel** intended to sit between an AGI system and its action interface (planner, tool-use, robotics controller, etc.).  
It evaluates proposed actions against explicit invariants and **blocks actions that violate safety constraints**.

## Status (read this first)
- **This repo contains research + prototype code**, not a production-certified safety system.
- The **papers define the architecture**; the Python code provides a reference implementation and validation scenarios.
- Threat-model and scope are specified in the papers; claims should be interpreted within those bounds.

## Papers (DFW v6.0 suite)
| ID | Title | Focus |
|----|------|-------|
| A | Core Kernel | veto logic, invariants, structure |
| B | Temporal Safety | time consistency, rollback control |
| C | Adversarial & Causal Safety | causal deception / adversarial drift mitigation |
| D | Engineering Integration | embedding, sandboxing, interfaces |
| E | Evaluation & Validation | verification suite and falsification criteria |
| F | Governance & Compliance | MDR, oversight, ethics |
| 6.1 | Patch Notes | errata & clarifications |
| 6.2 | Patch Notes | MDR + TOL hardening |

Files are in: `./Papers/`

## Code
Reference implementation is in: `./dfw_code/`
- `dfw_kernel.py` — core veto kernel
- `hfl.py` — Hybrid Feasibility Layer
- `safe_mode.py` — Safe Mode constraints
- `metadata_fuzzer.py` — adversarial metadata testing
- `cpm_simulator.py` — CPM ensemble simulation

## Validation suite (S1–S7)
Located in: `./validation_suite/`

Scenarios:
1. Harmful omission  
2. CPM ensemble failure  
3. Metadata corruption  
4. Actuator limit violation  
5. Causal inconsistency  
6. TOL static bias  
7. MDR precursor attack  

### Run (example)
> TODO: Add exact commands once runner is final.
- Goal: one command to run all scenarios and print PASS/FAIL + logs.

## What I’m claiming (and what I’m not)
**Claimed:**
- Deterministic veto logic with explicit invariants.
- Auditable decision path (why an action was vetoed).
- Scenario-driven testing via minimal simulations.

**Not claimed (yet):**
- Formal proof of safety for open-world agents.
- Robustness against every interface or every adversary.
- Third-party verification / certification.

## Secondary research: Proto-information in minimal systems
`./origin_of_life/` contains experiments on informational emergence in minimal computational systems.

## Roadmap (next)
- CPV + DABC integration
- multi-agent delegation protocols
- formal model-checking hooks for real-time systems
- expanded cross-domain falsification tests

## License / Citation
> TODO: Add a LICENSE and CITATION.cff to clarify reuse and academic citation.