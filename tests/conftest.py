"""Configure tests."""

import sys

import py
import pytest

from colorclass.codes import ANSICodeMapping
from colorclass.color import Color
from colorclass.core import ColorStr, PARENT_CLASS

IS_WINDOWS = sys.platform == 'win32'
PROJECT_ROOT = py.path.local(__file__).dirpath().join('..')


@pytest.fixture(autouse=True)
def set_defaults(monkeypatch):
    """Set ANSICodeMapping defaults before each test.

    :param monkeypatch: pytest fixture.
    """
    monkeypatch.setattr(ANSICodeMapping, 'DISABLE_COLORS', False)
    monkeypatch.setattr(ANSICodeMapping, 'LIGHT_BACKGROUND', False)


def assert_both_values(actual, expected_plain, expected_color, kind=None):
    """Handle asserts for color and non-color strings in color and non-color tests.

    :param ColorStr actual: Return value of ColorStr class method.
    :param expected_plain: Expected non-color value.
    :param expected_color: Expected color value.
    :param str kind: Type of string to test.
    """
    if kind.endswith('plain'):
        assert actual.value_colors == expected_plain
        assert actual.value_no_colors == expected_plain
        assert actual.has_colors is False
    elif kind.endswith('color'):
        assert actual.value_colors == expected_color
        assert actual.value_no_colors == expected_plain
        if '\033' in actual.value_colors:
            assert actual.has_colors is True
        else:
            assert actual.has_colors is False
    else:
        assert actual == expected_plain

    if kind.startswith('ColorStr'):
        assert actual.__class__ == ColorStr
    elif kind.startswith('Color'):
        assert actual.__class__ == Color


def get_instance(kind, sample=None, color='red'):
    """Get either a string, non-color ColorStr, or color ColorStr instance.

    :param str kind: Type of string to test.
    :param iter sample: Input test to derive instances from.
    :param str color: Color tags to use. Default is red.

    :return: Instance.
    """
    # First determine which class/type to use.
    if kind.startswith('ColorStr'):
        cls = ColorStr
    elif kind.startswith('Color'):
        cls = Color
    else:
        cls = PARENT_CLASS

    # Next handle NoneType samples.
    if sample is None:
        return cls()

    # Finally handle non-None samples.
    if kind.endswith('plain'):
        return cls(sample)
    elif kind.endswith('color'):
        tags = '{%s}' % color, '{/%s}' % color
        return cls(tags[0] + sample + tags[1])
    return sample
