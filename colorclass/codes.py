"""Handles mapping between color names and ANSI codes and determining auto color codes."""

from collections import Mapping

BASE_CODES = {
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


class ANSICodeMapping(Mapping):
    """Read-only subclass of dict, resolves closing tags (based on colorclass.CODES) and automatic colors.

    :cvar bool DISABLE_COLORS: Disable colors (strip color codes).
    :cvar bool LIGHT_BACKGROUND: Use low intensity color codes.
    """

    DISABLE_COLORS = False
    LIGHT_BACKGROUND = False

    def __init__(self):
        """Constructor."""
        self.__dict = BASE_CODES.copy()

    def __getitem__(self, item):
        """Return value for key.

        :param str item: Key.

        :return: Color code integer.
        """
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
        """Iterate dictionary."""
        return iter(self.__dict)

    def __len__(self):
        """Dictionary length."""
        return len(self.__dict)

    @property
    def autoblack(self):
        """Return automatic black foreground color depending on background color."""
        return self.__dict['black' if ANSICodeMapping.LIGHT_BACKGROUND else 'hiblack']

    @property
    def autored(self):
        """Return automatic red foreground color depending on background color."""
        return self.__dict['red' if ANSICodeMapping.LIGHT_BACKGROUND else 'hired']

    @property
    def autogreen(self):
        """Return automatic green foreground color depending on background color."""
        return self.__dict['green' if ANSICodeMapping.LIGHT_BACKGROUND else 'higreen']

    @property
    def autoyellow(self):
        """Return automatic yellow foreground color depending on background color."""
        return self.__dict['yellow' if ANSICodeMapping.LIGHT_BACKGROUND else 'hiyellow']

    @property
    def autoblue(self):
        """Return automatic blue foreground color depending on background color."""
        return self.__dict['blue' if ANSICodeMapping.LIGHT_BACKGROUND else 'hiblue']

    @property
    def automagenta(self):
        """Return automatic magenta foreground color depending on background color."""
        return self.__dict['magenta' if ANSICodeMapping.LIGHT_BACKGROUND else 'himagenta']

    @property
    def autocyan(self):
        """Return automatic cyan foreground color depending on background color."""
        return self.__dict['cyan' if ANSICodeMapping.LIGHT_BACKGROUND else 'hicyan']

    @property
    def autowhite(self):
        """Return automatic white foreground color depending on background color."""
        return self.__dict['white' if ANSICodeMapping.LIGHT_BACKGROUND else 'hiwhite']

    @property
    def autobgblack(self):
        """Return automatic black background color depending on background color."""
        return self.__dict['bgblack' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgblack']

    @property
    def autobgred(self):
        """Return automatic red background color depending on background color."""
        return self.__dict['bgred' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgred']

    @property
    def autobggreen(self):
        """Return automatic green background color depending on background color."""
        return self.__dict['bggreen' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibggreen']

    @property
    def autobgyellow(self):
        """Return automatic yellow background color depending on background color."""
        return self.__dict['bgyellow' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgyellow']

    @property
    def autobgblue(self):
        """Return automatic blue background color depending on background color."""
        return self.__dict['bgblue' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgblue']

    @property
    def autobgmagenta(self):
        """Return automatic magenta background color depending on background color."""
        return self.__dict['bgmagenta' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgmagenta']

    @property
    def autobgcyan(self):
        """Return automatic cyan background color depending on background color."""
        return self.__dict['bgcyan' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgcyan']

    @property
    def autobgwhite(self):
        """Return automatic white background color depending on background color."""
        return self.__dict['bgwhite' if ANSICodeMapping.LIGHT_BACKGROUND else 'hibgwhite']


def list_tags():
    """List the available tags.

    :return: Tuple of tuples. Child tuples are four items: opening tag, closing tag, main ansi value, closing ansi value
    :rtype: tuple
    """
    codes = ANSICodeMapping()
    grouped = set([(k, '/{0}'.format(k), codes[k], codes['/{0}'.format(k)]) for k in codes if not k.startswith('/')])

    # Add half-tags like /all.
    found = [c for r in grouped for c in r[:2]]
    missing = set([('', r[0], None, r[1]) if r[0].startswith('/') else (r[0], '', r[1], None)
                   for r in ANSICodeMapping().items() if r[0] not in found])
    grouped |= missing

    # Sort.
    payload = sorted([i for i in grouped if i[2] is None], key=lambda x: x[3])  # /all /fg /bg
    grouped -= set(payload)
    payload.extend(sorted([i for i in grouped if i[2] < 10], key=lambda x: x[2]))  # b i u flash
    grouped -= set(payload)
    payload.extend(sorted([i for i in grouped if i[0].startswith('auto')], key=lambda x: x[2]))  # auto colors
    grouped -= set(payload)
    payload.extend(sorted([i for i in grouped if not i[0].startswith('hi')], key=lambda x: x[2]))  # dark colors
    grouped -= set(payload)
    payload.extend(sorted(grouped, key=lambda x: x[2]))  # light colors
    return tuple(payload)
