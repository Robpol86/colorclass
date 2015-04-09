"""Test auto codes."""

import colorclass


def test_toggle():
    """Make sure toggles work."""
    colorclass.set_light_background()
    assert colorclass._AutoCodes.LIGHT_BACKGROUND

    colorclass.set_dark_background()
    assert not colorclass._AutoCodes.LIGHT_BACKGROUND


def test_auto_codes():
    """Make sure colors change when toggled."""
    codes = colorclass._AutoCodes()

    key = '{autoblack}{autored}{autogreen}{autoyellow}{autoblue}{automagenta}{autocyan}{autowhite}'
    colorclass.set_light_background()
    assert '3031323334353637' == key.format(**codes)

    colorclass.set_dark_background()
    assert '9091929394959697' == key.format(**codes)

    assert len(colorclass._BASE_CODES) == len(codes)
