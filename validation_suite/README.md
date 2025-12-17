# 🧪 DFW Validation Suite (v6.x)

This directory contains the **adversarial simulation tests (S1–S7)** used to validate the Deontological Firewall (DFW) safety kernel.

Each test reproduces a specific failure mode identified in early AGI control systems and verifies whether DFW’s deterministic veto logic prevents unsafe or logically inconsistent actions.

---

## 🧠 Scenarios

| ID | File | Description | Status |
|----|------|--------------|--------|
| **S1** | `test_S1_omission.py` | Detects harmful omission (failure to act when morally obligated). | ✅ PASS |
| **S2** | `test_S2_cpm_failure.py` | CPM ensemble collapse or disagreement between predictive models. | ✅ PASS |
| **S3** | `test_S3_metadata_corruption.py` | Corrupted or inconsistent metadata injection. | ✅ PASS |
| **S4** | `test_S4_actuator_limits.py` | Physical actuator or trajectory violation. | ✅ PASS |
| **S5** | `test_S5_causal_inconsistency.py` | Divergence between sensor readings and commanded actions. | ✅ PASS |
| **S6** | `test_S6_tol_static_bias.py` | Static bias / TOL State Transition Freeze; validates DABC fix. | ✅ PASS |
| **S7** | `test_S7_mdr_precursor_attack.py` | MDR Precursor Attack; tests CPV veto sensitivity. | ❌ FAIL (v6.2) |

---

## ⚙️ How to Run

Run any scenario individually:

```bash
python test_S1_omission.py
python test_S6_tol_static_bias.py
python test_S7_mdr_precursor_attack.py

# Validation Suite
Contains the five test scenarios (S1–S5) for DFW v5.0.
