"""Kairos Response Engine
=======================

This module provides a thin response engine that interprets emotional
input based on ``synergy_emotion_engine_schema.yaml``. It is intentionally
minimal and serves as a scaffold for future development.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional

# Note: PyYAML is not guaranteed to be available in this environment.
# A minimal YAML parser is implemented to load the static schema used by
# the tests. It supports only the subset of YAML features present in
# ``synergy_emotion_engine_schema.yaml``.

from typing import List

def _parse_scalar(val: str):
    """Convert a scalar YAML value to a Python object."""
    val = val.split("#", 1)[0].strip()
    if val.startswith("\"") and val.endswith("\""):
        val = val[1:-1]
    if val.isdigit():
        return int(val)
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    return val


def _simple_yaml_load(lines: List[str]):
    """Very small YAML loader handling dicts, lists, and multiline strings."""
    root: dict = {}
    stack = [(root, -1)]  # container and its indent level
    current_ml = None  # (container, key, base_indent)

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))

        container, parent_indent = stack[-1]

        if current_ml:
            c, key, base = current_ml
            if indent > base:
                c[key] += raw[base + 2 :] + "\n"
                continue
            else:
                c[key] = c[key].rstrip("\n")
                current_ml = None

        while indent <= parent_indent and len(stack) > 1:
            stack.pop()
            container, parent_indent = stack[-1]

        line = raw.strip()
        if line.startswith("- "):
            if not isinstance(container, list):
                raise ValueError("List item not inside list")
            item: dict = {}
            container.append(item)
            stack.append((item, indent))
            rest = line[2:].strip()
            if rest:
                key, val = rest.split(":", 1)
                val = val.strip()
                if val == "|":
                    item[key] = ""
                    current_ml = (item, key, indent)
                else:
                    item[key] = _parse_scalar(val)
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val == "":
                next_line = lines[i].strip() if i < len(lines) else ""
                new = [] if next_line.startswith("- ") else {}
                container[key] = new
                stack.append((new, indent))
            elif val == "|":
                container[key] = ""
                current_ml = (container, key, indent)
            else:
                container[key] = _parse_scalar(val)
    return root


@dataclass
class EmotionEntry:
    """Structured representation of a single emotion."""

    emoji: str
    label: str
    frequency_level: int
    polarity: str
    direction: str


@dataclass
class ResponseProfile:
    """Default response profile for a polarity."""

    polarity_response: str
    tone_profile: str
    breath_cue: str
    example_template: str


class KairosResponseEngine:
    """Load the emotion schema and provide simple lookup utilities."""

    def __init__(self, schema_path: str | None = None) -> None:
        self.schema_path = schema_path or os.path.join(
            os.path.dirname(__file__), "synergy_emotion_engine_schema.yaml"
        )
        self.system_meta: Dict[str, object] = {}
        self.emotions: Dict[str, EmotionEntry] = {}
        self.response_profiles: Dict[str, ResponseProfile] = {}
        self._load_schema()

    def _load_schema(self) -> None:
        with open(self.schema_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        data = _simple_yaml_load(lines)
        self.system_meta = data.get("system_meta", {})

        for entry in data.get("input_emotions", []):
            emotion = EmotionEntry(**entry)
            # store by emoji and lower‑cased label
            self.emotions[emotion.emoji] = emotion
            self.emotions[emotion.label.lower()] = emotion

        for name, profile in data.get("response_profiles", {}).items():
            self.response_profiles[name] = ResponseProfile(**profile)

    def lookup_emotion(self, token: str) -> Optional[EmotionEntry]:
        """Find emotion by emoji or label."""
        return self.emotions.get(token) or self.emotions.get(token.lower())

    def suggest_profile(self, emotion: EmotionEntry) -> Optional[ResponseProfile]:
        """Get default profile based on emotion polarity."""
        mapping = {"☀️": "masculine", "🌙": "feminine", "☯️": "balanced"}
        name = mapping.get(emotion.polarity)
        if name:
            return self.response_profiles.get(name)
        return None

    def craft_response(self, user_message: str, token: str) -> str:
        """Return a formatted response using the schema's example template."""
        emotion = self.lookup_emotion(token)
        if not emotion:
            return user_message
        profile = self.suggest_profile(emotion)
        if not profile:
            return user_message
        return profile.example_template.format(user_message=user_message)


if __name__ == "__main__":
    engine = KairosResponseEngine()
    demo = engine.craft_response("I appreciate the help!", "😍")
    print(demo)
