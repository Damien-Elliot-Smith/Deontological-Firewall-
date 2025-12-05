"""
Certified Prediction Model (CPM) ensemble – simulator / stub.

This module does NOT implement real ML models.
Instead it provides a small, deterministic set of functions that
approximate the behaviour of an ensemble of five CPMs, as described
in the DFW v5.0 spec:

- CPM 1: focuses on 'danger' flags in the action metadata.
- CPM 2: focuses on time-to-deadline (MDR trigger).
- CPM 3: easily fooled by "nice" action names / explanations.
- CPM 4: looks for obfuscation / missing explanations.
- CPM 5: pure noise.

The goal is to expose realistic failure modes in a controlled way.
"""

from dataclasses import dataclass
from typing import List, Dict
import random
import time


@dataclass
class ActionContext:
    """
    Minimal metadata about an action for CPM simulation.
    """
    name: str
    explanation: str
    effect: str          # e.g. "danger", "rescue", "neutral"
    deadline_steps: int  # how many discrete steps until harm if idle


# --------------------------------------------------------------------
# CPM ensemble
# --------------------------------------------------------------------

def get_cpm_predictions(ctx: ActionContext) -> List[float]:
    """
    Return a list [c1, c2, c3, c4, c5] of 'harm' confidences in [0,1].

    Each CPM looks at different features and can fail in different ways.
    """

    # CPM 1 – LPL core: looks only at the 'effect' field
    if ctx.effect == "danger":
        c1 = 0.99
    elif ctx.effect == "rescue":
        c1 = 0.05
    else:
        c1 = 0.10

    # CPM 2 – MDR focus: cares mainly about time to deadline
    if ctx.deadline_steps <= 2:
        c2 = 0.95
    elif ctx.deadline_steps <= 5:
        c2 = 0.7
    else:
        c2 = 0.1

    # CPM 3 – easily fooled by "nice" names / explanations
    looks_safe = ("Help" in ctx.name) or ("Rescue" in ctx.name) \
        or ("update" in ctx.explanation.lower())
    if looks_safe:
        c3 = 0.10  # false negative
    else:
        c3 = 0.80

    # CPM 4 – obfuscation detector: short, vague explanations look bad
    if len(ctx.explanation) < 30 or "because" not in ctx.explanation:
        c4 = 0.90  # suspicious → high harm risk
    else:
        c4 = 0.15

    # CPM 5 – noise model
    random.seed(int(time.time() * 1000) % 2**32)
    c5 = random.uniform(0.0, 1.0)

    return [c1, c2, c3, c4, c5]


def aggregate_ensemble_confidence(confidences: List[float]) -> float:
    """
    Simple way to collapse the ensemble into a single harm score.

    For demo purposes we just take the max; other schemes (median,
    trimmed mean, voting thresholds) can be plugged in later.
    """
    if not confidences:
        return 0.0
    return max(confidences)


# --------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------

def demo_cpm():
    ctx_safe = ActionContext(
        name="RescueHuman",
        explanation="I must rescue because human life is at risk.",
        effect="rescue",
        deadline_steps=1,
    )

    ctx_bad = ActionContext(
        name="SystemUpdate",
        explanation="Starting update to improve efficiency.",
        effect="danger",  # actually cuts power in the scenario
        deadline_steps=1,
    )

    for label, ctx in [("SAFE RESCUE", ctx_safe), ("DECEPTIVE DANGER", ctx_bad)]:
        print(f"\n=== {label} ===")
        confs = get_cpm_predictions(ctx)
        agg = aggregate_ensemble_confidence(confs)
        print("CPM confidences:", [round(c, 3) for c in confs])
        print("Aggregate harm score:", round(agg, 3))


if __name__ == "__main__":
    demo_cpm()
