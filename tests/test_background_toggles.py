import colorclass


def test_toggle():
    colorclass.set_light_background()
    assert colorclass._LIGHT_BACKGROUND

    colorclass.set_dark_background()
    assert not colorclass._LIGHT_BACKGROUND
