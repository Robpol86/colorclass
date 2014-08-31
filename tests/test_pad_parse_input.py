from colorclass import _parse_input


def test_simple():
    assert ('test', 'test') == _parse_input('test')
    assert ('\033[1mtest\033[22m', 'test') == _parse_input('{b}test{/b}')


def test_advanced():
    assert ('\033[1m{0}\033[22m', '{0}') == _parse_input('{b}{0}{/b}')
    assert ('\033[1;31mTest\033[0m', 'Test') == _parse_input('{b}{red}Test{/all}')

    actual = _parse_input('{b}{bgblue}{red}{red}This {red}is {red}a test: {green}{0}{/green}{/red}{/bgblue}{/b}')
    expected = ('\033[1;31;44mThis \033[31mis \033[31ma test: \033[32m{0}\033[22;39;49m', 'This is a test: {0}')
    assert expected == actual
