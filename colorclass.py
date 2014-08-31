"""Yet another ANSI color text library for Python. Provides "auto colors" for dark/light terminals.

https://github.com/Robpol86/colorclass
https://pypi.python.org/pypi/colorclass
"""

from collections import Mapping
import re
import sys

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'
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

    '/black': 39, '/red': 39, '/green': 39, '/yellow': 39, '/blue': 39, '/magenta': 39, '/cyan': 39, '/white': 39,
    '/hiblack': 39, '/hired': 39, '/higreen': 39, '/hiyellow': 39, '/hiblue': 39, '/himagenta': 39, '/hicyan': 39,
    '/hiwhite': 39,

    '/bgblack': 49, '/bgred': 49, '/bggreen': 49, '/bgyellow': 49, '/bgblue': 49, '/bgmagenta': 49, '/bgcyan': 49,
    '/bgwhite': 49, '/hibgblack': 49, '/hibgred': 49, '/hibggreen': 49, '/hibgyellow': 49, '/hibgblue': 49,
    '/hibgmagenta': 49, '/hibgcyan': 49, '/hibgwhite': 49,

    '/autored': 39, '/autoblack': 39, '/automagenta': 39, '/autowhite': 39, '/autoblue': 39, '/autoyellow': 39,
    '/autogreen': 39, '/autocyan': 39,
}
_LIGHT_BACKGROUND = False
_RE_GROUP_SEARCH = re.compile(r'(?:\033\[\d+m)+')
_RE_NUMBER_SEARCH = re.compile(r'\033\[(\d+)m')


class _AutoCodes(Mapping):
    """Read-only subclass of dict, resolves closing tags (based on colorclass.CODES) and automatic colors."""

    def __init__(self):
        self.__dict = _BASE_CODES.copy()

    def __getitem__(self, item):
        if item == 'autoblack':
            return self.autoblack
        elif item == 'autored':
            return self.autored
        elif item == 'autogreen':
            return self.autogreen
        elif item == 'autoyellow':
            return self.autoyellow
        elif item == 'autoblue':
            return self.autoblue
        elif item == 'automagenta':
            return self.automagenta
        elif item == 'autocyan':
            return self.autocyan
        elif item == 'autowhite':
            return self.autowhite
        else:
            return self.__dict[item]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    @property
    def autoblack(self):
        return self.__dict['black' if _LIGHT_BACKGROUND else 'hiblack']

    @property
    def autored(self):
        return self.__dict['red' if _LIGHT_BACKGROUND else 'hired']

    @property
    def autogreen(self):
        return self.__dict['green' if _LIGHT_BACKGROUND else 'higreen']

    @property
    def autoyellow(self):
        return self.__dict['yellow' if _LIGHT_BACKGROUND else 'hiyellow']

    @property
    def autoblue(self):
        return self.__dict['blue' if _LIGHT_BACKGROUND else 'hiblue']

    @property
    def automagenta(self):
        return self.__dict['magenta' if _LIGHT_BACKGROUND else 'himagenta']

    @property
    def autocyan(self):
        return self.__dict['cyan' if _LIGHT_BACKGROUND else 'hicyan']

    @property
    def autowhite(self):
        return self.__dict['white' if _LIGHT_BACKGROUND else 'hiwhite']


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
    if not codes:
        return incoming, incoming

    color_codes = dict((k, '\033[{0}m'.format(v)) for k, v in codes.items())
    incoming_padded = _pad_input(incoming)
    output_no_colors = incoming_padded.format(**dict((k, u'') for k in codes))
    output_colors = incoming_padded.format(**color_codes)

    # Simplify: '{b}{red}' -> '\033[1m\033[31m' -> '\033[1;31m'
    groups = sorted(set(_RE_GROUP_SEARCH.findall(output_colors)), key=len, reverse=True)  # Get codes, grouped adjacent.
    groups_simplified = [sorted(set(_RE_NUMBER_SEARCH.findall(i))) for i in groups]  # Sort/unique child codes.
    groups_compiled = ['\033[{0}m'.format(';'.join(g)) for g in groups_simplified]  # Final codes.
    assert len(groups_compiled) == len(groups)  # For testing.
    output_colors_simplified = output_colors
    for i in range(len(groups)):
        output_colors_simplified = output_colors_simplified.replace(groups[i], groups_compiled[i])

    return output_colors_simplified, output_no_colors


def set_light_background():
    """Chooses dark colors for all 'auto'-prefixed codes for readability on light backgrounds. Module-wide."""
    global _LIGHT_BACKGROUND
    _LIGHT_BACKGROUND = True


def set_dark_background():
    """Chooses dark colors for all 'auto'-prefixed codes for readability on light backgrounds. Module-wide."""
    global _LIGHT_BACKGROUND
    _LIGHT_BACKGROUND = False


def list_tags():
    """Lists the available tags.

    Returns:
    Tuple of tuples. Child tuples are four items: ('opening tag', 'closing tag', main ansi value, closing ansi value).
    """
    codes = _AutoCodes()
    payload = [(k, '/{0}'.format(k), codes[k], codes['/{0}'.format(k)]) for k in codes if not k.startswith('/')]
    payload.sort(key=lambda x: x[2])
    return tuple(payload)


class Color(unicode if sys.version_info[0] == 2 else str):
    """Unicode (str in Python3) subclass with ANSI terminal text color support.

    Example syntax: Color('{red}Sample Text{/red}')

    For a list of codes, call: colorclass.list_tags()
    """
    def __new__(cls, *args, **kwargs):
        parent_class = cls.__bases__[0]
        value_markup = args[0] if args else parent_class('')
        value_colors, value_no_colors = _parse_input(value_markup)
        if args:
            args = [value_no_colors] + list(args[1:])

        obj = parent_class.__new__(cls, *args, **kwargs)
        obj.value_markup, obj.value_colors, obj.value_no_colors = value_markup, value_colors, value_no_colors
        return obj
