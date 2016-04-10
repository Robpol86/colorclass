"""Test objects in module."""

import pytest

from colorclass.search import build_color_index, find_char_color


@pytest.mark.parametrize('in_,expected', [
    ['', ()],
    ['TEST', (0, 1, 2, 3)],
    ['!\033[31mRed\033[0m', (0, 6, 7, 8)],
    ['\033[1mA \033[31mB \033[32;41mC \033[0mD', (4, 5, 11, 12, 21, 22, 27)],
])
def test_build_color_index(in_, expected):
    """Test function.

    :param str in_: Input string to pass to function.
    :param str expected: Expected return value.
    """
    actual = build_color_index(in_)
    assert actual == expected


@pytest.mark.parametrize('in_,pos,expected', [
    ('TEST', 0, 'T'),

    ('\033[31mTEST', 0, '\033[31mT'),
    ('\033[31mTEST', 3, '\033[31mT'),

    ('\033[31mT\033[32mE\033[33mS\033[34mT', 0, '\033[31mT\033[32m\033[33m\033[34m'),
    ('\033[31mT\033[32mE\033[33mS\033[34mT', 2, '\033[31m\033[32m\033[33mS\033[34m'),

    ('\033[31mTEST\033[0m', 1, '\033[31mE\033[0m'),
    ('\033[31mTEST\033[0m', 3, '\033[31mT\033[0m'),

    ('T\033[31mES\033[0mT', 0, 'T\033[31m\033[0m'),
    ('T\033[31mES\033[0mT', 1, '\033[31mE\033[0m'),
    ('T\033[31mES\033[0mT', 2, '\033[31mS\033[0m'),
    ('T\033[31mES\033[0mT', 3, '\033[31m\033[0mT'),
])
def test_find_char_color(in_, pos, expected):
    """Test function.

    :param str in_: Input string to pass to function.
    :param int pos: Character position in non-color string to lookup.
    :param str expected: Expected return value.
    """
    index = build_color_index(in_)
    color_pos = index[pos]
    actual = find_char_color(in_, color_pos)
    assert actual == expected
