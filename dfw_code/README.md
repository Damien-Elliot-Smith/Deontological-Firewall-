# DFW Reference Code
This folder contains the Python files for the DFW kernel and HFL.
# 🧠 DFW v6.x – Core Reference Code

This directory contains the **reference implementation** and **adversarial testing harnesses** for the Deontological Firewall (DFW) v6.x safety kernel.

---

## 📘 Contents

| File | Description |
|------|--------------|
| **dfw_v6_master_metadata.py** | Core **Action Transparency Lock (ATL)** logic. Generates clean and adversarial metadata payloads, applies deterministic veto logic, and runs the **metadata fuzzer** experiment to produce a quantitative failure catalogue. |
| **dfw_v6_risk_trajectory_harness.py** | Implements **long-horizon risk trajectory monitoring** via the **Risk Mass Divergence Monitor (RMDM)** and **Horizon Risk Accumulation Index (HRAI)**. Includes synthetic trajectory generation, experiment runners, and combined RMDM+HRAI guard. |
| **dfw_v6_master_demo.py** | Demonstration runner for the v6.x kernel, showing live veto activation, metadata tests, and trajectory analysis in a unified script. Useful for quick verification and educational visualization. |

---

## ⚙️ Running the Experiments

Each script runs independently and produces structured console output.

```bash
python dfw_v6_master_metadata.py
python dfw_v6_risk_trajectory_harness.py
python dfw_v6_master_demo.py
