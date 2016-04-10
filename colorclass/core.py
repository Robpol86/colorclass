"""String subclass that handles ANSI color codes."""

from colorclass.codes import ANSICodeMapping
from colorclass.parse import parse_input, RE_SPLIT

PARENT_CLASS = type(u'')


class ColorBytes(bytes):
    """Str (bytes in Python3) subclass, .decode() overridden to return ColorStr instance."""

    def decode(*args, **kwargs):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        return ColorStr(super(ColorBytes, args[0]).decode(*args[1:], **kwargs))


class ColorStr(PARENT_CLASS):
    """Core color class."""

    def __new__(cls, *args, **kwargs):
        """Parse color markup and instantiate."""
        value_markup = args[0] if args else PARENT_CLASS()  # e.g. '{red}test{/red}'
        value_colors, value_no_colors = parse_input(value_markup, ANSICodeMapping.DISABLE_COLORS)

        # Instantiate.
        color_args = [cls, value_colors] + list(args[1:])
        obj = PARENT_CLASS.__new__(*color_args, **kwargs)

        # Add additional attributes and return.
        obj.value_colors, obj.value_no_colors = value_colors, value_no_colors
        obj.has_colors = value_colors != value_no_colors
        return obj

    def __len__(self):
        """Return length of string without color codes (what users expect)."""
        return self.value_no_colors.__len__()

    def capitalize(self):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).capitalize()
        return ColorStr().join(split)

    def center(self, width, fillchar=None):
        """Similar to str() method of the same name, returns ColorStr() instance.

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
        return ColorBytes(super(ColorStr, args[0]).encode(*args[1:], **kwargs))

    def decode(*args, **kwargs):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        return ColorStr(super(ColorStr, args[0]).decode(*args[1:], **kwargs))

    def find(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).find(*args, **kwargs)

    def format(*args, **kwargs):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        return ColorStr(super(ColorStr, args[0]).format(*args[1:], **kwargs))

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
        """Similar to str() method of the same name, returns ColorStr() instance.

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
        """Similar to str() method of the same name, returns ColorStr() instance.

        :param int width: Length of output string.
        :param str fillchar: Use this character instead of spaces.
        """
        if fillchar is not None:
            result = PARENT_CLASS(self.value_no_colors).rjust(width, fillchar)
        else:
            result = PARENT_CLASS(self.value_no_colors).rjust(width)
        return result.replace(self.value_no_colors, self.value_colors)

    def splitlines(self, **kwargs):
        """Similar to str() method of the same name, returns ColorStr() instances in a list.

        :param dict kwargs: Pass keyword arguments to PARENT_CLASS.splitlines.
        """
        return [ColorStr(l) for l in PARENT_CLASS(self.value_colors).splitlines(**kwargs)]

    def startswith(self, *args, **kwargs):
        """Similar to str() method of the same name."""
        return PARENT_CLASS(self.value_no_colors).startswith(*args, **kwargs)

    def swapcase(self):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).swapcase()
        return ColorStr().join(split)

    def title(self):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).title()
        return ColorStr().join(split)

    def translate(self, table):
        """Similar to str() method of the same name, returns ColorStr() instance.

        :param table: Translation table.
        """
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).translate(table)
        return ColorStr().join(split)

    def upper(self):
        """Similar to str() method of the same name, returns ColorStr() instance."""
        split = RE_SPLIT.split(self.value_colors)
        for i, item in enumerate(split):
            if RE_SPLIT.match(item):
                continue
            split[i] = PARENT_CLASS(item).upper()
        return ColorStr().join(split)

    def zfill(self, width):
        """Similar to str() method of the same name, returns ColorStr() instance.

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

        return ColorStr().join(split)
