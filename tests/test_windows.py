from __future__ import print_function
import os
import sys

import pytest

from colorclass import Color, Windows

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='Requires windows.')


def test_disable_safe():
    original_stderr_id, original_stdout_id = id(sys.stderr), id(sys.stdout)

    assert not Windows.is_enabled()
    assert not Windows.disable()

    assert not Windows.is_enabled()
    assert not Windows.disable()

    assert not Windows.is_enabled()
    assert not Windows.disable()

    assert original_stderr_id == id(sys.stderr)
    assert original_stdout_id == id(sys.stdout)


def test_enable_then_disable():
    original_stderr_id, original_stdout_id = id(sys.stderr), id(sys.stdout)

    assert not Windows.is_enabled()
    assert Windows.enable()
    assert original_stderr_id != id(sys.stderr)
    assert original_stdout_id != id(sys.stdout)

    assert Windows.disable()
    assert original_stderr_id == id(sys.stderr)
    #assert original_stdout_id == id(sys.stdout)  # pytest does some weird shit.


def test():
    with Windows(auto_colors=True):
        print(Color('{autored}Test{/autored}.'))
        sys.stdout.flush()

    Windows.enable(reset_atexit=True)
    print(Color('{autored}{autobgyellow}Test{bgblack}2{/bg}.{/all}'))
