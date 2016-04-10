"""Test objects in module."""

import sys
from functools import partial

import pytest

from tests.conftest import assert_both_values, get_instance


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_dunder(kind):
    """Test "dunder" methods (double-underscore).

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, 'test ME ')
    assert len(instance) == 8


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_encode_decode(kind):
    """Test encode and decode methods.

    :param str kind: Type of string to test.
    """
    assert_both = partial(assert_both_values, kind=kind)
    instance = get_instance(kind, 'test ME')

    if sys.version_info[0] == 2:
        assert instance.encode('utf-8') == instance
        assert instance.decode('utf-8') == instance
        assert_both(instance.decode('utf-8'), 'test ME', '\033[31mtest ME\033[39m')
        assert_both(instance.__class__.decode(instance, 'utf-8'), 'test ME', '\033[31mtest ME\033[39m')
        assert len(instance.decode('utf-8')) == 7
    else:
        assert instance.encode('utf-8') != instance
    assert instance.encode('utf-8') == instance.encode('utf-8')
    assert instance.encode('utf-8').decode('utf-8') == instance
    assert_both(instance.encode('utf-8').decode('utf-8'), 'test ME', '\033[31mtest ME\033[39m')
    assert_both(instance.__class__.encode(instance, 'utf-8').decode('utf-8'), 'test ME', '\033[31mtest ME\033[39m')
    assert len(instance.encode('utf-8').decode('utf-8')) == 7


@pytest.mark.parametrize('mode', ['fg within bg', 'bg within fg'])
@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_format(kind, mode):
    """Test format method.

    :param str kind: Type of string to test.
    :param str mode: Which combination to test.
    """
    assert_both = partial(assert_both_values, kind=kind)

    # Test str.format(ColorStr()).
    instance = get_instance(kind, 'test me')
    assert_both(instance.__class__('1{0}2'.format(instance)), '1test me2', '1\033[31mtest me\033[39m2')
    assert_both(instance.__class__(str.format('1{0}2', instance)), '1test me2', '1\033[31mtest me\033[39m2')

    # Get actual.
    template_pos = get_instance(kind, 'a{0}c{0}', 'bgred' if mode == 'fg within bg' else 'red')
    template_kw = get_instance(kind, 'a{value}c{value}', 'bgred' if mode == 'fg within bg' else 'red')
    instance = get_instance(kind, 'B', 'green' if mode == 'fg within bg' else 'bggreen')

    # Get expected.
    expected = ['aBcB', None]
    if mode == 'fg within bg':
        expected[1] = '\033[41ma\033[32mB\033[39mc\033[32mB\033[39;49m'
    else:
        expected[1] = '\033[31ma\033[42mB\033[49mc\033[42mB\033[49;39m'

    # Test.
    assert_both(template_pos.format(instance), expected[0], expected[1])
    assert_both(template_kw.format(value=instance), expected[0], expected[1])
    assert_both(instance.__class__.format(template_pos, instance), expected[0], expected[1])
    assert_both(instance.__class__.format(template_kw, value=instance), expected[0], expected[1])


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_c_f(kind):
    """Test C through F methods.

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, 'test me')
    assert_both = partial(assert_both_values, kind=kind)

    assert_both(instance.capitalize(), 'Test me', '\033[31mTest me\033[39m')

    assert_both(instance.center(11), '  test me  ', '  \033[31mtest me\033[39m  ')
    assert_both(instance.center(11, '.'), '..test me..', '..\033[31mtest me\033[39m..')
    assert_both(instance.center(12), '  test me   ', '  \033[31mtest me\033[39m   ')

    assert instance.count('t') == 2

    assert instance.endswith('me') is True
    assert instance.endswith('ME') is False

    assert instance.find('t') == 0
    assert instance.find('t', 0) == 0
    assert instance.find('t', 0, 1) == 0
    assert instance.find('t', 1) == 3
    assert instance.find('t', 1, 4) == 3
    assert instance.find('t', 1, 3) == -1
    assert instance.find('x') == -1
    assert instance.find('m') == 5


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_i(kind):
    """Test I methods.

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, 'tantamount')
    assert instance.index('t') == 0
    assert instance.index('t', 0) == 0
    assert instance.index('t', 0, 1) == 0
    assert instance.index('t', 1) == 3
    assert instance.index('t', 1, 4) == 3
    assert instance.index('m') == 5
    with pytest.raises(ValueError):
        assert instance.index('t', 1, 3)
    with pytest.raises(ValueError):
        assert instance.index('x')

    assert instance.isalnum() is True
    assert get_instance(kind, '123').isalnum() is True
    assert get_instance(kind, '.').isalnum() is False

    assert instance.isalpha() is True
    assert get_instance(kind, '.').isalpha() is False

    if sys.version_info[0] != 2:
        assert instance.isdecimal() is False
        assert get_instance(kind, '123').isdecimal() is True
        assert get_instance(kind, '.').isdecimal() is False

    assert instance.isdigit() is False
    assert get_instance(kind, '123').isdigit() is True
    assert get_instance(kind, '.').isdigit() is False

    if sys.version_info[0] != 2:
        assert instance.isnumeric() is False
        assert get_instance(kind, '123').isnumeric() is True
        assert get_instance(kind, '.').isnumeric() is False

    assert instance.isspace() is False
    assert get_instance(kind, ' ').isspace() is True

    assert instance.istitle() is False
    assert get_instance(kind, 'Test').istitle() is True

    assert instance.isupper() is False
    assert get_instance(kind, 'TEST').isupper() is True


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_j_s(kind):
    """Test J to S methods.

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, 'test me')
    assert_both = partial(assert_both_values, kind=kind)

    assert_both(instance.join(['A', 'B']), 'Atest meB', 'A\033[31mtest me\033[39mB')
    iterable = [get_instance(kind, 'A', 'green'), get_instance(kind, 'B', 'green')]
    assert_both(instance.join(iterable), 'Atest meB', '\033[32mA\033[39;31mtest me\033[39;32mB\033[39m')

    assert_both(instance.ljust(11), 'test me    ', '\033[31mtest me\033[39m    ')
    assert_both(instance.ljust(11, '.'), 'test me....', '\033[31mtest me\033[39m....')
    assert_both(instance.ljust(12), 'test me     ', '\033[31mtest me\033[39m     ')

    assert instance.rfind('t') == 3
    assert instance.rfind('t', 0) == 3
    assert instance.rfind('t', 0, 4) == 3
    assert instance.rfind('t', 0, 3) == 0
    assert instance.rfind('t', 3, 3) == -1
    assert instance.rfind('x') == -1
    assert instance.rfind('m') == 5

    tantamount = get_instance(kind, 'tantamount')
    assert tantamount.rindex('t') == 9
    assert tantamount.rindex('t', 0) == 9
    assert tantamount.rindex('t', 0, 5) == 3
    assert tantamount.rindex('m') == 5
    with pytest.raises(ValueError):
        assert tantamount.rindex('t', 1, 3)
    with pytest.raises(ValueError):
        assert tantamount.rindex('x')

    assert_both(instance.rjust(11), '    test me', '    \033[31mtest me\033[39m')
    assert_both(instance.rjust(11, '.'), '....test me', '....\033[31mtest me\033[39m')
    assert_both(instance.rjust(12), '     test me', '     \033[31mtest me\033[39m')

    actual = get_instance(kind, '1\n2\n3').splitlines()
    assert len(actual) == 3
    # assert_both(actual[0], '1', '\033[31m1\033[39m')
    # assert_both(actual[1], '2', '\033[31m2\033[39m')
    # assert_both(actual[2], '3', '\033[31m3\033[39m')

    assert instance.startswith('t') is True
    assert instance.startswith('T') is False

    assert_both(get_instance(kind, 'AbC').swapcase(), 'aBc', '\033[31maBc\033[39m')


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_t_z(kind):
    """Test T to Z methods.

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, u'test me')
    assert_both = partial(assert_both_values, kind=kind)

    assert_both(instance.title(), 'Test Me', '\033[31mTest Me\033[39m')
    assert_both(get_instance(kind, 'TEST YOU').title(), 'Test You', '\033[31mTest You\033[39m')

    table = {ord('t'): u'1', ord('e'): u'2', ord('s'): u'3'}
    assert_both(instance.translate(table), '1231 m2', '\033[31m1231 m2\033[39m')

    assert_both(instance.upper(), 'TEST ME', '\033[31mTEST ME\033[39m')

    number = get_instance(kind, '350')
    assert_both(number.zfill(1), '350', '\033[31m350\033[39m')
    assert_both(number.zfill(2), '350', '\033[31m350\033[39m')
    assert_both(number.zfill(3), '350', '\033[31m350\033[39m')
    assert_both(number.zfill(4), '0350', '\033[31m0350\033[39m')
    assert_both(number.zfill(10), '0000000350', '\033[31m0000000350\033[39m')


@pytest.mark.parametrize('kind', ['str', 'ColorStr plain', 'ColorStr color'])
def test_empty(kind):
    """Test with empty string.

    :param str kind: Type of string to test.
    """
    instance = get_instance(kind, u'')
    assert_both = partial(assert_both_values, kind=kind)

    assert len(instance) == 0

    assert instance.encode('utf-8') == instance.encode('utf-8')
    assert instance.encode('utf-8').decode('utf-8') == instance
    assert_both(instance.encode('utf-8').decode('utf-8'), '', '\033[31;39m')
    assert_both(instance.__class__.encode(instance, 'utf-8').decode('utf-8'), '', '\033[31;39m')
    assert len(instance.encode('utf-8').decode('utf-8')) == 0
    assert_both(instance.format(value=''), '', '\033[31;39m')

    assert_both(instance.capitalize(), '', '\033[31;39m')
    # assert_both(instance.center(5), '     ', '\033[39m     ')
    assert instance.count('') == 1
    assert instance.count('t') == 0
    assert instance.endswith('') is True
    assert instance.endswith('me') is False
    assert instance.find('') == 0
    assert instance.find('t') == -1

    assert instance.index('') == 0
    with pytest.raises(ValueError):
        assert instance.index('t')
    assert instance.isalnum() is False
    assert instance.isalpha() is False
    if sys.version_info[0] != 2:
        assert instance.isdecimal() is False
    assert instance.isdigit() is False
    if sys.version_info[0] != 2:
        assert instance.isnumeric() is False
    assert instance.isspace() is False
    assert instance.istitle() is False
    assert instance.isupper() is False

    assert_both(instance.join(['A', 'B']), 'AB', 'A\033[31;39mB')
    # assert_both(instance.ljust(5), '     ', '\033[39m     ')
    assert instance.rfind('') == 0
    assert instance.rfind('t') == -1
    assert instance.rindex('') == 0
    with pytest.raises(ValueError):
        assert instance.rindex('t')
    # assert_both(instance.rjust(5), '     ', '\033[39m     ')
    if kind in ('str', 'ColorStr plain'):
        assert instance.splitlines() == list()
    else:
        assert instance.splitlines() == ['\033[31;39m']
    assert instance.startswith('') is True
    assert instance.startswith('T') is False
    assert_both(instance.swapcase(), '', '\033[31;39m')

    assert_both(instance.title(), '', '\033[31;39m')
    assert_both(instance.translate({ord('t'): u'1', ord('e'): u'2', ord('s'): u'3'}), '', '\033[31;39m')
    assert_both(instance.upper(), '', '\033[31;39m')
    assert_both(instance.zfill(0), '', '')
    assert_both(instance.zfill(1), '0', '0')
