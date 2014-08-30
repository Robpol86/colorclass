"""Yet another ANSI color text library for Python.

https://github.com/Robpol86/colorclass
https://pypi.python.org/pypi/colorclass
"""

import sys

__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.0.1'


class Color(unicode if sys.version_info[0] == 2 else str):
    pass
