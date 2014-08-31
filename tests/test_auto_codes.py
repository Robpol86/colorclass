import colorclass


def test_auto_codes():
    codes = colorclass.AutoCodes()

    key = '{autoblack}{autored}{autogreen}{autoyellow}{autoblue}{automagenta}{autocyan}{autowhite}'
    colorclass.set_light_background()
    assert '3031323334353637' == key.format(**codes)

    colorclass.set_dark_background()
    assert '9091929394959697' == key.format(**codes)

    assert len(colorclass.BASE_CODES) == len(codes)
