# coding=utf-8

from colorclass import Color


def test_static_color_methods():
    assert Color('{autored}this is a test.{/autored}') == Color.red('this is a test.', auto=True)
    assert Color('{red}this is a test.{/red}') == Color.red('this is a test.')
    assert Color('{autobgred}this is a test.{/autobgred}') == Color.bgred('this is a test.', auto=True)
    assert Color('{bgred}this is a test.{/bgred}') == Color.bgred('this is a test.')
    assert Color('{autogreen}this is a test.{/autogreen}') == Color.green('this is a test.', auto=True)
    assert Color('{green}this is a test.{/green}') == Color.green('this is a test.')
    assert Color('{autobggreen}this is a test.{/autobggreen}') == Color.bggreen('this is a test.', auto=True)
    assert Color('{bggreen}this is a test.{/bggreen}') == Color.bggreen('this is a test.')
    assert Color('{autoblue}this is a test.{/autoblue}') == Color.blue('this is a test.', auto=True)
    assert Color('{blue}this is a test.{/blue}') == Color.blue('this is a test.')
    assert Color('{autobgblue}this is a test.{/autobgblue}') == Color.bgblue('this is a test.', auto=True)
    assert Color('{bgblue}this is a test.{/bgblue}') == Color.bgblue('this is a test.')
    assert Color('{autogreen}this is a test.{/autogreen}') == Color.green('this is a test.', auto=True)
    assert Color('{green}this is a test.{/green}') == Color.green('this is a test.')
    assert Color('{autobggreen}this is a test.{/autobggreen}') == Color.bggreen('this is a test.', auto=True)
    assert Color('{bggreen}this is a test.{/bggreen}') == Color.bggreen('this is a test.')
    assert Color('{autoyellow}this is a test.{/autoyellow}') == Color.yellow('this is a test.', auto=True)
    assert Color('{yellow}this is a test.{/yellow}') == Color.yellow('this is a test.')
    assert Color('{autobgyellow}this is a test.{/autobgyellow}') == Color.bgyellow('this is a test.', auto=True)
    assert Color('{bgyellow}this is a test.{/bgyellow}') == Color.bgyellow('this is a test.')
    assert Color('{autocyan}this is a test.{/autocyan}') == Color.cyan('this is a test.', auto=True)
    assert Color('{cyan}this is a test.{/cyan}') == Color.cyan('this is a test.')
    assert Color('{autobgcyan}this is a test.{/autobgcyan}') == Color.bgcyan('this is a test.', auto=True)
    assert Color('{bgcyan}this is a test.{/bgcyan}') == Color.bgcyan('this is a test.')
    assert Color('{automagenta}this is a test.{/automagenta}') == Color.magenta('this is a test.', auto=True)
    assert Color('{magenta}this is a test.{/magenta}') == Color.magenta('this is a test.')
    assert Color('{autobgmagenta}this is a test.{/autobgmagenta}') == Color.bgmagenta('this is a test.', auto=True)
    assert Color('{bgmagenta}this is a test.{/bgmagenta}') == Color.bgmagenta('this is a test.')
