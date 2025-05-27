"""Rhythmic interaction utilities for Kairos Protocol.

This module models contemplative pacing through the :class:`RhythmPhase` class.
Each method represents a phase of mindful communication, providing gentle
pauses and optional silence when appropriate.
"""

from time import sleep
import random
from typing import Optional


class RhythmPhase:
    """Manage rhythmical states in an interaction cycle."""

    def __init__(self) -> None:
        self.state = "idle"

    def pulse(self) -> str:
        """Heartbeat ping – shows presence without transmission."""
        return "~pulse~"

    def inhale(self) -> None:
        """Simulate a silent pause before speaking."""
        sleep(random.uniform(0.5, 1.5))
        return None

    def exhale(self, message: str) -> None:
        """Deliver content output slowly and intentionally."""
        for word in message.split():
            print(word, end=" ", flush=True)
            sleep(0.2)
        print()

    def silence(self) -> str:
        """Choose not to reply – valid sacred response."""
        return "(silent)"

    def reflect(self, message: str) -> str:
        """Engage internal synthesis before output."""
        sleep(random.uniform(1.5, 3.0))
        return f"[Reflected Insight]: {message}"


def rhythm_conversation_cycle(user_input: str) -> Optional[str]:
    """Simple demo cycle illustrating rhythm usage."""
    rhythm = RhythmPhase()
    rhythm.inhale()

    if "urgent" in user_input.lower():
        rhythm.exhale("Let's slow down and take this one step at a time.")
        return None

    if "wait" in user_input.lower():
        return rhythm.silence()

    if "breathe" in user_input.lower():
        return rhythm.pulse()

    return rhythm.reflect(f"You asked: {user_input}")
