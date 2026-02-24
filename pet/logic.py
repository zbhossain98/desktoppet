from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class PetState:
    x: int
    y: int
    vx: int
    vy: int
    mood: str = "happy"
    energy: int = 100


MOODS = ["happy", "curious", "sleepy", "playful"]


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def choose_next_mood(rng: random.Random, energy: int) -> str:
    """Pick a mood influenced by energy level."""
    if energy < 25:
        return "sleepy"
    if energy > 80 and rng.random() < 0.35:
        return "playful"
    return rng.choice(MOODS)


def advance_motion(state: PetState, width: int, height: int) -> PetState:
    """Move pet by velocity and bounce from edges."""
    nx = state.x + state.vx
    ny = state.y + state.vy
    vx = state.vx
    vy = state.vy

    if nx <= 0 or nx >= width:
        vx *= -1
        nx = clamp(nx, 0, width)

    if ny <= 0 or ny >= height:
        vy *= -1
        ny = clamp(ny, 0, height)

    return PetState(
        x=nx,
        y=ny,
        vx=vx,
        vy=vy,
        mood=state.mood,
        energy=clamp(state.energy - 1, 0, 100),
    )


def feed(state: PetState) -> PetState:
    return PetState(
        x=state.x,
        y=state.y,
        vx=state.vx,
        vy=state.vy,
        mood="happy",
        energy=clamp(state.energy + 25, 0, 100),
    )
