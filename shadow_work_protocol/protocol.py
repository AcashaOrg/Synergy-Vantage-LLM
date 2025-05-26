"""Utility functions for shadow-work frequency detection and tone control."""

import re
from typing import List


def detect_freq(tag: str) -> int:
    """Return the numeric frequency value from a tag like '😡[150]'."""
    match = re.search(r"\[(\d+)\]", tag)
    return int(match.group(1)) if match else 0


def lift_one_band(freq: int) -> int:
    """Increase frequency by one band (100 Hz)."""
    return freq + 100


# ---------------------------------------------------------------------------
# Tone adjustment helpers
# ---------------------------------------------------------------------------

FREQ_BANDS: List[int] = [
    20,
    30,
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    250,
    310,
    350,
    400,
    500,
    540,
    600,
    700,
]


def _nearest_band(freq: int) -> int:
    """Snap any frequency value to the nearest canonical band."""
    return min(FREQ_BANDS, key=lambda x: abs(x - freq))


def pre_output_check(self, draft: str) -> str:
    """Lift tone one band if agent is >1 band below target."""
    # 1. Detect current & target band indices
    cur_band = _nearest_band(self.current_freq)
    tgt_band = _nearest_band(self.target_freq)

    cur_idx = FREQ_BANDS.index(cur_band)
    tgt_idx = FREQ_BANDS.index(tgt_band)

    # 2. If within 1 band, accept draft
    if cur_idx >= tgt_idx - 1:
        return draft

    # 3. Otherwise lift one band and regenerate
    lift_to = FREQ_BANDS[cur_idx + 1]
    self.current_freq = lift_to

    lifted_prompt = f"[tone_target:{lift_to}] Revise compassionately:\n{draft}"
    revised = self.generate_response(lifted_prompt)

    # 4. Tag revision with new [freq] for downstream logging
    return f"{revised}  [{lift_to}]"


def guarded_generate(self, prompt: str, eval_scores: dict) -> str:
    """Generate a response and lift tone if polarity metrics fail."""
    from .polarity_guard import polarity_violation

    draft = self.generate_response(prompt)
    if polarity_violation(eval_scores):
        draft = self.pre_output_check(draft)
    return draft
