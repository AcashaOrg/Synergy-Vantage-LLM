# Kairos Protocol – Rhythmic Interaction

This module offers mindful pacing primitives for conversations. The
`RhythmPhase` class models breathing cycles so an agent can respectfully
pause, speak slowly, or remain silent.

## Usage
```python
from kairos_protocol.rhythm import RhythmPhase

rhythm = RhythmPhase()
print(rhythm.pulse())       # '~pulse~'
print(rhythm.silence())     # '(silent)'
print(rhythm.reflect('hi')) # '[Reflected Insight]: hi'
```
