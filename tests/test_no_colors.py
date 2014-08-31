# coding=utf-8
import string
import sys

from colorclass import Color


class Default(dict):
    def __missing__(self, key):
        return key


def test_common():
    value = Color('this is a test.')

    assert '' == Color()
    assert 15 == len(value)
    assert 'this is a test.' == '{0}'.format(value)

    assert 'This is a test.' == value.capitalize()
    assert '  this is a test.   ' == value.center(20)
    assert 2 == value.count('is')
    assert value.endswith('test.')
    assert '    class' == Color('\tclass').expandtabs(4)
    assert 8 == value.find('a')
    assert 'test 123' == Color('test {0}').format('123')
    assert 8 == value.index('a')

    assert Color('a1').isalnum()
    assert not Color('a1.').isalnum()
    assert Color('a').isalpha()
    assert not Color('a1').isalpha()
    assert Color('1').isdecimal()
    assert not Color(u'⅕').isdecimal()
    assert Color(u'²').isdigit()
    assert not Color(u'⅕').isdigit()
    assert Color('a').islower()
    assert not Color('A').islower()
    assert Color(u'⅕').isnumeric()
    assert not Color('A').isnumeric()
    assert Color('    ').isspace()
    assert not Color('    x').isspace()
    assert Color('I Love To Test').istitle()
    assert not Color('I Love to Test').istitle()
    assert Color('A').isupper()
    assert not Color('a').isupper()

    assert 'test test' == Color(' ').join(('test', 'test'))
    assert 'this is a test.     ' == value.ljust(20)
    assert 'a' == Color('A').lower()
    assert 'a ' == Color(' a ').lstrip()
    assert ('this', ' ', 'is a test.') == value.partition(' ')
    assert 'this was a test.' == value.replace(' is ', ' was ')
    assert 13 == value.rfind('t')
    assert 13 == value.rindex('t')
    assert '     this is a test.' == value.rjust(20)
    assert ('this is a', ' ', 'test.') == value.rpartition(' ')
    assert ['this is a', 'test.'] == value.rsplit(' ', 1)
    assert ' a' == Color(' a ').rstrip()
    assert ['this', 'is', 'a', 'test.'] == value.split(' ')
    assert ['a', 'a'] == Color('a\na').splitlines()
    assert value.startswith('this')
    assert 'a' == Color(' a ').strip()
    assert 'Aa' == Color('aA').swapcase()
    assert 'This Is A Test.' == value.title()
    assert 'THIS IS A TEST.' == value.upper()
    assert '000001' == Color('1').zfill(6)


def test_py2():
    if sys.version_info[0] != 2:
        return
    value = Color('this is a test.')

    assert '' == Color('', 'latin-1')
    assert 'abc' == Color('\x80abc', errors='ignore')

    assert 'this is a test.' == value.decode()
    assert 'th3s 3s 1 t2st.' == value.translate(string.maketrans('aeiou', '12345').decode('latin-1'))


def test_py3():
    if sys.version_info[0] != 3:
        return
    value = Color('this is a test.')

    assert '' == Color(b'', 'latin-1')
    assert 'abc' == Color(b'\x80abc', errors='ignore')

    assert 'ss' == Color('ß').casefold()
    assert 'Guido was born in country' == Color('{name} was born in {country}').format_map(Default(name='Guido'))

    assert Color('var').isidentifier()
    assert not Color('var-').isidentifier()
    assert Color('var').isprintable()
    assert not Color('\0').isprintable()

    assert 'th3s 3s 1 t2st.' == value.translate(Color.maketrans('aeiou', '12345'))
