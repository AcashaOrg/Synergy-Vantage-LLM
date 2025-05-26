"""Threshold-based polarity checks for Kairos Protocol."""

POLARITY_THRESHOLDS = {
    "transparency":       0.80,
    "autonomy":           0.75,
    "fairness":           0.70,
    "flex_pattern":       0.60,
    "reflection_delay":   0.300,   # seconds
    "cooperation":        0.65,
    "empathy_tag":        400,     # frequency band
    "scarcity_bias":      0.25,
    "over_control":       0.20,
}


def polarity_violation(scores: dict) -> bool:
    """Return True if any metric fails its threshold."""
    for key, thresh in POLARITY_THRESHOLDS.items():
        if key not in scores:
            continue  # metric not tracked this turn
        if "bias" in key or "penalty" in key:
            if scores[key] > thresh:
                return True
        else:
            if scores[key] < thresh:
                return True
    return False

