"""Test Windows methods."""

from __future__ import print_function

import ctypes
import sys
from textwrap import dedent

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

from colorclass import windows
from colorclass.codes import ANSICodeMapping
from colorclass.color import Color
from tests.conftest import PROJECT_ROOT
from tests.screenshot import RunNewConsole, screenshot_until_match


class MockKernel32(object):
    """Mock kernel32."""

    def __init__(self, stderr=windows.INVALID_HANDLE_VALUE, stdout=windows.INVALID_HANDLE_VALUE, set_mode=0x0):
        """Constructor."""
        self.set_mode = set_mode
        self.stderr = stderr
        self.stdout = stdout
        self.wAttributes = 7

    def GetConsoleMode(self, _, dword_pointer):  # noqa
        """Mock GetConsoleMode.

        :param _: Unused handle.
        :param dword_pointer: ctypes.byref(lpdword) return value.
        """
        ulong_ptr = ctypes.POINTER(ctypes.c_ulong)
        dword = ctypes.cast(dword_pointer, ulong_ptr).contents  # Dereference pointer.
        dword.value = self.set_mode
        return 1

    def GetConsoleScreenBufferInfo(self, _, csbi_pointer):  # noqa
        """Mock GetConsoleScreenBufferInfo.

        :param _: Unused handle.
        :param csbi_pointer: ctypes.byref(csbi) return value.
        """
        struct_ptr = ctypes.POINTER(windows.ConsoleScreenBufferInfo)
        csbi = ctypes.cast(csbi_pointer, struct_ptr).contents  # Dereference pointer.
        csbi.wAttributes = self.wAttributes
        return 1

    def GetStdHandle(self, handle):  # noqa
        """Mock GetStdHandle.

        :param int handle: STD_ERROR_HANDLE or STD_OUTPUT_HANDLE.
        """
        return self.stderr if handle == windows.STD_ERROR_HANDLE else self.stdout

    def SetConsoleTextAttribute(self, _, color_code):  # noqa
        """Mock SetConsoleTextAttribute.

        :param _: Unused handle.
        :param int color_code: Merged color code to set.
        """
        self.wAttributes = color_code
        return 1


class MockSys(object):
    """Mock sys standard library module."""

    def __init__(self, stderr=None, stdout=None):
        """Constructor."""
        self.stderr = stderr or type('', (), {})
        self.stdout = stdout or type('', (), {})


@pytest.mark.skipif(str(not windows.IS_WINDOWS))
def test_init_kernel32_unique():
    """Make sure function doesn't override other LibraryLoaders."""
    k32_a = ctypes.LibraryLoader(ctypes.WinDLL).kernel32
    k32_a.GetStdHandle.argtypes = [ctypes.c_void_p]
    k32_a.GetStdHandle.restype = ctypes.c_ulong

    k32_b, stderr_b, stdout_b = windows.init_kernel32()

    k32_c = ctypes.LibraryLoader(ctypes.WinDLL).kernel32
    k32_c.GetStdHandle.argtypes = [ctypes.c_long]
    k32_c.GetStdHandle.restype = ctypes.c_short

    k32_d, stderr_d, stdout_d = windows.init_kernel32()

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


@pytest.mark.parametrize('stderr_invalid', [False, True])
@pytest.mark.parametrize('stdout_invalid', [False, True])
def test_init_kernel32_valid_handle(monkeypatch, stderr_invalid, stdout_invalid):
    """Test valid/invalid handle handling.

    :param monkeypatch: pytest fixture.
    :param bool stderr_invalid: Mock stderr is valid.
    :param bool stdout_invalid: Mock stdout is valid.
    """
    mock_sys = MockSys()
    monkeypatch.setattr(windows, 'sys', mock_sys)
    if stderr_invalid:
        setattr(mock_sys.stderr, '_original_stream', True)
    if stdout_invalid:
        setattr(mock_sys.stdout, '_original_stream', True)

    stderr, stdout = windows.init_kernel32(MockKernel32(stderr=100, stdout=200))[1:]

    if stderr_invalid and stdout_invalid:
        assert stderr == windows.INVALID_HANDLE_VALUE
        assert stdout == windows.INVALID_HANDLE_VALUE
    elif stdout_invalid:
        assert stderr == 100
        assert stdout == windows.INVALID_HANDLE_VALUE
    elif stderr_invalid:
        assert stderr == windows.INVALID_HANDLE_VALUE
        assert stdout == 200
    else:
        assert stderr == 100
        assert stdout == 200


