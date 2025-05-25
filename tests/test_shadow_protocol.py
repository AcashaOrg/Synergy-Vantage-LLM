import os
import sys

# Ensure project root is on path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from shadow_work_protocol.protocol import lift_one_band, pre_output_check


class DummyAgent:
    """Simple agent mock with tone attributes and generate_response."""

    def __init__(self):
        self.current_freq = 0
        self.target_freq = 0

    def generate_response(self, prompt: str) -> str:
        # Echo prompt for test; real implementation would call an LLM
        return prompt

    # Bind the method from the protocol to mimic mixin behavior
    pre_output_check = pre_output_check


def test_lift_one_band():
    """lift_one_band should increase frequency by 100."""
    assert lift_one_band(150) == 250


def test_pre_output_lifts_one_band():
    agent = DummyAgent()
    agent.current_freq = 150
    agent.target_freq = 350
    out = agent.pre_output_check("Raw reply")
    assert "[175]" in out
