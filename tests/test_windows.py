"""Test Windows methods."""

from __future__ import print_function

import ctypes
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

from colorclass.color import Color
from colorclass.windows import (
    ConsoleScreenBufferInfo, get_console_info, init_kernel32, IS_WINDOWS, Windows, WINDOWS_CODES, WindowsStream
)

pytestmark = pytest.mark.skipif(not IS_WINDOWS, reason='Requires windows.')


class MockKernel32(object):
    """Mock kernel32."""

    def __init__(self):
        """Constructor."""
        self.wAttributes = 7

    def GetConsoleScreenBufferInfo(self, _, csbi_pointer):  # noqa
        """Mock GetConsoleScreenBufferInfo.

        :param _: Unused handle.
        :param csbi_pointer: ctypes.byref(csbi) return value.
        """
        struct_ptr = ctypes.POINTER(ConsoleScreenBufferInfo)
        csbi = ctypes.cast(csbi_pointer, struct_ptr).contents  # Dereference pointer.
        csbi.wAttributes = self.wAttributes
        return 1

    def SetConsoleTextAttribute(self, _, color_code):  # noqa
        """Mock SetConsoleTextAttribute.

        :param _: Unused handle.
        :param int color_code: Merged color code to set.
        """
        self.wAttributes = color_code
        return 1


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
    fg_color, bg_color = get_console_info(MockKernel32(), 0)
    assert fg_color == 7
    assert bg_color == 0


def test_windows_stream():
    """Test WindowsStream."""
    # Test error.
    stream = WindowsStream(init_kernel32()[0], 0, StringIO())
    assert stream.colors == (WINDOWS_CODES['white'], WINDOWS_CODES['black'])
    stream.colors = WINDOWS_CODES['red'] | WINDOWS_CODES['bgblue']  # No exception, just ignore.
    assert stream.colors == (WINDOWS_CODES['white'], WINDOWS_CODES['black'])

    # Test __getattr__() and color resetting.
    original_stream = StringIO()
    stream = WindowsStream(MockKernel32(), 0, original_stream)
    assert stream.writelines == original_stream.writelines  # Test __getattr__().
    assert stream.colors == (WINDOWS_CODES['white'], WINDOWS_CODES['black'])
    stream.colors = WINDOWS_CODES['red'] | WINDOWS_CODES['bgblue']
    assert stream.colors == (WINDOWS_CODES['red'], WINDOWS_CODES['bgblue'])
    stream.colors = None  # Resets colors to original.
    assert stream.colors == (WINDOWS_CODES['white'], WINDOWS_CODES['black'])

    # Test special negative codes.
    stream.colors = WINDOWS_CODES['red'] | WINDOWS_CODES['bgblue']
    stream.colors = WINDOWS_CODES['/fg']
    assert stream.colors == (WINDOWS_CODES['white'], WINDOWS_CODES['bgblue'])
    stream.colors = WINDOWS_CODES['red'] | WINDOWS_CODES['bgblue']
    stream.colors = WINDOWS_CODES['/bg']
    assert stream.colors == (WINDOWS_CODES['red'], WINDOWS_CODES['black'])
    stream.colors = WINDOWS_CODES['red'] | WINDOWS_CODES['bgblue']
    stream.colors = WINDOWS_CODES['bgblack']
    assert stream.colors == (WINDOWS_CODES['red'], WINDOWS_CODES['black'])

    # Test write.
    stream.write(Color('{/all}A{red}B{bgblue}C'))
    original_stream.seek(0)
    assert original_stream.read() == 'ABC'
    assert stream.colors == (WINDOWS_CODES['red'], WINDOWS_CODES['bgblue'])


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