def test_get_console_info():
    """Test function."""
    # Test error.
    if windows.IS_WINDOWS:
        with pytest.raises(OSError):
            windows.get_console_info(windows.init_kernel32()[0], windows.INVALID_HANDLE_VALUE)

    # Test no error with mock methods.
    kernel32 = MockKernel32()
    fg_color, bg_color, native_ansi = windows.get_console_info(kernel32, windows.INVALID_HANDLE_VALUE)
    assert fg_color == 7
    assert bg_color == 0
    assert native_ansi is False

    # Test different console modes.
    for not_native in (0x0, 0x1, 0x2, 0x1 | 0x2):
        kernel32.set_mode = not_native
        assert not windows.get_console_info(kernel32, windows.INVALID_HANDLE_VALUE)[-1]
    for native in (i | 0x4 for i in (0x0, 0x1, 0x2, 0x1 | 0x2)):
        kernel32.set_mode = native
        assert windows.get_console_info(kernel32, windows.INVALID_HANDLE_VALUE)[-1]


@pytest.mark.parametrize('stderr', [1, windows.INVALID_HANDLE_VALUE])
@pytest.mark.parametrize('stdout', [2, windows.INVALID_HANDLE_VALUE])
def test_bg_color_native_ansi(stderr, stdout):
    """Test function.

    :param int stderr: Value of parameter.
    :param int stdout: Value of parameter.
    """
    kernel32 = MockKernel32(set_mode=0x4)
    kernel32.wAttributes = 240
    actual = windows.bg_color_native_ansi(kernel32, stderr, stdout)
    if stderr == windows.INVALID_HANDLE_VALUE and stdout == windows.INVALID_HANDLE_VALUE:
        expected = 0, False
    else:
        expected = 240, True
    assert actual == expected


def test_windows_stream():
    """Test class."""
    # Test error.
    if windows.IS_WINDOWS:
        stream = windows.WindowsStream(windows.init_kernel32()[0], windows.INVALID_HANDLE_VALUE, StringIO())
        assert stream.colors == (windows.WINDOWS_CODES['white'], windows.WINDOWS_CODES['black'])
        stream.colors = windows.WINDOWS_CODES['red'] | windows.WINDOWS_CODES['bgblue']  # No exception, just ignore.
        assert stream.colors == (windows.WINDOWS_CODES['white'], windows.WINDOWS_CODES['black'])

    # Test __getattr__() and color resetting.
    original_stream = StringIO()
    stream = windows.WindowsStream(MockKernel32(), windows.INVALID_HANDLE_VALUE, original_stream)
    assert stream.writelines == original_stream.writelines  # Test __getattr__().
    assert stream.colors == (windows.WINDOWS_CODES['white'], windows.WINDOWS_CODES['black'])
    stream.colors = windows.WINDOWS_CODES['red'] | windows.WINDOWS_CODES['bgblue']
    assert stream.colors == (windows.WINDOWS_CODES['red'], windows.WINDOWS_CODES['bgblue'])
    stream.colors = None  # Resets colors to original.
    assert stream.colors == (windows.WINDOWS_CODES['white'], windows.WINDOWS_CODES['black'])

    # Test special negative codes.
    stream.colors = windows.WINDOWS_CODES['red'] | windows.WINDOWS_CODES['bgblue']
    stream.colors = windows.WINDOWS_CODES['/fg']
    assert stream.colors == (windows.WINDOWS_CODES['white'], windows.WINDOWS_CODES['bgblue'])
    stream.colors = windows.WINDOWS_CODES['red'] | windows.WINDOWS_CODES['bgblue']
    stream.colors = windows.WINDOWS_CODES['/bg']
    assert stream.colors == (windows.WINDOWS_CODES['red'], windows.WINDOWS_CODES['black'])
    stream.colors = windows.WINDOWS_CODES['red'] | windows.WINDOWS_CODES['bgblue']
    stream.colors = windows.WINDOWS_CODES['bgblack']
    assert stream.colors == (windows.WINDOWS_CODES['red'], windows.WINDOWS_CODES['black'])

    # Test write.
    stream.write(Color('{/all}A{red}B{bgblue}C'))
    original_stream.seek(0)
    assert original_stream.read() == 'ABC'
    assert stream.colors == (windows.WINDOWS_CODES['red'], windows.WINDOWS_CODES['bgblue'])

    # Test ignore invalid code.
    original_stream.seek(0)
    original_stream.truncate()
    stream.write('\x1b[0mA\x1b[31mB\x1b[44;999mC')
    original_stream.seek(0)
    assert original_stream.read() == 'ABC'
    assert stream.colors == (windows.WINDOWS_CODES['red'], windows.WINDOWS_CODES['bgblue'])


