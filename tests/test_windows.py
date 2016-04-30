"""Test Windows methods."""

from __future__ import print_function

import ctypes
import sys

import pytest

from colorclass.color import Color
from colorclass.windows import ConsoleScreenBufferInfo, get_console_info, init_kernel32, IS_WINDOWS, Windows

pytestmark = pytest.mark.skipif(not IS_WINDOWS, reason='Requires windows.')


def test_init_kernel32():
    """Test init_kernel32(). Make sure it doesn't override other LibraryLoaders."""
    k32_a = ctypes.LibraryLoader(ctypes.WinDLL).kernel32
    k32_a.GetStdHandle.argtypes = [ctypes.c_void_p]
    k32_a.GetStdHandle.restype = ctypes.c_ulong

    k32_b, stderr_b, stdout_b = init_kernel32()

    k32_c = ctypes.LibraryLoader(ctypes.WinDLL).kernel32
    k32_c.GetStdHandle.argtypes = [ctypes.c_long]
    k32_c.GetStdHandle.restype = ctypes.c_short

    k32_d, stderr_d, stdout_d = init_kernel32()

    # Verify external.
    assert k32_a.GetStdHandle.argtypes == [ctypes.c_void_p]
    assert k32_a.GetStdHandle.restype == ctypes.c_ulong
    assert k32_c.GetStdHandle.argtypes == [ctypes.c_long]
    assert k32_c.GetStdHandle.restype == ctypes.c_short

    # Verify ours.
    assert k32_b.GetStdHandle.argtypes == [ctypes.c_ulong]
    assert k32_b.GetStdHandle.restype == ctypes.c_void_p
    assert k32_d.GetStdHandle.argtypes == [ctypes.c_ulong]
    assert k32_d.GetStdHandle.restype == ctypes.c_void_p
    assert stderr_b == stderr_d
    assert stdout_b == stdout_d


def test_get_console_info():
    """Test get_console_info()."""
    # Test error.
    with pytest.raises(OSError):
        get_console_info(init_kernel32()[0], 0)

    # Test no error with mock GetConsoleScreenBufferInfo. Console unavailable when pytest running.
    def get_csbi(*args):
        """Mock GetConsoleScreenBufferInfo()."""
        csbi = ctypes.cast(args[1], ctypes.POINTER(ConsoleScreenBufferInfo)).contents  # Dereference pointer.
        csbi.wAttributes = 7
        return 1
    kernel32 = type('', (), dict(GetConsoleScreenBufferInfo=staticmethod(get_csbi)))()
    fg_color, bg_color = get_console_info(kernel32, 0)
    assert fg_color == 7
    assert bg_color == 0


def test_disable_safe():
    """Test for safety."""
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
    """Test enabling then disabling on Windows."""
    original_stderr_id, original_stdout_id = id(sys.stderr), id(sys.stdout)

    assert not Windows.is_enabled()
    assert Windows.enable()
    assert original_stderr_id != id(sys.stderr)
    assert original_stdout_id != id(sys.stdout)

    assert Windows.disable()
    assert original_stderr_id == id(sys.stderr)
    # assert original_stdout_id == id(sys.stdout)  # pytest does some weird shit.


def test():
    """Basic test."""
    with Windows(auto_colors=True):
        print(Color('{autored}Test{/autored}.'))
        sys.stdout.flush()

    Windows.enable(reset_atexit=True)
    print(Color('{autored}{autobgyellow}Test{bgblack}2{/bg}.{/all}'))
