"""Test auto codes."""

import colorclass
import colorclass.codes
import colorclass.toggles


def test_toggle():
    """Make sure toggles work."""
    colorclass.toggles.set_light_background()
    assert colorclass.codes.ANSICodeMapping.LIGHT_BACKGROUND

    colorclass.toggles.set_dark_background()
    assert not colorclass.codes.ANSICodeMapping.LIGHT_BACKGROUND