@pytest.mark.skipif(str(windows.IS_WINDOWS))
def test_windows_nix():
    """Test enable/disable on non-Windows platforms."""
    with windows.Windows():
        assert not windows.Windows.is_enabled()
        assert not hasattr(sys.stderr, '_original_stream')
        assert not hasattr(sys.stdout, '_original_stream')
    assert not windows.Windows.is_enabled()
    assert not hasattr(sys.stderr, '_original_stream')
    assert not hasattr(sys.stdout, '_original_stream')


def test_windows_auto_colors(monkeypatch):
    """Test Windows class with/out valid_handle and with/out auto_colors. Don't replace streams.

    :param monkeypatch: pytest fixture.
    """
    mock_sys = MockSys()
    monkeypatch.setattr(windows, 'atexit', type('', (), {'register': staticmethod(lambda _: 0 / 0)}))
    monkeypatch.setattr(windows, 'IS_WINDOWS', True)
    monkeypatch.setattr(windows, 'sys', mock_sys)
    monkeypatch.setattr(ANSICodeMapping, 'LIGHT_BACKGROUND', None)

    # Test no valid handles.
    kernel32 = MockKernel32()
    monkeypatch.setattr(windows, 'init_kernel32', lambda: (kernel32, -1, -1))
    assert not windows.Windows.enable()
    assert not windows.Windows.is_enabled()
    assert not hasattr(mock_sys.stderr, '_original_stream')
    assert not hasattr(mock_sys.stdout, '_original_stream')
    assert ANSICodeMapping.LIGHT_BACKGROUND is None

    # Test auto colors dark background.
    kernel32.set_mode = 0x4  # Enable native ANSI to have Windows skip replacing streams.
    monkeypatch.setattr(windows, 'init_kernel32', lambda: (kernel32, 1, 2))
    assert not windows.Windows.enable(auto_colors=True)
    assert not windows.Windows.is_enabled()
    assert not hasattr(mock_sys.stderr, '_original_stream')
    assert not hasattr(mock_sys.stdout, '_original_stream')
    assert ANSICodeMapping.LIGHT_BACKGROUND is False

    # Test auto colors light background.
    kernel32.wAttributes = 240
    assert not windows.Windows.enable(auto_colors=True)
    assert not windows.Windows.is_enabled()
    assert not hasattr(mock_sys.stderr, '_original_stream')
    assert not hasattr(mock_sys.stdout, '_original_stream')
    assert ANSICodeMapping.LIGHT_BACKGROUND is True


@pytest.mark.parametrize('valid', ['stderr', 'stdout', 'both'])
def test_windows_replace_streams(monkeypatch, tmpdir, valid):
    """Test Windows class stdout and stderr replacement.

    :param monkeypatch: pytest fixture.
    :param tmpdir: pytest fixture.
    :param str valid: Which mock stream(s) should be valid.
    """
    ac = list()  # atexit called.
    mock_sys = MockSys(stderr=tmpdir.join('stderr').open(mode='wb'), stdout=tmpdir.join('stdout').open(mode='wb'))
    monkeypatch.setattr(windows, 'atexit', type('', (), {'register': staticmethod(lambda _: ac.append(1))}))
    monkeypatch.setattr(windows, 'IS_WINDOWS', True)
    monkeypatch.setattr(windows, 'sys', mock_sys)

    # Mock init_kernel32.
    stderr = 1 if valid in ('stderr', 'both') else windows.INVALID_HANDLE_VALUE
    stdout = 2 if valid in ('stdout', 'both') else windows.INVALID_HANDLE_VALUE
    monkeypatch.setattr(windows, 'init_kernel32', lambda: (MockKernel32(), stderr, stdout))

    # Test.
    assert windows.Windows.enable(reset_atexit=True)
    assert windows.Windows.is_enabled()
    assert len(ac) == 1
    if stderr != windows.INVALID_HANDLE_VALUE:
        assert hasattr(mock_sys.stderr, '_original_stream')
    else:
        assert not hasattr(mock_sys.stderr, '_original_stream')
    if stdout != windows.INVALID_HANDLE_VALUE:
        assert hasattr(mock_sys.stdout, '_original_stream')
    else:
        assert not hasattr(mock_sys.stdout, '_original_stream')

    # Test multiple disable.
    assert windows.Windows.disable()
    assert not windows.Windows.is_enabled()
    assert not windows.Windows.disable()
    assert not windows.Windows.is_enabled()

    # Test context manager.
    with windows.Windows():
        assert windows.Windows.is_enabled()
    assert not windows.Windows.is_enabled()


