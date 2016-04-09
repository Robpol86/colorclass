"""Windows console screen buffer handlers."""

import atexit
import ctypes
import os
import re
import sys

from colorclass.codes import ANSICodeMapping, BASE_CODES
from colorclass.core import RE_SPLIT

RE_NUMBER_SEARCH = re.compile(r'\033\[([\d;]+)m')
WINDOWS_CODES = {
    '/all': -33, '/fg': -39, '/bg': -49,

    'black': 0, 'red': 4, 'green': 2, 'yellow': 6, 'blue': 1, 'magenta': 5, 'cyan': 3, 'white': 7,

    'bgblack': -8, 'bgred': 64, 'bggreen': 32, 'bgyellow': 96, 'bgblue': 16, 'bgmagenta': 80, 'bgcyan': 48,
    'bgwhite': 112,

    'hiblack': 8, 'hired': 12, 'higreen': 10, 'hiyellow': 14, 'hiblue': 9, 'himagenta': 13, 'hicyan': 11, 'hiwhite': 15,

    'hibgblack': 128, 'hibgred': 192, 'hibggreen': 160, 'hibgyellow': 224, 'hibgblue': 144, 'hibgmagenta': 208,
    'hibgcyan': 176, 'hibgwhite': 240,

    '/black': -39, '/red': -39, '/green': -39, '/yellow': -39, '/blue': -39, '/magenta': -39, '/cyan': -39,
    '/white': -39, '/hiblack': -39, '/hired': -39, '/higreen': -39, '/hiyellow': -39, '/hiblue': -39, '/himagenta': -39,
    '/hicyan': -39, '/hiwhite': -39,

    '/bgblack': -49, '/bgred': -49, '/bggreen': -49, '/bgyellow': -49, '/bgblue': -49, '/bgmagenta': -49,
    '/bgcyan': -49, '/bgwhite': -49, '/hibgblack': -49, '/hibgred': -49, '/hibggreen': -49, '/hibgyellow': -49,
    '/hibgblue': -49, '/hibgmagenta': -49, '/hibgcyan': -49, '/hibgwhite': -49,
}


