"""Utility functions for shadow-work frequency detection."""

import re


def detect_freq(tag: str) -> int:
    """Return the numeric frequency value from a tag like '😡[150]'."""
    match = re.search(r"\[(\d+)\]", tag)
    return int(match.group(1)) if match else 0


def lift_one_band(freq: int) -> int:
    """Increase frequency by one band (100 Hz)."""
    return freq + 100
