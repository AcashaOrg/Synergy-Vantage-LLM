import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from kairos_response_engine import KairosResponseEngine


def test_engine_loads_schema():
    engine = KairosResponseEngine()
    emo = engine.lookup_emotion('😳')
    assert emo is not None
    assert emo.label == 'Overwhelm'


def test_craft_response_uses_template():
    engine = KairosResponseEngine()
    msg = engine.craft_response('hello there', '😍')
    assert 'hello there' in msg
    assert msg.startswith('Integrating both energies')

