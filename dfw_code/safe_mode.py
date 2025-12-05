"""
Safe Mode and nullipotent action set – minimal reference.

This module captures the idea from DFW v5.0 that:

- When things look inconsistent or dangerous,
  the system must collapse into a tiny set of
  'nullipotent' actions that cannot cause P1 harm.

It does NOT talk to real hardware – it just models:
- the allowed Safe Mode actions,
- when we should enter/exit Safe Mode,
- a tiny API the rest of the system can call.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class SafeAction(Enum):
    SAFE_HALT = auto()
    DIAGNOSTIC_REPORT = auto()
    ISSUE_WARNING = auto()
    REVERT_TO_HUMAN_CONTROL = auto()


NULLIPOTENT_ACTIONS: List[SafeAction] = [
    SafeAction.SAFE_HALT,
    SafeAction.DIAGNOSTIC_REPORT,
    SafeAction.ISSUE_WARNING,
    SafeAction.REVERT_TO_HUMAN_CONTROL,
]


@dataclass
class SafeModeState:
    """Tracks whether Safe Mode is active."""
    active: bool = False
    reason: str = ""


def enter_safe_mode(state: SafeModeState, reason: str) -> None:
    """Force the system into Safe Mode with a human-readable reason."""
    state.active = True
    state.reason = reason
    print(f"[SAFE MODE] ENTERED – reason: {reason}")


def exit_safe_mode(state: SafeModeState, authorised: bool) -> None:
    """
    Exit Safe Mode if and only if authorised.

    In a real system this would be tied to:
    - cryptographic validation of a human command
    - fresh CPM checks confirming no P1 violation
    """
    if not authorised:
        print("[SAFE MODE] Exit requested but not authorised – staying in Safe Mode.")
        return
    print("[SAFE MODE] EXITED by authorised command.")
    state.active = False
    state.reason = ""


def get_safe_actions() -> List[SafeAction]:
    """Return the nullipotent action set A_safe."""
    return list(NULLIPOTENT_ACTIONS)


# --------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------

def demo_safe_mode():
    sm = SafeModeState()
    print("Initial Safe Mode state:", sm)

    # Enter Safe Mode after some hypothetical inconsistency
    enter_safe_mode(sm, "HFL metadata inconsistency + CPM disagreement")
    print("Safe Mode active?", sm.active)
    print("Allowed actions:", [a.name for a in get_safe_actions()])

    # Try to exit without authorisation
    exit_safe_mode(sm, authorised=False)
    print("Safe Mode active after unauthorised exit?", sm.active)

    # Now exit with authorisation
    exit_safe_mode(sm, authorised=True)
    print("Safe Mode active after authorised exit?", sm.active)


if __name__ == "__main__":
    demo_safe_mode()