@pytest.mark.skipif(str(not windows.IS_WINDOWS))
def test_enable_disable(tmpdir):
    """Test enabling, disabling, repeat. Make sure colors still work.

    :param tmpdir: pytest fixture.
    """
    screenshot = PROJECT_ROOT.join('test_windows_test_enable_disable.png')
    if screenshot.check():
        screenshot.remove()
    script = tmpdir.join('script.py')
    command = [sys.executable, str(script)]

    script.write(dedent("""\
    from __future__ import print_function
    import os, time
    from colorclass import Color, Windows

    with Windows(auto_colors=True):
        print(Color('{autored}Red{/autored}'))
    print('Red')
    with Windows(auto_colors=True):
        print(Color('{autored}Red{/autored}'))
    print('Red')

    stop_after = time.time() + 20
    while not os.path.exists(r'%s') and time.time() < stop_after:
        time.sleep(0.5)
    """) % str(screenshot))

    # Setup expected.
    with_colors = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_red_light_fg_*.bmp')]
    sans_colors = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_red_sans_*.bmp')]
    assert with_colors
    assert sans_colors

    # Run.
    with RunNewConsole(command) as gen:
        screenshot_until_match(str(screenshot), 15, with_colors, 2, gen)
        screenshot_until_match(str(screenshot), 15, sans_colors, 2, gen)


@pytest.mark.skipif(str(not windows.IS_WINDOWS))
def test_box_characters(tmpdir):
    """Test for unicode errors with special characters.

    :param tmpdir: pytest fixture.
    """
    screenshot = PROJECT_ROOT.join('test_windows_test_box_characters.png')
    if screenshot.check():
        screenshot.remove()
    script = tmpdir.join('script.py')
    command = [sys.executable, str(script)]

    script.write(dedent("""\
    from __future__ import print_function
    import os, time
    from colorclass import Color, Windows

    Windows.enable(auto_colors=True)
    chars = [
        '+', '-', '|',
        b'\\xb3'.decode('ibm437'),
        b'\\xb4'.decode('ibm437'),
        b'\\xb9'.decode('ibm437'),
        b'\\xba'.decode('ibm437'),
        b'\\xbb'.decode('ibm437'),
        b'\\xbc'.decode('ibm437'),
        b'\\xbf'.decode('ibm437'),
        b'\\xc0'.decode('ibm437'),
        b'\\xc1'.decode('ibm437'),
        b'\\xc2'.decode('ibm437'),
        b'\\xc3'.decode('ibm437'),
        b'\\xc4'.decode('ibm437'),
        b'\\xc5'.decode('ibm437'),
        b'\\xc8'.decode('ibm437'),
        b'\\xc9'.decode('ibm437'),
        b'\\xca'.decode('ibm437'),
        b'\\xcb'.decode('ibm437'),
        b'\\xcc'.decode('ibm437'),
        b'\\xcd'.decode('ibm437'),
        b'\\xce'.decode('ibm437'),
        b'\\xd9'.decode('ibm437'),
        b'\\xda'.decode('ibm437'),
    ]

    for c in chars:
        print(c, end='')
    print()
    for c in chars:
        print(Color.green(c, auto=True), end='')
    print()

    stop_after = time.time() + 20
    while not os.path.exists(r'%s') and time.time() < stop_after:
        time.sleep(0.5)
    """) % str(screenshot))

    # Setup expected.
    with_colors = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_box_green_*.bmp')]
    sans_colors = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_box_sans_*.bmp')]
    assert with_colors
    assert sans_colors

    # Run.
    with RunNewConsole(command) as gen:
        screenshot_until_match(str(screenshot), 15, with_colors, 1, gen)
        screenshot_until_match(str(screenshot), 15, sans_colors, 1, gen)
