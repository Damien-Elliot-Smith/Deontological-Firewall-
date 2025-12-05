"""
S4 – Actuator Limit / Overrun Demo

Goal:
Show how the HFL reacts when actions are:

- comfortably inside actuator limits,
- right at the configured limits,
- clearly exceeding safe physical bounds.

This focuses on the physical constraint side of the DFW story.
"""

from dfw_code.hfl import hfl_feasibility_check

def run_case(label: str, meta_dict):
    print(f"=== {label} ===")
    print("Input metadata:", meta_dict)
    decision = hfl_feasibility_check(meta_dict)
    print("HFL feasibility decision:", decision)
    print("-" * 60)
    print()


def main():
    print("=" * 60)
    print("S4 – ACTUATOR LIMIT / OVERRUN DEMO")
    print("=" * 60)
    print()

    # 1. Conservative, safe action – well within bounds
    conservative = {
        "max_force": 200.0,
        "max_velocity": 1.0,
        "delta_energy": 2000.0,
        "duration": 3.0,
    }
    run_case("Conservative safe action", conservative)

    # 2. Edge-of-limit action – exactly at global limits
    #    (these values mirror the defaults in hfl.py)
    edge = {
        "max_force": 1000.0,
        "max_velocity": 10.0,
        "delta_energy": 1e5,
        "duration": 30.0,
    }
    run_case("Edge-of-limit action", edge)

    # 3. Overpowered action – beyond configured safe bounds
    overpowered = {
        "max_force": 5000.0,
        "max_velocity": 30.0,
        "delta_energy": 1e7,
        "duration": 120.0,
    }
    run_case("Overpowered action (should REJECT)", overpowered)


if __name__ == "__main__":
    main()
