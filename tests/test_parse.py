"""Test objects in module."""

import pytest

from colorclass.parse import parse_input, prune_overridden


@pytest.mark.parametrize('in_,expected', [
    ('', ''),
    ('test', 'test'),
    ('\033[31mTEST\033[0m', '\033[31mTEST\033[0m'),
    ('\033[32;31mTEST\033[39;0m', '\033[31mTEST\033[0m'),
    ('\033[1;2mTEST\033[22;22m', '\033[1;2mTEST\033[22m'),
    ('\033[1;1;1;1;1;1mTEST\033[22m', '\033[1mTEST\033[22m'),
    ('\033[31;32;41;42mTEST\033[39;49m', '\033[32;42mTEST\033[39;49m'),
])
def test_prune_overridden(in_, expected):
    """Test function.

    :param str in_: Input string to pass to function.
    :param str expected: Expected return value.
    """
    actual = prune_overridden(in_)
    assert actual == expected


@pytest.mark.parametrize('disable', [True, False])
@pytest.mark.parametrize('in_,expected_colors,expected_no_colors', [
    ('', '', ''),
    ('test', 'test', 'test'),
    ('{b}TEST{/b}', '\033[1mTEST\033[22m', 'TEST'),
    ('{red}{bgred}TEST{/all}', '\033[31;41mTEST\033[0m', 'TEST'),
    ('{b}A {red}B {green}{bgred}C {/all}', '\033[1mA \033[31mB \033[32;41mC \033[0m', 'A B C '),
    ('C {/all}{b}{blue}{hiblue}{bgcyan}D {/all}', 'C \033[0;1;46;94mD \033[0m', 'C D '),
    ('D {/all}{i}\033[31;103mE {/all}', 'D \033[0;3;31;103mE \033[0m', 'D E '),
    ('{b}{red}{bgblue}{/all}{i}TEST{/all}', '\033[0;3mTEST\033[0m', 'TEST'),
    ('{red}{green}{blue}{black}{yellow}TEST{/fg}{/all}', '\033[33mTEST\033[0m', 'TEST'),
    ('{bgred}{bggreen}{bgblue}{bgblack}{bgyellow}TEST{/bg}{/all}', '\033[43mTEST\033[0m', 'TEST'),
    ('{red}T{red}E{red}S{red}T{/all}', '\033[31mTEST\033[0m', 'TEST'),
    ('{red}T{/all}E{/all}S{/all}T{/all}', '\033[31mT\033[0mEST', 'TEST'),
    ('{red}{bgblue}TES{red}{bgblue}T{/all}', '\033[31;44mTEST\033[0m', 'TEST'),
])
def test_parse_input(disable, in_, expected_colors, expected_no_colors):
    """Test function.

    :param bool disable: Disable colors?
    :param str in_: Input string to pass to function.
    :param str expected_colors: Expected first item of return value.
    :param str expected_no_colors: Expected second item of return value.
    """
    actual_colors, actual_no_colors = parse_input(in_, disable, False)
    if disable:
        assert actual_colors == expected_no_colors
    else:
        assert actual_colors == expected_colors
    assert actual_no_colors == expected_no_colors


@pytest.mark.parametrize('disable', [True, False])
@pytest.mark.parametrize('in_,expected_colors,expected_no_colors', [
    ('', '', ''),
    ('test', 'test', 'test'),
    ('{b}TEST{/b}', '{b}TEST{/b}', '{b}TEST{/b}'),
    ('D {/all}{i}\033[31;103mE {/all}', 'D {/all}{i}\033[31;103mE {/all}', 'D {/all}{i}E {/all}'),
])
def test_parse_input_keep_tags(disable, in_, expected_colors, expected_no_colors):
    """Test function with keep_tags=True.

    :param bool disable: Disable colors?
    :param str in_: Input string to pass to function.
    :param str expected_colors: Expected first item of return value.
    :param str expected_no_colors: Expected second item of return value.
    """
    actual_colors, actual_no_colors = parse_input(in_, disable, True)
    if disable:
        assert actual_colors == expected_no_colors
    else:
        assert actual_colors == expected_colors
    assert actual_no_colors == expected_no_colors
