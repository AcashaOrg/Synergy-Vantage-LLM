import sys
import os
from unittest.mock import patch

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from kairos_protocol.rhythm import RhythmPhase


@patch('kairos_protocol.rhythm.sleep', lambda *a, **k: None)
@patch('kairos_protocol.rhythm.random.uniform', lambda a, b: 0)
def test_inhale_and_reflect():
    r = RhythmPhase()
    assert r.inhale() is None
    out = r.reflect('hello')
    assert out == '[Reflected Insight]: hello'


def test_pulse_and_silence():
    r = RhythmPhase()
    assert r.pulse() == '~pulse~'
    assert r.silence() == '(silent)'


@patch('kairos_protocol.rhythm.sleep', lambda *a, **k: None)
def test_exhale_prints_slowly(capsys):
    r = RhythmPhase()
    r.exhale('slow speak')
    captured = capsys.readouterr().out.strip()
    assert captured == 'slow speak'
