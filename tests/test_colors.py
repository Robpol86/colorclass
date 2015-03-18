# coding=utf-8
import string
import sys

from colorclass import Color


class Default(dict):
    def __missing__(self, key):
        return key


def test_chaining():
    value = Color('{red}test{/red}')
    value2 = Color('{red}{0}{/red}').format(value)
    assert '\033[31;31mtest\033[39;39m' == value2
    assert 4 == len(value2)

    value3 = Color('{red}{0}{/red}').format(value2)
    assert '\033[31;31;31mtest\033[39;39;39m' == value3
    assert 4 == len(value3)

    value4 = Color('{red}{0}{/red}').format(value3)
    assert '\033[31;31;31;31mtest\033[39;39;39;39m' == value4
    assert 4 == len(value4)


def test_format():
    assert '\033[31mtest\033[39m' == '{0}'.format(Color('{red}test{/red}'))
    assert '\033[31;31mtest\033[39;39m' == Color('{red}{0}{/red}').format(Color('{red}test{/red}'))
    assert '\033[31mtest\033[39m' == Color('{red}{0}{/red}').format('test')

    assert '\033[31mtest\033[39m' == '%s' % Color('{red}test{/red}')
    value = Color('{red}%s{/red}') % Color('{red}test{/red}')
    assert '\033[31m\033[31mtest\033[39m\033[39m' == value
    assert '\033[31;31mtest\033[39;39m' == Color(value)
    assert '\033[31mtest\033[39m' == Color('{red}%s{/red}') % 'test'


def test_encode_decode():
    def decode(i):
        return i.decode('utf-8') if sys.version_info[0] == 2 else i

    assert (decode('\033[31mä\033[39;32möüß\033[39m') ==
            Color(decode('{red}ä{/red}{green}öüß{/green}')).encode('utf-8').decode('utf-8'))
    assert 4 == len(Color(decode('{red}ä{/red}{green}öüß{/green}')).encode('utf-8').decode('utf-8'))

    assert (u'\033[31m\ua000abcd\u07b4\033[39m'.encode('utf-8').decode('utf-8') ==
            Color(u'{red}\ua000abcd\u07b4{/red}'.encode('utf-8').decode('utf-8')).encode('utf-8').decode('utf-8'))
    assert 6 == len(Color(u'{red}\ua000abcd\u07b4{/red}'.encode('utf-8').decode('utf-8')).encode('utf-8')
                    .decode('utf-8'))


