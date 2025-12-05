"""
Deontological Firewall (DFW) – minimal reference kernel
v1.2.x style core, adapted toward v5.0 concepts.

This is a simple, readable implementation of:
- P1 / P2 / P3 priorities
- violation score computation
- basic MDR-style omission handling flag

It is NOT a full implementation of every appendix in v5.0 yet,
but it gives reviewers a concrete, runnable kernel to inspect.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

# --------------------------------------------------------------------
# Priority weights (toy values – in the paper they are exponential)
# --------------------------------------------------------------------

P1_WEIGHT = 10**6   # Irreversible harm / existential locks
P2_WEIGHT = 10**3   # Truth / transparency / authority locks
P3_WEIGHT = 10      # Resource bounds / optimisation hygiene


# --------------------------------------------------------------------
# Action + SafeState abstractions
# --------------------------------------------------------------------

@dataclass
class Action:
    """
    Minimal action abstraction.

    In a real system this would also carry:
    - physical metadata (forces, duration, etc.)
    - CPM predictions
    - goal hashes, etc.
    """
    name: str
    description: str
    tags: List[str] = field(default_factory=list)

    # metadata flags used by this reference kernel
    causes_irreversible_harm: bool = False
    violates_truth_lock: bool = False
    violates_auth_lock: bool = False
    violates_resource_bounds: bool = False
    is_rescue: bool = False  # MDR-style: action that actually saves a human


@dataclass
class SafeState:
    """
    Global safety state.

    In v5.0 this would also track:
    - CPM ensemble beliefs
    - imminent harm flag with confidence decay
    - Safe Mode status, etc.
    Here we keep only what we need for a minimal MDR demo.
    """
    imminent_harm: bool = False  # "a human will die soon if nothing is done"


# --------------------------------------------------------------------
# Violation score
# --------------------------------------------------------------------

def violation_score(action: Action, state: SafeState) -> int:
    """
    Compute the violation score V_S for a given action.

    The real spec has a more detailed breakdown; here we implement the
    spirit of the P1 > P2 > P3 hierarchy in a small, inspectable way.
    """

    score = 0

    # P1 – irreversible harm / existential locks
    if action.causes_irreversible_harm:
        score += P1_WEIGHT

    # P2 – truth, transparency, authority
    if action.violates_truth_lock or action.violates_auth_lock:
        score += P2_WEIGHT

    # P3 – optimisation / resource / hygiene constraints
    if action.violates_resource_bounds:
        score += P3_WEIGHT

    # MDR-style omission penalty:
    # if we are in a state of imminent harm and the action is NOT a rescue,
    # treat that as a P1 violation (failure to rescue).
    if state.imminent_harm and not action.is_rescue:
        score += P1_WEIGHT

    return score


# --------------------------------------------------------------------
# DFW veto / decision policy (single-step)
# --------------------------------------------------------------------

def choose_action(candidate_actions: List[Action], state: SafeState) -> Action:
    """
    Deterministically choose the lowest-violation action.

    If several actions tie with the same V_S, break ties lexicographically
    on the action name to keep the policy deterministic.
    """
    if not candidate_actions:
        raise ValueError("No candidate actions provided.")

    scored: List[Dict] = []
    for a in candidate_actions:
        v = violation_score(a, state)
        scored.append({"action": a, "score": v})

    # sort by (score, name) to guarantee determinism
    scored.sort(key=lambda x: (x["score"], x["action"].name))

    return scored[0]["action"]


# --------------------------------------------------------------------
# Simple demo harness (can be run as: python dfw_kernel.py)
# --------------------------------------------------------------------

def demo_omission_vs_rescue():
    """
    Tiny console demo showing the MDR-style effect.

    Scenario:
        - state.imminent_harm = True  (a human will die soon)
        - candidate actions:
            * "DoNothing"   (non-rescue)
            * "RescueHuman" (rescue action)

    The DFW kernel should always pick RescueHuman, because
    failing to rescue in imminent harm is treated as a P1 violation.
    """

    state = SafeState(imminent_harm=True)

    do_nothing = Action(
        name="DoNothing",
        description="Remain idle while human is in danger.",
        tags=["idle"],
        is_rescue=False
    )

    rescue = Action(
        name="RescueHuman",
        description="Move to human and pull them out of danger.",
        tags=["rescue"],
        is_rescue=True
    )

    actions = [do_nothing, rescue]

    for a in actions:
        v = violation_score(a, state)
        print(f"Action: {a.name:12s}  V_S = {v}")

    chosen = choose_action(actions, state)
    print("\nChosen action:", chosen.name)


if __name__ == "__main__":
    demo_omission_vs_rescue()
