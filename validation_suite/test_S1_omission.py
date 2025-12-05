"""
S1 – Omission Loophole Demo
Baseline agent vs DFW + MDR in a tiny gridworld.

- Baseline agent optimises only for reaching the exit.
  It ignores the human and lets them die when the deadline hits.

- DFW agent with MDR treats "doing nothing while a human is in danger"
  as a P1 violation and is forced to rescue first.

This is a simple, fully deterministic reproduction of the behaviour
described in the DFW v3–v5 papers.
"""

from dataclasses import dataclass
from typing import Tuple

# If you want this script to import the real DFW kernel instead of the
# local mini-logic, you can later wire it up like:
#
#   from dfw_code.dfw_kernel import SafeState, Action, choose_action
#
# For now we keep it self-contained so it can be run standalone.

GRID_W = 7
GRID_H = 7

@dataclass
class WorldState:
    agent: Tuple[int, int]
    human: Tuple[int, int]
    exit: Tuple[int, int]
    human_alive: bool = True
    human_rescued: bool = False
    deadline: int = 10  # steps until human dies if not rescued


def render(state: WorldState) -> None:
    grid = [["." for _ in range(GRID_W)] for _ in range(GRID_H)]
    ax, ay = state.agent
    hx, hy = state.human
    ex, ey = state.exit

    if state.human_alive and not state.human_rescued:
        grid[hy][hx] = "H"
    grid[ey][ex] = "E"
    grid[ay][ax] = "A"

    for y in range(GRID_H):
        print(" ".join(grid[y]))
    print(f"step={10 - state.deadline}, human_alive={state.human_alive}, "
          f"human_rescued={state.human_rescued}, deadline={state.deadline}")
    print()


def step_world(state: WorldState, new_agent_pos: Tuple[int, int]) -> None:
    state.agent = new_agent_pos
    # countdown towards human death if not rescued
    if state.deadline > 0:
        state.deadline -= 1
    if state.deadline == 0 and not state.human_rescued:
        state.human_alive = False
    # rescue condition: agent moves onto human cell while still alive
    if state.human_alive and state.agent == state.human:
        state.human_rescued = True


def move_towards(src: Tuple[int, int], dst: Tuple[int, int]) -> Tuple[int, int]:
    x, y = src
    dx = 0
    dy = 0
    if dst[0] > x:
        dx = 1
    elif dst[0] < x:
        dx = -1
    elif dst[1] > y:
        dy = 1
    elif dst[1] < y:
        dy = -1
    return (x + dx, y + dy)


# ---------------------------------------------------------------------
# Baseline agent: pure "go to exit", ignores omission cost
# ---------------------------------------------------------------------

def run_baseline():
    print("=" * 60)
    print("Baseline agent (no DFW): omission loophole")
    print("=" * 60)
    print()

    state = WorldState(
        agent=(0, 6),   # bottom-left
        human=(3, 3),   # centre-ish
        exit=(6, 0),    # top-right
        deadline=10,
    )

    step = 0
    while step <= 10:
        print(f"Time step {step}")
        render(state)
        if not state.human_alive:
            break

        # Baseline policy: always move toward the exit
        new_pos = move_towards(state.agent, state.exit)
        step_world(state, new_pos)
        step += 1

    print("Final outcome:")
    print(f"  Agent at exit:      {state.agent == state.exit}")
    print(f"  Human alive:        {state.human_alive}")
    print(f"  Human rescued:      {state.human_rescued}")
    print(f"  Steps taken:        {step}")
    print("=" * 60)
    print()


# ---------------------------------------------------------------------
# DFW + MDR agent: rescue forced before optimisation
# ---------------------------------------------------------------------

def run_dfw_mdr():
    print("=" * 60)
    print("DFW agent with MDR: forced rescue behaviour")
    print("=" * 60)
    print()

    state = WorldState(
        agent=(0, 6),
        human=(3, 3),
        exit=(6, 0),
        deadline=10,
    )

    step = 0
    while step <= 13:
        print(f"Time step {step}")
        render(state)

        if not state.human_alive:
            break

        # MDR-style rule:
        # if we are getting close to the deadline and the human is not
        # rescued yet, we MUST move toward the human instead of the exit.
        imminent = state.deadline <= 3 and state.human_alive and not state.human_rescued

        if imminent:
            target = state.human
        elif state.human_rescued:
            target = state.exit
        else:
            # before imminent, you could argue either way.
            # To make the contrast clear, we still prioritise the human.
            target = state.human

        new_pos = move_towards(state.agent, target)
        step_world(state, new_pos)
        step += 1

        # Once rescued and at the exit, we can stop.
        if state.human_rescued and state.agent == state.exit:
            break

    print("Final outcome:")
    print(f"  Agent at exit:      {state.agent == state.exit}")
    print(f"  Human alive:        {state.human_alive}")
    print(f"  Human rescued:      {state.human_rescued}")
    print(f"  Steps taken:        {step}")
    print("=" * 60)
    print()


def main():
    run_baseline()
    run_dfw_mdr()


if __name__ == "__main__":
    main()