def test_common():
    value = Color('{red}this is a test.{/red}')

    assert Color('{red}this is a test.{/red}') == value
    assert Color('\033[31mthis is a test.\033[39m') == value
    assert 15 == len(value)
    assert '\033[31mthis is a test.\033[39m' == '{0}'.format(value)

    assert '\033[31mThis is a test.\033[39m' == value.capitalize()
    assert '  \033[31mthis is a test.\033[39m   ' == value.center(20)
    assert '@@\033[31mthis is a test.\033[39m@@@' == value.center(20, '@')
    assert 2 == value.count('is')
    assert 2 == Color('{red}I love m&ms{/red}').count('m')
    assert value.endswith('test.')
    assert '    \033[31mclass\033[39m' == Color('\t{red}class{/red}').expandtabs(4)
    assert 8 == value.find('a')
    assert 7 == Color('{red}I love m&ms{/red}').find('m')
    assert '\033[31mtest 123\033[39m' == Color('{red}test {0}{/red}').format('123')
    assert 8 == value.index('a')
    assert 7 == Color('{red}I love m&ms{/red}').index('m')

    assert Color('{red}a1{/red}').isalnum()
    assert not Color('{red}a1.{/red}').isalnum()
    assert Color('{red}a{/red}').isalpha()
    assert not Color('{red}a1{/red}').isalpha()
    assert Color('{red}1').isdecimal()
    assert not Color(u'{red}⅕{/red}').isdecimal()
    assert Color(u'{red}²{/red}').isdigit()
    assert not Color(u'{red}⅕{/red}').isdigit()
    assert Color('{red}a{/red}').islower()
    assert not Color('{red}A{/red}').islower()
    assert Color(u'{red}⅕{/red}').isnumeric()
    assert not Color('{red}A{/red}').isnumeric()
    assert Color('{red}    {/red}').isspace()
    assert not Color('{red}    x{/red}').isspace()
    assert Color('{red}I Love To Test{/red}').istitle()
    assert not Color('{red}I Love to Test{/red}').istitle()
    assert Color('{red}A{/red}').isupper()
    assert not Color('{red}a{/red}').isupper()

    assert 'test\033[0mtest' == Color('{/all}').join(('test', 'test'))
    assert '\033[31mthis is a test.\033[39m     ' == value.ljust(20)
    assert '\033[31ma\033[39m' == Color('{red}A{/red}').lower()
    assert '\033[31ma\033[39m ' == Color(' {red}a{/red} ').lstrip()
    assert '\033[31m a \033[39m' == Color('{red} a {/red}').lstrip()
    assert ('\033[31mthis', ' ', 'is a test.\033[39m') == value.partition(' ')
    assert '\033[31mthis was a test.\033[39m' == value.replace(' is ', ' was ')
    assert 13 == value.rfind('t')
    assert 13 == value.rindex('t')
    assert '     \033[31mthis is a test.\033[39m' == value.rjust(20)
    assert ('\033[31mthis is a', ' ', 'test.\033[39m') == value.rpartition(' ')
    assert ['\033[31mthis is a', 'test.\033[39m'] == value.rsplit(' ', 1)
    assert ' \033[31ma\033[39m' == Color(' {red}a{/red} ').rstrip()
    assert '\033[31m a \033[39m' == Color('{red} a {/red}').rstrip()
    assert ['\033[31mthis', 'is', 'a', 'test.\033[39m'] == value.split(' ')

    values = Color('{red}a{/red}\n{green}a{/green}').splitlines()
    assert ['\033[31ma\033[39m', '\033[32ma\033[39m'] == values
    assert [1, 1] == [len(i) for i in values]

    assert value.startswith('this')
    assert '\033[31ma\033[39m' == Color(' {red}a{/red} ').strip()
    assert '\033[31m a \033[39m' == Color('{red} a {/red}').strip()
    assert '\033[31mAa\033[39m' == Color('{red}aA{/red}').swapcase()
    assert '\033[31mThis Is A Test.\033[39m' == value.title()
    assert '\033[31mTHIS IS A TEST.\033[39m' == value.upper()
    assert '\033[31m000001\033[39m' == Color('{red}1{/red}').zfill(6)
    assert '00001\033[31m1\033[39m' == Color('1{red}1{/red}').zfill(6)


def test_py2():
    if sys.version_info[0] != 2:
        return
    value = Color('{red}this is a test.{/red}')

    assert '\033[31m \033[39m' == Color('{red} {/red}', 'latin-1')
    assert '\033[31mabc\033[39m' == Color('{red}\x80abc{/red}', errors='ignore')

    assert '\033[31mthis is a test.\033[39m' == value.decode()
    assert '\033[31mth3s 3s 1 t2st.\033[39m' == value.translate(string.maketrans('aeioum', '123456').decode('latin-1'))


def test_py3():
    if sys.version_info[0] != 3:
        return
    value = Color('{red}this is a test.{/red}')

    if hasattr(Color, 'casefold'):
        assert '\033[31mss\033[39m' == Color('{red}ß{/red}').casefold()

    actual = Color('{red}{name} was born in {country}{/red}').format_map(Default(name='Guido'))
    assert '\033[31mGuido was born in country\033[39m' == actual

    assert not Color('{red}var{/red}').isidentifier()
    assert not Color('var-').isidentifier()
    assert not Color('{red}var{/red}').isprintable()
    assert not Color('{red}\0{/red}').isprintable()

    assert '\033[31mth3s 3s 1 t2st.\033[39m' == value.translate(Color.maketrans('aeiou', '12345'))
