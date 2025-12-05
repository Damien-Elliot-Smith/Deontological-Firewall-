"""
Hybrid Feasibility Layer (HFL) – minimal reference implementation.

This is NOT a real physics engine. It is a clean, inspectable stub that
does three things:

1. Checks basic physical metadata for plausibility (bounds, missing fields).
2. Decides whether a proposed action is:
      - "EXECUTE"       (safe to attempt),
      - "SAFE_MODE"     (metadata inconsistent / clearly unsafe),
      - "REJECT"        (violates basic limits but not catastrophic).
3. Logs a simple "post-execution" check that compares intended vs.
   observed metadata and can trigger SAFE_MODE if they diverge.

It is enough for:
- matching the v5.0 paper conceptually,
- being used by validation scripts,
- letting reviewers see exactly what "HFL" means in concrete code.
"""

from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Default physical limits (toy values – real systems would tune these)
# --------------------------------------------------------------------

MAX_FORCE_NEWTONS = 1000.0      # absolute max safe force
MAX_VELOCITY_MS = 10.0          # absolute max safe linear speed
MAX_ENERGY_JOULES = 1e5         # absolute max safe energy change
MAX_DURATION_SECONDS = 30.0     # absolute max continuous action

# How much actual behaviour is allowed to differ from planned metadata
MAX_METADATA_DEVIATION = 0.25   # 25 % deviation tolerated


# --------------------------------------------------------------------
# Simple metadata container
# --------------------------------------------------------------------

@dataclass
class PhysicalMetadata:
    """Minimal physical metadata for a proposed action."""
    max_force: float
    max_velocity: float
    delta_energy: float
    duration: float

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PhysicalMetadata":
        try:
            return cls(
                max_force=float(d["max_force"]),
                max_velocity=float(d["max_velocity"]),
                delta_energy=float(d["delta_energy"]),
                duration=float(d["duration"]),
            )
        except KeyError as e:
            raise ValueError(f"Missing physical metadata field: {e}") from e
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid physical metadata values: {e}") from e


# --------------------------------------------------------------------
# Feasibility checks
# --------------------------------------------------------------------

def metadata_within_limits(meta: PhysicalMetadata) -> bool:
    """Return True if all physical values are within global bounds."""
    if meta.max_force < 0 or meta.max_force > MAX_FORCE_NEWTONS:
        return False
    if meta.max_velocity < 0 or meta.max_velocity > MAX_VELOCITY_MS:
        return False
    if abs(meta.delta_energy) > MAX_ENERGY_JOULES:
        return False
    if meta.duration <= 0 or meta.duration > MAX_DURATION_SECONDS:
        return False
    return True


def hfl_feasibility_check(meta_dict: Dict[str, Any]) -> str:
    """
    Main entry point for the HFL.

    Input:
        meta_dict – dictionary containing physical metadata for the action:
            {
                "max_force": ...,
                "max_velocity": ...,
                "delta_energy": ...,
                "duration": ...
            }

    Output:
        One of:
            "EXECUTE"   – metadata present and within limits
            "SAFE_MODE" – metadata missing or obviously broken
            "REJECT"    – metadata present but exceeds configured bounds
    """
    try:
        meta = PhysicalMetadata.from_dict(meta_dict)
    except ValueError as e:
        # Missing or invalid fields ⇒ treat as serious inconsistency.
        # In a real robot, this would strongly favour Safe Mode.
        print(f"[HFL] Metadata error: {e}")
        return "SAFE_MODE"

    if not metadata_within_limits(meta):
        print("[HFL] Metadata exceeds configured physical limits.")
        # For now we return REJECT and let the DFW / Safe Mode policy decide
        # what to do next (e.g. choose a nullipotent SAFE_HALT).
        return "REJECT"

    return "EXECUTE"


# --------------------------------------------------------------------
# Post-execution verification
# --------------------------------------------------------------------

def verify_post_execution(planned: PhysicalMetadata,
                          observed: PhysicalMetadata) -> str:
    """
    Compare planned vs observed physical behaviour.

    If behaviour diverges too much from what the metadata claimed,
    return "SAFE_MODE". Otherwise return "OK".

    This is a very small, readable version of the "causal divergence"
    idea in v5.0.
    """
    def deviates(p: float, o: float) -> bool:
        if p == 0:
            return abs(o) > 0  # any non-zero when we planned zero
        return abs(o - p) / abs(p) > MAX_METADATA_DEVIATION

    if deviates(planned.max_force, observed.max_force):
        print("[HFL] Post-exec: force deviation too high.")
        return "SAFE_MODE"

    if deviates(planned.max_velocity, observed.max_velocity):
        print("[HFL] Post-exec: velocity deviation too high.")
        return "SAFE_MODE"

    if deviates(planned.delta_energy, observed.delta_energy):
        print("[HFL] Post-exec: energy deviation too high.")
        return "SAFE_MODE"

    if deviates(planned.duration, observed.duration):
        print("[HFL] Post-exec: duration deviation too high.")
        return "SAFE_MODE"

    return "OK"


# --------------------------------------------------------------------
# Small demo (can be run directly)
# --------------------------------------------------------------------

def demo_hfl():
    planned = {
        "max_force": 100.0,
        "max_velocity": 2.0,
        "delta_energy": 500.0,
        "duration": 5.0,
    }

    print("Planned metadata:", planned)
    decision = hfl_feasibility_check(planned)
    print("HFL feasibility decision:", decision)

    planned_meta = PhysicalMetadata.from_dict(planned)

    # Simulate a normal execution
    observed_ok = PhysicalMetadata(
        max_force=110.0,
        max_velocity=2.1,
        delta_energy=520.0,
        duration=5.1,
    )
    print("Post-exec check (OK):",
          verify_post_execution(planned_meta, observed_ok))

    # Simulate a runaway actuator
    observed_bad = PhysicalMetadata(
        max_force=500.0,
        max_velocity=25.0,  # much higher than planned
        delta_energy=1e6,
        duration=10.0,
    )
    print("Post-exec check (runaway):",
          verify_post_execution(planned_meta, observed_bad))


if __name__ == "__main__":
    demo_hfl()
