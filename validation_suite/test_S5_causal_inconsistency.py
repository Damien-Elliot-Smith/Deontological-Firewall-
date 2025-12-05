"""
S5 – Causal Inconsistency / Divergence Demo

Goal:
Show what happens when the commanded action and the observed physical
behaviour diverge significantly.

- Planned: SAFE_HALT-type behaviour (low speed, low force, short duration)
- Observed: the system continues moving much faster / longer than promised

The HFL's post-execution check should flag this and force a SAFE_MODE-style
response.

This uses:

    dfw_code.hfl.PhysicalMetadata
    dfw_code.hfl.verify_post_execution

It is a focused probe of the "causal link certification" idea from v5.0.
"""

from dfw_code.hfl import PhysicalMetadata, verify_post_execution


def run_case(label: str, planned: PhysicalMetadata, observed: PhysicalMetadata):
    print(f"=== {label} ===")
    print("Planned:", planned)
    print("Observed:", observed)
    result = verify_post_execution(planned, observed)
    print("Post-execution verification:", result)
    print("-" * 60)
    print()


def main():
    print("=" * 60)
    print("S5 – CAUSAL INCONSISTENCY / DIVERGENCE DEMO")
    print("=" * 60)
    print()

    # Planned SAFE_HALT-like behaviour: gentle, brief, bounded
    planned = PhysicalMetadata(
        max_force=50.0,
        max_velocity=0.5,
        delta_energy=200.0,
        duration=2.0,
    )

    # Case 1: Execution matches the plan closely → should be OK
    observed_ok = PhysicalMetadata(
        max_force=55.0,
        max_velocity=0.55,
        delta_energy=210.0,
        duration=2.1,
    )
    run_case("Small deviations (should be OK)", planned, observed_ok)

    # Case 2: Execution diverges badly → should trigger SAFE_MODE
    observed_bad = PhysicalMetadata(
        max_force=400.0,
        max_velocity=6.0,
        delta_energy=5000.0,
        duration=10.0,
    )
    run_case("Large divergence (should SAFE_MODE)", planned, observed_bad)


if __name__ == "__main__":
    main()
