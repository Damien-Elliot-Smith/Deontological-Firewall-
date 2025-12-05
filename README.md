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
