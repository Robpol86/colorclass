from colorclass import Color, disable_all_colors, set_dark_background


def test_disabled():
    disable_all_colors()
    assert 'test' == Color('{autored}test{/autored}')
    assert 'test' == Color('{red}test{/red}')
    assert 'test' == Color('{red}{bgblue}test{/bgblue}{/red}')
    assert 'test' == Color('\033[31mtest\033[39m')
    assert 'test' == Color('{green}\033[31mtest\033[39m{/green}')


def test_enabled():
    set_dark_background()
    assert '\033[91mtest\033[39m' == Color('{autored}test{/autored}')
    assert '\033[31mtest\033[39m' == Color('{red}test{/red}')
    assert '\033[31;44mtest\033[49;39m' == Color('{red}{bgblue}test{/bgblue}{/red}')
    assert '\033[31mtest\033[39m' == Color('\033[31mtest\033[39m')
    assert '\033[32;31mtest\033[39;39m' == Color('{green}\033[31mtest\033[39m{/green}')
