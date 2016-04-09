"""Test objects in module."""

import pytest

from colorclass.codes import ANSICodeMapping, BASE_CODES, list_tags


def test_ansi_code_mapping_whitelist():
    """Test whitelist enforcement."""
    auto_codes = ANSICodeMapping('{green}{bgred}Test{/all}')

    # Test __getitem__.
    with pytest.raises(KeyError):
        assert not auto_codes['red']
    assert auto_codes['green'] == 32

    # Test iter and len.
    assert sorted(auto_codes) == ['/all', 'bgred', 'green']
    assert len(auto_codes) == 3


@pytest.mark.parametrize('toggle', ['light', 'dark', 'none'])
def test_auto_toggles(toggle):
    """Test auto colors and ANSICodeMapping class toggles.

    :param str toggle: Toggle method to call.
    """
    # Toggle.
    if toggle == 'light':
        ANSICodeMapping.DISABLE_COLORS = False
        ANSICodeMapping.LIGHT_BACKGROUND = True
    elif toggle == 'dark':
        ANSICodeMapping.DISABLE_COLORS = False
        ANSICodeMapping.LIGHT_BACKGROUND = False
    else:
        ANSICodeMapping.DISABLE_COLORS = True
        ANSICodeMapping.LIGHT_BACKGROUND = False

    # Test iter and len.
    auto_codes = ANSICodeMapping('}{'.join([''] + list(BASE_CODES) + ['']))
    count = 0
    for k, v in auto_codes.items():
        count += 1
        assert str(k) == k
        assert v is None or int(v) == v
    assert len(auto_codes) == count

    # Test foreground properties.
    key_fg = '{autoblack}{autored}{autogreen}{autoyellow}{autoblue}{automagenta}{autocyan}{autowhite}'
    actual = key_fg.format(**auto_codes)
    if toggle == 'light':
        assert actual == '3031323334353637'
    elif toggle == 'dark':
        assert actual == '9091929394959697'
    else:
        assert actual == 'NoneNoneNoneNoneNoneNoneNoneNone'

    # Test background properties.
    key_fg = '{autobgblack}{autobgred}{autobggreen}{autobgyellow}{autobgblue}{autobgmagenta}{autobgcyan}{autobgwhite}'
    actual = key_fg.format(**auto_codes)
    if toggle == 'light':
        assert actual == '4041424344454647'
    elif toggle == 'dark':
        assert actual == '100101102103104105106107'
    else:
        assert actual == 'NoneNoneNoneNoneNoneNoneNoneNone'


def test_list_tags():
    """Test list_tags()."""
    actual = list_tags()
    assert ('red', '/red', 31, 39) in actual
    assert sorted(t for i in actual for t in i[:2] if t is not None) == sorted(BASE_CODES)