class WindowsCSBI(object):
    """Interface with Windows CONSOLE_SCREEN_BUFFER_INFO API/DLL calls. Gets info for stderr and stdout.

    References:
        http://msdn.microsoft.com/en-us/library/windows/desktop/ms683231
        https://code.google.com/p/colorama/issues/detail?id=47.
        pytest's py project: py/_io/terminalwriter.py.

    Class variables:
    CSBI -- ConsoleScreenBufferInfo class/struct (not instance, the class definition itself) defined in _define_csbi().
    HANDLE_STDERR -- GetStdHandle() return integer for stderr.
    HANDLE_STDOUT -- GetStdHandle() return integer for stdout.
    WINDLL -- my own loaded instance of ctypes.WinDLL.
    """

    CSBI = None
    HANDLE_STDERR = None
    HANDLE_STDOUT = None
    WINDLL = ctypes.LibraryLoader(getattr(ctypes, 'WinDLL', None))
    WINTYPES = __import__('ctypes.wintypes').wintypes if os.name == 'nt' else None

    @staticmethod
    def _define_csbi():
        """Define structs and populates WindowsCSBI.CSBI."""
        if WindowsCSBI.CSBI is not None:
            return

        class COORD(ctypes.Structure):
            """Windows COORD structure. http://msdn.microsoft.com/en-us/library/windows/desktop/ms682119."""

            _fields_ = [('X', ctypes.c_short), ('Y', ctypes.c_short)]

        class SmallRECT(ctypes.Structure):
            """Windows SMALL_RECT structure. http://msdn.microsoft.com/en-us/library/windows/desktop/ms686311."""

            _fields_ = [('Left', ctypes.c_short), ('Top', ctypes.c_short), ('Right', ctypes.c_short),
                        ('Bottom', ctypes.c_short)]

        class ConsoleScreenBufferInfo(ctypes.Structure):
            """Windows CONSOLE_SCREEN_BUFFER_INFO structure.

            http://msdn.microsoft.com/en-us/library/windows/desktop/ms682093
            """

            _fields_ = [
                ('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', WindowsCSBI.WINTYPES.WORD),
                ('srWindow', SmallRECT),
                ('dwMaximumWindowSize', COORD)
            ]

        WindowsCSBI.CSBI = ConsoleScreenBufferInfo

    @staticmethod
    def initialize():
        """Initialize the WINDLL resource and populated the CSBI class variable."""
        WindowsCSBI._define_csbi()
        WindowsCSBI.HANDLE_STDERR = WindowsCSBI.HANDLE_STDERR or WindowsCSBI.WINDLL.kernel32.GetStdHandle(-12)
        WindowsCSBI.HANDLE_STDOUT = WindowsCSBI.HANDLE_STDOUT or WindowsCSBI.WINDLL.kernel32.GetStdHandle(-11)
        if WindowsCSBI.WINDLL.kernel32.GetConsoleScreenBufferInfo.argtypes:
            return

        WindowsCSBI.WINDLL.kernel32.GetStdHandle.argtypes = [WindowsCSBI.WINTYPES.DWORD]
        WindowsCSBI.WINDLL.kernel32.GetStdHandle.restype = WindowsCSBI.WINTYPES.HANDLE
        WindowsCSBI.WINDLL.kernel32.GetConsoleScreenBufferInfo.restype = WindowsCSBI.WINTYPES.BOOL
        WindowsCSBI.WINDLL.kernel32.GetConsoleScreenBufferInfo.argtypes = [
            WindowsCSBI.WINTYPES.HANDLE, ctypes.POINTER(WindowsCSBI.CSBI)
        ]

    @staticmethod
    def get_info(handle):
        """Get information about this current console window (for Microsoft Windows only).

        Don't forget to call WindowsCSBI.initialize() once in your application before calling this method.

        Returns dictionary with different integer values. Keys are:
            buffer_width -- width of the buffer (Screen Buffer Size in cmd.exe layout tab).
            buffer_height -- height of the buffer (Screen Buffer Size in cmd.exe layout tab).
            terminal_width -- width of the terminal window.
            terminal_height -- height of the terminal window.
            bg_color -- current background color (http://msdn.microsoft.com/en-us/library/windows/desktop/ms682088).
            fg_color -- current text color code.

        :raise IOError: If attempt to get information fails (if there is no console window).

        :param handle: Either WindowsCSBI.HANDLE_STDERR or WindowsCSBI.HANDLE_STDOUT.

        :return: Terminal info.
        :rtype: dict
        """
        # Query Win32 API.
        csbi = WindowsCSBI.CSBI()
        try:
            if not WindowsCSBI.WINDLL.kernel32.GetConsoleScreenBufferInfo(handle, ctypes.byref(csbi)):
                raise IOError('Unable to get console screen buffer info from win32 API.')
        except ctypes.ArgumentError:
            raise IOError('Unable to get console screen buffer info from win32 API.')

        # Parse data.
        result = dict(
            buffer_width=int(csbi.dwSize.X - 1),
            buffer_height=int(csbi.dwSize.Y),
            terminal_width=int(csbi.srWindow.Right - csbi.srWindow.Left),
            terminal_height=int(csbi.srWindow.Bottom - csbi.srWindow.Top),
            bg_color=int(csbi.wAttributes & 240),
            fg_color=int(csbi.wAttributes % 16),
        )
        return result


