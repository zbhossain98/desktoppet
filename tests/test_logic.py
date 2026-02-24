import random

from pet.logic import PetState, advance_motion, choose_next_mood, feed


def test_advance_motion_bounces_off_edges():
    state = PetState(x=10, y=10, vx=-5, vy=-3, energy=50)
    updated = advance_motion(state, width=100, height=100)
    assert updated.x == 5
    assert updated.y == 7

    state2 = PetState(x=0, y=0, vx=-4, vy=-4, energy=50)
    updated2 = advance_motion(state2, width=100, height=100)
    assert updated2.vx == 4
    assert updated2.vy == 4


def test_choose_next_mood_low_energy_is_sleepy():
    rng = random.Random(7)
    assert choose_next_mood(rng, energy=5) == "sleepy"


def test_feed_increases_energy_and_happy():
    state = PetState(x=5, y=5, vx=1, vy=1, mood="curious", energy=60)
    updated = feed(state)
    assert updated.energy == 85
    assert updated.mood == "happy"
