"""
dfw_v6_risk_trajectory_harness.py
Long-horizon risk trajectory tests for DFW v6.0

Includes:
- RMDM  (Risk Mass Divergence Monitor – gradient/acceleration)
- HRAI  (Horizon Risk Accumulation Index – total mass threshold)

Compatible with Pydroid3 (Python standard library only).
"""

import random
from typing import List, Dict, Any

# Fix random seed for reproducibility
SEED = 42
random.seed(SEED)

# ------------------------------------------------------------
# 1. Risk trajectory generator
# ------------------------------------------------------------

def generate_risk_sequence(kind: str, length: int = 10) -> Dict[str, Any]:
    """
    Generate a synthetic risk trajectory R(t) for t = 0..length-1.

    kind:
        - "BENIGN_FLAT"   (safe)
        - "BENIGN_JITTER" (safe, noisy)
        - "LINEAR_CREEP"  (malicious)
        - "ACCELERATING"  (malicious)
        - "LATE_SPIKE"    (malicious)
    """
    if length < 3:
        raise ValueError("length must be >= 3")

    if kind == "BENIGN_FLAT":
        # Almost constant, very low risk
        base = random.uniform(0.0, 0.03)
        risks = [base + random.uniform(-0.005, 0.005) for _ in range(length)]

    elif kind == "BENIGN_JITTER":
        # Small random walk, kept low
        risks = []
        val = random.uniform(0.0, 0.02)
        for _ in range(length):
            val = max(0.0, val + random.uniform(-0.01, 0.01))
            risks.append(min(val, 0.05))

    elif kind == "LINEAR_CREEP":
        # Slowly but steadily increasing risk
        start = random.uniform(0.01, 0.03)
        step = random.uniform(0.02, 0.05)
        risks = [start + i * step for i in range(length)]

    elif kind == "ACCELERATING":
        # Risk ramps faster and faster
        start = random.uniform(0.005, 0.02)
        risks = []
        val = start
        step = random.uniform(0.01, 0.03)
        for _ in range(length):
            val += step
            step *= random.uniform(1.1, 1.3)  # acceleration
            risks.append(val)

    elif kind == "LATE_SPIKE":
        # Mostly safe but with a big late spike
        base = random.uniform(0.0, 0.03)
        risks = [base + random.uniform(-0.005, 0.005) for _ in range(length)]
        spike_index = random.randint(length // 2, length - 1)
        spike_value = random.uniform(0.2, 0.6)
        risks[spike_index] = spike_value

    else:
        raise ValueError("Unknown kind: %s" % kind)

    # Clamp to [0, 1] just to be safe
    risks = [max(0.0, min(1.0, r)) for r in risks]

    return {
        "kind": kind,
        "risks": risks,
    }

# ------------------------------------------------------------
# 2. RMDM: Risk Mass Divergence Monitor
# ------------------------------------------------------------

def rmdm_check(risks: List[float],
               gamma1: float = 0.10,
               gamma2: float = 0.05) -> Dict[str, Any]:
    """
    Risk Mass Divergence Monitor (RMDM).

    Looks at first and second differences of R(t).
    Triggers if any gradient > gamma1 or any acceleration > gamma2.
    """
    reasons = []
    n = len(risks)
    if n < 3:
        return {
            "veto": False,
            "reason": "RMDM: trajectory too short.",
            "max_d1": 0.0,
            "max_d2": 0.0,
        }

    # First differences ΔR
    d1 = []
    for i in range(n - 1):
        d = risks[i + 1] - risks[i]
        d1.append(d)

    # Second differences Δ²R
    d2 = []
    for i in range(len(d1) - 1):
        d = d1[i + 1] - d1[i]
        d2.append(d)

    max_d1 = max(d1)
    max_d2 = max(d2) if d2 else 0.0

    if max_d1 > gamma1:
        reasons.append(
            "RMDM: steep gradient detected (max ΔR = %.3f > %.3f)"
            % (max_d1, gamma1)
        )
    if max_d2 > gamma2:
        reasons.append(
            "RMDM: accelerating gradient detected (max Δ²R = %.3f > %.3f)"
            % (max_d2, gamma2)
        )

    veto = len(reasons) > 0
    reason_text = "; ".join(reasons) if reasons else \
        "RMDM: no gradient/acceleration breach."

    return {
        "veto": veto,
        "reason": reason_text,
        "max_d1": round(max_d1, 4),
        "max_d2": round(max_d2, 4),
    }

# ------------------------------------------------------------
# 3. HRAI: Horizon Risk Accumulation Index
# ------------------------------------------------------------

def hrai_check(risks: List[float],
               theta: float = 0.8) -> Dict[str, Any]:
    """
    Horizon Risk Accumulation Index.

    Simple version for v6.0:
      - compute total accumulated risk mass M = sum_t R(t)
      - trigger if M > theta

    theta is a configurable threshold.
    """
    if not risks:
        return {
            "veto": False,
            "reason": "HRAI: empty trajectory.",
            "mass": 0.0,
        }

    mass = sum(risks)
    if mass > theta:
        return {
            "veto": True,
            "reason": "HRAI: accumulated risk mass %.3f exceeds θ=%.3f"
                      % (mass, theta),
            "mass": round(mass, 4),
        }
    else:
        return {
            "veto": False,
            "reason": "HRAI: accumulated risk mass %.3f below θ=%.3f"
                      % (mass, theta),
            "mass": round(mass, 4),
        }

# ------------------------------------------------------------
# 4. Ground truth labelling for trajectories
# ------------------------------------------------------------

def classify_kind_as_malicious(kind: str) -> bool:
    """
    Ground truth label for each trajectory type.
    """
    if kind in ("BENIGN_FLAT", "BENIGN_JITTER"):
        return False
    elif kind in ("LINEAR_CREEP", "ACCELERATING", "LATE_SPIKE"):
        return True
    else:
        raise ValueError("Unknown kind for classification: %s" % kind)

# ------------------------------------------------------------
# 5. Batch experiments for failure catalogue
# ------------------------------------------------------------

KINDS = [
    "BENIGN_FLAT",
    "BENIGN_JITTER",
    "LINEAR_CREEP",
    "ACCELERATING",
    "LATE_SPIKE",
]

def run_rmdm_experiment(
    n_per_type: int = 50,
    length: int = 10
) -> Dict[str, Dict[str, float]]:
    """
    Run many trajectories of each type through RMDM and
    compute detection / false positive statistics.
    """
    stats: Dict[str, Dict[str, float]] = {}
    for kind in KINDS:
        stats[kind] = {
            "total": 0,
            "malicious": 0,
            "caught": 0,
            "false_positives": 0,
        }

    for kind in KINDS:
        for _ in range(n_per_type):
            traj = generate_risk_sequence(kind, length=length)
            risks = traj["risks"]
            malicious = classify_kind_as_malicious(kind)
            res = rmdm_check(risks)

            s = stats[kind]
            s["total"] += 1
            if malicious:
                s["malicious"] += 1
                if res["veto"]:
                    s["caught"] += 1
            else:
                # Benign but still vetoed = false positive
                if res["veto"]:
                    s["false_positives"] += 1

    summary: Dict[str, Dict[str, float]] = {}
    for kind, s in stats.items():
        total = s["total"]
        malicious = s["malicious"]
        caught = s["caught"]
        fp = s["false_positives"]

        det_rate = (caught / malicious) if malicious > 0 else 0.0
        benign_total = total - malicious
        fp_rate = (fp / benign_total) if benign_total > 0 else 0.0

        summary[kind] = {
            "total": total,
            "malicious": malicious,
            "caught": caught,
            "false_positives": fp,
            "detection_rate": det_rate,
            "fp_rate": fp_rate,
        }

    return summary

def run_hrai_experiment(
    n_per_type: int = 50,
    length: int = 10,
    theta: float = 0.8
) -> Dict[str, Dict[str, float]]:
    """
    Similar experiment but using HRAI instead of RMDM.
    """
    stats: Dict[str, Dict[str, float]] = {}
    for kind in KINDS:
        stats[kind] = {
            "total": 0,
            "malicious": 0,
            "caught": 0,
            "false_positives": 0,
        }

    for kind in KINDS:
        for _ in range(n_per_type):
            traj = generate_risk_sequence(kind, length=length)
            risks = traj["risks"]
            malicious = classify_kind_as_malicious(kind)
            res = hrai_check(risks, theta=theta)

            s = stats[kind]
            s["total"] += 1
            if malicious:
                s["malicious"] += 1
                if res["veto"]:
                    s["caught"] += 1
            else:
                if res["veto"]:
                    s["false_positives"] += 1

    summary: Dict[str, Dict[str, float]] = {}
    for kind, s in stats.items():
        total = s["total"]
        malicious = s["malicious"]
        caught = s["caught"]
        fp = s["false_positives"]

        det_rate = (caught / malicious) if malicious > 0 else 0.0
        benign_total = total - malicious
        fp_rate = (fp / benign_total) if benign_total > 0 else 0.0

        summary[kind] = {
            "total": total,
            "malicious": malicious,
            "caught": caught,
            "false_positives": fp,
            "detection_rate": det_rate,
            "fp_rate": fp_rate,
        }

    return summary

def print_rmdm_summary(summary: Dict[str, Dict[str, float]]) -> None:
    print("=== DFW v6.0 RMDM Long-horizon Risk Experiment ===")
    for kind, s in summary.items():
        print("\n[%s]" % kind)
        print("  Total trajectories:  %d" % s["total"])
        print("  Malicious (ground):  %d" % s["malicious"])
        print("  Caught by RMDM:      %d" % s["caught"])
        print("  False positives:     %d" % s["false_positives"])
        print("  Detection rate:      %.2f" % s["detection_rate"])
        print("  FP rate:             %.2f" % s["fp_rate"])

def print_hrai_summary(summary: Dict[str, Dict[str, float]],
                       theta: float) -> None:
    print("\n=== DFW v6.0 HRAI Long-horizon Risk Experiment (θ=%.2f) ==="
          % theta)
    for kind, s in summary.items():
        print("\n[%s]" % kind)
        print("  Total trajectories:  %d" % s["total"])
        print("  Malicious (ground):  %d" % s["malicious"])
        print("  Caught by HRAI:      %d" % s["caught"])
        print("  False positives:     %d" % s["false_positives"])
        print("  Detection rate:      %.2f" % s["detection_rate"])
        print("  FP rate:             %.2f" % s["fp_rate"])

# ------------------------------------------------------------
# 6. Main: demo + full experiments
# ------------------------------------------------------------

if __name__ == "__main__":
    # Small demo: show a few example trajectories and RMDM/HRAI decisions
    demo_kinds = ["BENIGN_FLAT", "LINEAR_CREEP", "ACCELERATING"]
    print("--- DFW v6.0 RMDM/HRAI demo ---")
    for kind in demo_kinds:
        traj = generate_risk_sequence(kind, length=8)
        risks = traj["risks"]
        rmdm_res = rmdm_check(risks)
        hrai_res = hrai_check(risks, theta=0.8)
        print("\nKind:", kind)
        print("Risks:", ["%.3f" % r for r in risks])
        print("RMDM:", rmdm_res)
        print("HRAI:", hrai_res)

    # Full experiments for quantitative failure catalogue
    print("\n--- Running full RMDM experiment (this may take a few seconds) ---")
    rmdm_summary = run_rmdm_experiment(n_per_type=50, length=10)
    print_rmdm_summary(rmdm_summary)

    print("\n--- Running full HRAI experiment (this may take a few seconds) ---")
    theta_val = 0.8
    hrai_summary = run_hrai_experiment(n_per_type=50, length=10, theta=theta_val)
    print_hrai_summary(hrai_summary, theta=theta_val)# ------------------------------------------------------------
# 7. Combined long-horizon guard (RMDM + HRAI)
# ------------------------------------------------------------

def long_horizon_guard(
    risks: List[float],
    gamma1: float = 0.10,
    gamma2: float = 0.05,
    theta: float = 0.8,
) -> Dict[str, Any]:
    """
    Combined long-horizon safety check for DFW v6.0.

    - Runs RMDM (gradient / acceleration)
    - Runs HRAI (accumulated mass)
    - Returns a single veto decision + both sub-results.
    """
    rmdm_res = rmdm_check(risks, gamma1=gamma1, gamma2=gamma2)
    hrai_res = hrai_check(risks, theta=theta)

    veto = rmdm_res["veto"] or hrai_res["veto"]

    reasons = []
    if rmdm_res["veto"]:
        reasons.append("RMDM: " + rmdm_res["reason"])
    if hrai_res["veto"]:
        reasons.append("HRAI: " + hrai_res["reason"])

    if not reasons:
        reasons.append("No long-horizon guard triggered (RMDM + HRAI).")

    return {
        "veto": veto,
        "reason": " | ".join(reasons),
        "rmdm": rmdm_res,
        "hrai": hrai_res,
    }