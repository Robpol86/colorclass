"""Colorful worry-free console applications for Linux, Mac OSX, and Windows.

Supported natively on Linux and Mac OSX (Just Works), and on Windows it works the same if Windows.enable() is called.

Gives you expected and sane results from methods like len() and .capitalize().

https://github.com/Robpol86/colorclass
https://pypi.python.org/pypi/colorclass
"""

import atexit
from collections import Mapping
import ctypes
import os
import re
import sys
import struct

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.1.0'
_BASE_CODES = {
    '/all': 0, 'b': 1, 'f': 2, 'i': 3, 'u': 4, 'flash': 5, 'outline': 6, 'negative': 7, 'invis': 8, 'strike': 9,
    '/b': 22, '/f': 22, '/i': 23, '/u': 24, '/flash': 25, '/outline': 26, '/negative': 27, '/invis': 28,
    '/strike': 29, '/fg': 39, '/bg': 49,

    'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,

    'bgblack': 40, 'bgred': 41, 'bggreen': 42, 'bgyellow': 43, 'bgblue': 44, 'bgmagenta': 45, 'bgcyan': 46,
    'bgwhite': 47,

    'hiblack': 90, 'hired': 91, 'higreen': 92, 'hiyellow': 93, 'hiblue': 94, 'himagenta': 95, 'hicyan': 96,
    'hiwhite': 97,

    'hibgblack': 100, 'hibgred': 101, 'hibggreen': 102, 'hibgyellow': 103, 'hibgblue': 104, 'hibgmagenta': 105,
    'hibgcyan': 106, 'hibgwhite': 107,

    'autored': None, 'autoblack': None, 'automagenta': None, 'autowhite': None, 'autoblue': None, 'autoyellow': None,
    'autogreen': None, 'autocyan': None,

    'autobgred': None, 'autobgblack': None, 'autobgmagenta': None, 'autobgwhite': None, 'autobgblue': None,
    'autobgyellow': None, 'autobggreen': None, 'autobgcyan': None,

    '/black': 39, '/red': 39, '/green': 39, '/yellow': 39, '/blue': 39, '/magenta': 39, '/cyan': 39, '/white': 39,
    '/hiblack': 39, '/hired': 39, '/higreen': 39, '/hiyellow': 39, '/hiblue': 39, '/himagenta': 39, '/hicyan': 39,
    '/hiwhite': 39,

    '/bgblack': 49, '/bgred': 49, '/bggreen': 49, '/bgyellow': 49, '/bgblue': 49, '/bgmagenta': 49, '/bgcyan': 49,
    '/bgwhite': 49, '/hibgblack': 49, '/hibgred': 49, '/hibggreen': 49, '/hibgyellow': 49, '/hibgblue': 49,
    '/hibgmagenta': 49, '/hibgcyan': 49, '/hibgwhite': 49,

    '/autored': 39, '/autoblack': 39, '/automagenta': 39, '/autowhite': 39, '/autoblue': 39, '/autoyellow': 39,
    '/autogreen': 39, '/autocyan': 39,

    '/autobgred': 49, '/autobgblack': 49, '/autobgmagenta': 49, '/autobgwhite': 49, '/autobgblue': 49,
    '/autobgyellow': 49, '/autobggreen': 49, '/autobgcyan': 49,
}
_WINDOWS_CODES = {
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
_RE_GROUP_SEARCH = re.compile(r'(?:\033\[[\d;]+m)+')
_RE_NUMBER_SEARCH = re.compile(r'\033\[([\d;]+)m')
_RE_SPLIT = re.compile(r'(\033\[[\d;]+m)')
PARENT_CLASS = unicode if sys.version_info[0] == 2 else str


class _AutoCodes(Mapping):
    """Read-only subclass of dict, resolves closing tags (based on colorclass.CODES) and automatic colors."""
    DISABLE_COLORS = False
    LIGHT_BACKGROUND = False

    def __init__(self):
        self.__dict = _BASE_CODES.copy()

    def __getitem__(self, item):
        if item == 'autoblack':
            answer = self.autoblack
        elif item == 'autored':
            answer = self.autored
        elif item == 'autogreen':
            answer = self.autogreen
        elif item == 'autoyellow':
            answer = self.autoyellow
        elif item == 'autoblue':
            answer = self.autoblue
        elif item == 'automagenta':
            answer = self.automagenta
        elif item == 'autocyan':
            answer = self.autocyan
        elif item == 'autowhite':
            answer = self.autowhite
        elif item == 'autobgblack':
            answer = self.autobgblack
        elif item == 'autobgred':
            answer = self.autobgred
        elif item == 'autobggreen':
            answer = self.autobggreen
        elif item == 'autobgyellow':
            answer = self.autobgyellow
        elif item == 'autobgblue':
            answer = self.autobgblue
        elif item == 'autobgmagenta':
            answer = self.autobgmagenta
        elif item == 'autobgcyan':
            answer = self.autobgcyan
        elif item == 'autobgwhite':
            answer = self.autobgwhite
        else:
            answer = self.__dict[item]
        return answer

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    @property
    def autoblack(self):
        """Returns automatic black foreground color depending on background color."""
        return self.__dict['black' if _AutoCodes.LIGHT_BACKGROUND else 'hiblack']

    @property
    def autored(self):
        """Returns automatic red foreground color depending on background color."""
        return self.__dict['red' if _AutoCodes.LIGHT_BACKGROUND else 'hired']

    @property
    def autogreen(self):
        """Returns automatic green foreground color depending on background color."""
        return self.__dict['green' if _AutoCodes.LIGHT_BACKGROUND else 'higreen']

    @property
    def autoyellow(self):
        """Returns automatic yellow foreground color depending on background color."""
        return self.__dict['yellow' if _AutoCodes.LIGHT_BACKGROUND else 'hiyellow']

    @property
    def autoblue(self):
        """Returns automatic blue foreground color depending on background color."""
        return self.__dict['blue' if _AutoCodes.LIGHT_BACKGROUND else 'hiblue']

    @property
    def automagenta(self):
        """Returns automatic magenta foreground color depending on background color."""
        return self.__dict['magenta' if _AutoCodes.LIGHT_BACKGROUND else 'himagenta']

    @property
    def autocyan(self):
        """Returns automatic cyan foreground color depending on background color."""
        return self.__dict['cyan' if _AutoCodes.LIGHT_BACKGROUND else 'hicyan']

    @property
    def autowhite(self):
        """Returns automatic white foreground color depending on background color."""
        return self.__dict['white' if _AutoCodes.LIGHT_BACKGROUND else 'hiwhite']

    @property
    def autobgblack(self):
        """Returns automatic black background color depending on background color."""
        return self.__dict['bgblack' if _AutoCodes.LIGHT_BACKGROUND else 'hibgblack']

    @property
    def autobgred(self):
        """Returns automatic red background color depending on background color."""
        return self.__dict['bgred' if _AutoCodes.LIGHT_BACKGROUND else 'hibgred']

    @property
    def autobggreen(self):
        """Returns automatic green background color depending on background color."""
        return self.__dict['bggreen' if _AutoCodes.LIGHT_BACKGROUND else 'hibggreen']

    @property
    def autobgyellow(self):
        """Returns automatic yellow background color depending on background color."""
        return self.__dict['bgyellow' if _AutoCodes.LIGHT_BACKGROUND else 'hibgyellow']

    @property
    def autobgblue(self):
        """Returns automatic blue background color depending on background color."""
        return self.__dict['bgblue' if _AutoCodes.LIGHT_BACKGROUND else 'hibgblue']

    @property
    def autobgmagenta(self):
        """Returns automatic magenta background color depending on background color."""
        return self.__dict['bgmagenta' if _AutoCodes.LIGHT_BACKGROUND else 'hibgmagenta']

    @property
    def autobgcyan(self):
        """Returns automatic cyan background color depending on background color."""
        return self.__dict['bgcyan' if _AutoCodes.LIGHT_BACKGROUND else 'hibgcyan']

    @property
    def autobgwhite(self):
        """Returns automatic white background color depending on background color."""
        return self.__dict['bgwhite' if _AutoCodes.LIGHT_BACKGROUND else 'hibgwhite']


def _pad_input(incoming):
    """Avoid IndexError and KeyError by ignoring un-related fields.

    Example: '{0}{autored}' becomes '{{0}}{autored}'.

    Positional arguments:
    incoming -- the input unicode value.

    Returns:
    Padded unicode value.
    """
    incoming_expanded = incoming.replace('{', '{{').replace('}', '}}')
    for key in _BASE_CODES:
        before, after = '{{%s}}' % key, '{%s}' % key
        if before in incoming_expanded:
            incoming_expanded = incoming_expanded.replace(before, after)
    return incoming_expanded


def _parse_input(incoming):
    """Performs the actual conversion of tags to ANSI escaped codes.

    Provides a version of the input without any colors for len() and other methods.

    Positional arguments:
    incoming -- the input unicode value.

    Returns:
    2-item tuple. First item is the parsed output. Second item is a version of the input without any colors.
    """
    codes = dict((k, v) for k, v in _AutoCodes().items() if '{%s}' % k in incoming)
    color_codes = dict((k, '' if _AutoCodes.DISABLE_COLORS else '\033[{0}m'.format(v)) for k, v in codes.items())
    incoming_padded = _pad_input(incoming)
    output_colors = incoming_padded.format(**color_codes)

    # Simplify: '{b}{red}' -> '\033[1m\033[31m' -> '\033[1;31m'
    groups = sorted(set(_RE_GROUP_SEARCH.findall(output_colors)), key=len, reverse=True)  # Get codes, grouped adjacent.
    groups_simplified = [[x for n in _RE_NUMBER_SEARCH.findall(i) for x in n.split(';')] for i in groups]
    groups_compiled = ['\033[{0}m'.format(';'.join(g)) for g in groups_simplified]  # Final codes.
    assert len(groups_compiled) == len(groups)  # For testing.
    output_colors_simplified = output_colors
    for i in range(len(groups)):
        output_colors_simplified = output_colors_simplified.replace(groups[i], groups_compiled[i])
    output_no_colors = _RE_SPLIT.sub('', output_colors_simplified)

    # Strip any remaining color codes.
    if _AutoCodes.DISABLE_COLORS:
        output_colors_simplified = _RE_NUMBER_SEARCH.sub('', output_colors_simplified)

    return output_colors_simplified, output_no_colors


def disable_all_colors():
    """Disable all colors. Strips any color tags or codes."""
    _AutoCodes.DISABLE_COLORS = True


def set_light_background():
    """Chooses dark colors for all 'auto'-prefixed codes for readability on light backgrounds."""
    _AutoCodes.DISABLE_COLORS = False
    _AutoCodes.LIGHT_BACKGROUND = True


def set_dark_background():
    """Chooses dark colors for all 'auto'-prefixed codes for readability on light backgrounds."""
    _AutoCodes.DISABLE_COLORS = False
    _AutoCodes.LIGHT_BACKGROUND = False


def list_tags():
    """Lists the available tags.

    Returns:
    Tuple of tuples. Child tuples are four items: ('opening tag', 'closing tag', main ansi value, closing ansi value).
    """
    codes = _AutoCodes()
    payload = [(k, '/{0}'.format(k), codes[k], codes['/{0}'.format(k)]) for k in codes if not k.startswith('/')]
    payload.sort(key=lambda x: x[2])
    return tuple(payload)


class Color(PARENT_CLASS):
    """Unicode (str in Python3) subclass with ANSI terminal text color support.

    Example syntax: Color('{red}Sample Text{/red}')

    For a list of codes, call: colorclass.list_tags()
    """

    def __new__(cls, *args, **kwargs):
        parent_class = cls.__bases__[0]
        value_markup = args[0] if args else parent_class()
        value_colors, value_no_colors = _parse_input(value_markup)
        if args:
            args = [value_colors] + list(args[1:])

        obj = parent_class.__new__(cls, *args, **kwargs)
        obj.value_colors, obj.value_no_colors = value_colors, value_no_colors
        obj.has_colors = bool(_RE_NUMBER_SEARCH.match(value_colors))
        return obj

    def __len__(self):
        return self.value_no_colors.__len__()

    def capitalize(self):
        split = _RE_SPLIT.split(self.value_colors)
        for i in range(len(split)):
            if _RE_SPLIT.match(split[i]):
                continue
            split[i] = PARENT_CLASS(split[i]).capitalize()
        return Color().join(split)

    def center(self, width, fillchar=None):
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).center(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).center(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def count(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).count(*args, **kwargs)

    def endswith(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).endswith(*args, **kwargs)

    def find(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).find(*args, **kwargs)

    def format(*args, **kwargs):
        return Color(super(Color, args[0]).format(*args[1:], **kwargs))

    def index(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).index(*args, **kwargs)

    def isalnum(self):
        return PARENT_CLASS(self.value_no_colors).isalnum()

    def isalpha(self):
        return PARENT_CLASS(self.value_no_colors).isalpha()

    def isdecimal(self):
        return PARENT_CLASS(self.value_no_colors).isdecimal()

    def isdigit(self):
        return PARENT_CLASS(self.value_no_colors).isdigit()

    def isnumeric(self):
        return PARENT_CLASS(self.value_no_colors).isnumeric()

    def isspace(self):
        return PARENT_CLASS(self.value_no_colors).isspace()

    def istitle(self):
        return PARENT_CLASS(self.value_no_colors).istitle()

    def isupper(self):
        return PARENT_CLASS(self.value_no_colors).isupper()

    def ljust(self, width, fillchar=None):
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).ljust(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).ljust(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def rfind(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).rfind(*args, **kwargs)

    def rindex(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).rindex(*args, **kwargs)

    def rjust(self, width, fillchar=None):
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).rjust(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).rjust(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def splitlines(self):
        return [Color(l) for l in PARENT_CLASS(self.value_colors).splitlines()]

    def startswith(self, *args, **kwargs):
        return PARENT_CLASS(self.value_no_colors).startswith(*args, **kwargs)

    def swapcase(self):
        split = _RE_SPLIT.split(self.value_colors)
        for i in range(len(split)):
            if _RE_SPLIT.match(split[i]):
                continue
            split[i] = PARENT_CLASS(split[i]).swapcase()
        return Color().join(split)

    def title(self):
        split = _RE_SPLIT.split(self.value_colors)
        for i in range(len(split)):
            if _RE_SPLIT.match(split[i]):
                continue
            split[i] = PARENT_CLASS(split[i]).title()
        return Color().join(split)

    def translate(self, table):
        split = _RE_SPLIT.split(self.value_colors)
        for i in range(len(split)):
            if _RE_SPLIT.match(split[i]):
                continue
            split[i] = PARENT_CLASS(split[i]).translate(table)
        return Color().join(split)

    def upper(self):
        split = _RE_SPLIT.split(self.value_colors)
        for i in range(len(split)):
            if _RE_SPLIT.match(split[i]):
                continue
            split[i] = PARENT_CLASS(split[i]).upper()
        return Color().join(split)

    def zfill(self, width):
        if not self.value_no_colors:
            return PARENT_CLASS().zfill(width)

        split = _RE_SPLIT.split(self.value_colors)
        filled = PARENT_CLASS(self.value_no_colors).zfill(width)
        if len(split) == 1:
            return filled

        padding = filled.replace(self.value_no_colors, '')
        if not split[0]:
            split[2] = padding + split[2]
        else:
            split[0] = padding + split[0]

        return Color().join(split)


class Windows(object):
    """Enable and disable Windows support for ANSI color character codes.

    Call static method Windows.enable() to enable color support for the remainder of the process' lifetime.

    This class is also a context manager. You can do this:
    with Windows():
        print(Color('{autored}Test{/autored}'))
    """

    @staticmethod
    def disable():
        """Restore sys.stderr and sys.stdout to their original objects. Resets colors to their original values."""
        if os.name != 'nt' or not Windows.is_enabled():
            return False

        getattr(sys.stderr, '_reset_colors', lambda: False)()
        getattr(sys.stdout, '_reset_colors', lambda: False)()

        if isinstance(sys.stderr, _WindowsStream):
            sys.stderr = getattr(sys.stderr, 'original_stream')
        if isinstance(sys.stderr, _WindowsStream):
            sys.stdout = getattr(sys.stdout, 'original_stream')

        return True

    @staticmethod
    def is_enabled():
        """Returns True if either stderr or stdout has colors enabled."""
        return isinstance(sys.stderr, _WindowsStream) or isinstance(sys.stdout, _WindowsStream)

    @staticmethod
    def enable(auto_colors=False, reset_atexit=False):
        """Enables color text with print() or sys.stdout.write() (stderr too).

        Keyword arguments:
        auto_colors -- automatically selects dark or light colors based on current terminal's background color. Only
            works with {autored} and related tags.
        reset_atexit -- resets original colors upon Python exit (in case you forget to reset it yourself with a closing
            tag).
        """
        if os.name != 'nt':
            return False

        # Overwrite stream references.
        if getattr(sys.stderr, 'isatty', lambda: False)() and not isinstance(sys.stderr, _WindowsStream):
            sys.stderr.flush()
            sys.stderr = _WindowsStream(stderr=True)
        if getattr(sys.stdout, 'isatty', lambda: False)() and not isinstance(sys.stdout, _WindowsStream):
            sys.stdout.flush()
            sys.stdout = _WindowsStream(stderr=False)
        if not isinstance(sys.stderr, _WindowsStream) and not isinstance(sys.stdout, _WindowsStream):
            return False

        # Automatically select which colors to display.
        bg_color = getattr(sys.stdout, 'default_bg', getattr(sys.stderr, 'default_bg', None))
        if auto_colors and bg_color is not None:
            set_light_background() if bg_color in (112, 96, 48, 240, 176, 224) else set_dark_background()

        # Reset on exit if requested.
        if reset_atexit:
            atexit.register(lambda: Windows.disable())

        return True  # One or both streams are TTYs.

    def __init__(self, auto_colors=False, reset_atexit=False):
        self.auto_colors = auto_colors
        self.reset_atexit = reset_atexit

    def __enter__(self):
        Windows.enable(auto_colors=self.auto_colors, reset_atexit=self.reset_atexit)

    def __exit__(self, *_):
        Windows.disable()


class _WindowsStream(object):
    """Replacement stream (overwrites sys.stdout and sys.stderr). When writing or printing, ANSI codes are converted.

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
    COMPILED_CODES -- 'translation' dictionary. Keys are ANSI codes (values of _BASE_CODES), values are Windows codes.
    STD_ERROR_HANDLE -- http://msdn.microsoft.com/en-us/library/windows/desktop/ms683231
    STD_OUTPUT_HANDLE -- http://msdn.microsoft.com/en-us/library/windows/desktop/ms683231

    Instance variables:
    original_stream -- the original stream to write non-code text to.
    win32_stream -- handle to the Windows stderr or stdout device. Used by other Windows functions.
    default_fg -- the foreground Windows color code at the time of instantiation.
    default_bg -- the background Windows color code at the time of instantiation.
    """

    ALL_BG_CODES = [v for k, v in _WINDOWS_CODES.items() if k.startswith('bg') or k.startswith('hibg')]
    COMPILED_CODES = dict((v, _WINDOWS_CODES[k]) for k, v in _BASE_CODES.items() if k in _WINDOWS_CODES)
    STD_ERROR_HANDLE = -12
    STD_OUTPUT_HANDLE = -11

    def __init__(self, stderr=False):
        self.original_stream = sys.stderr if stderr else sys.stdout
        std_handle = self.STD_ERROR_HANDLE if stderr else self.STD_OUTPUT_HANDLE
        self.win32_stream = ctypes.windll.kernel32.GetStdHandle(std_handle)
        self.default_fg, self.default_bg = self._get_colors()

    def __getattr__(self, item):
        """If an attribute/function/etc is not defined in this function, retrieve the one from the original stream.

        Fixes ipython arrow key presses.
        """
        return getattr(self.original_stream, item)

    def _get_colors(self):
        """Returns a tuple of two integers representing current colors: (foreground, background)."""
        console_screen_buffer_info = ctypes.create_string_buffer(22)
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(self.win32_stream, console_screen_buffer_info)
        w_attributes = struct.unpack('hhhhHhhhhhh', console_screen_buffer_info.raw)[4]
        current_fg, current_bg = w_attributes % 16, w_attributes & 240
        return current_fg, current_bg

    def _reset_colors(self):
        """Sets the foreground and background colors to their original values (when class was instantiated)."""
        self._set_color(self.default_fg | self.default_bg)

    def _set_color(self, color_code):
        """Changes the foreground and background colors for subsequently printed characters.

        Since setting a color requires including both foreground and background codes (merged), setting just the
        foreground color resets the background color to black, and vice versa.

        This function first gets the current background and foreground colors, merges in the requested color code, and
        sets the result.

        However if we need to remove just the foreground color but leave the background color the same (or vice versa)
        such as when {/red} is used, we must merge the default foreground color with the current background color. This
        is the reason for those negative values.

        Positional arguments:
        color_code -- integer color code from _WINDOWS_CODES.
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
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.win32_stream, final_color_code)

    def write(self, p_str):
        for segment in _RE_SPLIT.split(p_str):
            if not segment:
                # Empty string. p_str probably starts with colors so the first item is always ''.
                continue
            if not _RE_SPLIT.match(segment):
                # No color codes, print regular text.
                self.original_stream.write(segment)
                self.original_stream.flush()
                continue
            for color_code in (int(c) for c in _RE_NUMBER_SEARCH.findall(segment)[0].split(';')):
                if color_code in self.COMPILED_CODES:
                    self._set_color(self.COMPILED_CODES[color_code])
