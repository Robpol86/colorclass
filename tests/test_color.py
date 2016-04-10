"""Test objects in module."""

from functools import partial

import pytest

from colorclass.color import Color
from tests.conftest import assert_both_values, get_instance


def test_colorize_methods():
    """Test colorize convenience methods."""
    assert Color.black('TEST').value_colors == '\033[30mTEST\033[39m'
    assert Color.bgblack('TEST').value_colors == '\033[40mTEST\033[49m'
    assert Color.red('TEST').value_colors == '\033[31mTEST\033[39m'
    assert Color.bgred('TEST').value_colors == '\033[41mTEST\033[49m'
    assert Color.green('TEST').value_colors == '\033[32mTEST\033[39m'
    assert Color.bggreen('TEST').value_colors == '\033[42mTEST\033[49m'
    assert Color.yellow('TEST').value_colors == '\033[33mTEST\033[39m'
    assert Color.bgyellow('TEST').value_colors == '\033[43mTEST\033[49m'
    assert Color.blue('TEST').value_colors == '\033[34mTEST\033[39m'
    assert Color.bgblue('TEST').value_colors == '\033[44mTEST\033[49m'
    assert Color.magenta('TEST').value_colors == '\033[35mTEST\033[39m'
    assert Color.bgmagenta('TEST').value_colors == '\033[45mTEST\033[49m'
    assert Color.cyan('TEST').value_colors == '\033[36mTEST\033[39m'
    assert Color.bgcyan('TEST').value_colors == '\033[46mTEST\033[49m'
    assert Color.white('TEST').value_colors == '\033[37mTEST\033[39m'
    assert Color.bgwhite('TEST').value_colors == '\033[47mTEST\033[49m'

    assert Color.black('this is a test.', auto=True) == Color('{autoblack}this is a test.{/autoblack}')
    assert Color.black('this is a test.') == Color('{black}this is a test.{/black}')
    assert Color.bgblack('this is a test.', auto=True) == Color('{autobgblack}this is a test.{/autobgblack}')
    assert Color.bgblack('this is a test.') == Color('{bgblack}this is a test.{/bgblack}')
    assert Color.red('this is a test.', auto=True) == Color('{autored}this is a test.{/autored}')
    assert Color.red('this is a test.') == Color('{red}this is a test.{/red}')
    assert Color.bgred('this is a test.', auto=True) == Color('{autobgred}this is a test.{/autobgred}')
    assert Color.bgred('this is a test.') == Color('{bgred}this is a test.{/bgred}')
    assert Color.green('this is a test.', auto=True) == Color('{autogreen}this is a test.{/autogreen}')
    assert Color.green('this is a test.') == Color('{green}this is a test.{/green}')
    assert Color.bggreen('this is a test.', auto=True) == Color('{autobggreen}this is a test.{/autobggreen}')
    assert Color.bggreen('this is a test.') == Color('{bggreen}this is a test.{/bggreen}')
    assert Color.yellow('this is a test.', auto=True) == Color('{autoyellow}this is a test.{/autoyellow}')
    assert Color.yellow('this is a test.') == Color('{yellow}this is a test.{/yellow}')
    assert Color.bgyellow('this is a test.', auto=True) == Color('{autobgyellow}this is a test.{/autobgyellow}')
    assert Color.bgyellow('this is a test.') == Color('{bgyellow}this is a test.{/bgyellow}')
    assert Color.blue('this is a test.', auto=True) == Color('{autoblue}this is a test.{/autoblue}')
    assert Color.blue('this is a test.') == Color('{blue}this is a test.{/blue}')
    assert Color.bgblue('this is a test.', auto=True) == Color('{autobgblue}this is a test.{/autobgblue}')
    assert Color.bgblue('this is a test.') == Color('{bgblue}this is a test.{/bgblue}')
    assert Color.magenta('this is a test.', auto=True) == Color('{automagenta}this is a test.{/automagenta}')
    assert Color.magenta('this is a test.') == Color('{magenta}this is a test.{/magenta}')
    assert Color.bgmagenta('this is a test.', auto=True) == Color('{autobgmagenta}this is a test.{/autobgmagenta}')
    assert Color.bgmagenta('this is a test.') == Color('{bgmagenta}this is a test.{/bgmagenta}')
    assert Color.cyan('this is a test.', auto=True) == Color('{autocyan}this is a test.{/autocyan}')
    assert Color.cyan('this is a test.') == Color('{cyan}this is a test.{/cyan}')
    assert Color.bgcyan('this is a test.', auto=True) == Color('{autobgcyan}this is a test.{/autobgcyan}')
    assert Color.bgcyan('this is a test.') == Color('{bgcyan}this is a test.{/bgcyan}')
    assert Color.white('this is a test.', auto=True) == Color('{autowhite}this is a test.{/autowhite}')
    assert Color.white('this is a test.') == Color('{white}this is a test.{/white}')
    assert Color.bgwhite('this is a test.', auto=True) == Color('{autobgwhite}this is a test.{/autobgwhite}')
    assert Color.bgwhite('this is a test.') == Color('{bgwhite}this is a test.{/bgwhite}')


@pytest.mark.parametrize('kind', ['str', 'Color plain', 'Color color'])
def test_chaining(kind):
    """Test chaining Color instances.

    :param str kind: Type of string to test.
    """
    assert_both = partial(assert_both_values, kind=kind)

    # Test string.
    instance = get_instance(kind, 'TEST')
    for color in ('green', 'blue', 'yellow'):
        instance = get_instance(kind, instance, color)
    assert_both(instance, 'TEST', '\033[33;34;32;31mTEST\033[39;39;39;39m')

    # Test empty.
    instance = get_instance(kind)
    for color in ('red', 'green', 'blue', 'yellow'):
        instance = get_instance(kind, instance, color)
    assert_both(instance, '', '\033[33;34;32;31;39;39;39;39m')

    # Test complicated.
    instance = 'TEST'
    for color in ('black', 'bgred', 'green', 'bgyellow', 'blue', 'bgmagenta', 'cyan', 'bgwhite'):
        instance = get_instance(kind, instance, color=color)
    assert_both(instance, 'TEST', '\033[47;36;45;34;43;32;41;30mTEST\033[39;49;39;49;39;49;39;49m')

    # Test format and length.
    instance = get_instance(kind, '{0}').format(get_instance(kind, 'TEST'))
    assert_both(instance, 'TEST', '\033[31;31mTEST\033[39;39m')
    assert len(instance) == 4
    instance = get_instance(kind, '{0}').format(instance)
    assert_both(instance, 'TEST', '\033[31;31;31mTEST\033[39;39;39m')
    assert len(instance) == 4
    instance = get_instance(kind, '{0}').format(instance)
    assert_both(instance, 'TEST', '\033[31;31;31;31mTEST\033[39;39;39;39m')
    assert len(instance) == 4