class WindowsStreamStdOut(object):
    """Replacement stream which overrides sys.stdout. When writing or printing, ANSI codes are converted.

    ANSI (Linux/Unix) color codes are converted into win32 system calls, changing the next character's color before
    printing it. Resources referenced:
        https://github.com/tartley/colorama
        http://www.cplusplus.com/articles/2ywTURfi/
        http://thomasfischer.biz/python-and-windows-terminal-colors/
        http://stackoverflow.com/questions/17125440/c-win32-console-color
        http://www.tysos.org/svn/trunk/mono/corlib/System/WindowsConsoleDriver.cs
        http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
        http://msdn.microsoft.com/en-us/library/windows/desktop/ms682088#_win32_character_attributes

    Class variables:
    ALL_BG_CODES -- list of background Windows codes. Used to determine if requested color is foreground or background.
    COMPILED_CODES -- 'translation' dictionary. Keys are ANSI codes (values of BASE_CODES), values are Windows codes.
    ORIGINAL_STREAM -- the original stream to write non-code text to.
    WIN32_STREAM_HANDLE -- handle to the Windows stdout device. Used by other Windows functions.

    Instance variables:
    default_fg -- the foreground Windows color code at the time of instantiation.
    default_bg -- the background Windows color code at the time of instantiation.
    """

    ALL_BG_CODES = [v for k, v in WINDOWS_CODES.items() if k.startswith('bg') or k.startswith('hibg')]
    COMPILED_CODES = dict((v, WINDOWS_CODES[k]) for k, v in BASE_CODES.items() if k in WINDOWS_CODES)
    ORIGINAL_STREAM = sys.stdout
    WIN32_STREAM_HANDLE = WindowsCSBI.HANDLE_STDOUT

    def __init__(self):
        """Constructor."""
        WindowsCSBI.initialize()
        self.default_fg, self.default_bg = self._get_colors()
        for attr in dir(self.ORIGINAL_STREAM):
            if hasattr(self, attr):
                continue
            setattr(self, attr, getattr(self.ORIGINAL_STREAM, attr))

    def __getattr__(self, item):
        """If an attribute/function/etc is not defined in this function, retrieve the one from the original stream.

        Fixes ipython arrow key presses.
        """
        return getattr(self.ORIGINAL_STREAM, item)

    def _get_colors(self):
        """Return a tuple of two integers representing current colors: (foreground, background)."""
        try:
            csbi = WindowsCSBI.get_info(self.WIN32_STREAM_HANDLE)
            return csbi['fg_color'], csbi['bg_color']
        except IOError:
            return 7, 0

    def _reset_colors(self):
        """Set the foreground and background colors to their original values (when class was instantiated)."""
        self._set_color(-33)

    def _set_color(self, color_code):
        """Change the foreground and background colors for subsequently printed characters.

        Since setting a color requires including both foreground and background codes (merged), setting just the
        foreground color resets the background color to black, and vice versa.

        This function first gets the current background and foreground colors, merges in the requested color code, and
        sets the result.

        However if we need to remove just the foreground color but leave the background color the same (or vice versa)
        such as when {/red} is used, we must merge the default foreground color with the current background color. This
        is the reason for those negative values.

        :param int color_code: Color code from WINDOWS_CODES.
        """
        # Get current color code.
        current_fg, current_bg = self._get_colors()

        # Handle special negative codes. Also determine the final color code.
        if color_code == -39:
            final_color_code = self.default_fg | current_bg  # Reset the foreground only.
        elif color_code == -49:
            final_color_code = current_fg | self.default_bg  # Reset the background only.
        elif color_code == -33:
            final_color_code = self.default_fg | self.default_bg  # Reset both.
        elif color_code == -8:
            final_color_code = current_fg  # Black background.
        else:
            new_is_bg = color_code in self.ALL_BG_CODES
            final_color_code = color_code | (current_fg if new_is_bg else current_bg)

        # Set new code.
        WindowsCSBI.WINDLL.kernel32.SetConsoleTextAttribute(self.WIN32_STREAM_HANDLE, final_color_code)

    def write(self, p_str):
        """Write to stream.

        :param str p_str: string to print.
        """
        for segment in RE_SPLIT.split(p_str):
            if not segment:
                # Empty string. p_str probably starts with colors so the first item is always ''.
                continue
            if not RE_SPLIT.match(segment):
                # No color codes, print regular text.
                self.ORIGINAL_STREAM.write(segment)
                self.ORIGINAL_STREAM.flush()
                continue
            for color_code in (int(c) for c in RE_NUMBER_SEARCH.findall(segment)[0].split(';')):
                if color_code in self.COMPILED_CODES:
                    self._set_color(self.COMPILED_CODES[color_code])


