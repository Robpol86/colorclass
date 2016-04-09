"""Colorful worry-free console applications for Linux, Mac OS X, and Windows.

Supported natively on Linux and Mac OSX (Just Works), and on Windows it works the same if Windows.enable() is called.

Gives you expected and sane results from methods like len() and .capitalize().

https://github.com/Robpol86/colorclass
https://pypi.python.org/pypi/colorclass
"""

from colorclass.codes import list_tags  # noqa
from colorclass.parse import parse_input, RE_NUMBER_SEARCH, RE_SPLIT
from colorclass.toggles import disable_all_colors  # noqa
from colorclass.toggles import set_dark_background  # noqa
from colorclass.toggles import set_light_background  # noqa
from colorclass.windows import Windows  # noqa

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '1.2.0'
PARENT_CLASS = type(u'')


class ColorBytes(bytes):
    """Str (bytes in Python3) subclass, .decode() overridden to return Color() instance."""

    def decode(*args, **kwargs):
        """Similar to str() method of the same name, returns Color() instance."""
        return Color(super(ColorBytes, args[0]).decode(*args[1:], **kwargs))


class Color(PARENT_CLASS):
    """Unicode (str in Python3) subclass with ANSI terminal text color support.

    Example syntax: Color('{red}Sample Text{/red}')

    For a list of codes, call: colorclass.list_tags()
    """

    @classmethod
    def red(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('red', string, auto=auto)

    @classmethod
    def bgred(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bgred', string, auto=auto)

    @classmethod
    def green(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('green', string, auto=auto)

    @classmethod
    def bggreen(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bggreen', string, auto=auto)

    @classmethod
    def blue(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('blue', string, auto=auto)

    @classmethod
    def bgblue(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bgblue', string, auto=auto)

    @classmethod
    def yellow(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('yellow', string, auto=auto)

    @classmethod
    def bgyellow(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bgyellow', string, auto=auto)

    @classmethod
    def cyan(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('cyan', string, auto=auto)

    @classmethod
    def bgcyan(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bgcyan', string, auto=auto)

    @classmethod
    def magenta(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('magenta', string, auto=auto)

    @classmethod
    def bgmagenta(cls, string, auto=False):
        """Color-code entire string.

        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        return cls.colorize('bgmagenta', string, auto=auto)

    @classmethod
    def colorize(cls, color, string, auto=False):
        """Color-code entire string using specified color.

        :param str color: Color of string.
        :param str string: String to colorize.
        :param bool auto: Enable auto-color (dark/light terminal).

        :return: Class instance for colorized string.
        :rtype: Color
        """
        tag = '{0}{1}'.format('auto' if auto else '', color)
        return cls('{%s}%s{/%s}' % (tag, string, tag))

    def __new__(cls, *args, **kwargs):
        """Constructor."""
        parent_class = cls.__bases__[0]
        value_markup = args[0] if args else parent_class()
        value_colors, value_no_colors = parse_input(value_markup)
        if args:
            args = [value_colors] + list(args[1:])

        obj = parent_class.__new__(cls, *args, **kwargs)
        obj.value_colors, obj.value_no_colors = value_colors, value_no_colors
        obj.has_colors = bool(RE_NUMBER_SEARCH.match(value_colors))
        return obj

    def __len__(self):
        """Return length of string without color codes (what users expect)."""
        return self.value_no_colors.__len__()

    def capitalize(self):
        """Similar to str() method of the same name, returns Color() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).capitalize()
        return Color().join(split)

    def center(self, width, fillchar=None):
        """Similar to str() method of the same name, returns Color() instance.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).center(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).center(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def count(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).count(*args, **kwargs)

    def endswith(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).endswith(*args, **kwargs)

    def encode(*args, **kwargs):
        """Similar to str() method of the same name, returns ColorBytes() instance."""
        return ColorBytes(super(Color, args[0]).encode(*args[1:], **kwargs))

    def decode(*args, **kwargs):
        """Similar to str() method of the same name, returns Color() instance."""
        return Color(super(Color, args[0]).decode(*args[1:], **kwargs))

    def find(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).find(*args, **kwargs)

    def format(*args, **kwargs):
        """Similar to str() method of the same name, returns Color() instance."""
        return Color(super(Color, args[0]).format(*args[1:], **kwargs))

    def index(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).index(*args, **kwargs)

    def isalnum(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isalnum()

    def isalpha(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isalpha()

    def isdecimal(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isdecimal()

    def isdigit(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isdigit()

    def isnumeric(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isnumeric()

    def isspace(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isspace()

    def istitle(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).istitle()

    def isupper(self):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).isupper()

    def ljust(self, width, fillchar=None):
        """Similar to str() method of the same name, returns Color() instance.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).ljust(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).ljust(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def rfind(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).rfind(*args, **kwargs)

    def rindex(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).rindex(*args, **kwargs)

    def rjust(self, width, fillchar=None):
        """Similar to str() method of the same name, returns Color() instance.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).rjust(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).rjust(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def splitlines(self, **kwargs):
        """Similar to str() method of the same name, returns Color() instances in a list.

        :param dict kwargs: Pass keyword arguments to PARENT_CLASS.splitlines.
        """
        return [Color(l) for l in PARENT_CLASS(self.value_colors).splitlines(**kwargs)]

    def startswith(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).startswith(*args, **kwargs)

    def swapcase(self):
        """Similar to str() method of the same name, returns Color() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).swapcase()
        return Color().join(split)

    def title(self):
        """Similar to str() method of the same name, returns Color() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).title()
        return Color().join(split)

    def translate(self, table):
        """Similar to str() method of the same name, returns Color() instance.

        :param table: Translation table.
        """
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).translate(table)
        return Color().join(split)

    def upper(self):
        """Similar to str() method of the same name, returns Color() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).upper()
        return Color().join(split)

    def zfill(self, width):
        """Similar to str() method of the same name, returns Color() instance.

        :param int width: Length of output string.
        """
        if not self.value_no_colors:
            return PARENT_CLASS().zfill(width)

        split = RE_SPLIT.split(self.value_colors)
        filled = PARENT_CLASS(self.value_no_colors).zfill(width)
        if len(split) == 1:
            return filled

        padding = filled.replace(self.value_no_colors, '')
        if not split[0]:
            split[2] = padding + split[2]
        else:
            split[0] = padding + split[0]

        return Color().join(split)
