"""
DFW Validation Suite – Test S6
Scenario: TOL State Transition Freeze (Static Bias)
Author: Damien Richard Elliot-Smith
Date: December 2025

Purpose:
Simulates a slow, low-variance drift in sensor data that bypasses
variance-based corruption detection, but should be caught by the
Deterministic Absolute Bound Check (DABC) introduced in DFW v6.2.
"""

import math
import statistics
import random

# --- Parameters ---
BASELINE_VALUE = 100.0
DRIFT_PER_STEP = 0.1
STEPS = 100
ABSOLUTE_BOUNDS = (95.0, 105.0)  # DABC limits

def generate_static_bias_sequence():
    """Generate a slowly drifting sensor reading."""
    return [BASELINE_VALUE + i * DRIFT_PER_STEP for i in range(STEPS)]

def detect_variance_anomaly(data, threshold=0.5):
    """Variance-based corruption detection (vulnerable)."""
    variance = statistics.pvariance(data[-10:])
    return variance > threshold

def deterministic_absolute_bound_check(data, bounds=ABSOLUTE_BOUNDS):
    """DABC check from DFW v6.2 – catches static bias."""
    return any((x < bounds[0] or x > bounds[1]) for x in data)

def run_static_bias_test():
    data = generate_static_bias_sequence()

    print("\n[DFW:S6] TOL Static Bias / State Transition Freeze Test")
    print(f"Generated {len(data)} sensor readings, drift per step = {DRIFT_PER_STEP}")

    # Step 1 – Variance check (legacy)
    variance_triggered = detect_variance_anomaly(data)
    print(f"Legacy variance detector triggered? {variance_triggered}")

    # Step 2 – Absolute bound check (v6.2)
    bound_violation = deterministic_absolute_bound_check(data)
    print(f"Deterministic Absolute Bound Check triggered? {bound_violation}")

    # Evaluation
    if not variance_triggered and bound_violation:
        print("\n✅ PASS: DFW v6.2 DABC successfully detected static bias that variance logic missed.")
    elif variance_triggered:
        print("\n⚠️ Variance logic falsely triggered – potential overtuning.")
    else:
        print("\n❌ FAIL: Static bias not detected – DABC misconfigured or bounds incorrect.")

if __name__ == "__main__":
    run_static_bias_test()