class WindowsStreamStdErr(WindowsStreamStdOut):
    """Replacement stream which overrides sys.stderr. Subclasses WindowsStreamStdOut."""

    ORIGINAL_STREAM = sys.stderr
    WIN32_STREAM_HANDLE = WindowsCSBI.HANDLE_STDERR


class Windows(object):
    """Enable and disable Windows support for ANSI color character codes.

    Call static method Windows.enable() to enable color support for the remainder of the process' lifetime.

    This class is also a context manager. You can do this:
    with Windows():
        print(Color('{autored}Test{/autored}'))

    Or this:
    with Windows(auto_colors=True):
        print(Color('{autored}Test{/autored}'))
    """

    @classmethod
    def disable(cls):
        """Restore sys.stderr and sys.stdout to their original objects. Resets colors to their original values.

        :return: If streams restored successfully.
        :rtype: bool
        """
        if os.name != 'nt' or not cls.is_enabled():
            return False

        getattr(sys.stderr, '_reset_colors', lambda: False)()
        getattr(sys.stdout, '_reset_colors', lambda: False)()

        if hasattr(sys.stderr, 'ORIGINAL_STREAM'):
            sys.stderr = getattr(sys.stderr, 'ORIGINAL_STREAM')
        if hasattr(sys.stdout, 'ORIGINAL_STREAM'):
            sys.stdout = getattr(sys.stdout, 'ORIGINAL_STREAM')

        return True

    @staticmethod
    def is_enabled():
        """Return True if either stderr or stdout has colors enabled."""
        return hasattr(sys.stderr, 'ORIGINAL_STREAM') or hasattr(sys.stdout, 'ORIGINAL_STREAM')

    @classmethod
    def enable(cls, auto_colors=False, reset_atexit=False):
        """Enable color text with print() or sys.stdout.write() (stderr too).

        :param bool auto_colors: Automatically selects dark or light colors based on current terminal's background
            color. Only works with {autored} and related tags.
        :param bool reset_atexit: Resets original colors upon Python exit (in case you forget to reset it yourself with
            a closing tag).

        :return: If streams replaced successfully.
        :rtype: bool
        """
        if os.name != 'nt':
            return False

        # Overwrite stream references.
        if not hasattr(sys.stderr, 'ORIGINAL_STREAM'):
            sys.stderr.flush()
            sys.stderr = WindowsStreamStdErr()
        if not hasattr(sys.stdout, 'ORIGINAL_STREAM'):
            sys.stdout.flush()
            sys.stdout = WindowsStreamStdOut()
        if not hasattr(sys.stderr, 'ORIGINAL_STREAM') and not hasattr(sys.stdout, 'ORIGINAL_STREAM'):
            return False

        # Automatically select which colors to display.
        bg_color = getattr(sys.stdout, 'default_bg', getattr(sys.stderr, 'default_bg', None))
        if auto_colors and bg_color is not None:
            if bg_color in (112, 96, 240, 176, 224, 208, 160):
                ANSICodeMapping.set_light_background()
            else:
                ANSICodeMapping.set_dark_background()

        # Reset on exit if requested.
        if reset_atexit:
            atexit.register(cls.disable)

        return True

    def __init__(self, auto_colors=False):
        """Constructor."""
        self.auto_colors = auto_colors

    def __enter__(self):
        """Context manager, enables colors on Windows."""
        self.enable(auto_colors=self.auto_colors)

    def __exit__(self, *_):
        """Context manager, disabled colors on Windows."""
        self.disable()
