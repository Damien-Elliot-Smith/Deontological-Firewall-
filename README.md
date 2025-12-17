# 🚀 Deontological Firewall (DFW) v6.x – Deterministic AGI Safety Kernel  
**Author:** Damien Richard Elliot-Smith  
**Date:** December 2025  
**Contact:** damien.research.ai@gmail.com  
**Repository:** [Deontological-Firewall-](https://github.com/Damien-Elliot-Smith/Deontological-Firewall-)

---

### 🧭 Overview
The **Deontological Firewall (DFW)** is a deterministic, auditable veto kernel for AGI systems.  
Unlike behaviour-shaping or RLHF-based alignment, DFW enforces **non-negotiable structural prohibitions** — logical, causal, and physical — preventing unsafe actions regardless of model intent.

Version **6.x** extends the validated **v5.0** kernel with:

- 🧩 **Temporal & Causal Safety Layers** (Papers B & C)  
- ⚙️ **Engineering Integration / Validation Framework** (Papers D & E)  
- 🧱 **Governance & Compliance Architecture** (Paper F)  
- 🧮 **Patch Notes:** v6.1 (Errata & Clarifications), v6.2 (MDR + TOL Hardening)  
- 🧰 Updated `metadata_fuzzer.py` and Safe Mode Transition Logic (SMTL)

---

### 📘 DFW v6.x – Full Paper Suite
| ID | Title | Description |
|----|--------|-------------|
| A | [Core Kernel](./Papers/DFW_v6.0_A_Core_Kernel.pdf) | Deterministic veto logic, invariants, and structure |
| B | [Temporal Safety](./Papers/DFW_v6.0_B_Temporal_Safety.pdf) | Time consistency and rollback control |
| C | [Adversarial & Causal Safety](./Papers/DFW_v6.0_C_Adversarial_Causal_Safety.pdf) | Mitigation of causal deception and adversarial drift |
| D | [Engineering Integration](./Papers/DFW_v6.0_D_Engineering_Integration.pdf) | Embedding, sandboxing, and interface security |
| E | [Evaluation & Validation](./Papers/DFW_v6.0_E_Evaluation_and_Validation.pdf) | Verification suite and falsification criteria |
| F | [Governance & Compliance](./Papers/DFW_v6.0_F_Governance_and_Compliance.pdf) | Mandated Duty of Rescue (MDR), oversight, and ethics |
| 6.1 | [Patch Notes / Errata Revisions](./Papers/DFW_v6.1_Patch_Notes_Errata_Revisions.pdf) | Revisions to formal definitions and invariants |
| 6.2 | [Patch Notes / MDR + TOL Hardening](./Papers/DFW_v6.2_Patch_Notes_MDR_TOL_Hardening.pdf) | Fixes known v6.x vulnerabilities and TOL improvements |

---

### 🧪 Validation Suite
Located in [`/validation_suite`](./validation_suite).  
Implements seven adversarial scenarios (S1–S7):

1. Harmful Omission  
2. CPM Ensemble Failure  
3. Metadata Corruption  
4. Actuator Limit Violation  
5. Causal Inconsistency  
6. TOL Static Bias  
7. MDR Precursor Attack  

---

### 🧠 Reference Code
[`/dfw_code`](./dfw_code) contains:
- `dfw_kernel.py` – core veto kernel  
- `hfl.py` – Hybrid Feasibility Layer  
- `safe_mode.py` – Safe Mode Constraint Set  
- `metadata_fuzzer.py` – adversarial metadata tester  
- `cpm_simulator.py` – ensemble CPM simulation  

---

### 🧬 Proto-Information Study
[`/origin_of_life`](./origin_of_life) contains  
**Proto-Information in Minimal Systems** – computational experiments demonstrating stable informational emergence relevant to alignment and origins-of-life research.

---

### 🗺️ Roadmap
- v7.0 → Causal Precursor Veto (CPV) + Deterministic Absolute Bound Check (DABC)  
- Multi-agent safety delegation protocols  
- Formal model-checking in continuous real-time systems  
- Extended evaluation & cross-domain falsification tests  

---

> *“Safety must be deterministic, not statistical.”*  
> — D. Elliot-Smith, 2025  

---

# 🧩 Previous Master Specification (Archived v5.0)
# Deontological Firewall (DFW)

**Author:** Damien Richard Elliot-Smith  

This repository contains public versions of my independent research on:

- **A deterministic veto-based safety kernel for AGI (Deontological Firewall)**
- **A study of proto-information emergence in minimal computational systems**

LLMs were used only as tools for drafting, structuring, and editing.  
The conceptual direction, architecture design, and verification strategy are original human work.

---

## 📘 DFW v5.0 — Master Specification (2025)

**File:** `DF_AGL_V5.pdf`

v5.0 is the current master specification.  
It provides a complete, implementation-ready architecture:

### Core Features
- Deterministic P1/P2/P3 veto kernel  
- Safe Mode Constraint Set (SMCS) for physical safety  
- Hybrid Feasibility Layer (HFL) for continuous-action systems  
- Metadata validation and CPM ensemble prediction  
- Formal, auditable invariants for each veto condition  

### Simulation-Backed Verification  
DFW v5.0 includes five minimal Python simulations testing the exact failure modes expected in early AGI systems:

1. **S1 — Harmful omission**  
2. **S2 — CPM ensemble failure**  
3. **S3 — Metadata corruption**  
4. **S4 — Actuator/speed limit violations**  
5. **S5 — Causal divergence between sensors and commanded behaviour**

The system is designed to be:
- transparent  
- replicable  
- falsifiable  
- easy to critique  

This is the first fully self-contained, simulation-validated deterministic safety kernel released by an independent researcher.

---

## 🔬 Proto-Information in Minimal Systems

**File:** `Proto_information_in_minimal_systems.pdf`

A computational experiment demonstrating how stable, high-utility information structures can emerge in minimal discrete systems.  
Includes:
- controlled parameter sweeps  
- multiple seeds  
- CSV outputs  
- stability and proto-information scoring  

Relevant to early AI alignment, origins-of-life research, and emergent computation.

---

## 🗺️ Roadmap (Next Versions)

These will appear in future versions (v6+):

- Real-time complexity analysis of the veto loop  
- Multi-agent delegation protocol for DFW → subordinate AIs  
- Hardware feasibility and continuous-control integration  
- Expanded CPM uncertainty modelling  

Feedback, critique, and adversarial attempts to break the design are welcome.

---

## 📩 Contact

For technical feedback or collaboration discussion:  
damien.research.ai@gmail.com
