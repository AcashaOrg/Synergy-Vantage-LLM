from shadow_work_protocol.protocol import lift_one_band


def test_lift_one_band():
    """lift_one_band should increase frequency by 100."""
    assert lift_one_band(150) == 250
