# coding=utf-8
import sys

from colorclass import Color


def test_unicode():
    value = Color('this is a test.')

    assert u'this is a test.' == '{0}'.format(value)
    assert u'This is a test.' == value.capitalize()
    assert u'  this is a test.   ' == value.center(20)
    assert 2 == value.count(u'is')


def test_unicode_py2():
    if sys.version_info[0] != 2:
        return

    value = Color('this is a test.')

    assert u'this is a test.' == value.decode()


def test_unicode_py3():
    if sys.version_info[0] != 3:
        return

    assert u'ss' == Color(u'ß').casefold()
