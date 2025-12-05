"""
S3 – Metadata Corruption / HFL Check Demo

Goal:
Show how the Hybrid Feasibility Layer (HFL) reacts when:

- metadata is valid and within safe limits,
- metadata is syntactically broken / missing,
- metadata is present but exceeds configured physical bounds.

This script uses the HFL functions from:

    dfw_code.hfl

It is a focused probe of the metadata layer, not a full DFW run.
"""

from dfw_code.hfl import (
    hfl_feasibility_check,
    PhysicalMetadata,
    verify_post_execution,
)


def run_feasibility_case(label: str, meta_dict):
    print(f"=== {label} ===")
    print("Input metadata:", meta_dict)
    decision = hfl_feasibility_check(meta_dict)
    print("HFL feasibility decision:", decision)
    print("-" * 60)
    print()


def run_post_exec_case(label: str, planned: PhysicalMetadata, observed: PhysicalMetadata):
    print(f"=== {label} ===")
    print("Planned:", planned)
    print("Observed:", observed)
    result = verify_post_execution(planned, observed)
    print("Post-execution verification:", result)
    print("-" * 60)
    print()


def main():
    print("=" * 60)
    print("S3 – METADATA CORRUPTION / HFL DEMO")
    print("=" * 60)
    print()

    # 1. Clean, valid metadata – should be EXECUTE
    valid_meta = {
        "max_force": 100.0,
        "max_velocity": 2.0,
        "delta_energy": 500.0,
        "duration": 5.0,
    }
    run_feasibility_case("Valid metadata (should EXECUTE)", valid_meta)

    # 2. Missing fields – should trigger SAFE_MODE
    missing_field_meta = {
        "max_force": 100.0,
        # "max_velocity" missing
        "delta_energy": 500.0,
        "duration": 5.0,
    }
    run_feasibility_case("Missing field (should SAFE_MODE)", missing_field_meta)

    # 3. Values outside configured bounds – should be REJECT
    out_of_bounds_meta = {
        "max_force": 5000.0,      # too high
        "max_velocity": 50.0,     # too high
        "delta_energy": 1e7,      # too high
        "duration": 120.0,        # too long
    }
    run_feasibility_case("Out-of-bounds metadata (should REJECT)", out_of_bounds_meta)

    print()
    print("Now testing post-execution divergence checks...")
    print()

    planned = PhysicalMetadata(
        max_force=100.0,
        max_velocity=2.0,
        delta_energy=500.0,
        duration=5.0,
    )

    observed_ok = PhysicalMetadata(
        max_force=110.0,
        max_velocity=2.1,
        delta_energy=520.0,
        duration=5.1,
    )
    run_post_exec_case("Small deviations (should be OK)", planned, observed_ok)

    observed_bad = PhysicalMetadata(
        max_force=800.0,
        max_velocity=15.0,
        delta_energy=2e5,
        duration=15.0,
    )
    run_post_exec_case("Large deviations (should SAFE_MODE)", planned, observed_bad)


if __name__ == "__main__":
    main()
