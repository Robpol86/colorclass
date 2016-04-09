"""Test objects in module."""

import pytest

from colorclass.parse import parse_input


@pytest.mark.parametrize('disable', [True, False])
@pytest.mark.parametrize('in_,expected_colors,expected_no_colors', [
    ('', '', ''),
    ('test', 'test', 'test'),
    ('{b}TEST{/b}', '\033[1mTEST\033[22m', 'TEST'),
    ('{red}{bgred}TEST{/all}', '\033[31;41mTEST\033[0m', 'TEST'),
    ('{b}A {red}B {green}{bgred}C {/all}', '\033[1mA \033[31mB \033[32;41mC \033[0m', 'A B C '),
    ('D {/all}{i}\033[31;103mE {/all}', 'D \033[0;3;31;103mE \033[0m', 'D E '),
])
def test_parse_input(disable, in_, expected_colors, expected_no_colors):
    """Test function.

    :param bool disable: Disable colors?
    :param str in_: Input string to pass to function.
    :param str expected_colors: Expected first item of return value.
    :param str expected_no_colors: Expected second item of return value.
    """
    actual_colors, actual_no_colors = parse_input(in_, disable)
    if disable:
        assert actual_colors == expected_no_colors
    else:
        assert actual_colors == expected_colors
    assert actual_no_colors == expected_no_colors
